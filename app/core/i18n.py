from typing import Dict, Any

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        # Sidebar Menu
        "app_title": "KissKH Pro",
        "app_subtitle": "Drama & Movie Downloader",
        "nav_browse": "Browse KissKH",
        "nav_downloader": "New Download",
        "nav_queue": "Download Queue ({count})",
        "nav_history": "Download History",
        "nav_settings": "Settings & Keys",
        "active_downloads": "Active Downloads: {count}",


        # Web Tab
        "btn_back": "◄ Back",
        "btn_forward": "Next ►",
        "btn_reload": "↻ Reload",
        "btn_home": "Home 🏠",
        "btn_zoom_in": "Zoom +",
        "btn_zoom_out": "Zoom -",
        "btn_send_to_downloader": "Send URL to Downloader 📥",
        "address_placeholder": "Enter KissKH URL...",

        # Downloader Tab
        "url_card_title": "Movie / Drama URL or Search Title",
        "url_placeholder": "Paste KissKH URL (e.g., https://kisskh.is/Drama/...) or enter title...",
        "btn_paste": "Paste Link",
        "group_episodes": "Episode Selection",
        "rb_all_episodes": "Download All Episodes",
        "rb_single_episode": "Single Episode:",
        "rb_range_episodes": "Episode Range:",
        "lbl_from": "From:",
        "lbl_to": "To:",
        "group_quality_sub": "Quality & Subtitle Options",
        "lbl_quality": "Video Quality:",
        "chk_subtitles": "Download Subtitles",
        "lbl_sub_lang": "Subtitle Language:",
        "chk_decrypt_sub": "Decrypt Subtitle Files",
        "card_folder_title": "Save Destination Folder",
        "btn_browse": "Browse...",
        "btn_open_folder": "Open Folder",
        "btn_add_queue": "Add to Download Queue",
        "btn_download_now": "Start Download Now",

        # Queue Tab
        "queue_title": "Download Queue",
        "btn_start_queue": "Start Queue",
        "btn_pause_queue": "Pause Queue",
        "btn_clear_completed": "Clear Completed",
        "col_title": "Title / Link",
        "col_episodes": "Episodes",
        "col_quality": "Quality",
        "col_subtitles": "Subtitles",
        "col_progress": "Progress",
        "col_status": "Status",

        # History Tab
        "history_title": "Download History",
        "search_history_placeholder": "Search history by title...",
        "btn_redownload": "Re-download 🔄",
        "btn_delete_selected": "Delete Selected 🗑️",
        "btn_clear_all": "Clear All History",
        "col_id": "ID",
        "col_datetime": "Date & Time",

        # Settings Tab
        "group_keys": "KissKH Authentication Keys (kkey)",
        "lbl_stream_key": "Stream Key (KISSKH_STREAM_KEY):",
        "lbl_sub_key": "Subtitle Key (KISSKH_SUB_KEY):",
        "lbl_decrypt_key": "Decrypt Key (KISSKH_KEY):",
        "lbl_decrypt_iv": "Initialization Vector (KISSKH_INITIALIZATION_VECTOR):",
        "chk_show_keys": "Show Keys",
        "card_playwright_title": "Option A: Playwright Auto-Key Extractor (Recommended)",
        "playwright_desc": "Installing Playwright Chromium allows kisskh-downloader to automatically fetch stream/subtitle keys in the background for every download without entering keys manually!",
        "btn_install_playwright": "Install Playwright Chromium",
        "card_get_key_title": "Option B: Auto-Extract Keys from Episode URL",
        "get_key_desc": "Paste any KissKH episode URL below (e.g., https://kisskh.is/Drama/Show-Name/Episode-1?id=...) to extract and fill Stream and Subtitle keys into the fields above.",
        "btn_fetch_keys": "🔑 Fetch Keys Now",
        "group_pref": "Default Application Preferences",
        "lbl_def_quality": "Default Quality:",
        "lbl_def_sub_lang": "Default Subtitle Language:",
        "lbl_website_url": "KissKH Website Base URL:",
        "group_theme_lang": "Theme & Language / រចនាប័ទ្ម និង ភាសា",
        "lbl_theme": "App Theme / រចនាប័ទ្ម:",
        "lbl_language": "App Language / ភាសា:",
        "theme_dark": "Dark Mode (ងងឹត)",
        "theme_light": "Light Mode (ភ្លឺ)",
        "btn_save_settings": "Save Settings",

        # Subtitle languages
        "lang_en": "English (en)",
        "lang_id": "Indonesian (id)",
        "lang_es": "Spanish (es)",
        "lang_vi": "Vietnamese (vi)",
        "lang_th": "Thai (th)",
        "lang_pt": "Portuguese (pt)",
        "lang_ar": "Arabic (ar)",
        "lang_all": "All Languages (all)",
    },
    "km": {
        # Sidebar Menu
        "app_title": "KissKH Pro",
        "app_subtitle": "កម្មវិធីទាញយកកុន និង រឿងភាគ",
        "nav_browse": "មើល KissKH",
        "nav_downloader": "ទាញយកថ្មី",
        "nav_queue": "បញ្ជីទាញយក ({count})",
        "nav_history": "ប្រវត្តិទាញយក",
        "nav_settings": "ការកំណត់ & កូនសោ",
        "active_downloads": "កំពុងទាញយកសកម្ម: {count}",


        # Web Tab
        "btn_back": "◄ ត្រឡប់ក្រោយ",
        "btn_forward": "បន្ទាប់ ►",
        "btn_reload": "↻ ផ្ទុកឡើងវិញ",
        "btn_home": "ទំព័រដើម 🏠",
        "btn_zoom_in": "ពង្រីក +",
        "btn_zoom_out": "បង្រួម -",
        "btn_send_to_downloader": "បញ្ជូនតំណទៅទាញយក 📥",
        "address_placeholder": "បញ្ចូលតំណភ្ជាប់ KissKH...",

        # Downloader Tab
        "url_card_title": "តំណភ្ជាប់ ឬ ឈ្មោះរឿងភាគ/កុន KissKH",
        "url_placeholder": "បិទភ្ជាប់តំណ KissKH (ឧ. https://kisskh.is/Drama/...) ឬ បញ្ចូលចំណងជើង...",
        "btn_paste": "បិទភ្ជាប់តំណ",
        "group_episodes": "ការជ្រើសរើសភាគ",
        "rb_all_episodes": "ទាញយកគ្រប់ភាគទាំងអស់",
        "rb_single_episode": "ភាគទោល:",
        "rb_range_episodes": "រវាងភាគ:",
        "lbl_from": "ពីភាគ:",
        "lbl_to": "ដល់ភាគ:",
        "group_quality_sub": "ជម្រើសគុណភាព និង អក្សររត់",
        "lbl_quality": "គុណភាពវីដេអូ:",
        "chk_subtitles": "ទាញយកអក្សររត់ (Subtitles)",
        "lbl_sub_lang": "ភាសាអក្សររត់:",
        "chk_decrypt_sub": "ពន្លាឯកសារអក្សររត់",
        "card_folder_title": "ថតផ្ទុកឯកសារទាញយក",
        "btn_browse": "ស្វែងរក...",
        "btn_open_folder": "បើកថត",
        "btn_add_queue": "បន្ថែមទៅបញ្ជីទាញយក",
        "btn_download_now": "ចាប់ផ្តើមទាញយកភ្លាមៗ",

        # Queue Tab
        "queue_title": "បញ្ជីទាញយក",
        "btn_start_queue": "ចាប់ផ្តើមបញ្ជី",
        "btn_pause_queue": "ផ្អាកបញ្ជី",
        "btn_clear_completed": "សម្អាតដែលបានរួចរាល់",
        "col_title": "ចំណងជើង / តំណ",
        "col_episodes": "ចំនួនភាគ",
        "col_quality": "គុណភាព",
        "col_subtitles": "អក្សររត់",
        "col_progress": "ដំណើរការ",
        "col_status": "ស្ថានភាព",

        # History Tab
        "history_title": "ប្រវត្តិទាញយក",
        "search_history_placeholder": "ស្វែងរកប្រវត្តិតាមចំណងជើង...",
        "btn_redownload": "ទាញយកឡើងវិញ 🔄",
        "btn_delete_selected": "លុបដែលបានជ្រើស 🗑️",
        "btn_clear_all": "លុបប្រវត្តិទាំងអស់",
        "col_id": "លេខសម្គាល់",
        "col_datetime": "កាលបរិច្ឆេទ & ម៉ោង",

        # Settings Tab
        "group_keys": "កូនសោផ្ទៀងផ្ទាត់ KissKH (kkey)",
        "lbl_stream_key": "កូនសោ Stream (KISSKH_STREAM_KEY):",
        "lbl_sub_key": "កូនសោ Subtitle (KISSKH_SUB_KEY):",
        "lbl_decrypt_key": "កូនសោ ពន្លា (KISSKH_KEY):",
        "lbl_decrypt_iv": "កូនសោ IV (KISSKH_INITIALIZATION_VECTOR):",
        "chk_show_keys": "បង្ហាញកូនសោ",
        "card_playwright_title": "ជម្រើស A: កម្មវិធីទាញយកកូនសោស្វ័យប្រវត្តិ Playwright (ណែនាំ)",
        "playwright_desc": "ការដំឡើង Playwright Chromium ជួយឲ្យកម្មវិធីទាញយកកូនសោ stream/subtitle ដោយស្វ័យប្រវត្តិនៅផ្ទៃក្រោយ ដោយមិនចាំបាច់បញ្ចូលកូនសោដោយដៃ!",
        "btn_install_playwright": "ដំឡើង Playwright Chromium",
        "card_get_key_title": "ជម្រើស B: ស្រង់កូនសោស្វ័យប្រវត្តិចេញពីតំណភាគ",
        "get_key_desc": "បិទភ្ជាប់តំណភាគ KissKH ណាមួយខាងក្រោម (ឧ. https://kisskh.is/Drama/Show-Name/Episode-1?id=...) ដើម្បីស្រង់ និង បំពេញកូនសោ Stream និង Subtitle ដោយស្វ័យប្រវត្តិ។",
        "btn_fetch_keys": "🔑 ទាញយកកូនសោឥឡូវនេះ",
        "group_pref": "ការកំណត់លំនាំដើមរបស់កម្មវិធី",
        "lbl_def_quality": "គុណភាពលំនាំដើម:",
        "lbl_def_sub_lang": "ភាសាអក្សររត់លំនាំដើម:",
        "lbl_website_url": "អាសយដ្ឋានគេហទំព័រ KissKH:",
        "group_theme_lang": "រចនាប័ទ្ម និង ភាសា / Theme & Language",
        "lbl_theme": "រចនាប័ទ្មកម្មវិធី / Theme:",
        "lbl_language": "ភាសាកម្មវិធី / Language:",
        "theme_dark": "ម៉ូតងងឹត (Dark Mode)",
        "theme_light": "ម៉ូតភ្លឺ (Light Mode)",
        "btn_save_settings": "រក្សាទុកការកំណត់",

        # Subtitle languages
        "lang_en": "អង់គ្លេស (en)",
        "lang_id": "ឥណ្ឌូណេស៊ី (id)",
        "lang_es": "អេស្ប៉ាញ (es)",
        "lang_vi": "វៀតណាម (vi)",
        "lang_th": "ថៃ (th)",
        "lang_pt": "ព័រទុយហ្គាល់ (pt)",
        "lang_ar": "អារ៉ាប់ (ar)",
        "lang_all": "គ្រប់ភាសាទាំងអស់ (all)",
    }
}

def tr(key: str, lang: str = "en", **kwargs) -> str:
    """Translates key into target language with optional formatting string."""
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    text = lang_dict.get(key, TRANSLATIONS["en"].get(key, key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            pass
    return text
