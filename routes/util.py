from os import mkdir

from flask import json, request
from . import blueprint
from time import strftime
from datetime import datetime

gpc_update = datetime(year=2021, month=12, day=9, hour=0, minute=0, second=0, microsecond=0)

gpc_update
@blueprint.route('/.well-known/gpc.json', methods = ['GET'])
def gpc():
    """
    See [https://globalprivacycontrol.github.io/gpc-spec/]
    """
    response = json.jsonify(
        gpc = True,
        lastUpdate = strftime("%Y-%m-%d", gpc_update.timetuple())
    )
    response.last_modified = gpc_update
    return response