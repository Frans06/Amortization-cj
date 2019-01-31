# -*- coding: utf-8 -*-
"""
This is a config file por enviroment variable definitions

Example:
    import and inherit Class::

        import config

Class Config define global and enviromental Variables.

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension
"""

import os

ENV_PATH = None
#ENV = None
class Config(): # pylint: disable-msg=R0903, R0902
    '''
        Simple config class to be heritated
    '''
    def __init__(self, LOGGER):
        LOGGER.info('Defining Enviroment variables:: App name: %s', os.getenv('APP_NAME', None))
        LOGGER.info('   Enviroment: %s', os.getenv('ENV', None))
        LOGGER.info('   Debug: %s', os.getenv('DEBUG', None))
        LOGGER.info('   Testing: %s', os.getenv('TESTING', None))


class DevelopmentConfig(Config): # pylint: disable-msg=R0903
    '''
    Config development case
    '''
    DEBUG = True
    ENV = 'development'
    '''
    selecting enviroment file
    '''

class TestConfig(Config): # pylint: disable-msg=R0903
    '''
    Config testing case
    '''
    DEBUG = True
    TESTING = True
    ENV = 'development'

class ProductionConfig(Config): # pylint: disable-msg=R0903
    '''
    Config Production case
    '''
    DEBUG = False
    ENV = 'production'

class CIConfig: # pylint: disable-msg=R0903
    '''
    Continue Integration config
    '''
    SERVICE = 'travis-ci'
    HOOK_URL = 'web-hooking-url-from-ci-service'
