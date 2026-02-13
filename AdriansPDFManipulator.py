"""Adrian's PDF Manipulator — extract PDF pages matching search terms."""

import threading
from pathlib import Path
from tkinter import (
    BooleanVar,
    IntVar,
    StringVar,
    Tk,
    filedialog,
    messagebox,
)
from tkinter.ttk import (
    Button,
    Checkbutton,
    Entry,
    Frame,
    Label,
    LabelFrame,
    Progressbar,
    Radiobutton,
    Spinbox,
)

from pypdf import PdfReader, PdfWriter


def find_matching_pages(reader, terms, match_logic, case_sensitive, progress_cb=None):
    """Return a set of 0-based page indices whose text matches the search criteria."""
    matching = set()
    total = len(reader.pages)
    all_empty = True

    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        if text.strip():
            all_empty = False

        if not case_sensitive:
            text_check = text.lower()
            check_terms = [t.lower() for t in terms]
        else:
            text_check = text
            check_terms = terms

        if match_logic == "AND":
            if all(term in text_check for term in check_terms):
                matching.add(i)
        else:
            if any(term in text_check for term in check_terms):
                matching.add(i)

        if progress_cb:
            progress_cb(i + 1, total, f"Scanning page {i + 1}/{total}...")

    return matching, all_empty


def expand_and_merge(matching_pages, buffer_size, total_pages):
    """Expand each match by ±buffer and return a sorted list of page indices."""
    if not matching_pages:
        return []

    expanded = set()
    for p in matching_pages:
        for offset in range(-buffer_size, buffer_size + 1):
            candidate = p + offset
            if 0 <= candidate < total_pages:
                expanded.add(candidate)

    return sorted(expanded)


def create_output_pdf(reader, page_indices, output_path):
    """Copy selected pages to a new PDF file."""
    writer = PdfWriter()
    for i in page_indices:
        writer.add_page(reader.pages[i])

    with open(output_path, "wb") as f:
        writer.write(f)


