from random import random

import logger

log = logger.logger()

log.logRace([3+random(), 3+random(), 3+random(), 3+random()])

