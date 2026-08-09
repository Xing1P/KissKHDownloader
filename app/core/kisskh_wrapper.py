import sys
import os
from typing import List, Dict, Optional

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

    @classmethod
    def get_environment(
        cls,
        stream_key: str = "",
        sub_key: str = "",
        decrypt_key: str = "",
        decrypt_iv: str = "",
    ) -> Dict[str, str]:
        """Prepares environment variables including auth and subtitle keys."""
        env = os.environ.copy()
        if stream_key:
            env["KISSKH_STREAM_KEY"] = stream_key
        if sub_key:
            env["KISSKH_SUB_KEY"] = sub_key
        if decrypt_key:
            env["KISSKH_KEY"] = decrypt_key
        if decrypt_iv:
            env["KISSKH_INITIALIZATION_VECTOR"] = decrypt_iv
        return env
