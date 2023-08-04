import subprocess
import shlex
from pvaccess import Channel
import docker
import threading
from time import sleep
import sys
import os

def obtain_offset_PTP(): #linuxptp
    orden = "sudo ./linuxptp/pmc -u -b 0 'GET CURRENT_DATA_SET'"

    # pmc command in bash and obtain result in 'offsetFromMaster'
    process = subprocess.Popen(shlex.split(orden), stdout=subprocess.PIPE, text=True)
    salida, error = process.communicate()

    pos_ini = salida.find("offset")
    pos_fin = salida.find("mean")

    offsetFromMaster = salida[pos_ini+17:pos_fin]
    pos_chars = offsetFromMaster.find("\n")
    offsetFromMaster = offsetFromMaster[:pos_chars]
    offsetFromMaster = float(offsetFromMaster)

    return offsetFromMaster

def obtain_offset_NTP(ptp_instance): # chrony 
    orden = "docker exec -it ntp" + str(ptp_instance) + " chronyc tracking"

    # chronyc command in bash and obtain 'Last offset'
    process = subprocess.Popen(shlex.split(orden), stdout=subprocess.PIPE, text=True)
    salida, error = process.communicate()

    pos_ini = salida.find("Last offset     :")
    
    salida = salida[pos_ini+17:]

    pos_fin = salida.find("seconds")

    offsetFromMaster = salida[:pos_fin]
    offsetFromMaster = float(offsetFromMaster) * 1e9

    return offsetFromMaster

class run_PTP(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True

    def run(self):
        while self.running:
            self.offset = obtain_offset_PTP()
            PTP_slave.put(self.offset)

    def stop(self):
        self.running = False

class run_NTP(threading.Thread):
    def __init__(self, i):
        threading.Thread.__init__(self)
        self.running = True
        self.i = i
        self.str_i = str(self.i)
        self.is_killed = False
        self.is_up = False

    def run(self):
        while self.running:
            self.is_up = bool(int(str(channel_NTP_up[self.i].get())[55:57]))
            if self.is_up == True:
                if self.is_killed == False:
                    self.offset = obtain_offset_NTP(self.i)
                    channel_NTP[self.i].put(self.offset)

                else:
                    client.containers.run("chrony", cap_add=["SYS_TIME"], volumes=[os.getcwd() + ":/home"], auto_remove=True, network="host", name="ntp" + self.str_i, detach=True)
                    exec("NTP_container_" + self.str_i + " = client.containers.get('ntp" + self.str_i + "')")
                    self.is_killed = False
                    sleep(2)

            elif self.is_up == False:
                if self.is_killed == False:
                    exec("NTP_container_" + self.str_i + ".kill()")
                    self.is_killed = True

    def stop(self):
        self.running = False

if __name__ == "__main__":

    channel_NTP_up = []
    channel_NTP = []

    device = sys.argv[1]

    n_ntp = int(sys.argv[2])

    threads_NTP = []

    client = docker.from_env()

    # Start dockers and declare variables (Channels)

    finish_all = Channel(device + ":finish_all")
    finish_all.put(1)

    PTP_slave = Channel(device + ":PTP_slave")

    thread_PTP = run_PTP()

    for i in range(20):
        str_i = str(i)

        channel_NTP_up.append(Channel(device + ":client_up:" + str_i))
        channel_NTP.append(Channel(device + ":NTP_client:" + str_i))

        if i < n_ntp:
            client.containers.run("chrony", cap_add=["SYS_TIME"], volumes=[os.getcwd() + ":/home"], auto_remove=True, network="host", name="ntp" + str_i, detach=True)

            exec("NTP_container_"+ str_i + " = client.containers.get('ntp" + str_i + "')")

            channel_NTP_up[i].put(1)

            threads_NTP.append(run_NTP(i))

        else:
            channel_NTP_up[i].put(0)

    # ------------------------------------------------- LOOOOOP ---------------------------------------

    thread_PTP.start()

    for i in range(n_ntp):
        threads_NTP[i].start()

    while True:
        count = 0

        for i in range(n_ntp):
            if bool(int(str(channel_NTP_up[i].get())[55:57])) == False:
                count += 1

        if count == (n_ntp) or bool(int(str(finish_all.get())[55:57])) == False:
            break

    # Espera a que todos los procesos terminen
    thread_PTP.stop()

    for thread in threads_NTP:
        thread.stop()

    for i in range(n_ntp):
        str_i = str(i)
        if bool(int(str(channel_NTP_up[i].get())[55:57])) == True:
            client.containers.get("ntp" + str_i).kill()

    print("Script FINISHED! \n")
