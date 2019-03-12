#!/usr/bin/python3
import hashlib
import requests
import argparse

FOUND_STRING = '''your password was found:
- Hash {password_hash}
- {occurrences}'''

NOT_FOUND_STRING = "your password wasn't found"

# Take the password passed from the commandline as an argument
parser = argparse.ArgumentParser()
file_or_string = parser.add_mutually_exclusive_group(required=True)
file_or_string.add_argument(
    '-F', '--file', type=str, help="file to read password from (only the first line is read)")
file_or_string.add_argument(
    '-P', '--password', type=str, help="provide password in plaintext (CAUTION: may appear in logs!)")
args = parser.parse_args()

password = ''

# Depending on the provided arguments, either read password from file or use it directly
if args.file:
    with open(args.file, 'r') as f:
        password = f.readline().strip()
else:
    password = args.password

# Hash the password with SHA1
sha_1 = hashlib.sha1()
sha_1.update(password.encode("utf-8"))
password_hash = sha_1.hexdigest().upper()

# Send the first 5 characters to the API and get the response as an array
url = "https://api.pwnedpasswords.com/range/{}".format(password_hash[:5])
list_of_hashes = requests.get(url=url).text.split("\r\n")

found_password = False

# Check all hashes in the array, until a matching one is found or none are left, print the result
for foundHash in list_of_hashes:
    split = foundHash.split(":")
    if password_hash[5:] == split[0]:
        occurrences = "1 occurrence" if split[1] == "1" else "{:,d} occurrences".format(int(split[1]))
        print(FOUND_STRING.format(password_hash=password_hash, occurrences=occurrences))
        found_password = True
        break
if not found_password:
    print(NOT_FOUND_STRING)
