import time
from random import random

import logger

count = 10

log = logger.logger()

for i in range(count):
    time.sleep(.5)
    log.logRace([3+random(), 3+random(), 3+random(), 3+random()])
    print(i)

