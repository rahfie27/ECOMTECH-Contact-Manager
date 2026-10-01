import sys
import sqlite3
import json
import os
import shutil
import html
import re
import csv
import uuid
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog

# ===================== APPLICATION PATH =====================
def get_application_directory():
    """Return the real application folder in source and compiled builds.

    PyInstaller one-file builds extract bundled modules to a temporary _MEI
    directory, so __file__ must not be used for persistent application data.
    sys.executable points to the actual .exe selected by the user.
    """
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


# ===================== MULTILINGUAL SUPPORT =====================
class Translator:
    def __init__(self):
        self.current_language = "en"
        self.languages = {
            "en": "English",
            "id": "Indonesian",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "pt": "Portuguese",
            "ru": "Russian",
            "zh": "Chinese",
            "ja": "Japanese",
            "ko": "Korean",
            "ar": "Arabic",
            "hi": "Hindi",
            "bn": "Bengali",
            "tr": "Turkish",
            "it": "Italian",
            "nl": "Dutch"
        }

        self.translations = {
            "en": {
                "app_title": "Contact Manager",
                "menu_file": "File",
                "menu_import": "Import",
                "menu_export": "Export",
                "menu_tools": "Tools",
                "menu_language": "Language",
                "menu_theme": "Theme",
                "menu_help": "Help",
                "menu_about": "About",
                "menu_exit": "Exit",
                "search": "Search",
                "search_placeholder": "Search contacts...",
                "add_contact": "Add New Contact",
                "name": "Name",
                "phone": "Phone",
                "email": "Email",
                "address": "Address",
                "company": "Company",
                "job_title": "Job Title",
                "website": "Website",
                "birthday": "Birthday",
                "category": "Category",
                "notes": "Notes",
                "save": "Save",
                "edit": "Edit",
                "delete": "Delete",
                "clear": "Clear",
                "import_vcf": "Import VCF",
                "export_vcf": "Export VCF",
                "export_selected": "Export Selected",
                "export_csv": "Export CSV",
                "export_vcard": "Export VCard",
                "light_theme": "Light Theme",
                "dark_theme": "Dark Theme",
                "vcard_uid": "VCard UID",
                "last_modified": "Last modified",
                "total_contacts": "Total contacts",
                "viewing_contact": "Viewing contact",
                "adding_contact": "Adding new contact...",
                "ready": "Ready",
                "confirm_delete": "Confirm Delete",
                "delete_question": "Are you sure you want to delete",
                "validation_name": "Name is required!",
                "validation_phone": "Phone number is required!",
                "import_complete": "Import Complete",
                "export_complete": "Export Complete",
                "import_error": "Import Error",
                "export_error": "Export Error",
                "no_contacts": "No contacts to export.",
                "no_selection": "No contacts selected.",
                "success": "Success",
                "error": "Error",
                "warning": "Warning",
                "info": "Information",
                "category_family": "Family",
                "category_friends": "Friends",
                "category_work": "Work",
                "category_other": "Other",
                "phone_mobile": "Mobile",
                "phone_home": "Home",
                "phone_work": "Work",
                "phone_other": "Other",
                "email_personal": "Personal",
                "email_work": "Work",
                "email_other": "Other",
                "generate_uids": "Generate VCard UIDs",
                "generate_uids_question": "Generate unique VCard UIDs for all contacts?",
                "uids_generated": "VCard UIDs generated for all contacts.",
                "import_contacts": "Import Contacts",
                "export_contacts": "Export Contacts",
                "select_file": "Select File",
                "all_files": "All Files",
                "vcf_files": "VCard Files",
                "csv_files": "CSV Files",
                "settings": "Settings",
                "language_settings": "Language Settings",
                "theme_settings": "Theme Settings",
                "save_settings": "Save Settings",
                "cancel": "Cancel",
                "close": "Close",
                "yes": "Yes",
                "no": "No",
                "ok": "OK",
                "about_title": "About Contact Manager",
                "about_content": "Created by:\n"
                                "rahfie27\n"
                                "E-COMPUTER\n"
                                "SERVICE KOMPUTER PANGGILAN BOGOR\n"
                                "Copyright © ECOMTECH 2026 - All Right Reserved\n\n"
                                "WARNING!\n"
                                "MAY CONTAIN A LOT OF BUGS\n"
                                "This software is provided as-is without warranty.",
                "duplicate_handling": "Found {} contacts. How to import?",
                "keep_all": "Keep All",
                "skip_duplicates": "Skip Duplicates",
                "import_count": "Imported {} contacts.",
                "duplicate_count": "Skipped {} duplicates.",
                "export_count": "Exported {} contacts.",
                "select_contacts": "Select contacts from the list.",
                "contact_deleted": "Deleted contact",
                "contact_added": "Added new contact",
                "contact_updated": "Updated contact"
            },
            "id": {
                "app_title": "Manajer Kontak",
                "menu_file": "File",
                "menu_import": "Impor",
                "menu_export": "Ekspor",
                "menu_tools": "Alat",
                "menu_language": "Bahasa",
                "menu_theme": "Tema",
                "menu_help": "Bantuan",
                "menu_about": "Tentang",
                "menu_exit": "Keluar",
                "search": "Cari",
                "search_placeholder": "Cari kontak...",
                "add_contact": "Tambah Kontak Baru",
                "name": "Nama",
                "phone": "Telepon",
                "email": "Email",
                "address": "Alamat",
                "company": "Perusahaan",
                "job_title": "Jabatan",
                "website": "Website",
                "birthday": "Tanggal Lahir",
                "category": "Kategori",
                "notes": "Catatan",
                "save": "Simpan",
                "edit": "Edit",
                "delete": "Hapus",
                "clear": "Bersihkan",
                "import_vcf": "Impor VCF",
                "export_vcf": "Ekspor VCF",
                "export_selected": "Ekspor Terpilih",
                "export_csv": "Ekspor CSV",
                "export_vcard": "Ekspor VCard",
                "light_theme": "Tema Terang",
                "dark_theme": "Tema Gelap",
                "vcard_uid": "UID VCard",
                "last_modified": "Terakhir diubah",
                "total_contacts": "Total kontak",
                "viewing_contact": "Melihat kontak",
                "adding_contact": "Menambahkan kontak baru...",
                "ready": "Siap",
                "confirm_delete": "Konfirmasi Hapus",
                "delete_question": "Yakin ingin menghapus",
                "validation_name": "Nama diperlukan!",
                "validation_phone": "Nomor telepon diperlukan!",
                "import_complete": "Impor Selesai",
                "export_complete": "Ekspor Selesai",
                "import_error": "Kesalahan Impor",
                "export_error": "Kesalahan Ekspor",
                "no_contacts": "Tidak ada kontak untuk diekspor.",
                "no_selection": "Tidak ada kontak terpilih.",
                "success": "Berhasil",
                "error": "Kesalahan",
                "warning": "Peringatan",
                "info": "Informasi",
                "category_family": "Keluarga",
                "category_friends": "Teman",
                "category_work": "Kerja",
                "category_other": "Lainnya",
                "phone_mobile": "Ponsel",
                "phone_home": "Rumah",
                "phone_work": "Kantor",
                "phone_other": "Lainnya",
                "email_personal": "Pribadi",
                "email_work": "Kantor",
                "email_other": "Lainnya",
                "generate_uids": "Buat UID VCard",
                "generate_uids_question": "Buat UID VCard unik untuk semua kontak?",
                "uids_generated": "UID VCard dibuat untuk semua kontak.",
                "import_contacts": "Impor Kontak",
                "export_contacts": "Ekspor Kontak",
                "select_file": "Pilih File",
                "all_files": "Semua File",
                "vcf_files": "File VCard",
                "csv_files": "File CSV",
                "settings": "Pengaturan",
                "language_settings": "Pengaturan Bahasa",
                "theme_settings": "Pengaturan Tema",
                "save_settings": "Simpan Pengaturan",
                "cancel": "Batal",
                "close": "Tutup",
                "yes": "Ya",
                "no": "Tidak",
                "ok": "OK",
                "about_title": "Tentang Manajer Kontak",
                "about_content": "Dibuat oleh:\n"
                                "rahfie27\n"
                                "E-COMPUTER\n"
                                "SERVICE KOMPUTER PANGGILAN BOGOR\n"
                                "Hak Cipta © ECOMTECH 2026 - Semua Hak Dilindungi\n\n"
                                "PERINGATAN!\n"
                                "MUNGKIN TERDAPAT BANYAK BUG\n"
                                "Software ini diberikan apa adanya tanpa garansi.",
                "duplicate_handling": "Ditemukan {} kontak. Bagaimana mengimpor?",
                "keep_all": "Simpan Semua",
                "skip_duplicates": "Lewati Duplikat",
                "import_count": "Diimpor {} kontak.",
                "duplicate_count": "Dilewati {} duplikat.",
                "export_count": "Diekspor {} kontak.",
                "select_contacts": "Pilih kontak dari daftar.",
                "contact_deleted": "Kontak dihapus",
                "contact_added": "Kontak baru ditambahkan",
                "contact_updated": "Kontak diperbarui"
            }
        }

