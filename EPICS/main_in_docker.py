import subprocess
import sys
import os
import shlex
import time
import pvaccess
dir (pvaccess)

os.chdir("/home/eusebio/linuxptp")
# orden = "vcgencmd measure_temp"
orden = "sudo docker exec -it ptp" + sys.argv[1] + " ./pmc -u -b 0 'GET CURRENT_DATA_SET'"

c = pvaccess.Channel('timer_' + sys.argv[1])

while True:
    process = subprocess.Popen(shlex.split(orden), stdout=subprocess.PIPE, text=True)
    salida, error = process.communicate()

    pos_ini = salida.find("offset")
    pos_fin = salida.find("mean")

    offsetFromMaster = salida[pos_ini+17:pos_fin]
    pos_chars = offsetFromMaster.find("\n")
    offsetFromMaster = offsetFromMaster[:pos_chars]
    offsetFromMaster = int(float(offsetFromMaster))
    # print(offsetFromMaster)
    c.put(offsetFromMaster)

    time.sleep(0.5)
