from opcua import Client
import threading
import pvaccess
dir (pvaccess)

def main(url, device):
    client = Client(url)
    
    channel_NTP = []
    channel_PTP = []

    for i in range(20):
        channel_NTP.append(pvaccess.Channel(device + ":NTP_client:" + str(i)))
        channel_PTP.append(pvaccess.Channel(device + ":PTP_slave:" + str(i)))

    client.connect()

    root = client.get_root_node()

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

    # --------------------------------- NTP --------------------------------------
    for i in range(20):
        try:
            NTP_clients.append(variables.get_child("2:NTP_client_" + str(i)))
        except:
            break

    # ----------------------------------------LOOOOOOOOOOOPPPP-----------------------------------
    while running:
        for i in range(len(NTP_clients)):
            channel_NTP[i].put(int(NTP_clients[i].get_value()))
    
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

    list_devices = ["nano2gb", "nano4gb", "rpi4"]
    list_urls = ["opc.tcp://169.254.145.193:4897", "opc.tcp://169.254.145.194:4897","opc.tcp://169.254.145.195:4897"]

    for device_i, url_i in zip(list_devices, list_urls):
        threads.append(gateway(device=device_i, url=url_i))
    
    for thread in threads:
        thread.start()

    print("Threads running!")

    try:
        while True:
            pass
    
    except KeyboardInterrupt:

        print("Trying to kill threads...")

        running = False

        for thread in threads:
            thread.join()

        print("Script FINISHED! \n")
