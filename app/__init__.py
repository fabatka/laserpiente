import logging
import os
from configparser import ConfigParser
from logging.handlers import RotatingFileHandler
from flask_bootstrap import Bootstrap
from flask import Flask

bootstrap = Bootstrap()

env_loglevel_map = {
    'dev': logging.DEBUG,
    'prod': logging.INFO
}


def create_app(config_file_path='config.ini'):
    app_instance = Flask(__name__)
    config = ConfigParser()
    config.read(config_file_path)
    app_instance.config['file'] = config

    bootstrap.init_app(app_instance)
    from app.views.quiz import bp as quiz_bp
    app_instance.register_blueprint(quiz_bp)
    from app.static.utils import bp as utils_bp
    app_instance.register_blueprint(utils_bp)

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
