from flask import render_template, request, Blueprint, session
import jsonpickle

from dungeon_floors import floor_1, spooktober_floor
import services.level_service as maze_funcs

blueprint = Blueprint('level', __name__, template_folder='templates')


@blueprint.route('/test_level')
def test_level():
    dungeon, player = floor_1.initialize()
    store_data(dungeon, player)
    return render_template('levels/test_level.html', im_path=maze_funcs.get_image_path(),
                           text=maze_funcs.interact(dungeon, player))


@blueprint.route('/test_level_post', methods=['POST'])
def test_level_post():
    command = request.form['command'].strip().lower()
    dungeon, player = retrieve_data()

    if maze_funcs.start_mini_game(command, dungeon, player):
        tile = maze_funcs.get_current_tile(dungeon, player)
        if tile.creature.name == 'Thor':
            letter_tiles = [f'static/img/letters/{letter.upper()}.png' for letter in tile.creature.game.scrambled]
            store_data(dungeon, player)
            return render_template('mini_games/word_scramble.html', text=maze_funcs.mini_game_text(dungeon, player),
                                   letter_tiles=letter_tiles)
        elif tile.creature.name == 'Audumbla':
            store_data(dungeon, player)
            return render_template('mini_games/bull_cow_game.html', text=maze_funcs.mini_game_text(dungeon, player))
        else:
            raise ValueError("Trying to load mini game for an invalid creature.")

    text = maze_funcs.make_action(command, dungeon, player, floor_1.TILE_SIZE)
    if maze_funcs.check_win(dungeon, player):
        store_data(dungeon, player)
        return render_template('main/congratulations.html')

    text.extend(maze_funcs.interact(dungeon, player))
    store_data(dungeon, player)

    return render_template('levels/test_level.html', im_path=maze_funcs.get_image_path(), text=text)


@blueprint.route('/spooktober_level')
def spooktober_level():
    dungeon, player = spooktober_floor.initialize()
    store_data(dungeon, player)
    starting_text = ["You awaken in a dimly lit room. Despite being at least 12 feet wide in every "
                     "direction it feels constricting and charnel. You hesitate to move forward, but "
                     "the longer you remain motionless the more you feel a sense of unexplained "
                     "urgency build up around you, almost as if it emanated from the walls themselves.", '']
    starting_text.extend(maze_funcs.interact(dungeon, player))
    return render_template('levels/spooktober_level.html', im_path=maze_funcs.get_image_path(),
                           text=starting_text)


@blueprint.route('/spooktober_level_post', methods=['POST'])
def spooktober_level_post():
    command = request.form['command'].strip().lower()
    dungeon, player = retrieve_data()

    if maze_funcs.start_mini_game(command, dungeon, player):
        tile = maze_funcs.get_current_tile(dungeon, player)
        if tile.creature.name == 'Thor':
            letter_tiles = [f'static/img/letters/{letter.upper()}.png' for letter in tile.creature.game.scrambled]
            store_data(dungeon, player)
            return render_template('mini_games/word_scramble.html', text=maze_funcs.mini_game_text(dungeon, player),
                                   letter_tiles=letter_tiles)
        elif tile.creature.name == 'Audumbla':
            store_data(dungeon, player)
            return render_template('mini_games/bull_cow_game.html', text=maze_funcs.mini_game_text(dungeon, player))
        else:
            raise ValueError("Trying to load mini game for an invalid creature.")

    text = maze_funcs.make_action(command, dungeon, player, spooktober_floor.TILE_SIZE)
    if maze_funcs.check_win(dungeon, player):
        store_data(dungeon, player)
        return render_template('main/spooktober_end.html')

    text.extend(maze_funcs.interact(dungeon, player))
    store_data(dungeon, player)

    return render_template('levels/spooktober_level.html', im_path=maze_funcs.get_image_path(), text=text)


def store_data(dungeon, player):
    session['dungeon'], session['player'] = jsonpickle.encode(dungeon), jsonpickle.encode(player)


def retrieve_data():
    return jsonpickle.decode(session['dungeon']), jsonpickle.decode(session['player'])
