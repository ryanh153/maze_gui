import flask
import jsonpickle

import dungeon_floors.floor_1 as floor_1
import services.level_service as maze_funcs

blueprint = flask.Blueprint('mini_games', __name__, template_folder='templates')


@blueprint.route('/word_scramble')
def word_scramble():
    dungeon, player = retrieve_data()
    tile = maze_funcs.get_current_tile(dungeon, player)
    letter_tiles = [f'static/img/letters/{letter.upper()}.png' for letter in tile.creature.game.scrambled]

    return flask.render_template('mini_games/word_scramble.html', im_path=maze_funcs.get_image_path(),
                                 text=maze_funcs.game_text(),  letter_tiles=letter_tiles)


@blueprint.route('/word_scramble_post', methods=['POST'])
def word_scramble_post():
    player_guess = flask.request.form['player_guess'].strip().lower()
    dungeon, player = retrieve_data()

    if player_guess == 'exit':
        tile = maze_funcs.get_current_tile(dungeon, player)
        tile.creature.started_game = False
        text = maze_funcs.interact(dungeon, player)
        store_data(dungeon, player)
        return flask.render_template('levels/test_level.html', im_path=maze_funcs.get_image_path(), text=text)
    else:
        solved, text = maze_funcs.mini_game_guess(player_guess, dungeon, player, floor_1.TILE_SIZE)

    if solved:
        text.extend(maze_funcs.interact(dungeon, player))
        store_data(dungeon, player)
        return flask.render_template('levels/test_level.html', im_path=maze_funcs.get_image_path(), text=text)
    else:
        tile = maze_funcs.get_current_tile(dungeon, player)
        letter_tiles = [f'static/img/letters/{letter.upper()}.png' for letter in tile.creature.game.scrambled]
        store_data(dungeon, player)

        return flask.render_template('mini_games/word_scramble.html', im_path=maze_funcs.get_image_path(), text=text,
                                     letter_tiles=letter_tiles)


@blueprint.route('/bull_cow_game')
def bull_cow_game():
    return flask.render_template('mini_games/bull_cow_game.html', im_path=maze_funcs.get_image_path(),
                                 text=maze_funcs.game_text())


@blueprint.route('/bull_cow_game_post', methods=['POST'])
def bull_cow_game_post():
    player_guess = flask.request.form['player_guess'].strip().lower()
    dungeon, player = retrieve_data()

    if player_guess == 'exit':
        tile = maze_funcs.get_current_tile(dungeon, player)
        tile.creature.started_game = False
        text = maze_funcs.interact(dungeon, player)
        store_data(dungeon, player)
        return flask.render_template('levels/test_level.html', im_path=maze_funcs.get_image_path(), text=text)
    else:
        solved, text = maze_funcs.mini_game_guess(player_guess, dungeon, player, floor_1.TILE_SIZE)

    if solved:
        text.extend(maze_funcs.interact(dungeon, player))
        store_data(dungeon, player)
        return flask.render_template('levels/test_level.html', im_path=maze_funcs.get_image_path(), text=text)
    else:
        store_data(dungeon, player)
        return flask.render_template('mini_games/bull_cow_game.html', im_path=maze_funcs.get_image_path(), text=text)


def store_data(dungeon, player):
    flask.session['dungeon'], flask.session['player'] = jsonpickle.encode(dungeon), jsonpickle.encode(player)


def retrieve_data():
    return jsonpickle.decode(flask.session['dungeon']), jsonpickle.decode(flask.session['player'])
