import subprocess
import shlex
from opcua import ua, uamethod, Server
import docker

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

if __name__ == "__main__":

    list_containers_up = [False, False, False, False, False, False, False, False, False, False]

    i = 0

    n = 5

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

    for i in range(n):
        str_i = str(i)
        exec("Timer_" + str_i + " = myobj.add_variable(idx, 'Timer_" + str_i + "', 0, ua.VariantType.Float)")
        exec("Timer_" + str_i + ".set_writable()")

        exec("print('Name Space and ID of Timer " + str_i + " : ', Timer_" + str_i + ")")

        client.containers.run("ptp4l:latest", command="ptp4l -S -s -i eth0", auto_remove=True, network="multicast", name="ptp" + str(i), detach=True)

        exec("container_"+ str_i + " = client.containers.get('ptp" + str_i + "')")

    # OPC-UA-Server Start
    server.start()

    try: 
        while True:
            for i in range(n):
                str_i = str(i)
                exec("offsetFromMaster_" + str_i + " = obtain_offset_slave(" + str_i + ")")
                exec("Timer_" + str_i + ".set_value(offsetFromMaster_" + str_i + ", ua.VariantType.Float)")


    except KeyboardInterrupt:
        server.stop()

        for i in range(n):
            str_i = str(i)
            exec("container_" + str_i + ".kill()")

        print("Script CANCELLED AND STOPPED!")