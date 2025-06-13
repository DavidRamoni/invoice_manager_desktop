import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sqlite3
import os
import pdfplumber
import openpyxl

# Create folders
os.makedirs("reports", exist_ok=True)

# Connect or create the SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier TEXT,
    date TEXT,
    total TEXT,
    filepath TEXT
)
''')
conn.commit()

# Extract data from PDF
def extract_pdf_data(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

    supplier = "Unknown"
    date = "Unknown"
    total = "0.00"

    for line in text.split("\n"):
        if "Supplier" in line:
            supplier = line.split(":")[-1].strip()
        if "Date" in line:
            date = line.split(":")[-1].strip()
        if "Total" in line:
            total = line.split(":")[-1].strip()

    return supplier, date, total

# Save to database
def save_invoice(supplier, date, total, filepath):
    cursor.execute("INSERT INTO invoices (supplier, date, total, filepath) VALUES (?, ?, ?, ?)",
                   (supplier, date, total, filepath))
    conn.commit()
    load_table()
    messagebox.showinfo("Saved", "Invoice successfully saved to database.")

# Export all data to Excel
def export_to_excel():
    cursor.execute("SELECT supplier, date, total FROM invoices")
    data = cursor.fetchall()
    if not data:
        messagebox.showwarning("No Data", "No invoices to export.")
        return

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Invoice Summary"
    ws.append(["Supplier", "Date", "Total"])
    for row in data:
        ws.append(row)

    output_path = os.path.join("reports", "invoices_report.xlsx")
    wb.save(output_path)
    messagebox.showinfo("Success", f"Excel report saved to:\n{output_path}")

# Load data into the table
def load_table():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT id, supplier, date, total FROM invoices")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

# Function to clear all invoices from database
def clear_invoices():
    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete all invoices?")
    if confirm:
        cursor.execute("DELETE FROM invoices")
        conn.commit()
        load_table()
        messagebox.showinfo("Cleared", "All invoices have been deleted.")

# Choose and process PDF
def select_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        try:
            supplier, date, total = extract_pdf_data(file_path)
            save_invoice(supplier, date, total, file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not read PDF:\n{e}")

# Build GUI
root = tk.Tk()
root.title("Invoice Manager")
root.geometry("600x400")

frame = tk.Frame(root)
frame.pack(pady=10)

btn_select = tk.Button(frame, text="📥 Load Invoice PDF", command=select_pdf, width=25)
btn_select.grid(row=0, column=0, padx=10)

btn_export = tk.Button(frame, text="📊 Export to Excel", command=export_to_excel, width=25)
btn_export.grid(row=0, column=1, padx=10)
btn_clear = tk.Button(frame, text="🧹 Clear Invoices", command=clear_invoices, width=25)
btn_clear.grid(row=0, column=2, padx=10)

# Table to display invoices
columns = ("ID", "Supplier", "Date", "Total")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

# Load existing data
load_table()

# Start app
root.mainloop()
conn.close()
