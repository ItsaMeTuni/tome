from .core import as_bool, get
from .database import *
from .email import *
from .jwt import *

DEBUG = as_bool(get("DEBUG", False))
