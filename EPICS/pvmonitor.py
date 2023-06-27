# https://github.com/epics-base/pvaPy
# https://epics.anl.gov/extensions/pvaPy/1.4.0/README.html

import pvaccess
dir (pvaccess)

c = pvaccess.Channel('temperature:water')

def echo(x):
    print ('New PV value:', x)

c.subscribe('echo', echo)
c.startMonitor()