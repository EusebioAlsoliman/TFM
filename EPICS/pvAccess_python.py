import subprocess
import shlex
from pvaccess import Channel
import docker
import threading
from time import sleep
import sys
import os

def obtain_offset_PTP(): #linuxptp
    orden = "journalctl --unit=ptp4l.service"

    # from journalctl obtain the offset and freq values
    process = subprocess.Popen(shlex.split(orden), stdout=subprocess.PIPE, text=True)
    output, error = process.communicate()

    output = output[-113:]

    try: 
        pos_offset = output.find("offset")
        pos_freq = output.find("freq")
        pos_path = output.find("path")

        # Get offset
        offsetFromMaster = output[pos_offset+6:pos_freq-3]
        offsetFromMaster = float(offsetFromMaster)

        # get freq
        freq = output[pos_freq+4:pos_path]
        freq = float(freq)

        return offsetFromMaster, freq

    except:
        return -999999, -999999
    
def obtain_portState_PTP():
    orden = "sudo ./linuxptp/pmc -u -b 0 'GET PORT_DATA_SET'"

    process = subprocess.Popen(shlex.split(orden), stdout=subprocess.PIPE, text=True)
    output, error = process.communicate()

    pos = output.find("portState")
    portState = output[pos+9:]

    pos = portState.find("\n")
    portState = portState[:pos]
    portState = portState.replace(" ", "")

    return str(portState)

def obtain_slave_code_PTP():
    orden = "sudo ./linuxptp/pmc -u -b 0 'GET CURRENT_DATA_SET'"

    process = subprocess.Popen(shlex.split(orden), stdout=subprocess.PIPE, text=True)
    output, error = process.communicate()

    pos = output.find("CURRENT_DATA_SET")
    slave_code = output[pos:]
    
    pos = slave_code.find("\n")
    slave_code = slave_code[pos+2:]

    pos = slave_code.find("seq")
    slave_code = slave_code[:pos]

    return slave_code

def obtain_NTP_data(ptp_instance = 0, docker = False): # chrony 
    if docker:
        orden = "docker exec -it ntp" + str(ptp_instance) + " chronyc tracking"
    else:
        orden = "chronyc tracking"

    # chronyc command in bash and obtain 'Last offset'
    process = subprocess.Popen(shlex.split(orden), stdout=subprocess.PIPE, text=True)
    output, error = process.communicate()

    pos_offset = output.find("Last offset     :")
    
    output = output[pos_offset+17:]

    pos_fin = output.find("seconds")

    offsetFromMaster = output[:pos_fin]
    offsetFromMaster = float(offsetFromMaster) * 1e9

    pos_leap_status = output.find("Leap status     :")
    leap_status = output[pos_leap_status+17:]
    leap_status = leap_status.replace(" ", "")
    leap_status = leap_status.replace("\n", "")

    return offsetFromMaster, leap_status

class run_host(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True

    def run(self):
        while self.running:
            self.offset_PTP, self.freq = obtain_offset_PTP()
            self.offset_NTP, self.leap_status = obtain_NTP_data()
            self.portState = obtain_portState_PTP()

            PTP_slave.put(self.offset_PTP)
            PTP_freq.put(self.freq)
            portState.put(self.portState)

            NTP_host.put(self.offset_NTP)
            NTP_host_leap_status.put(self.leap_status)

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
                    self.offset, self.leap_status = obtain_NTP_data(self.i)
                    channel_NTP[self.i].put(self.offset)
                    channel_NTP_leap_status[self.i].put(self.leap_status)

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
    channel_NTP_leap_status = []

    device = sys.argv[1]

    n_ntp = int(sys.argv[2])

    threads_NTP = []

    client = docker.from_env()

    # Start dockers and declare variables (Channels)

    finish_all = Channel(device + ":finish_all")
    finish_all.put(1)

    PTP_slave = Channel(device + ":PTP_slave")

    PTP_slave_code = Channel(device + ":PTP_slave_code")
    PTP_slave_code.put(obtain_slave_code_PTP())

    PTP_freq = Channel(device + ":PTP_freq")

    portState = Channel(device + ":portState")

    NTP_host = Channel(device + ":NTP_host")
    NTP_host_leap_status = Channel(device + ":NTP_host_leap_status")

    thread_PTP = run_host()

    for i in range(20):
        str_i = str(i)

        channel_NTP_up.append(Channel(device + ":client_up:" + str_i))
        channel_NTP.append(Channel(device + ":NTP_client:" + str_i))
        channel_NTP_leap_status.append(Channel(device + ":leap_status:" + str_i))

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

        if (count == n_ntp) or bool(int(str(finish_all.get())[55:57])) == False:
            break

    # Wait for all processes to stop
    thread_PTP.stop()

    for thread in threads_NTP:
        thread.stop()

    for i in range(20):
        str_i = str(i)
        if (i < n_ntp) and (bool(int(str(channel_NTP_up[i].get())[55:57])) == True):
            client.containers.get("ntp" + str_i).kill()
        channel_NTP_up[i].put(0)

    print("Script FINISHED! \n")
