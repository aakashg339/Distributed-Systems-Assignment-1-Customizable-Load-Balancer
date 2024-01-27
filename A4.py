import hashlib

def new_hash_function(key):
    # Example: Using SHA-1 instead of MD5
    return int(hashlib.sha1(key.encode()).hexdigest(), 16)
