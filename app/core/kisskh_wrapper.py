import sys
import os
from typing import List, Dict, Optional
from urllib.parse import urlsplit, urlunsplit, parse_qs, urlencode

class KissKHWrapper:
    """Constructs command line arguments and environment variables for kisskh-downloader CLI."""

    @staticmethod
    def get_python_executable() -> str:
        """Returns current python executable path."""
        return sys.executable

    @classmethod
    def build_download_cmd(
        cls,
        url_or_name: str,
        output_dir: str,
        quality: str = "1080p",
        first_ep: Optional[int] = None,
        last_ep: Optional[int] = None,
        all_episodes: bool = True,
        enable_subtitles: bool = True,
        sub_lang: str = "en",
        decrypt_subtitles: bool = False,
        decrypt_key: str = "",
        decrypt_iv: str = "",
        skip_recap: bool = False,
    ) -> List[str]:
        """Builds command list for subprocess execution."""
        cmd = [
            cls.get_python_executable(),
            "-m", "kisskh_downloader.cli",
            "dl",
            url_or_name,
            "-o", output_dir,
            "-q", quality,
        ]

        if not all_episodes:
            if first_ep is not None and first_ep > 0:
                cmd.extend(["-f", str(first_ep)])
            if last_ep is not None and last_ep > 0:
                cmd.extend(["-l", str(last_ep)])
        if skip_recap:
            cmd.append("--skip-recap")

        if enable_subtitles and sub_lang:
            cmd.extend(["-s", sub_lang])
            has_env_keys = bool(os.environ.get("KISSKH_KEY") and os.environ.get("KISSKH_INITIALIZATION_VECTOR"))
            has_passed_keys = bool(decrypt_key and decrypt_iv)

            if decrypt_subtitles and (has_passed_keys or has_env_keys):
                cmd.append("-ds")
                if decrypt_key:
                    cmd.extend(["-k", decrypt_key])
                if decrypt_iv:
                    cmd.extend(["-iv", decrypt_iv])

        return cmd

    @staticmethod
    def drama_url(url: str) -> str:
        """Strips episode info from a KissKH URL so the CLI honours -f/-l instead of one episode."""
        parts = urlsplit(url)
        segments = parts.path.split("/")
        drama_id = parse_qs(parts.query).get("id")
        if len(segments) < 3 or not drama_id:
            return url
        path = "/".join(segments[:3])  # "/Drama/<slug>"
        return urlunsplit((parts.scheme, parts.netloc, path, urlencode({"id": drama_id[0]}), ""))

    @classmethod
    def get_environment(
        cls,
        stream_key: str = "",
        sub_key: str = "",
        decrypt_key: str = "",
        decrypt_iv: str = "",
        base_url: str = "",
    ) -> Dict[str, str]:
        """Prepares environment variables including auth and subtitle keys."""
        env = os.environ.copy()
        # Piped CLI output uses the ANSI codepage on Windows and crashes on box-drawing chars.
        env["PYTHONIOENCODING"] = "utf-8"
        if stream_key:
            env["KISSKH_STREAM_KEY"] = stream_key
        if sub_key:
            env["KISSKH_SUB_KEY"] = sub_key
        if decrypt_key:
            env["KISSKH_KEY"] = decrypt_key
        if decrypt_iv:
            env["KISSKH_INITIALIZATION_VECTOR"] = decrypt_iv
        if base_url:
            # The CLI defaults to a hard-coded mirror; point it at the configured site.
            parts = urlsplit(base_url.strip())
            if parts.scheme and parts.netloc:
                env["KISSKH_BASE_URL"] = f"{parts.scheme}://{parts.netloc}"
        return env
