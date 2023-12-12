from repositories import ImageRepository
from .level import Level
from .easy_level import EasyLevel
from .medium_level import MediumLevel
from .hard_level import HardLevel


def load_levels(images):
    return [EasyLevel(images), MediumLevel(images), HardLevel(images)]
