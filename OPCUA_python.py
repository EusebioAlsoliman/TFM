import subprocess
import shlex
from opcua import ua, Server
import docker
import threading
from time import sleep
import sys
import os

def obtain_offset_PTP(): #linuxptp
    orden = "journalctl --unit=ptp4l.service"

    # from journalctl obtain the offset and freq values
    if device == "nano2gb":
        process = subprocess.Popen(shlex.split(orden), stdout=subprocess.PIPE, universal_newlines=True)
    else:
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

    if device == "nano2gb":
        process = subprocess.Popen(shlex.split(orden), stdout=subprocess.PIPE, universal_newlines=True)
    else:
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

    if device == "nano2gb":
        process = subprocess.Popen(shlex.split(orden), stdout=subprocess.PIPE, universal_newlines=True)
    else:
        process = subprocess.Popen(shlex.split(orden), stdout=subprocess.PIPE, text=True)
    output, error = process.communicate()

    pos = output.find("CURRENT_DATA_SET")
    slave_code = output[pos:]
    
    pos = slave_code.find("\n")
    slave_code = slave_code[pos+2:]

    pos = slave_code.find("seq")
    slave_code = slave_code[:pos]

    return slave_code

def obtain_NTP_data(ptp_instance): # chrony 
    orden = "docker exec -it ntp" + str(ptp_instance) + " chronyc tracking"

    # chronyc command in bash and obtain 'Last offset'
    if device == "nano2gb":
        process = subprocess.Popen(shlex.split(orden), stdout=subprocess.PIPE, universal_newlines=True)
    else:
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
    leap_status = str(leap_status)

    return offsetFromMaster, leap_status

