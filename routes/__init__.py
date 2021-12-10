from flask import Blueprint

blueprint = Blueprint('routes', __name__)

from . import search
from . import track
from . import util