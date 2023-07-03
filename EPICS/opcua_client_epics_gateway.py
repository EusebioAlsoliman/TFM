from opcua import Client
import pvaccess
dir (pvaccess)

def read_opcua_value(node):
    
    previous_value = node.get_value()
    actual_value = node.get_value()

    while previous_value == actual_value:
        actual_value = node.get_value()

    return actual_value

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

        while True:
            
            offset_1 = read_opcua_value(timer_1)
            offset_2 = read_opcua_value(timer_2)

            t1.put(offset_1)
            t2.put(offset_2)

    except KeyboardInterrupt:
        client.disconnect()
        print("Cliente desconectado")