class run_PTP(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True

    def run(self):
        while self.running:
            self.offset, self.freq = obtain_offset_PTP()
            self.portState = obtain_portState_PTP()

            PTP_slave.set_value(self.offset, ua.VariantType.Float)
            PTP_freq.set_value(self.freq, ua.VariantType.Float)
            portState.set_value(self.portState, ua.VariantType.String)

    def stop(self):
        self.running = False

class run_NTP(threading.Thread):
    def __init__(self, i):
        threading.Thread.__init__(self)
        self.running = True
        self.i = i
        self.str_i = str(self.i)
        self.is_killed = False

    def run(self):
        while self.running:
            if list_NTP_up[self.i].get_value() == True:

                if self.is_killed == False:
                    self.offset, self.leap_status = obtain_NTP_data(self.i)
                    exec("NTP_client_" + self.str_i + ".set_value(" + str(self.offset) + ", ua.VariantType.Float)")
                    exec("NTP_leap_status_" + self.str_i + '.set_value("' + self.leap_status + '", ua.VariantType.String)')

                else:
                    client.containers.run("chrony", cap_add=["SYS_TIME"], volumes=[os.getcwd() + ":/home"], auto_remove=True, network="host", name="ntp" + self.str_i, detach=True)
                    exec("NTP_container_" + self.str_i + " = client.containers.get('ntp" + self.str_i + "')")
                    self.is_killed = False
                    sleep(2)

            elif list_NTP_up[self.i].get_value() == False:
                if self.is_killed == False:
                    exec("NTP_container_" + self.str_i + ".kill()")
                    self.is_killed = True

    def stop(self):
        self.running = False

if __name__ == "__main__":

    list_NTP_up = [False] * 20

    device = sys.argv[1]

    n_ntp = int(sys.argv[2])

    threads_NTP = []

    client = docker.from_env()

    # OPC-UA-Server Setup

    server = Server()

    if device == "rpi4":
        endpoint = "opc.tcp://169.254.145.195:4897"
        servername = "Pi-4-OPC-UA-Server"
    elif device == "nano2gb":
        endpoint = "opc.tcp://169.254.145.193:4897"
        servername = "Jetson-2GB-OPC-UA-Server"
    elif device == "nano4gb":
        endpoint = "opc.tcp://169.254.145.194:4897"
        servername = "Jetson-4GB-OPC-UA-Server"

    server.set_endpoint(endpoint)

    server.set_server_name(servername)

    # OPC-UA-Modelling

    root_node = server.get_root_node()
    object_node = server.get_objects_node()
    idx = server.register_namespace("OPCUA_SERVER")
    myobj = object_node.add_object(idx, "Variables")

    print("Root Node ID                        :", root_node)
    print("Object Node ID                      :", object_node)
    print("Name Space and ID of Variable Object:", myobj)

    # OPC-UA-Server Add Variable and start dockers

    finish_all = myobj.add_variable(idx, "Finish_all", True, ua.VariantType.Boolean)
    finish_all.set_writable()

    print("Name Space and ID of Finish all : ", finish_all)

    PTP_slave = myobj.add_variable(idx, "PTP_slave", 0, ua.VariantType.Float)
    PTP_slave.set_writable()

    print('Name Space and ID of PTP Slave: ', PTP_slave)

    PTP_slave_code = myobj.add_variable(idx, "PTP_slave_code", obtain_slave_code_PTP(), ua.VariantType.String)

    print('Name Space and ID of PTP Slave Code: ', PTP_slave_code)

    PTP_freq = myobj.add_variable(idx, "PTP_freq", 0, ua.VariantType.Float)
    PTP_freq.set_writable()

    print('Name Space and ID of PTP Freq: ', PTP_freq)

    portState = myobj.add_variable(idx, "portState", 0, ua.VariantType.String)
    portState.set_writable()

    print('Name Space and ID of port State: ', portState)

    thread_PTP = run_PTP()

    for i in range(20):
        str_i = str(i)
        exec("NTP_client_" + str_i + " = myobj.add_variable(idx, 'NTP_client_" + str_i + "', 0, ua.VariantType.Float)")
        exec("NTP_client_" + str_i + ".set_writable()")

        exec("print('Name Space and ID of NTP Client " + str_i + " : ', NTP_client_" + str_i + ")")

        exec("list_NTP_up[" + str_i + "] = myobj.add_variable(idx, 'list_NTP_up[" + str_i + "]', 0, ua.VariantType.Boolean)")
        exec("list_NTP_up[" + str_i + "].set_writable()")

        exec("print('Name Space and ID of NTP Conf " + str_i + " : ', list_NTP_up[" + str_i + "])")

        exec("NTP_leap_status_" + str_i + " = myobj.add_variable(idx, 'NTP_leap_status_" + str_i + "', '----', ua.VariantType.String)")
        exec("NTP_leap_status_" + str_i + ".set_writable()")

        exec("print('Name Space and ID of NTP Leap Status " + str_i + " : ', NTP_leap_status_" + str_i + ")")

        if i < n_ntp:
            client.containers.run("chrony", cap_add=["SYS_TIME"], volumes=[os.getcwd() + ":/home"], auto_remove=True, network="host", name="ntp" + str_i, detach=True)

            exec("NTP_container_"+ str_i + " = client.containers.get('ntp" + str_i + "')")

            # Initialize containers
            exec("list_NTP_up[" + str_i + "].set_value(True, ua.VariantType.Boolean)")

            threads_NTP.append(run_NTP(i))

        else:
            exec("list_NTP_up[" + str_i + "].set_value(False, ua.VariantType.Boolean)")

    # OPC-UA-Server Start
    server.start()

    # ------------------------------------------------- LOOOOOP ---------------------------------------

    thread_PTP.start()


    for i in range(n_ntp):
        threads_NTP[i].start()

    while True:
        count = 0

        for i in range(n_ntp):
            if list_NTP_up[i].get_value() == False:
                count += 1

        if (count == n_ntp) or finish_all.get_value() == False:
            break

    # Espera a que todos los procesos terminen
    thread_PTP.stop()

    for thread in threads_NTP:
        thread.stop()

    for i in range(n_ntp):
        str_i = str(i)
        if (i < n_ntp) and (list_NTP_up[i].get_value() == True):
            client.containers.get("ntp" + str_i).kill()
        exec("list_NTP_up[" + str_i + "].set_value(False, ua.VariantType.Boolean)")

    server.stop()

    print("Script FINISHED! \n")
