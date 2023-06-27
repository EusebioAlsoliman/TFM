# https://github.com/epics-base/pvaPy
# https://epics.anl.gov/extensions/pvaPy/1.4.0/README.html

import time
import pvaccess
dir (pvaccess)

c = pvaccess.Channel('temperature:water')

while True:
    print(c.get())
    time.sleep(1)