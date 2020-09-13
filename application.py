import flask


application = flask.Flask(__name__)
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


def main():
    register_blueprints()
    application.run(debug=True)


def register_blueprints():
    from views import main_views
    from views import level_views
    from views import mini_game_views

    application.register_blueprint(main_views.blueprint)
    application.register_blueprint(level_views.blueprint)
    application.register_blueprint(mini_game_views.blueprint)


# @app.after_request
# def add_header(request):
#     """
#     Force re-load after any request (forces re-load of map image)
#     """
#     request.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     request.headers["Pragma"] = "no-cache"
#     request.headers["Expires"] = "0"
#     return request


main()
# if __name__ == "__main__":
#     main()
