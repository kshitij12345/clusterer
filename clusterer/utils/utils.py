import os
import hashlib

def ListFilesInDir(dir):
    files = []
    for root, dirnames, filenames in os.walk(dir):
        for filename in filenames:
            files.append(os.path.join(root, filename))

    return files

def make_file(file_path):
    import os
    import errno

    if not os.path.exists(os.path.dirname(file_path)):
        try:
            file_path = file_path.replace('\\','/')
            os.makedirs(os.path.dirname(file_path))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    return open(file_path, 'wb')

        
def pickle_functions(functions):
    import pickle
    for function in functions:
        functions[function] = pickle.dumps(functions[function])
    return functions

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