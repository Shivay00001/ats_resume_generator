# ATS Resume Generator

Desktop GUI app (tkinter). Builds ATS-friendly resumes and exports them as PDF/DOCX/TXT.

## Run

```bash
pip install python-docx fpdf2
python main.py
```

Requires Python 3.10+ with tkinter. Verified boot on Python 3.12 (Linux, xvfb, 2026-09-24) — window initializes with no errors.

Not a web/cloud app: it is a desktop tool. Package with PyInstaller for distribution.
