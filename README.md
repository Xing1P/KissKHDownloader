# 🎬 KissKH Movie & Drama Downloader (PySide6 / Qt6 GUI)

[🇬🇧 English](#-english) | [🇰🇭 ភាសាខ្មែរ](#-ភាសាខ្មែរ-khmer)

---

## 🇬🇧 English

A modern, fast, and feature-rich desktop application built with **Python 3** and **PySide6 (Qt6)** to download Asian dramas, movies, anime, episodes, and subtitles from KissKH powered by `kisskh-downloader`.

---

### ✨ Key Features

- 🌐 **Embedded Web Browser**: Browse KissKH directly inside the app with a 1-click **"Send URL to Downloader 📥"** button.
- 🎨 **Light & Dark Theme Switcher**: Toggle instantly between sleek **Dark Mode** (`#0f172a`) and crisp **Light Mode** (`#f8fafc`).
- 🇰🇭 **Bilingual Support (English & Khmer ភាសាខ្មែរ)**: On-the-fly language switching powered by Google Font **Kantumruy Pro**.
- 🎬 **Flexible Episode Selection**: Download single movies, specific episode ranges (`-f` / `-l`), or **all episodes** in one click.
- 💬 **Subtitle Downloader & Decrypter**: Download subtitles in your preferred language (`English`, `Indonesian`, `Spanish`, `Vietnamese`, `Thai`, `Portuguese`, `Arabic`, `All`) with optional subtitle decryption (`KISSKH_KEY` & `KISSKH_INITIALIZATION_VECTOR`).
- 📜 **SQLite Download History**: Automatically tracks download history with search filtering, 1-click **Open Folder 📁**, and **Re-download 🔄**.
- 🔑 **Auto Key Extractor**: Built-in 1-click episode key extractor and background **Playwright Chromium** auto-key generation.
- ⚡ **Multi-Threaded Queue**: Queue up multiple series and download asynchronously without freezing the app interface.
- 💻 **Live Activity Log Console**: Real-time output log console with color-coded severity levels.

---

### 🚀 Installation & Setup

1. **Clone or Download the Repository**

2. **Create a Virtual Environment (Recommended)**
   ```bash
   python -m venv venv
   
   # Windows (PowerShell):
   .\venv\Scripts\activate
   
   # Linux / macOS:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright Chromium (Optional but Recommended for Auto-Keying)**
   ```bash
   playwright install chromium
   ```
   *(Or click "Install Playwright Chromium" inside the Settings tab of the application!)*

---

### 🏃 Running the Application

To launch the PySide6 Qt GUI application, run:

```bash
python app/main.py
```

### 📦 Building Executables & DMG (.exe / .dmg)

To build standalone binary packages for your current operating system:

```bash
python build.py
```

- **Windows**: Generates `dist/KissKH_Downloader_Windows.zip` containing `KissKH_Downloader.exe`.
- **macOS**: Generates `dist/KissKH_Downloader_macOS.dmg` disk image containing `KissKH_Downloader.app`.

---

<br/>

---

## 🇰🇭 ភាសាខ្មែរ (Khmer)

កម្មវិធីដេសថប (Desktop App) ទំនើប លឿន និងសម្បូរបែបដែលបង្កើតឡើងដោយ **Python 3** និង **PySide6 (Qt6)** សម្រាប់ទាញយក រឿងភាគអាស៊ី រឿងភាគកុន អានីមេ (Anime) និងអក្សររត់ (Subtitles) ពីគេហទំព័រ KissKH ដោយប្រើប្រាស់ `kisskh-downloader`។

---

### ✨ លក្ខណៈពិសេសចម្បង

- 🌐 **កម្មវិធីរុករកបណ្តាញដែលបានបង្កប់ (Embedded Browser)**: មើលគេហទំព័រ KissKH ដោយផ្ទាល់ក្នុងកម្មវិធី ជាមួយប៊ូតុង **"បញ្ជូនតំណទៅទាញយក 📥"** ដោយចុចតែម្តង។
- 🎨 **ការផ្លាស់ប្តូររចនាប័ទ្ម (Dark & Light Mode)**: ប្តូររវាងម៉ូតងងឹត (**Dark Mode**) និងម៉ូតភ្លឺ (**Light Mode**) បានយ៉ាងលឿន និងច្បាស់ត្រជាក់ភ្នែក។
- 🇰🇭 **គាំទ្រពីរភាសា (អង់គ្លេស & ភាសាខ្មែរ)**: ប្តូរភាសាភ្លាមៗក្នុងកម្មវិធី ដោយប្រើប្រាស់ពុម្ពអក្សរ Google Font **Kantumruy Pro** ស្រស់ស្អាត។
- 🎬 **ការជ្រើសរើសភាគទាញយក**: ទាញយកភាគទោល រវាងភាគ (ពីភាគណា ដល់ភាគណា) ឬ **ទាញយកគ្រប់ភាគទាំងអស់** ដោយចុចតែម្តង។
- 💬 **ការទាញយក និងពន្លាអក្សររត់ (Subtitles)**: ជ្រើសរើសភាសាអក្សររត់ដែលអ្នកចូលចិត្ត (អង់គ្លេស, ឥណ្ឌូណេស៊ី, អេស្ប៉ាញ, វៀតណាម, ថៃ, ព័រទុយហ្គាល់, អារ៉ាប់, ឬគ្រប់ភាសា) ព្រមទាំងមានសមត្ថភាពពន្លាឯកសារអក្សររត់ (`.srt` / `.vtt`)។
- 📜 **ប្រវត្តិទាញយក (SQLite Database)**: រក្សាទុកប្រវត្តិទាញយកដោយស្វ័យប្រវត្តិ អាចស្វែងរក បើកថតផ្ទុកឯកសារ **Open Folder 📁** និង **ទាញយកឡើងវិញ 🔄** បានយ៉ាងងាយស្រួល។
- 🔑 **ប្រព័ន្ធស្រង់កូនសោស្វ័យប្រវត្តិ**: មានឧបករណ៍ស្រង់កូនសោចេញពីតំណភាគ និងការដំឡើង **Playwright Chromium** ដើម្បីទាញយកកូនសោនៅផ្ទៃក្រោយដោយស្វ័យប្រវត្តិ។
- ⚡ **បញ្ជីទាញយកច្រើនភាគ (Multi-Threaded Queue)**: បន្ថែមរឿងភាគទៅក្នុងបញ្ជី និងទាញយកនៅផ្ទៃក្រោយដោយមិនធ្វើឲ្យកម្មវិធីគាំងឡើយ។
- 💻 **ផ្ទាំងបង្ហាញសកម្មភាព (Live Activity Log)**: មើលកំណត់ត្រាសកម្មភាពនៃដំណើរការទាញយកជាក់ស្តែងជាពណ៌បែងចែកច្បាស់លាស់។

---

### 🚀 ការដំឡើង និង ដំណើរការ

1. **ទាញយក ឬ Clone គម្រោងនេះ**

2. **បង្កើត Virtual Environment (ណែនាំ)**
   ```bash
   python -m venv venv
   
   # លើ Windows (PowerShell):
   .\venv\Scripts\activate
   
   # លើ Linux / macOS:
   source venv/bin/activate
   ```

3. **ដំឡើង Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **ដំឡើង Playwright Chromium (សម្រាប់ទាញយកកូនសោស្វ័យប្រវត្តិ)**
   ```bash
   playwright install chromium
   ```
   *(ឬចុចប៊ូតុង "ដំឡើង Playwright Chromium" នៅក្នុងផ្ទាំងការកំណត់របស់កម្មវិធី!)*

---

### 🏃 របៀបបើកដំណើរការកម្មវិធី

ដើម្បីបើកកម្មវិធី PySide6 Qt GUI សូមវាយពាក្យបញ្ជា៖

```bash
python app/main.py
```

---

### 📦 ការបង្កើនជាឯកសារដំឡើង (.exe / .dmg)

ដើម្បីបង្កើតឯកសារ executable / installer សម្រាប់ប្រព័ន្ធប្រតិបត្តិការរបស់អ្នក៖

```bash
python build.py
```

- **Windows**: នឹងបង្កើត `dist/KissKH_Downloader_Windows.zip` ដែលមាន `KissKH_Downloader.exe`។
- **macOS**: នឹងបង្កើត `dist/KissKH_Downloader_macOS.dmg` ដែលមាន `KissKH_Downloader.app`។

---

## 📜 License

This project is intended for personal and educational use.