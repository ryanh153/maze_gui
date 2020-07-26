import flask

import dungeon_floors.floor_1 as floor_1

blueprint = flask.Blueprint('level', __name__, template_folder='templates')


@blueprint.route('/test_level')
def test_level():
    floor_1.initialize()
    return flask.render_template('levels/test_level.html', im_path=floor_1.get_image_path(), text=floor_1.interact())


@blueprint.route('/player_input', methods=['POST'])
def player_input():
    command = flask.request.form['command'].strip().lower()
    text = floor_1.make_action(command)
    if floor_1.check_win():
        return flask.render_template('main/congratulations.html')
    text.extend(floor_1.interact())
    print(text)
    return flask.render_template('levels/test_level.html', im_path=floor_1.get_image_path(),
                                 text=text)
