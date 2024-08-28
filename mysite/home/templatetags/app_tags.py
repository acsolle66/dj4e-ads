import hashlib
from urllib.parse import urlencode
from django import template

# https://brobin.me/blog/2016/07/super-simple-django-gravatar/

# A "gravatar" is a globally recognized avatar that is based on email address
# People must register their email address and then upload a gravatar
# If an email address has no gravatar, a generic image is put in its place

# To use the gravatar filter in a template include
# {% load app_tags %}

register = template.Library()


@register.filter(name="gravatar")
def gravatar(user, size=60):
    email = user.email
    email_encoded = email.strip().lower().encode("utf-8")
    email_hash = hashlib.sha256(email_encoded).hexdigest()
    params = urlencode({'s': str(size)})
    return f"https://www.gravatar.com/avatar/{email_hash}?{params}"
