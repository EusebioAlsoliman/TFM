from time import sleep
from pvaccess import Channel

temperatura_agua = Channel("temperatura:agua")

while True:
    print(temperatura_agua.get())
    sleep(1)