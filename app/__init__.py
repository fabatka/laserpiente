import logging
import os
from configparser import ConfigParser
from logging.handlers import RotatingFileHandler
from flask_bootstrap import Bootstrap
from flask import Flask
from flask_mail import Mail

bootstrap = Bootstrap()
mail = Mail()

env_loglevel_map = {
    'dev': logging.DEBUG,
    'prod': logging.INFO
}


def create_app(config_file_path='config.ini'):
    app_instance = Flask(__name__)
    config = ConfigParser()
    config.read(config_file_path)
    app_instance.config['file'] = config
    app_instance.config['MAIL_SERVER'] = config['email']['host']
    app_instance.config['MAIL_PORT'] = config['email']['port']
    app_instance.config['MAIL_USERNAME'] = config['email']['user']
    app_instance.config['MAIL_PASSWORD'] = config['email']['password']
    app_instance.config['MAIL_USE_TLS'] = config['email']['tls'].lower() == 'true'
    app_instance.config['MAIL_USE_SSL'] = config['email']['ssl'].lower() == 'true'
    app_instance.config['MAIL_DOMAIN'] = config['email']['domain']
    app_instance.config['MAIL_RECIPIENT'] = config['email']['recipient']

    bootstrap.init_app(app_instance)
    mail.init_app(app_instance)
    from app.views.error_handlers import bp as error_handlers_bp
    app_instance.register_blueprint(error_handlers_bp)
    from app.views.error import bp as error_bp
    app_instance.register_blueprint(error_bp)
    from app.views.home import bp as home_bp
    app_instance.register_blueprint(home_bp)
    from app.views.quiz_conj_dual_indicativo_presente import bp as quiz_conj_dual_indicativo_presente_bp
    app_instance.register_blueprint(quiz_conj_dual_indicativo_presente_bp)
    from app.views.quiz_subj_probabilidad import bp as quiz_subj_probabilidad_bp
    app_instance.register_blueprint(quiz_subj_probabilidad_bp)
    from app.views.quiz_numeros import bp as quiz_numeros
    app_instance.register_blueprint(quiz_numeros)
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
