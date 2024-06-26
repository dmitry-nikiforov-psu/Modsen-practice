import os

from hash import compute_hash_wrapper
from m import Pool

def get_image_paths(folders):
    image_paths = []
    for folder in folders:
        for root, _, files in os.walk(folder):
            image_paths.extend([os.path.join(root, f) for f in files if f.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif'))])
    return image_paths

def find_image_duplicates(folders, hash_size=8, progress_callback=None):
    image_paths = get_image_paths(folders)
    total_images = len(image_paths)

    with Pool() as pool:
        results = []
        for i, result in enumerate(pool.imap_unordered(compute_hash_wrapper, [(p, hash_size) for p in image_paths])):
            results.append(result)
            if progress_callback:
                progress_callback(i + 1, total_images)

    hashes = {}
    duplicates = {}

    for img_hash, image_path in results:
        if img_hash in hashes:
            if hashes[img_hash] not in duplicates:
                duplicates[hashes[img_hash]] = []
            duplicates[hashes[img_hash]].append(image_path)
        else:
            hashes[img_hash] = image_path

    return duplicates
