from config import wsgi
import json
import random
import string
from random import randint

from core.pos.models import *
from core.security.models import *

numbers = list(string.digits)
letters = list(string.ascii_letters)
alphanumeric = numbers + letters

