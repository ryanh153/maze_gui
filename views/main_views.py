import flask


blueprint = flask.Blueprint('main', __name__, template_folder='templates')


@blueprint.route('/')
def index():
    return flask.render_template('main/index.html')


@blueprint.route('/instructions')
def instructions():
    return flask.render_template('main/instructions.html')


@blueprint.route('/enter_code')
def enter_code():
    return flask.render_template('main/enter_code.html')


@blueprint.route('/code_entered', methods=['POST'])
def code_entered():
    if flask.request.method == 'POST':
        return flask.render_template('main/enter_code.html', text="Codes not implemented yet. Sorry.")