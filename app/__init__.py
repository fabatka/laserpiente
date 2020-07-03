import logging
import os
from datetime import datetime as dt, timedelta as td
from logging.handlers import RotatingFileHandler, SMTPHandler
from flask import Flask, send_from_directory, request
from flask_mail import Mail
from flask_assets import Environment

from app.config import parse_config
from app.assets import bundles

mail = Mail()

env_loglevel_map = {
    'dev': logging.DEBUG,
    'prod': logging.INFO
}


def create_app():
    app_instance = Flask(__name__, static_folder='static')

    cnf = parse_config()
    app_instance.config['file'] = cnf
    app_instance.config['MAIL_SERVER'] = cnf['email']['host']
    app_instance.config['MAIL_PORT'] = cnf['email']['port']
    app_instance.config['MAIL_USERNAME'] = cnf['email']['user']
    app_instance.config['MAIL_PASSWORD'] = cnf['email']['password']
    app_instance.config['MAIL_USE_TLS'] = cnf['email']['tls'].lower() == 'true'
    app_instance.config['MAIL_USE_SSL'] = cnf['email']['ssl'].lower() == 'true'
    app_instance.config['MAIL_DOMAIN'] = cnf['email']['domain']
    app_instance.config['MAIL_RECIPIENT'] = cnf['email']['recipient']

    mail.init_app(app_instance)
    asset_env = Environment(app_instance)
    asset_env.register(bundles)
    from app.views.error_handlers import bp as error_handlers_bp
    app_instance.register_blueprint(error_handlers_bp)
    from app.views.error import bp as error_bp
    app_instance.register_blueprint(error_bp)
    from app.views.home import bp as home_bp
    app_instance.register_blueprint(home_bp)
    from app.views.quiz_conjugacion import bp as quiz_conj_dual_indicativo_presente_bp
    app_instance.register_blueprint(quiz_conj_dual_indicativo_presente_bp)
    from app.views.quiz_subjuntivo import bp as quiz_subjuntivo_bp
    app_instance.register_blueprint(quiz_subjuntivo_bp)
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
    if app_instance.config['file']['env']['env'] == 'dev':
        app_instance.logger.setLevel(logging.DEBUG)
        app_instance.env = 'development'
        app_instance.logger.debug('Debug mode active')
        app_instance.debug = True
    elif app_instance.config['file']['env']['env'] == 'prod':
        app_instance.logger.setLevel(logging.INFO)
        app_instance.env = 'production'

        app_instance.logger.info('Production environment detected, setting up mail log handler')
        mail_handler = SMTPHandler(
            mailhost=(app_instance.config['MAIL_SERVER'], app_instance.config['MAIL_PORT']),
            fromaddr=f"{app_instance.config['MAIL_USERNAME']}@{app_instance.config['MAIL_SERVER']}",
            toaddrs=app_instance.config['MAIL_RECIPIENT'],
            subject='La Serpiente Failure',
            credentials=(app_instance.config['MAIL_USERNAME'], app_instance.config['MAIL_PASSWORD']),
            secure=() if app_instance.config['MAIL_USE_TLS'] else None)
        mail_handler.setLevel(logging.ERROR)
        app_instance.logger.addHandler(mail_handler)

    @app_instance.after_request
    def add_headers(response):
        expiry_time = dt.utcnow() + td(days=250)
        response.headers["Expires"] = expiry_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
        response.cache_control.max_age = 60 * 60 * 24 * 250
        # to prevent clickjacking
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        # to prevent mime sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"
        # xss protection for older browsers
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response

    @app_instance.route('/robots.txt')
    @app_instance.route('/sitemap.xml')
    def static_from_root():
        return send_from_directory(app_instance.static_folder, request.path[1:])

    return app_instance
