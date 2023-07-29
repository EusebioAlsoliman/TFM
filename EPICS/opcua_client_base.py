from opcua import Client
import pvaccess
dir (pvaccess)

if __name__ == "__main__":

    client = Client("opc.tcp://169.254.145.195:4897")

    # channel_NTP = pvaccess.Channel("rpi4:NTP_clients")
    # channel_PTP = pvaccess.Channel("rpi4:PTP_slaves")

    channel_NTP = []
    channel_PTP = []

    for i in range(20):
        channel_NTP.append(pvaccess.Channel("rpi4:NTP_client:" + str(i)))
        channel_PTP.append(pvaccess.Channel("rpi4:PTP_slave:" + str(i)))


    try:
        client.connect()

        # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
        root = client.get_root_node()
        print("Objects node is: ", root)

        # Node objects have methods to read and write node attributes as well as browse or populate address space
        print("Children of root are: ", root.get_children())

        objects = root.get_child("0:Objects")

        variables = objects.get_child("2:Variables")

        PTP_slaves = []
        NTP_clients = []

        # ---------------------------------- PTP -------------------------------------
        for i in range(20):
            try:
                PTP_slaves.append(variables.get_child("2:PTP_slave_" + str(i)))
            except:
                break

        print(PTP_slaves)
        
        for slave in PTP_slaves:
            print(slave.get_value())


        # --------------------------------- NTP --------------------------------------
        for i in range(20):
            try:
                NTP_clients.append(variables.get_child("2:NTP_client_" + str(i)))
            except:
                break
        
        print(NTP_clients)

        for clients in NTP_clients:
            print(clients.get_value())

        array_data_NTP = [0] * 20


        # ----------------------------------------LOOOOOOOOOOOPPPP-----------------------------------
        while True:
            for i in range(len(NTP_clients)):
                # array_data_NTP[i] = int(NTP_clients[i].get_value())
                channel_NTP[i].put(int(NTP_clients[i].get_value()))
            
            # channel_NTP.put(array_data_NTP)

    finally:
        client.disconnect()
        print("Client disconnected succesfully!!!!")