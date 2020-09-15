from flask import render_template, request, Blueprint, session
import jsonpickle

import dungeon_floors.floor_1 as floor_1

blueprint = Blueprint('level', __name__, template_folder='templates')


@blueprint.route('/test_level')
def test_level():
    dungeon, player = floor_1.initialize()
    store_data(dungeon, player)
    return render_template('levels/test_level.html', im_path=floor_1.get_image_path(),
                           text=floor_1.interact(dungeon, player))


@blueprint.route('/test_level_post', methods=['POST'])
def test_level_post():
    command = request.form['command'].strip().lower()
    dungeon, player = retrieve_data()
    print(f'level post')

    if floor_1.start_mini_game(command, dungeon, player):
        tile = floor_1.get_current_tile(dungeon, player)
        if tile.creature.name == 'Thor':
            letter_tiles = [f'static/img/letters/{letter.upper()}.png' for letter in tile.creature.game.scrambled]
            store_data(dungeon, player)
            return render_template('mini_games/word_scramble.html', text=floor_1.mini_game_text(dungeon, player),
                                         letter_tiles=letter_tiles)
        elif tile.creature.name == 'Audumbla':
            store_data(dungeon, player)
            return render_template('mini_games/bull_cow_game.html', text=floor_1.mini_game_text(dungeon, player))
        else:
            raise ValueError("Trying to load mini game for an invalid creature.")

    text = floor_1.make_action(command, dungeon, player)
    if floor_1.check_win(dungeon, player):
        store_data(dungeon, player)
        return render_template('main/congratulations.html')

    text.extend(floor_1.interact(dungeon, player))
    store_data(dungeon, player)

    return render_template('levels/test_level.html', im_path=floor_1.get_image_path(), text=text)


def store_data(dungeon, player):
    print(f'storing pos: {player.pos}')
    session['dungeon'], session['player'] = jsonpickle.encode(dungeon), jsonpickle.encode(player)


def retrieve_data():
    print(f'retrieving pos: {jsonpickle.decode(session["player"]).pos}')
    return jsonpickle.decode(session['dungeon']), jsonpickle.decode(session['player'])