class PDFManipulatorApp:
    def __init__(self, root):
        self.root = root
        root.title("Adrian's PDF Manipulator")
        root.minsize(550, 420)
        root.resizable(True, True)

        pad = {"padx": 10, "pady": 5}

        # --- File selection ---
        file_frame = LabelFrame(root, text="Input PDF(s)", padding=8)
        file_frame.pack(fill="x", **pad)

        self.file_paths = []
        self.file_display_var = StringVar(value="No files selected.")
        Entry(file_frame, textvariable=self.file_display_var, state="readonly").pack(
            side="left", fill="x", expand=True, padx=(0, 5)
        )
        Button(file_frame, text="Browse...", command=self.browse_file).pack(side="right")

        # --- Search terms ---
        terms_frame = LabelFrame(root, text="Search Terms", padding=8)
        terms_frame.pack(fill="x", **pad)

        Label(terms_frame, text="Enter search terms (comma-separated):").pack(anchor="w")
        self.terms_var = StringVar()
        Entry(terms_frame, textvariable=self.terms_var).pack(fill="x", pady=(2, 0))

        # --- Search options ---
        opts_frame = LabelFrame(root, text="Search Options", padding=8)
        opts_frame.pack(fill="x", **pad)

        logic_frame = Frame(opts_frame)
        logic_frame.pack(fill="x", pady=2)
        Label(logic_frame, text="Match logic:").pack(side="left", padx=(0, 8))
        self.match_logic_var = StringVar(value="OR")
        Radiobutton(logic_frame, text="ANY term (OR)", variable=self.match_logic_var, value="OR").pack(side="left", padx=(0, 10))
        Radiobutton(logic_frame, text="ALL terms (AND)", variable=self.match_logic_var, value="AND").pack(side="left")

        case_frame = Frame(opts_frame)
        case_frame.pack(fill="x", pady=2)
        self.case_sensitive_var = BooleanVar(value=False)
        Checkbutton(case_frame, text="Case sensitive", variable=self.case_sensitive_var).pack(side="left")

        buffer_frame = Frame(opts_frame)
        buffer_frame.pack(fill="x", pady=2)
        Label(buffer_frame, text="Page buffer (± pages around each match):").pack(side="left", padx=(0, 8))
        self.buffer_var = IntVar(value=0)
        Spinbox(buffer_frame, from_=0, to=50, textvariable=self.buffer_var, width=5).pack(side="left")

        keep_frame = Frame(opts_frame)
        keep_frame.pack(fill="x", pady=2)
        Label(keep_frame, text="Always keep first N pages:").pack(side="left", padx=(0, 8))
        self.keep_first_var = IntVar(value=0)
        Spinbox(keep_frame, from_=0, to=500, textvariable=self.keep_first_var, width=5).pack(side="left")

        # --- Action ---
        action_frame = Frame(root, padding=8)
        action_frame.pack(fill="x", **pad)
        self.extract_btn = Button(
            action_frame, text="Extract Matching Pages", command=self.process_pdf
        )
        self.extract_btn.pack(fill="x")

        # --- Progress / Status ---
        status_frame = LabelFrame(root, text="Status", padding=8)
        status_frame.pack(fill="x", **pad)

        self.progress = Progressbar(status_frame, mode="determinate")
        self.progress.pack(fill="x", pady=(0, 4))
        self.status_var = StringVar(value="Ready.")
        Label(status_frame, textvariable=self.status_var).pack(anchor="w")

    def browse_file(self):
        paths = filedialog.askopenfilenames(
            title="Select one or more PDF files",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
        )
        if paths:
            self.file_paths = list(paths)
            if len(self.file_paths) == 1:
                self.file_display_var.set(self.file_paths[0])
            else:
                self.file_display_var.set(f"{len(self.file_paths)} files selected")

    def validate_inputs(self):
        if not self.file_paths:
            messagebox.showerror("Error", "Please select one or more PDF files.")
            return None
        for fp in self.file_paths:
            if not Path(fp).is_file():
                messagebox.showerror("Error", f"File not found:\n{fp}")
                return None

        raw_terms = self.terms_var.get()
        terms = [t.strip() for t in raw_terms.split(",") if t.strip()]
        if not terms:
            messagebox.showerror("Error", "Please enter at least one search term.")
            return None

        logic = self.match_logic_var.get()
        case_sensitive = self.case_sensitive_var.get()

        try:
            buffer_size = self.buffer_var.get()
        except Exception:
            buffer_size = 0

        try:
            keep_first = self.keep_first_var.get()
        except Exception:
            keep_first = 0

        return self.file_paths, terms, logic, case_sensitive, buffer_size, keep_first

    def process_pdf(self):
        inputs = self.validate_inputs()
        if not inputs:
            return

        file_paths, terms, logic, case_sensitive, buffer_size, keep_first = inputs

        # Ask for output location before starting
        if len(file_paths) == 1:
            default_name = f"{Path(file_paths[0]).stem}_filtered.pdf"
        else:
            default_name = "merged_filtered.pdf"
        output_path = filedialog.asksaveasfilename(
            title="Save filtered PDF as",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=default_name,
        )
        if not output_path:
            return

        self.extract_btn.config(state="disabled")
        self.progress["value"] = 0
        self.status_var.set("Starting...")

        thread = threading.Thread(
            target=self._process_worker,
            args=(file_paths, terms, logic, case_sensitive, buffer_size, keep_first, output_path),
            daemon=True,
        )
        thread.start()

    def _process_worker(self, file_paths, terms, logic, case_sensitive, buffer_size, keep_first, output_path):
        writer = PdfWriter()
        total_files = len(file_paths)
        total_matched = 0
        total_output = 0
        skipped_files = []

        for file_idx, filepath in enumerate(file_paths):
            file_label = Path(filepath).name

            try:
                reader = PdfReader(filepath)
            except Exception as e:
                self.root.after(0, self._on_error, f"Cannot open {file_label}:\n{e}")
                return

            total_pages = len(reader.pages)

            def progress_cb(current, total, msg):
                prefix = f"[{file_idx + 1}/{total_files}] {file_label}: "
                self.root.after(0, self._update_progress, current, total, prefix + msg)

            matching, all_empty = find_matching_pages(
                reader, terms, logic, case_sensitive, progress_cb
            )

            if all_empty:
                skipped_files.append(file_label)
                continue

            if not matching and keep_first <= 0:
                continue

            pages_to_extract = expand_and_merge(matching, buffer_size, total_pages)

            # Always include the first N pages regardless of matches
            if keep_first > 0:
                first_pages = list(range(min(keep_first, total_pages)))
                pages_to_extract = sorted(set(pages_to_extract) | set(first_pages))

            total_matched += len(matching)
            total_output += len(pages_to_extract)

            for i in pages_to_extract:
                writer.add_page(reader.pages[i])

        if skipped_files:
            self.root.after(
                0,
                self._on_warning,
                f"No text could be extracted from: {', '.join(skipped_files)}. "
                "These may be scanned/image PDFs. OCR is not supported.",
            )

        if total_output == 0:
            self.root.after(0, self._on_info, "No pages matched your search terms in any file.")
            self.root.after(0, self._reset_ui)
            return

        self.root.after(0, self._update_progress, 0, 1, "Writing output PDF...")

        try:
            with open(output_path, "wb") as f:
                writer.write(f)
        except Exception as e:
            self.root.after(0, self._on_error, f"Failed to write output PDF:\n{e}")
            return

        self.root.after(
            0,
            self._on_complete,
            f"Done! {total_matched} page(s) matched across {total_files} file(s). "
            f"Saved {total_output} page(s) (including ±{buffer_size} buffer) to:\n{output_path}",
        )

    def _update_progress(self, current, total, message):
        if total > 0:
            self.progress["value"] = (current / total) * 100
        self.status_var.set(message)

    def _on_complete(self, message):
        self.progress["value"] = 100
        self.status_var.set("Complete.")
        self.extract_btn.config(state="normal")
        messagebox.showinfo("Success", message)

    def _on_error(self, message):
        self.status_var.set("Error.")
        self.extract_btn.config(state="normal")
        messagebox.showerror("Error", message)

    def _on_warning(self, message):
        messagebox.showwarning("Warning", message)

    def _on_info(self, message):
        self.status_var.set("No matches.")
        messagebox.showinfo("Info", message)

    def _reset_ui(self):
        self.progress["value"] = 0
        self.extract_btn.config(state="normal")


def main():
    root = Tk()
    PDFManipulatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
