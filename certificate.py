import hashlib

def makecertificate(paths, receivers):
    assert(paths)
    assert(receivers)

    #Sort zipped with truncated to ensure same hash ordering
    snames, spaths = zip(*sorted([(path.rsplit('/', 1)[-1], path) for path in paths]))

    hash = hashfiles(*spaths)

    receivermails = sorted(receivers)

    return "{0}\n{1}\n{2}".format(", ".join(snames), ", ".join(receivermails), str(hash))

def writefile(filename, string):
    file = open(filename, "w+")
    file.write(string)
    file.close()

def readfile(filename):
    file = open(filename, "r")
    return file.read()

def certify(cert, imagepaths, receivers):
    storednamesraw, mailsraw, storedhash = cert.split("\n")
    storednames = storednamesraw.strip().split(", ")

    imagenames = [path.rsplit('/', 1)[-1] for path in imagepaths]
    imagenames = sorted(imagenames)
    if imagenames != storednames:
        return (False, "One or more image names has a mismatch")

    mails = mailsraw.strip().split(", ")
    if sorted(receivers) != mails:
        return (False, "One or more recipient mails has a mismatch")

    newhash = str(hashfiles(*imagenames))
    if newhash != storedhash:
        return (False, "One or more images had a mismatch")

    return (True, "The certificate was matched!")

def hashfiles(*paths):
    BLOCKSIZE = 65536
    hasher = hashlib.md5()

    for path in paths:
        with open(path, 'rb') as imagedata:
            buf = imagedata.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = imagedata.read(BLOCKSIZE)
    return hasher.hexdigest()


'''
cert = makecertificate(["apple/linux/Lenna.png", "Edit.png"], ["mail1", "mail3", "mail2"])
writefile("Certtest", cert)
cert2 = readfile("Certtest")
success, message = certify(cert2, ["apple/linux/Lenna.png", "Edit.png"], ["mail3", "mail1", "mail2"])
print(message)
'''