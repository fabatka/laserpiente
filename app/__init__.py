import logging
import os
from configparser import ConfigParser
from logging.handlers import RotatingFileHandler

from flask import Flask

from app.views.main import bp as main_bp
from app.static.utils import bp as utils_bp


env_loglevel_map = {
    'dev': logging.DEBUG,
    'prod': logging.INFO
}


def create_app(config_file_path='config.ini'):
    app_instance = Flask(__name__)
    config = ConfigParser()
    config.read(config_file_path)
    app_instance.config['file'] = config

    # Logging
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/laserpiente.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))

    file_handler.setLevel(env_loglevel_map[app_instance.config['file']['env']['env']])
    app_instance.logger.addHandler(file_handler)
    app_instance.logger.setLevel(env_loglevel_map[app_instance.config['file']['env']['env']])
    app_instance.logger.info('La Serpiente startup')

    return app_instance


if __name__ == '__main__':
    app = create_app()
    app.register_blueprint(main_bp)
    app.register_blueprint(utils_bp)
    app.run()
