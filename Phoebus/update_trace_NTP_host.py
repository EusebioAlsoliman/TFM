#executed with jython

from connect2j import scriptContext

with scriptContext('widget', 'pvs', 'PVUtil', 'ColorFontUtil', dict=globals()):

	RED = ColorFontUtil.RED
	BLUE = ColorFontUtil.BLUE
	GREEN = ColorFontUtil.getColorFromRGB(0, 255, 0)

	device = PVUtil.getString(pvs[0])

	if device == "rpi4":
		color_offset = GREEN
	elif device == "nano2gb":
		color_offset = BLUE
	elif device == "nano4gb":
		color_offset = RED

	# Offset trace
	widget.setPropertyValue("traces[0].y_pv", "pva://" + device + ":NTP_host")

	widget.setPropertyValue("traces[0].color", color_offset)

	widget.setPropertyValue("traces[0].name", device + " offset")

