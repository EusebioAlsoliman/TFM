#executed with jython

from connect2j import scriptContext

with scriptContext('widget', 'pvs', 'PVUtil', 'ColorFontUtil', dict=globals()):

	RED = ColorFontUtil.RED
	ORANGE = ColorFontUtil.getColorFromRGB(255, 255, 0)
	GREEN = ColorFontUtil.getColorFromRGB(0, 255, 0)
	PINK = ColorFontUtil.PINK

	value = PVUtil.getDouble(pvs[0])

	if value > 50:
		color = RED
	else:
		color = PINK

	widget.setPropertyValue("background_color", color)
