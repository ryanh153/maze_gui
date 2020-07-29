import flask

import dungeon_floors.floor_1 as floor_1

blueprint = flask.Blueprint('mini_games', __name__, template_folder='templates')


@blueprint.route('/word_scramble')
def word_scramble():
    floor_1.initialize()
    return flask.render_template('mini_games/word_scramble.html', im_path=floor_1.get_image_path(), text=floor_1.interact())


@blueprint.route('/word_scramble_post', methods=['POST'])
def word_scramble_post():
    player_guess = flask.request.form['player_guess'].strip().lower()
    text = floor_1.mini_game_guess(player_guess)

    return flask.render_template('mini_games/word_scramble.html')
