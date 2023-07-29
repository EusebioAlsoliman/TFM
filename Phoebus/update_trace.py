#executed with jython
""" Input:
    pvs[0] - Value around -5 .. 5
    pvs[1] - Default value for X
    pvs[2] - Scaling factor
"""
from connect2j import scriptContext

with scriptContext('widget', 'pvs', 'PVUtil', dict=globals()):
	node = PVUtil.getDouble(pvs[0])
	print("NODOO")
	print('%g'%(node))
	print("pva://rpi4_NTP_client:" + str('%g'%(node)))
	widget.setPropertyValue("traces[0].y_pv", "pva://rpi4:NTP_client:" + str('%g'%(node)))