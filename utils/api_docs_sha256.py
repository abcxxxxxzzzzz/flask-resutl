import hashlib

def encryption(api_doc_username):
    sha256 = hashlib.sha256()
    sha256.update(api_doc_username.encode('utf-8'))
    api_doc_password = sha256.hexdigest()
    return api_doc_password

