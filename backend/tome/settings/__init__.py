from .core import as_bool, get
from .database import *  # noqa: F401 F403
from .email import *  # noqa: F401 F403
from .jwt import *  # noqa: F401 F403
from .signup import *  # noqa: F401 F403

DEBUG = as_bool(get("DEBUG", False))
