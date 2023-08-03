#executed with jython

from connect2j import scriptContext

with scriptContext('widget', 'pvs', 'PVUtil', dict=globals()):

	device = PVUtil.getString(pvs[0])

	if device == "rpi4":
		device_str = "Raspberry Pi 4"
	elif device == "nano2gb":
		device_str = "Jetson Nano 2 GB"
	elif device == "nano4gb":
		device_str = "Jetson Nano 4 GB"

	widget.setPropertyValue("text", "Nodo PTP del dispositivo " + device_str)

