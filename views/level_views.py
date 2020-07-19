import flask

import dungeon_floors.floor_1 as floor_1

blueprint = flask.Blueprint('level', __name__, template_folder='templates')


@blueprint.route('/test_level')
def test_level():
    return flask.render_template('levels/test_level.html', im_path=floor_1.im_path, text=floor_1.interact())


@blueprint.route('/player_input', methods=['POST'])
def player_input():
    if flask.request.method == 'POST':
        floor_1.move(flask.request.form['direction'])
        return flask.render_template('levels/test_level.html', im_path=floor_1.im_path, text=floor_1.interact())
