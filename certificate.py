import hashlib

def makecertificate(paths, receivers):
    assert(paths)
    assert(receivers)

    spaths = sorted(paths)
    pathsstring = ", ".join(spaths)

    hash = hashfiles(*spaths)

    receivermails = sorted(receivers)

    return "{0}\n{1}\n{2}".format(pathsstring, ", ".join(receivermails), str(hash))

def writefile(filename, string):
    file = open(filename, "w+")
    file.write(string)
    file.close()

def readfile(filename):
    file = open(filename, "r")
    return file.read()

def certify(cert, receivers):
    imagenamesraw, mailsraw, storedhash = cert.split("\n")
    imagenames = imagenamesraw.strip().split(", ")
    mails = mailsraw.strip().split(", ")

    newhash = str(hashfiles(*imagenames))

    if newhash != storedhash:
        return (False, "One or more images had a mismatch")
    if sorted(receivers) != mails:
        return (False, "One or more recipient mails has a mismatch")

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


cert = makecertificate(["Edit.png", "Lenna.png"], ["mail1", "mail3", "mail2"])
writefile("Certtest", cert)
cert2 = readfile("Certtest")
success, message = certify(cert2, ["mail3", "mail1", "mail2"])
print(message)