import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from duplicate_finder import find_image_duplicates

class DuplicateFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Поиск дубликатов")

        self.folders = []
        self.duplicates = {}

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        tk.Label(frame, text="Выбрать папку:").grid(row=0, column=0, sticky="w")
        self.folder_listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, width=50, height=10)
        self.folder_listbox.grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Добавить папку", command=self.add_folder).grid(row=0, column=2)
        tk.Button(frame, text="Удалить", command=self.remove_selected_folders).grid(row=1, column=2)

        tk.Button(frame, text="Найти дубликаты", command=self.find_duplicates).grid(row=2, column=0, columnspan=3, pady=10)

        self.progress = ttk.Progressbar(frame, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=3, column=0, columnspan=3, pady=10)

        self.tree = ttk.Treeview(frame, columns=("File"), show="headings")
        self.tree.heading("File", text="Файл")
        self.tree.grid(row=4, column=0, columnspan=3, pady=10)

        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<Button-3>", self.on_right_click)

    def add_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folders.append(folder_selected)
            self.folder_listbox.insert(tk.END, folder_selected)

    def remove_selected_folders(self):
        selected_indices = self.folder_listbox.curselection()
        for index in reversed(selected_indices):
            self.folder_listbox.delete(index)
            del self.folders[index]

    def find_duplicates(self):
        if not self.folders:
            messagebox.showwarning("Ошибка", "Нужно выбрать папку.")
            return

        self.progress["value"] = 0
        self.progress["maximum"] = 100

        def progress_callback(current, total):
            self.progress["value"] = (current / total) * 100
            self.root.update_idletasks()

        self.duplicates = find_image_duplicates(self.folders, progress_callback=progress_callback)

        for item in self.tree.get_children():
            self.tree.delete(item)

        if self.duplicates:
            for original in self.duplicates.keys():
                self.tree.insert("", "end", values=(os.path.basename(original),))
        else:
            messagebox.showinfo("Info", "Дубликатов не найдено.")

    def on_double_click(self, event):
        item = self.tree.selection()[0]
        file = self.tree.item(item, "values")[0]

        self.show_duplicates(file)

    def show_duplicates(self, file_name):
        original_path = None
        for folder in self.folders:
            potential_path = os.path.join(folder, file_name)
            if os.path.exists(potential_path):
                original_path = potential_path
                break

        if original_path and original_path in self.duplicates:
            duplicates = self.duplicates[original_path]
            top = tk.Toplevel(self.root)
            top.title(f"Дубликаты {file_name}")

            for dup in duplicates:
                img = Image.open(dup)
                img.thumbnail((400, 400))
                img = ImageTk.PhotoImage(img)

                panel = tk.Label(top, image=img)
                panel.image = img
                panel.pack()

                tk.Button(top, text="Открыть папку", command=lambda p=dup: self.open_folder(p)).pack(pady=10)
        else:
            messagebox.showinfo("Info", "Дубликатов не найдено.")

    def open_folder(self, image_path):
        os.startfile(image_path)

    def on_right_click(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            menu = tk.Menu(self.root, tearoff=0)
            menu.add_command(label="Посмотреть путь", command=self.show_path)
            menu.post(event.x_root, event.y_root)

    def show_path(self):
        item = self.tree.selection()[0]
        file = self.tree.item(item, "values")[0]
        for folder in self.folders:
            path = os.path.join(folder, file)
            if os.path.exists(path):
                messagebox.showinfo("Путь к файлу", f"Путь: {path}")
                break

def main():
    root = tk.Tk()
    app = DuplicateFinderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
