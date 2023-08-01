from opcua import Client
from threading import Thread
from pvaccess import Channel
from time import sleep

def main(url, device):
    
    # Initialize EPICS variables (channels)
    EPICS_channel_NTP = Channel(device + ":NTP_clients")
    EPICS_channel_PTP = Channel(device + ":PTP_slaves")
    EPICS_channel_NTP_up = []

    for i in range(20):
        EPICS_channel_NTP_up.append(Channel(device + ":client_up:" + str(i)))

    EPICS_channel_finish_all = Channel(device + ":finish_all")

    # Initialize OPC UA client and variables
    client = Client(url)

    client.connect()

    root = client.get_root_node()

    objects = root.get_child("0:Objects")

    variables = objects.get_child("2:Variables")

    OPCUA_PTP_slaves = []
    OPCUA_NTP_clients = []
    OPCUA_NTP_up = []

    OPCUA_finish_all_var = variables.get_child("2:Finish_all")

    for i in range(20):
        # ---------------------------------- PTP -------------------------------------
        OPCUA_PTP_slaves.append(variables.get_child("2:PTP_slave_" + str(i)))

        # --------------------------------- NTP --------------------------------------
        OPCUA_NTP_clients.append(variables.get_child("2:NTP_client_" + str(i)))

        # ---------------------------------- NTP_client_up -------------------------------------
        OPCUA_NTP_up.append(variables.get_child("2:list_NTP_up[" + str(i) + "]"))

        EPICS_channel_NTP_up[i].put(int(OPCUA_NTP_up[i].get_value()))

    EPICS_channel_finish_all.put(0)

    array_data_NTP = [0] * 20

    # ----------------------------------------LOOOOOOOOOOOPPPP-----------------------------------
    try:
        while running:
            if i == 20:
                i = 0
                EPICS_channel_NTP.put(array_data_NTP)
                OPCUA_finish_all_var.set_value(bool(int(str(EPICS_channel_finish_all.get())[55:57])))

            array_data_NTP[i] = int(OPCUA_NTP_clients[i].get_value())
            OPCUA_NTP_up[i].set_value(bool(int(str(EPICS_channel_NTP_up[i].get())[55:57])))

            i+=1
    
    finally:
        client.disconnect()
        print("Client from device " + device + " disconnected succesfully!!!!")

class gateway(Thread):
    def __init__(self, device, url):
        Thread.__init__(self)
        self.device = device
        self.url = url

    def run(self):
        main(device=self.device, url=self.url)

if __name__ == "__main__":

    threads = []

    running = True

    list_devices = ["nano2gb", "nano4gb", "rpi4"]
    list_urls = ["opc.tcp://169.254.145.193:4897", "opc.tcp://169.254.145.194:4897", "opc.tcp://169.254.145.195:4897"]

    # list_devices = ["nano2gb"]
    # list_urls = ["opc.tcp://169.254.145.193:4897"]

    for device_i, url_i in zip(list_devices, list_urls):
        threads.append(gateway(device=device_i, url=url_i))
    
    for thread in threads:
        thread.start()

    print("Threads running!")

    try:
        while True:
            pass
    
    except KeyboardInterrupt:

        print("Killing threads...")

        running = False

        for thread in threads:
            thread.join()

        print("Script FINISHED! \n")
