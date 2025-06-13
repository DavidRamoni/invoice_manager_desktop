# Invoice PDF to Excel Converter Desktop App

This is a simple desktop application built with Python and Tkinter that allows users to load invoice PDFs, extract relevant data, and export the data to an Excel file. The app also stores invoices in a local SQLite database.

---

## Features

- Load and parse invoice PDF files
- Extract supplier, date, product details, and totals
- Display loaded invoices in a table within the app
- Export all invoice data to an Excel spreadsheet
- Clear all invoices from the database with a single click
- Simple and user-friendly GUI using Tkinter
- Standalone executable available for easy distribution

---

## Getting Started

### Prerequisites

- Python 3.x installed on your system
- Required Python packages:
  - `tkinter` (usually comes pre-installed with Python)
  - `pdfplumber`
  - `openpyxl`
  - `sqlite3` (standard library)
  - `pandas`

You can install the required packages using:

bash
pip install pdfplumber openpyxl pandas

Running the App
Clone or download this repository.

Run the app:
python app.py

Use the GUI to load invoice PDFs, view the data, export to Excel, or clear invoices.

Contact
For questions or feedback, feel free to reach out!
