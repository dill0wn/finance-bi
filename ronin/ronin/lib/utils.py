from hashlib import sha256

from .logging import getLogger

log = getLogger('ronin.model.utils')

def read_secret(secret_name: str) -> str:
    if not secret_name.startswith('/run/secrets/'):
        secret_name = f'/run/secrets/{secret_name}'

    secret = None
    try:
        secret = open(secret_name, 'r').read().strip()
        log.debug(f"[Secret] {secret_name}: sha256-{sha256(secret.encode('utf8')).hexdigest()}")
    except FileNotFoundError as e:
        print(f"Error: {e}")

    return secret