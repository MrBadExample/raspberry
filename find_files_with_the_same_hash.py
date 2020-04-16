import hashlib
import os


# r - for text files
# rb - for non-text files
def gethash(file):
    hasher = hashlib.md5()
    with open(file, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()


def build_hashmap(diretory):
    hashmap = {}
    for folder, dirs, files in os.walk(diretory):
        for file in files:
            path = os.path.join(folder, file)
            if os.path.islink(path):
                continue
            hash = gethash(path)
            if hash in hashmap:
                matching = hashmap[hash]
                print("{} and {} are the same files. Hash of both is {}".format(path, matching, hash))
            else:
                hashmap[hash] = path

print(build_hashmap("/home/pi/Pictures"))


