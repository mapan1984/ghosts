import os
import re
import threading
from urllib.request import urlopen

from downloader import download

HOSTS_URL = r"https://github.com/racaljk/hosts/raw/master/hosts"
COMMIT_CODE_URL = "https://github.com/racaljk/hosts/blob/master/hosts"
COMMIT_CODE_REG = r'''<a\s+class="commit-tease-sha".*>\s*(.*)\s*</a>'''
LOCAL_DIR = os.path.abspath(os.path.dirname(__file__))
COMMIT_CODE_FILE = os.path.join(LOCAL_DIR, "commit_code")
HOSTS_DIR = r"C:\Windows\System32\drivers\etc"
HOSTS_PATH = os.path.join(HOSTS_DIR, "hosts")

def get_new_commit_code(url, reg):
    response = urlopen(url)
    html = response.read().decode('utf-8')
    new_commit_code = re.search(reg, html).group(1)
    response.close()
    return new_commit_code

def get_old_commit_code(filename):
    file = open(filename, "r")
    old_commit_code = file.read()
    file.close()
    return old_commit_code

def refresh_commit_code(filename, commit_code):
    file = open(filename, "w")
    file.write(commit_code)
    file.close()

if __name__ == "__main__":
    print("get new commit code...")
    new_commit_code = get_new_commit_code(COMMIT_CODE_URL, COMMIT_CODE_REG)
    if not os.path.isfile(COMMIT_CODE_FILE):
        print("refresh hosts")
        refresh_commit_code(COMMIT_CODE_FILE, new_commit_code)
        download(HOSTS_URL, HOSTS_PATH)
    else:
        print("get old commit code...")
        old_commit_code = get_old_commit_code(COMMIT_CODE_FILE)
        if old_commit_code != new_commit_code:
            print("refresh hosts")
            refresh_commit_code(COMMIT_CODE_FILE, new_commit_code)
            download(HOSTS_URL, HOSTS_PATH)
        else:
            print("hosts is newst")
