# ECOMTECH Contact Manager

Desktop contact-management application built with Python, PyQt5, and SQLite.

## Features

- Create, edit, delete, and search contacts
- SQLite-backed local contact storage
- Import/export VCF/vCard and CSV data
- Export selected contacts
- Contact categories and notes
- Multilingual interface
- Light/dark themes
- Persistent application settings
- VCard UID generation

## Requirements

- Python 3.10+
- PyQt5

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python Contact_Manager.py
```

## Build Windows EXE

```powershell
py -m pip install -r requirements.txt
py -m pip install pyinstaller
pyinstaller --noconfirm --clean --windowed --onefile --name ECOMTECH-Contact-Manager Contact_Manager.py
```

The executable is generated under `dist/`.

## Data

The application uses SQLite for local contact storage. Review the application code for the exact database path and settings behavior.

## License

MIT License. See `LICENSE`.
