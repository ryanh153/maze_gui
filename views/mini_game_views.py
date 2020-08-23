import flask

import dungeon_floors.floor_1 as floor_1

blueprint = flask.Blueprint('mini_games', __name__, template_folder='templates')


@blueprint.route('/word_scramble')
def word_scramble():

    tile = floor_1.get_current_tile()
    letter_tiles = [f'static/img/letters/{letter.upper()}.png' for letter in tile.creature.game.scrambled]

    return flask.render_template('mini_games/word_scramble.html', im_path=floor_1.get_image_path(),
                                 text=floor_1.game_text(),  letter_tiles=letter_tiles)


@blueprint.route('/word_scramble_post', methods=['POST'])
def word_scramble_post():
    player_guess = flask.request.form['player_guess'].strip().lower()
    solved, text = floor_1.mini_game_guess(player_guess)

    if solved:
        text.extend(floor_1.interact())
        return flask.render_template('levels/test_level.html', im_path=floor_1.get_image_path(), text=text)
    else:
        tile = floor_1.get_current_tile()
        letter_tiles = [f'static/img/letters/{letter.upper()}.png' for letter in tile.creature.game.scrambled]

        return flask.render_template('mini_games/word_scramble.html', im_path=floor_1.get_image_path(), text=text,
                                     letter_tiles=letter_tiles)


@blueprint.route('/bull_cow_game')
def bull_cow_game():
    return flask.render_template('mini_games/bull_cow_game.html', im_path=floor_1.get_image_path(),
                                 text=floor_1.game_text())


@blueprint.route('/bull_cow_game_post', methods=['POST'])
def bull_cow_game_post():
    player_guess = flask.request.form['player_guess'].strip().lower()
    solved, text = floor_1.mini_game_guess(player_guess)

    if solved:
        text.extend(floor_1.interact())
        return flask.render_template('levels/test_level.html', im_path=floor_1.get_image_path(), text=text)
    else:
        return flask.render_template('mini_games/bull_cow_game.html', im_path=floor_1.get_image_path(), text=text)
