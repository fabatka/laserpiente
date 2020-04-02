from flask import Flask

from app.views.main import bp as main_bp


def create_app():
    app_instance = Flask(__name__)
    return app_instance


if __name__ == '__main__':
    app = create_app()
    app.register_blueprint(main_bp)
    app.run()
