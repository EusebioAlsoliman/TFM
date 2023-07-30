#executed with jython

from connect2j import scriptContext

with scriptContext('widget', 'pvs', 'PVUtil', 'ColorFontUtil', dict=globals()):

	RED = ColorFontUtil.RED
	ORANGE = ColorFontUtil.getColorFromRGB(255, 255, 0)
	GREEN = ColorFontUtil.getColorFromRGB(0, 255, 0)
	PINK = ColorFontUtil.PINK

	node = PVUtil.getDouble(pvs[0])
	device = PVUtil.getString(pvs[1])

	if device == "rpi4":
		color = GREEN
	elif device == "nano2gb":
		color = ORANGE
	elif device == "nano4gb":
		color = RED

	widget.setPropertyValue("traces[0].y_pv", "pva://" + device + ":NTP_client:" + str('%g'%(node)))

	widget.setPropertyValue("traces[0].color", color)

	widget.setPropertyValue("traces[0].name", device + " Node: " + str('%g'%(node)))
