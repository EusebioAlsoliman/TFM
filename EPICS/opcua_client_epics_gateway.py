from opcua import Client
import pvaccess
dir (pvaccess)

if __name__ == "__main__":

    client = Client("opc.tcp://169.254.145.192:4897")

    t1 = pvaccess.Channel('timer_1')
    t2 = pvaccess.Channel('timer_2')

    try:
        client.connect()

        # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
        root = client.get_root_node()
        print("Objects node is: ", root)

        # Node objects have methods to read and write node attributes as well as browse or populate address space
        print("Children of root are: ", root.get_children())

        # get a specific node knowing its node id
        timer_1 = client.get_node("ns=2;i=3")
        timer_2 = client.get_node("ns=2;i=4")

        offset_1_before = timer_1.get_value()
        offset_2_before = timer_2.get_value()

        offset_1_after = offset_1_before
        offset_2_after = offset_2_before

        while True:
            
            offset_1_before = timer_1.get_value()
            offset_2_before = timer_2.get_value()

            if offset_1_before != offset_1_after:
                # print(offset_1_before)
                t1.put(offset_1_before)

            if offset_2_before != offset_2_after:
                # print(offset_2_before)
                t2.put(offset_2_before)

            offset_1_after = offset_1_before
            offset_2_after = offset_2_before

    except KeyboardInterrupt:
        client.disconnect()
        print("Cliente desconectado")