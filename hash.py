from PIL import Image
import imagehash

def compute_hash(image_path, hash_size=8):
    image = Image.open(image_path)
    return imagehash.average_hash(image, hash_size=hash_size), image_path

def compute_hash_wrapper(args):
    return compute_hash(*args)
