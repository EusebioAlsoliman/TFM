import subprocess
import sys
import os
import shlex
from opcua import ua, uamethod, Server
from time import sleep

def obtain_offset_slave(ptp_instance):
    orden = "sudo docker exec -it ptp" + str(ptp_instance) + " ./pmc -u -b 0 'GET CURRENT_DATA_SET'"
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

if __name__ == "__main__":

    i = 0

    # Cambiamos directorio y establecemos la orden por la bash
    os.chdir("/home/eusebio/linuxptp")
    orden_1 = "sudo docker exec -it ptp1 ./pmc -u -b 0 'GET CURRENT_DATA_SET'"
    orden_2 = "sudo docker exec -it ptp2 ./pmc -u -b 0 'GET CURRENT_DATA_SET'"
    
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

    # OPC-UA-Server Add Variable

    Temp = myobj.add_variable(idx, "Temperature", 0, ua.VariantType.Float)
    Temp.set_writable()

    print("Name Space and ID of Temperature : ", Temp)

    Timer_1 = myobj.add_variable(idx, "First timer", 0, ua.VariantType.Float)
    Timer_1.set_writable()

    print("Name Space and ID of First Timer : ", Timer_1)

    Timer_2 = myobj.add_variable(idx, "Second timer", 0, ua.VariantType.Float)
    Timer_2.set_writable()

    print("Name Space and ID of Second Timer : ", Timer_2)

    # OPC-UA-Server Start
    server.start()

    try: 
        while True:

            offsetFromMaster_1 = obtain_offset_slave(1)
            offsetFromMaster_2 = obtain_offset_slave(2)

            Timer_1.set_value(offsetFromMaster_1, ua.VariantType.Float)
            Timer_2.set_value(offsetFromMaster_2, ua.VariantType.Float)

            # Demo de la temperatura
            Temp.set_value(i*0.25, ua.VariantType.Float)
            sleep(0.5)
            if i == 20:
                i = 0
            else:
                i += 1
    except KeyboardInterrupt:
        server.stop()
