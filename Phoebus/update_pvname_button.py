#executed with jython

from connect2j import scriptContext

with scriptContext('widget', 'pvs', 'PVUtil', dict=globals()):

	node = PVUtil.getString(pvs[0])
	device = PVUtil.getString(pvs[1])

	widget.setPropertyValue("pv_name", "pva://" + device + ":client_up:" + node)

