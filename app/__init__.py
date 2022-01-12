import logging
import threading
from time import sleep

from flask import Flask, Blueprint
from flask.logging import default_handler

import config


def setup_logging(application):
    logging_formatter = logging.Formatter('[%(levelname)s][%(asctime)s] in %(module)s/%(funcName)s: %(message)s')
    default_handler.setFormatter(logging_formatter)
    application.logger.addHandler(default_handler)
    return application.logger


bp = Blueprint("app", __name__)
application_object = Flask(__name__)
application_object_logger = setup_logging(application_object)

from app.proxy_loader import ProxyLoader


def initialize_application_data(application):
    application.proxy_loader = ProxyLoader()
    threading.Thread(target=application.proxy_loader.run_proxy_loader).start()
    while not all(proxy_list.__len__() > config.MINIMAL_PROXY_COUNT for proxy_list in [
        application.proxy_loader.inn_proxy_list, application.proxy_loader.suspension_proxy_list,
            application.proxy_loader.suspension_zip_proxy_list]):
        sleep(10)
    return application


def create_app(application):
    from app import routes
    application = initialize_application_data(application)
    application.register_blueprint(bp, url_prefix="/")
    application.logger.setLevel(logging.DEBUG)
    application.logger.info("nalog.ru service successfully launched")
    return application


application_object = create_app(application_object)
