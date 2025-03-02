from accounts.models import User
import random
from django.conf import settings

from knox.models import AuthToken
from django.utils import timezone
from django.contrib.auth import login
from django.utils.text import slugify
from django.db import IntegrityError


def generate_username(name):

    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)