#executed with jython

from connect2j import scriptContext

with scriptContext('widget', 'pvs', 'PVUtil', dict=globals()):

	node = PVUtil.getString(pvs[0])
	device = PVUtil.getString(pvs[1])

	if device == "rpi4":
		device_str = "Raspberry Pi 4"
	elif device == "nano2gb":
		device_str = "Jetson Nano 2 GB"
	elif device == "nano4gb":
		device_str = "Jetson Nano 4 GB"

	widget.setPropertyValue("text", "Dispositivo: " + device_str + " | Nodo: " + node)

