import hashlib
import json, sys, os
# ---------------------------------------------------------------------------- #
# Prepare Class:
class Neuromancer:
    def __init__(self, filename, tolerance=10):
        self.filename = filename
        self.file_hash = ""
        self.tolerance = tolerance

    def check_tolerance(self, score):
        if score >= self.tolerance:
            return True
        else:
            return False

    def get_similarity(self, score):
        return round((score / 128) * 100, 2)

    def compare(self, sign_a, sign_b):
        score = 0
        for i in range(128):
            if sign_a[i] == sign_b[i]:
                score += 1
        return score

    def first_check(self, sign_a, sign_b):
        if sign_a == sign_b:
            return True
        else:
            return False

    def binary_to_hexadecimal(self, binary_str):
        return hex(int(binary_str, 2))

    def hash_file(self):
        try:
            with open(self.filename, "rb") as fl:
                data = fl.read()
            binary_data = ''.join(format(byte, '08b') for byte in data)
            hexadecimal_data = self.binary_to_hexadecimal(binary_data)
            self.file_hash = hashlib.blake2b(hexadecimal_data.encode("utf-8")).hexdigest()
        except Exception as error:
            print(error)


# ---------------------------------------------------------------------------- #
# Logo:
def show_logo():
    print("\033[01m") # Prepare Formating & First Color
    print("\033[35m_____   __")
    print("___  | / /________  _____________________ _________ __________________________")
    print("__   |/ /_  _ \  / / /_  ___/  __ \_  __ `__ \  __ `/_  __ \  ___/  _ \_  ___/")
    print("_  /|  / /  __/ /_/ /_  /   / /_/ /  / / / / / /_/ /_  / / / /__ /  __/  /")
    print("/_/ |_/  \___/\__,_/ /_/    \____//_/ /_/ /_/\__,_/ /_/ /_/\___/ \___//_/")
    print("\033[00m") # Reset Colors & Formating

# --------------------------------------------------------------------------- #
# Menu:
show_logo()
if len(sys.argv) != 2:
    print("\033[35m[!]\033[00m Usage: {0} <filename>".format(sys.argv[0]))
    sys.exit()

# Read file:
print("\033[35m[+]\033[00m Reading {0}.".format(sys.argv[1]))
neuro = Neuromancer(sys.argv[1])

# Hashing file:
print("\033[35m[+]\033[00m Hashing file.")
neuro.hash_file()

# Loading database:
print("\033[35m[+]\033[00m Loading database.")
if os.path.exists("sigs.json"):
    fl = open("sigs.json")
    signatures = json.load(fl)
    fl.close()
else:
    print("\033[31m[!]\033[00m The file 'sigs.json' does not exist.")
    sys.exit()

# Checking hashes:
print("\033[35m[+]\033[00m Comparing hashes. This could take a while.")
for key in signatures.keys():
    # Primary check:
    if neuro.first_check(neuro.file_hash, signatures[key]):
        print("\033[31m[!] Sample found: {0}\033[00m".format(key))
        sys.exit()
    # Tolerance check:
    score = neuro.compare(neuro.file_hash, signatures[key])
    percent = neuro.get_similarity(score)
    if neuro.check_tolerance(percent):
        print("\033[93m[!] Possible sample found: {0} [{1}%]\033[00m".format(key, percent))
        sys.exit()
# No sample found:
print("\033[32m[*] No sample found for {0}.\033[00m".format(sys.argv[1]))
