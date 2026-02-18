from .client import trending
from .models import Repo
from importlib.metadata import version

__version__ = version("github-trending-repos-api")
__all__ = ["trending", "Repo"]
