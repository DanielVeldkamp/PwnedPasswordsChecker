import hashlib
import requests
import sys

password = sys.argv[1]

sha_1 = hashlib.sha1()
sha_1.update(password.encode("utf-8"))
passwordHash = sha_1.hexdigest().upper()

arrayOfHashes = requests.get(url = "https://api.pwnedpasswords.com/range/{}".format(passwordHash[:5])).text.split("\r\n")

noPasswordFound = True

for foundHash in arrayOfHashes:
    split = foundHash.split(":")
    if passwordHash[5:] == split[0]:
        print("{} was found\nHash {}, {} occurences".format(password, passwordHash, split[1]))
        noPasswordFound = False

if noPasswordFound:
    print("{} was not found".format(password))
