'''
Aplication manager used to create application class and define some enviroments
values.

Example:
    In order to run program we need to install pipenv and run it after install
    dependencies

        $ export NAME_APP
        $ export APP_ENV
        $ python manage.py

Attributes:

    Add modules reference

Todo:
    * Add more documentation
    * You have to also use ``sphinx.ext.todo`` extension
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import config
from router.v1.app import create_app

APP, CONF = create_app(config, config_overrides=False)
PORT = int(os.getenv('PORT') if os.getenv('PORT') else 5000)

if __name__ == '__main__':
    APP.serve('0.0.0.0', port=PORT, debug=CONF.DEBUG)
