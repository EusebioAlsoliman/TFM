from opcua import Client

def read_opcua_value(node):
    
    previous_value = node.get_value()
    actual_value = node.get_value()

    while previous_value == actual_value:
        actual_value = node.get_value()

    return actual_value

if __name__ == "__main__":

    client = Client("opc.tcp://169.254.145.192:4897")

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
            
            print("Timer_1:" + str(read_opcua_value(timer_1))) # get value of node as a DataValue object
            print("Timer_2:" + str(read_opcua_value(timer_2)))

    except KeyboardInterrupt:
        client.disconnect()
        print("Cliente desconectado")