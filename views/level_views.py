from pathlib import Path

import flask

from scripts.floor_1 import move

blueprint = flask.Blueprint('level', __name__, template_folder='templates')


@blueprint.route('/test_level')
def test_level():
    im_path = Path('static/img/my_image.png').absolute()
    return flask.render_template('levels/test_level.html', im_path=im_path)


@blueprint.route('/player_input', methods=['POST'])
def player_input():
    if flask.request.method == 'POST':
        print(flask.request.form['direction'])
        print(type(flask.request.form['direction']))
        move(flask.request.form['direction'])
        im_path = Path('static/img/my_image.png').absolute()
        return flask.render_template('levels/test_level.html', im_path=im_path)
