from m import Pool

def parallel_process(function, data, hash_size=8, progress_callback=None):
    total_items = len(data)
    with Pool() as pool:
        results = []
        for i, result in enumerate(pool.imap_unordered(function, [(item, hash_size) for item in data])):
            results.append(result)
            if progress_callback:
                progress_callback(i + 1, total_items)
    return results


