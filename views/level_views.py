import flask

import dungeon_floors.floor_1 as floor_1

blueprint = flask.Blueprint('level', __name__, template_folder='templates')


@blueprint.route('/test_level')
def test_level():
    floor_1.initialize()
    return flask.render_template('levels/test_level.html', im_path=floor_1.get_image_path(), text=floor_1.interact())


@blueprint.route('/test_level_post', methods=['POST'])
def test_level_post():
    command = flask.request.form['command'].strip().lower()

    if floor_1.start_mini_game(command):
        tile = floor_1.get_current_tile()
        if tile.creature.name == 'Thor':
            letter_tiles = [f'static/img/letters/{letter.upper()}.png' for letter in tile.creature.game.scrambled]
            return flask.render_template('mini_games/word_scramble.html', text=floor_1.mini_game_text(),
                                         letter_tiles=letter_tiles)
        elif tile.creature.name == 'Audumbla':
            return flask.render_template('mini_games/bull_cow_game.html', text=floor_1.mini_game_text())
        else:
            raise ValueError("Trying to load mini game for an invalid creature.")

    text = floor_1.make_action(command)
    if floor_1.check_win():
        return flask.render_template('main/congratulations.html')

    text.extend(floor_1.interact())

    return flask.render_template('levels/test_level.html', im_path=floor_1.get_image_path(),
                                 text=text)
