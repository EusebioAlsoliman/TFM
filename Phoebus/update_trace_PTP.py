#executed with jython

from connect2j import scriptContext

with scriptContext('widget', 'pvs', 'PVUtil', 'ColorFontUtil', dict=globals()):

	RED = ColorFontUtil.RED
	BLUE = ColorFontUtil.BLUE
	ORANGE = ColorFontUtil.getColorFromRGB(255, 255, 0)
	GREEN = ColorFontUtil.getColorFromRGB(0, 255, 0)
	PINK = ColorFontUtil.PINK

	device = PVUtil.getString(pvs[0])

	if device == "rpi4":
		color = GREEN
	elif device == "nano2gb":
		color = BLUE
	elif device == "nano4gb":
		color = RED

	widget.setPropertyValue("traces[0].y_pv", "pva://" + device + ":PTP_slave")

	widget.setPropertyValue("traces[0].color", color)

	widget.setPropertyValue("traces[0].name", device)
