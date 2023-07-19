import subprocess
import shlex
from opcua import ua, uamethod, Server
import docker
import threading

def obtain_offset_slave(ptp_instance):
    orden = "docker exec -it ptp" + str(ptp_instance) + " ./pmc -u -b 0 'GET CURRENT_DATA_SET'"
    # Lanzar pmc por la bash y obtener resultado en 'offsetFromMaster'
    process = subprocess.Popen(shlex.split(orden), stdout=subprocess.PIPE, text=True)
    salida, error = process.communicate()

    pos_ini = salida.find("offset")
    pos_fin = salida.find("mean")

    offsetFromMaster = salida[pos_ini+17:pos_fin]
    pos_chars = offsetFromMaster.find("\n")
    offsetFromMaster = offsetFromMaster[:pos_chars]
    offsetFromMaster = float(offsetFromMaster)

    return offsetFromMaster

class run_timer(threading.Thread):
    def __init__(self, i):
        threading.Thread.__init__(self)
        self.running = True
        self.i = i
        self.str_i = str(self.i)
    
    def run(self):
        while self.running:
            exec("offsetFromMaster_" + self.str_i + " = obtain_offset_slave(" + self.str_i + ")")
            self.offset = obtain_offset_slave(self.i)
            exec("Timer_" + self.str_i + ".set_value(" + str(self.offset) + ", ua.VariantType.Float)")

    def stop(self):
        self.running = False

if __name__ == "__main__":

    list_containers_up = [True, True, True, False, False, False, False, False, False, False]

    i = 0

    n = 4

    threads = []

    client = docker.from_env()

    # OPC-UA-Server Setup

    server = Server()

    endpoint = "opc.tcp://169.254.145.192:4897"
    server.set_endpoint(endpoint)

    servername = "Raspberry-OPC-UA-Server"
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

    Finished_all = myobj.add_variable(idx, "Finish all", False, ua.VariantType.Boolean)
    Finished_all.set_writable()

    print("Name Space and ID of Finish all : ", Finished_all)

    for i in range(n):

        str_i = str(i)
        exec("Timer_" + str_i + " = myobj.add_variable(idx, 'Timer_" + str_i + "', 0, ua.VariantType.Float)")
        exec("Timer_" + str_i + ".set_writable()")

        exec("print('Name Space and ID of Timer " + str_i + " : ', Timer_" + str_i + ")")

        exec("list_containers_up[" + str_i + "] = myobj.add_variable(idx, 'list_containers_up[" + str_i + "]', 0, ua.VariantType.Boolean)")
        exec("list_containers_up[" + str_i + "].set_writable()")

        exec("print('Name Space and ID of Conf " + str_i + " : ', list_containers_up[" + str_i + "])")

        client.containers.run("ptp4l", command="ptp4l -S -s -i eth0", auto_remove=True, network="multicast", name="ptp" + str(i), detach=True)

        exec("container_"+ str_i + " = client.containers.get('ptp" + str_i + "')")

        # Initialize containers_up
        exec("list_containers_up[" + str_i + "].set_value(list_containers_up[" + str_i + "], ua.VariantType.Boolean)")

        threads.append(run_timer(i))

    # OPC-UA-Server Start
    server.start()

    # ------------------------------------------------- LOOOOOP ---------------------------------------

    try:
        for i in range(n):
            threads[i].start()

        while True:
            count = 0
            for i in range(n):
                if list_containers_up[i].get_value() == False:
                    count += 1

            if count == n or Finished_all.get_value() == True:
                break

        # Espera a que todos los procesos terminen
        for thread in threads:
            thread.stop()

        server.stop()

        for i in range(n):
            str_i = str(i)
            exec("container_" + str_i + ".kill()")

        print("Script FINISHED! \n")


    except KeyboardInterrupt:
        server.stop()

        for i in range(n):
            str_i = str(i)
            exec("container_" + str_i + ".kill()")

        # Espera a que todos los procesos terminen
        for thread in threads:
            thread.join()

        # Detiene los procesos en ejecucion
        for thread in threads:
            thread.terminate()

        # Elimina los procesos terminados
        threads = []

        print("Script CANCELLED AND STOPPED! \n")