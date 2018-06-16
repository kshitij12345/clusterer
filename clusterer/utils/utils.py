import os
import hashlib

def ListFilesInDir(dir):
    files = []
    for root, dirnames, filenames in os.walk(dir):
        for filename in filenames:
            files.append(os.path.join(root, filename))

    return files

def HashFile(file_path):
    # BUF_SIZE is totally arbitrary, change for your app!
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
    sha = hashlib.sha256()

    with open(file_path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha.update(data)

    return sha.hexdigest()

def CreateHashDict(files):
    HashDict = dict()
    for file in files:
        HashDict[file] = HashFile(file)

    return HashDict