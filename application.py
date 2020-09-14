import flask


application = flask.Flask(__name__)
application.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


def main():
    register_blueprints()
    application.run(debug=False)


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
    print("made request")
    request.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    request.headers["Pragma"] = "no-cache"
    request.headers["Expires"] = "0"
    return request

# print('about to call main')
# main()
print('above if check')
if __name__ == "__main__":
    print('about to call main')
    main()