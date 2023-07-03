import asyncio
from asyncua import Client

client = Client(url="opc.tcp://169.254.145.192:4897")

async def init(client):
    await client.connect()

async def timer_1(client):
    await asyncio.sleep(1)
    while 1:
        print("timer_1")
        timer_1 = await client.get_node("ns=2;i=3").get_value()
        print(timer_1)
        await asyncio.sleep(1)

async def timer_2(client):
    await asyncio.sleep(1)
    while 1:
        print("timer_2")
        timer_2 = await client.get_node("ns=2;i=4").get_value()
        print(timer_2)
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.ensure_future(init(client))
    asyncio.ensure_future(timer_1(client))
    asyncio.ensure_future(timer_2(client))
    asyncio.get_event_loop().run_forever()