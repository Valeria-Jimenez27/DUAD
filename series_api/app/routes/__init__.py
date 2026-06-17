from flask import Blueprint

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")

from . import auth       # noqa: F401
from . import series     # noqa: F401
from . import platforms  # noqa: F401
from . import genres     # noqa: F401
