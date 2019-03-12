import hashlib
import requests
import sys

# Take the password passed from the commandline as an argument
password = sys.argv[1]

# Hash the password with SHA1
sha_1 = hashlib.sha1()
sha_1.update(password.encode("utf-8"))
passwordHash = sha_1.hexdigest().upper()

# Send the first 5 characters to the API and get the response as an array
arrayOfHashes = requests.get(url = "https://api.pwnedpasswords.com/range/{}".format(passwordHash[:5])).text.split("\r\n")

noPasswordFound = True

# Check all hashes in the array, until a matching one is found or none are left, print the result
for foundHash in arrayOfHashes:
    split = foundHash.split(":")
    if passwordHash[5:] == split[0]:
        occurrences = "1 occurrence" if split[1] == "1" else "{:,d} occurrences".format(int(split[1]))
        print("{} was found\nHash {}, {}".format(password, passwordHash, occurrences))
        noPasswordFound = False

if noPasswordFound:
    print("{} was not found".format(password))
    
