import os

FILE = "user_providers.txt"

def load_user_provider(user_id):
    if not os.path.exists(FILE):
        return None
    with open(FILE, "r") as f:
        for line in f:
            if line.startswith(str(user_id) + "="):
                return line.strip().split("=")[1]
    return None

def save_user_provider(user_id, provider_name):
    lines = []
    found = False
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            lines = f.readlines()
    with open(FILE, "w") as f:
        for line in lines:
            if line.startswith(str(user_id) + "="):
                f.write(f"{user_id}={provider_name}\n")
                found = True
            else:
                f.write(line)
        if not found:
            f.write(f"{user_id}={provider_name}\n")
