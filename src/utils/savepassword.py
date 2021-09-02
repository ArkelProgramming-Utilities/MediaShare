import hashlib

file = open("../../config/private.txt", "w")
password = input("password: ")
hash = hashlib.sha1(password.encode())
file.write(hash.hexdigest())

file.close()