#!/usr/bin/python
import os
from time import sleep

import defopt

from ronin.healthcheck import HealthcheckHandler
from ronin.healthcheck import create_app
from ronin.model.db import init_databases
from ronin.lib.logging import getLogger

HC_PORT = int(os.environ.get("RONIN_HEALTH_PORT"))

log = getLogger('ronin.main')



flapp = None

def execute(*, verbose: bool = False):

    # Create the database engine
    engine_kwargs = dict()
    if verbose:
        engine_kwargs['echo'] = 'debug'

    init_databases(**engine_kwargs)
    global flapp
    flapp = create_app()
    flapp.run(port=HC_PORT, debug=True)
    # HealthcheckHandler.run()

    try:
        log.info("Running... Hit ctrl-c to exit")
        while True:
            sleep(1)
    except KeyboardInterrupt:
        exit(0)


if __name__ == '__main__':
    log.info("Starting...")
    defopt.run(execute)