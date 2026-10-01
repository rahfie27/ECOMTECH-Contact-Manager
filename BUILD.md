# Build Guide

## Windows

```powershell
py -m pip install -r requirements.txt
py -m pip install pyinstaller
pyinstaller --noconfirm --clean --windowed --onefile --name ECOMTECH-Contact-Manager Contact_Manager.py
```

The standalone executable will be placed in `dist/`.
