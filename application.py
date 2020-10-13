from flask import Flask, session
from flask_session import Session


application = Flask(__name__)
application.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
application.config['SESSION_TYPE'] = 'filesystem'
Session(application)


def register_blueprints():
    from views import main_views
    from views import level_views
    from views import mini_game_views

    application.register_blueprint(main_views.blueprint)
    application.register_blueprint(level_views.blueprint)
    application.register_blueprint(mini_game_views.blueprint)


@application.after_request
def add_header(request):
    """
    Force re-load after any request (forces re-load of map image)
    """
    request.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    request.headers["Pragma"] = "no-cache"
    request.headers["Expires"] = "0"
    return request


# blueprints must be registered in remote as well so it can't go inside if statement
register_blueprints()

if __name__ == "__main__":
    application.run(debug=False)
