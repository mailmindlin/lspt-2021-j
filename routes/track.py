from . import blueprint
from werkzeug.exceptions import NotImplemented

@blueprint.route('/track', methods = ['POST'])
def track():
    # TODO
    raise NotImplemented()