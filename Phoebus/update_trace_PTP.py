#executed with jython

from connect2j import scriptContext

with scriptContext('widget', 'pvs', 'PVUtil', 'ColorFontUtil', dict=globals()):

	RED = ColorFontUtil.RED
	BLUE = ColorFontUtil.BLUE
	GREEN = ColorFontUtil.getColorFromRGB(0, 255, 0)

	DARK_RED = ColorFontUtil.getColorFromRGB(153, 0, 0)
	DARK_BLUE = ColorFontUtil.getColorFromRGB(0, 0, 128)
	DARK_GREEN = ColorFontUtil.getColorFromRGB(51, 102, 51)

	device = PVUtil.getString(pvs[0])

	if device == "rpi4":
		color_offset = GREEN
		color_freq = DARK_GREEN
	elif device == "nano2gb":
		color_offset = BLUE
		color_freq = DARK_BLUE
	elif device == "nano4gb":
		color_offset = RED
		color_freq = DARK_RED

	# Offset trace
	widget.setPropertyValue("traces[0].y_pv", "pva://" + device + ":PTP_slave")

	widget.setPropertyValue("traces[0].color", color_offset)

	widget.setPropertyValue("traces[0].name", device + " offset")

	# Freq trace
	widget.setPropertyValue("traces[1].y_pv", "pva://" + device + ":PTP_freq")

	widget.setPropertyValue("traces[1].color", color_freq)

	widget.setPropertyValue("traces[1].name", device + " freq")
