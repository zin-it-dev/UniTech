import hashlib
from urllib.parse import urlencode


def gravatar_url(email, size=40, default="identicon", rating="g"):
    digest = hashlib.sha256(email.lower().encode("utf-8")).hexdigest()
    params = urlencode({"s": size, "d": default, "r": rating})
    return f"https://www.gravatar.com/avatar/{digest}?{params}"
