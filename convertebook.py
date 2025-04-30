import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os

SUPPORTED_FORMATS = [
    "epub", "mobi", "azw3", "pdf", "txt", "htmlz", "docx", "fb2",
    "rtf", "oeb", "lit", "pdb", "lrf", "zip", "pmlz", "rb", "snb",
    "tcr", "txz"
]

class EbookConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ebook Converter")

        # Input file selection
        tk.Label(root, text="Select Input File:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.input_entry = tk.Entry(root, width=40)
        self.input_entry.grid(row=0, column=1, padx=5)
        tk.Button(root, text="Browse", command=self.browse_input).grid(row=0, column=2, padx=5)

        # Output format
        tk.Label(root, text="Select Output Format:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.format_var = tk.StringVar()
        self.format_var.set(SUPPORTED_FORMATS[0])
        self.format_menu = ttk.Combobox(root, textvariable=self.format_var, values=SUPPORTED_FORMATS, state="readonly")
        self.format_menu.grid(row=1, column=1, padx=5, pady=5, columnspan=2)

        # Output file selection
        tk.Label(root, text="Save Output As:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.output_entry = tk.Entry(root, width=40)
        self.output_entry.grid(row=2, column=1, padx=5)
        tk.Button(root, text="Browse", command=self.browse_output).grid(row=2, column=2, padx=5)

        # Convert button
        tk.Button(root, text="Convert", command=self.convert).grid(row=3, column=1, pady=15)

    def browse_input(self):
        file_path = filedialog.askopenfilename(title="Choose ebook file")
        if file_path:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, file_path)
            # Suggest default output path
            base, _ = os.path.splitext(file_path)
            default_out = f"{base}.{self.format_var.get()}"
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, default_out)

    def browse_output(self):
        file_path = filedialog.asksaveasfilename(
            title="Save as",
            defaultextension=f".{self.format_var.get()}",
            filetypes=[(f"{self.format_var.get().upper()} files", f"*.{self.format_var.get()}")]
        )
        if file_path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, file_path)

    def convert(self):
        input_file = self.input_entry.get().strip()
        output_file = self.output_entry.get().strip()
        output_format = self.format_var.get()

        if not input_file or not output_file:
            messagebox.showerror("Error", "Please select both input and output files.")
            return

        command = ["ebook-convert", input_file, output_file]
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                messagebox.showinfo("Success", f"File converted successfully:\n{output_file}")
            else:
                messagebox.showerror("Conversion Failed", result.stderr)
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = EbookConverterApp(root)
    root.mainloop()

