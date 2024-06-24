import os
from PIL import Image, ImageTk
import imagehash
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

def find_image_duplicates(folder, hash_size=8, progress_callback=None):
    def get_image_paths(folder):
        return [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif'))]

    def compute_hash(image_path):
        image = Image.open(image_path)
        return imagehash.average_hash(image, hash_size=hash_size)

    def find_duplicates_in_folder(folder):
        image_paths = get_image_paths(folder)
        hashes = {}
        duplicates = []

        total_images = len(image_paths)
        for i, image_path in enumerate(tqdm(image_paths, desc="Анализ изображений")):
            img_hash = compute_hash(image_path)
            if img_hash in hashes:
                duplicates.append((hashes[img_hash], image_path))
            else:
                hashes[img_hash] = image_path

            if progress_callback:
                progress_callback(i + 1, total_images)

        return duplicates

    duplicates = find_duplicates_in_folder(folder)
    return duplicates

class DuplicateFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Поиск Дубликатов v 1.0")

        self.folder_path = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        tk.Label(frame, text="Выберите папку:").grid(row=0, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.folder_path, width=50).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Выбрать", command=self.browse_folder).grid(row=0, column=2)

        tk.Button(frame, text="Искать дубликаты", command=self.find_duplicates).grid(row=1, column=0, columnspan=3, pady=10)

        self.progress = ttk.Progressbar(frame, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=2, column=0, columnspan=3, pady=10)

        self.tree = ttk.Treeview(frame, columns=("File 1", "File 2"), show="headings")
        self.tree.heading("File 1", text="Файл 1")
        self.tree.heading("File 2", text="Файл 2")
        self.tree.grid(row=3, column=0, columnspan=3, pady=10)

        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<Button-3>", self.on_right_click)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)

    def find_duplicates(self):
        folder = self.folder_path.get()
        if not folder:
            messagebox.showwarning("Ошибка", "Выберите папку.")
            return

        self.progress["value"] = 0
        self.progress["maximum"] = 100

        def progress_callback(current, total):
            self.progress["value"] = (current / total) * 100
            self.root.update_idletasks()

        duplicates = find_image_duplicates(folder, progress_callback=progress_callback)

        for item in self.tree.get_children():
            self.tree.delete(item)

        if duplicates:
            for dup in duplicates:
                self.tree.insert("", "end", values=(os.path.basename(dup[0]), os.path.basename(dup[1])))
        else:
            messagebox.showinfo("Info", "Нет дубликатов :(.")

    def on_double_click(self, event):
        item = self.tree.selection()[0]
        file1, file2 = self.tree.item(item, "values")

        self.show_image(file1)
        self.show_image(file2)

    def show_image(self, image_name):
        folder = self.folder_path.get()
        image_path = os.path.join(folder, image_name)

        top = tk.Toplevel(self.root)
        top.title(image_name)

        img = Image.open(image_path)
        img.thumbnail((400, 400))
        img = ImageTk.PhotoImage(img)

        panel = tk.Label(top, image=img)
        panel.image = img
        panel.pack()

        tk.Button(top, text="Открыть папку", command=lambda: self.open_folder(image_path)).pack(pady=10)

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
        file1, file2 = self.tree.item(item, "values")
        folder = self.folder_path.get()
        path1 = os.path.join(folder, file1)
        path2 = os.path.join(folder, file2)
        messagebox.showinfo("Путь файла", f"Файл 1: {path1}\nФайл: {path2}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DuplicateFinderApp(root)
    root.mainloop()