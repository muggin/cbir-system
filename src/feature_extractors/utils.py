import imagehash

hashing_functions = {
    'ahash': imagehash.average_hash,
    'phash': imagehash.phash,
    'dhash': imagehash.dhash,
    'whash': imagehash.whash
}