import os
from PIL import Image
import imagehash
from tqdm import tqdm

def find_image_duplicates(folder, hash_size=8):
    def get_image_paths(folder):
        return [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif'))]

    def compute_hash(image_path):
        image = Image.open(image_path)
        return imagehash.average_hash(image, hash_size=hash_size)

    def find_duplicates_in_folder(folder):
        image_paths = get_image_paths(folder)
        hashes = {}
        duplicates = []

        for image_path in tqdm(image_paths, desc="Analyzing images"):
            img_hash = compute_hash(image_path)
            if img_hash in hashes:
                duplicates.append((hashes[img_hash], image_path))
            else:
                hashes[img_hash] = image_path

        return duplicates

    duplicates = find_duplicates_in_folder(folder)
    return duplicates

def main():
    folder = 'C:/modsen/project/image1/dataset/data1'  # Укажите путь к вашей папке с изображениями

    duplicates = find_image_duplicates(folder)

    if duplicates:
        print("Found duplicates:")
        for dup in duplicates:
            print(f"Duplicate pair: {dup[0]} and {dup[1]}")
    else:
        print("No duplicates found.")

if __name__ == "__main__":
    main()