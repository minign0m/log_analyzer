import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import re
import os

class LogAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Log Error Analyzer")
        self.root.geometry("900x600")

        self.all_lines = []          # все строки файла
        self.current_lines = []      # отфильтрованные строки
        self.filename = None

        # Верхняя панель
        top = tk.Frame(root)
        top.pack(fill=tk.X, padx=5, pady=5)

        tk.Button(top, text="Открыть файл", command=self.open_file).pack(side=tk.LEFT, padx=2)
        self.file_label = tk.Label(top, text="Файл не выбран", fg="gray")
        self.file_label.pack(side=tk.LEFT, padx=10)

        # Панель фильтров
        filter_frame = tk.Frame(root)
        filter_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(filter_frame, text="Уровень:").pack(side=tk.LEFT)
        self.level_var = tk.StringVar(value="ALL")
        level_menu = tk.OptionMenu(filter_frame, self.level_var, "ALL", "ERROR", "WARNING", "INFO")
        level_menu.pack(side=tk.LEFT, padx=5)

        tk.Label(filter_frame, text="Текст:").pack(side=tk.LEFT, padx=(10, 0))
        self.search_var = tk.StringVar()
        tk.Entry(filter_frame, textvariable=self.search_var, width=30).pack(side=tk.LEFT, padx=5)

        tk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter).pack(side=tk.LEFT, padx=5)
        tk.Button(filter_frame, text="Сбросить", command=self.reset_filter).pack(side=tk.LEFT, padx=5)
        tk.Button(filter_frame, text="Экспорт", command=self.export).pack(side=tk.LEFT, padx=5)

        # Статистика
        self.stats_label = tk.Label(root, text="ERROR: 0 | WARNING: 0", fg="blue")
        self.stats_label.pack(anchor=tk.W, padx=5)

        # Текстовое поле
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 10))
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def open_file(self):
        path = filedialog.askopenfilename(
            title="Выберите LOG или TXT файл",
            filetypes=[("LOG files", "*.log"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                self.all_lines = f.readlines()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть файл:\n{e}")
            return

        self.filename = os.path.basename(path)
        self.file_label.config(text=self.filename, fg="black")
        self.current_lines = self.all_lines.copy()
        self.display_lines(self.current_lines)
        self.update_stats()

    def display_lines(self, lines):
        self.text_area.delete("1.0", tk.END)
        for line in lines:
            self.text_area.insert(tk.END, line)
        self.text_area.see("1.0")

    def apply_filter(self):
        if not self.all_lines:
            messagebox.showinfo("Нет данных", "Сначала откройте файл.")
            return

        level = self.level_var.get()
        search = self.search_var.get().strip().lower()

        filtered = []
        for line in self.all_lines:
            # фильтр по уровню
            if level != "ALL" and level not in line.upper():
                continue
            # фильтр по тексту
            if search and search not in line.lower():
                continue
            filtered.append(line)

        self.current_lines = filtered
        self.display_lines(filtered)
        if not filtered:
            messagebox.showinfo("Фильтр", "Нет строк, удовлетворяющих условиям.")

    def reset_filter(self):
        self.level_var.set("ALL")
        self.search_var.set("")
        if self.all_lines:
            self.current_lines = self.all_lines.copy()
            self.display_lines(self.current_lines)
        else:
            self.text_area.delete("1.0", tk.END)

    def update_stats(self):
        error_count = sum(1 for line in self.all_lines if "ERROR" in line.upper())
        warning_count = sum(1 for line in self.all_lines if "WARNING" in line.upper())
        self.stats_label.config(text=f"ERROR: {error_count} | WARNING: {warning_count}")

    def export(self):
        if not self.current_lines:
            messagebox.showinfo("Экспорт", "Нет данных для экспорта. Откройте файл или измените фильтр.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.writelines(self.current_lines)
            messagebox.showinfo("Экспорт", f"Сохранено: {path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LogAnalyzerApp(root)
    root.mainloop()