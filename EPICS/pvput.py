# https://github.com/epics-base/pvaPy
# https://epics.anl.gov/extensions/pvaPy/1.4.0/README.html

import time
import pvaccess
dir (pvaccess)

c = pvaccess.Channel('temperature:water')
i = 0

while True:
    if i == 10:
        i = 0
    c.put(20 + i)
    i += 1
    time.sleep(1)