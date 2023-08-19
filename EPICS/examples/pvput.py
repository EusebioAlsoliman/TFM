from time import sleep
from pvaccess import Channel

temperatura_agua = Channel("temperatura:agua")
i = 0

while True:
    if i == 10:
        i = 0
    temperatura_agua.put(20 + i)
    i += 1
    sleep(1)