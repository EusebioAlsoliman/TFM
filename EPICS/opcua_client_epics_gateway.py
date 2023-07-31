from opcua import Client
import threading
import pvaccess
dir (pvaccess)

def get_bool_index(EPICS_var):
    pv = str(EPICS_var.get())
    pv_pos = pv.find("int index")
    pv = pv[pv_pos+9:]
    pv_pos = pv.find("\n")
    pv = bool(int(pv[:pv_pos]))

    return pv

def main(url, device):
    
    # Initialize EPICS variables (channels)
    EPICS_channel_NTP = []
    EPICS_channel_PTP = []
    EPICS_channel_NTP_up = []

    for i in range(20):
        EPICS_channel_NTP.append(pvaccess.Channel(device + ":NTP_client:" + str(i)))
        EPICS_channel_PTP.append(pvaccess.Channel(device + ":PTP_slave:" + str(i)))
        EPICS_channel_NTP_up.append(pvaccess.Channel(device + ":client_up:" + str(i)))

    EPICS_channel_finish_all = pvaccess.Channel(device + ":finish_all")

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

    # ----------------------------------------LOOOOOOOOOOOPPPP-----------------------------------
    try:
        while running:
            for i in range(20):
                EPICS_channel_NTP[i].put(int(OPCUA_NTP_clients[i].get_value()))
                OPCUA_NTP_up[i].set_value(get_bool_index(EPICS_channel_NTP_up[i]))
            
            OPCUA_finish_all_var.set_value(get_bool_index(EPICS_channel_finish_all))
    
    finally:
        client.disconnect()
        print("Client from device " + device + " disconnected succesfully!!!!")

class gateway(threading.Thread):
    def __init__(self, device, url):
        threading.Thread.__init__(self)
        self.device = device
        self.url = url

    def run(self):
        main(device=self.device, url=self.url)

if __name__ == "__main__":

    threads = []

    running = True

    # list_devices = ["nano2gb", "nano4gb", "rpi4"]
    # list_urls = ["opc.tcp://169.254.145.193:4897", "opc.tcp://169.254.145.194:4897", "opc.tcp://169.254.145.195:4897"]

    list_devices = ["nano2gb"]
    list_urls = ["opc.tcp://169.254.145.193:4897"]

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
