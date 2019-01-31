'''
Main flask aplication server.
'''
import os
import logging
from apistar import App, Route
from colorlog import ColoredFormatter
from .handler import amortization_table_handler
from dotenv import load_dotenv

def _setup_logger(name=__name__, propagation=True):
    """Return a logger with a default ColoredFormatter."""
    # TODO: Add Log File option
    formatter = ColoredFormatter(
        "%(log_color)s%(levelname)-8s::%(name)-12s=> %(reset)s %(blue)s%(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red',
        }
    )

    logger = logging.getLogger(name)
    for handlers in logger.handlers:
        logger.removeHandler(handlers)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = propagation
    logger = _set_logger_level(logger)
    return logger

def _set_logger_level(logger):
    """Setting logger level acconrding to env variable"""
    if os.getenv('LOG') != 'TRUE':
        if os.getenv('ENV') == 'DEV':
            logger.setLevel(level=logging.DEBUG)
        elif os.getenv('ENV') == 'PROD':
            logger.setLevel(level=logging.WARN)
        else:
            logger.setLevel(level=logging.INFO)
    return logger

def create_app(config, config_overrides=None):
    """
    Create all the API configurations, this handle the database connection, the routes
    initialization, the SSL certificate and all the error handlers

    Arguments
        name: config,             type: module,         summary: This file is in
              charge of the database connections and credentials
        name: config_overrides,   type: boolean,        summary: This will say
              if the initial config is other rather the initial one

    Call
        create_app('module')

    Response
        app server class
    """
    routes = [
        Route('/amortization-table', method='POST', handler=amortization_table_handler),
    ]

    app = App(routes=routes)
    env = os.getenv('ENV', None)
    if env is None:
        print("Environment variable 'env' not set, returning development configs.")
        env = 'DEV'
    logger = _setup_logger('werkzeug')
    if env == 'DEV':
        load_dotenv(dotenv_path='../../config/.env/.development')
        config = config.DevelopmentConfig(logger)
    elif env == 'TEST':
        load_dotenv(dotenv_path='../../config/.env/.testing')
        config = config.TestConfig(logger)
    elif env == 'PROD':
        load_dotenv(dotenv_path='../../config/.env/.production')
        config = config.ProductionConfig(logger)
    else:
        raise ValueError('Invalid environment name')
    return app, config
