import subprocess
import shlex
from opcua import ua, Server
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
            PTP_slave.set_value(self.offset, ua.VariantType.Float)

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
                    self.offset = obtain_offset_NTP(self.i)
                    exec("NTP_client_" + self.str_i + ".set_value(" + str(self.offset) + ", ua.VariantType.Float)")

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

    n_ntp = int(sys.argv[1])

    threads_NTP = []

    client = docker.from_env()

    # OPC-UA-Server Setup

    server = Server()

    endpoint = "opc.tcp://169.254.145.195:4897"
    server.set_endpoint(endpoint)

    servername = "Pi-4-OPC-UA-Server"
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

    Finished_all = myobj.add_variable(idx, "Finish_all", True, ua.VariantType.Boolean)
    Finished_all.set_writable()

    print("Name Space and ID of Finish all : ", Finished_all)

    PTP_slave = myobj.add_variable(idx, "PTP_slave", 0, ua.VariantType.Float)
    PTP_slave.set_writable()

    print('Name Space and ID of PTP Slave: ', PTP_slave)

    thread_PTP = run_PTP()

    for i in range(20):
        str_i = str(i)
        exec("NTP_client_" + str_i + " = myobj.add_variable(idx, 'NTP_client_" + str_i + "', 0, ua.VariantType.Float)")
        exec("NTP_client_" + str_i + ".set_writable()")

        exec("print('Name Space and ID of NTP Client " + str_i + " : ', NTP_client_" + str_i + ")")

        exec("list_NTP_up[" + str_i + "] = myobj.add_variable(idx, 'list_NTP_up[" + str_i + "]', 0, ua.VariantType.Boolean)")
        exec("list_NTP_up[" + str_i + "].set_writable()")

        exec("print('Name Space and ID of NTP Conf " + str_i + " : ', list_NTP_up[" + str_i + "])")

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

        if count == (n_ntp) or Finished_all.get_value() == False:
            break

    # Espera a que todos los procesos terminen
    thread_PTP.stop()

    for thread in threads_NTP:
        thread.stop()

    for i in range(n_ntp):
        str_i = str(i)
        if list_NTP_up[i].get_value() == True:
            client.containers.get("ntp" + str_i).kill()

    server.stop()

    print("Script FINISHED! \n")
