import flask

app = flask.Flask(__name__)


def main():
    register_blueprints()
    app.run(debug=True)


def register_blueprints():
    from views import main_views
    from views import level_views

    app.register_blueprint(main_views.blueprint)
    app.register_blueprint(level_views.blueprint)


main()
