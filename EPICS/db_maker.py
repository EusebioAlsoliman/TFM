fixed_variables = """
record(int64in, "node_ID")
{
    field(DESC, "Node ID selected in CSS Phoebus")
    field(VAL, "0")
}

record(stringin, "device_name")
{
    field(DESC, "Device selected in CSS Phoebus")
    field(VAL, "rpi4")
}

record(ai, "rpi4:PTP_slave")
{
    field(DESC, "PTP slave offset in Pi 4")
	field(LOLO, "-500000")
	field(LOW, "-200000")
	field(HIGH, "200000")
	field(HIHI, "500000")
	field(LSV, "MINOR")
	field(HSV, "MINOR")
	field(LLSV, "MAJOR")
	field(HHSV, "MAJOR")
}

record(ai, "nano2gb:PTP_slave")
{
    field(DESC, "PTP slave offset in Nano 2GB")
	field(LOLO, "-500000")
	field(LOW, "-200000")
	field(HIGH, "200000")
	field(HIHI, "500000")
	field(LSV, "MINOR")
	field(HSV, "MINOR")
	field(LLSV, "MAJOR")
	field(HHSV, "MAJOR")
}

record(ai, "nano4gb:PTP_slave")
{
    field(DESC, "PTP slave offset in Nano 4GB")
	field(LOLO, "-500000")
	field(LOW, "-200000")
	field(HIGH, "200000")
	field(HIHI, "500000")
	field(LSV, "MINOR")
	field(HSV, "MINOR")
	field(LLSV, "MAJOR")
	field(HHSV, "MAJOR")
}

record(bi, "rpi4:finish_all")
{
	field(DESC, "Finish OPC UA Server in Raspberry Pi 4")
    field(ZNAM, "False")
    field(ONAM, "True")
    field(VAL, "1")
}

record(bi, "nano2gb:finish_all")
{
	field(DESC, "Finish OPC UA Server in Jetson Nano 2GB")
    field(ZNAM, "False")
    field(ONAM, "True")
    field(VAL, "1")
}

record(bi, "nano4gb:finish_all")
{
	field(DESC, "Finish OPC UA Server in Jetson Nano 4GB")
    field(ZNAM, "False")
    field(ONAM, "True")
    field(VAL, "1")
}

record(stringin, "rpi4:PTP_slave_code")
{
	field(DESC, "ID of the PTP slave")
}

record(stringin, "nano2gb:PTP_slave_code")
{
	field(DESC, "ID of the PTP slave")
}

record(stringin, "nano4gb:PTP_slave_code")
{
	field(DESC, "ID of the PTP slave")
}

record(ai, "rpi4:PTP_freq")
{
	field(DESC, "Updated frequency of the clock")
}

record(ai, "nano2gb:PTP_freq")
{
	field(DESC, "Updated frequency of the clock")
}

record(ai, "nano4gb:PTP_freq")
{
	field(DESC, "Updated frequency of the clock")
}

record(stringin, "rpi4:portState")
{
	field(DESC, "portState of the PTP slave")
}

record(stringin, "nano2gb:portState")
{
	field(DESC, "portState of the PTP slave")
}

record(stringin, "nano4gb:portState")
{
	field(DESC, "portState of the PTP slave")
}

record(ai, "rpi4:NTP_host")
{
    field(DESC, "NTP host in rpi4")
	field(LOLO, "-500000")
	field(LOW, "-200000")
	field(HIGH, "200000")
	field(HIHI, "500000")
	field(LSV, "MINOR")
	field(HSV, "MINOR")
	field(LLSV, "MAJOR")
	field(HHSV, "MAJOR")
}

record(ai, "nano2gb:NTP_host")
{
    field(DESC, "NTP host in nano2gb")
	field(LOLO, "-500000")
	field(LOW, "-200000")
	field(HIGH, "200000")
	field(HIHI, "500000")
	field(LSV, "MINOR")
	field(HSV, "MINOR")
	field(LLSV, "MAJOR")
	field(HHSV, "MAJOR")
}

record(ai, "nano4gb:NTP_host")
{
    field(DESC, "NTP host in nano4gb")
	field(LOLO, "-500000")
	field(LOW, "-200000")
	field(HIGH, "200000")
	field(HIHI, "500000")
	field(LSV, "MINOR")
	field(HSV, "MINOR")
	field(LLSV, "MAJOR")
	field(HHSV, "MAJOR")
}

record(stringin, "rpi4:NTP_host_leap_status")
{
	field(DESC, "Leap status NTP client in host, rpi4")
}

record(stringin, "nano2gb:NTP_host_leap_status")
{
	field(DESC, "Leap status NTP client in host, nano2gb")
}

record(stringin, "nano4gb:NTP_host_leap_status")
{
	field(DESC, "Leap status NTP client in host, nano4gb")
}
"""

template_dynamic = """
record(ai, "{device}:NTP_client:{index}")
{
    field(DESC, "NTP client {index} offset in {device}")
	field(LOLO, "-500000")
	field(LOW, "-200000")
	field(HIGH, "200000")
	field(HIHI, "500000")
	field(LSV, "MINOR")
	field(HSV, "MINOR")
	field(LLSV, "MAJOR")
	field(HHSV, "MAJOR")
}

record(bi, "{device}:client_up:{index}")
{
	field(DESC, "Switch ON/OFF the Node {index} of {device}")
    field(ZNAM, "False")
    field(ONAM, "True")
}

record(stringin, "{device}:leap_status:{index}")
{
	field(DESC, "Leap Status of Node {index} of {device}")
}
"""

devices = ["rpi4", "nano2gb", "nano4gb"]
with open("test.db", "w") as f:
	f.write(fixed_variables)
	for i in range(0, 20):
		for device in devices:
			record_str = template_dynamic.replace("{index}", str(i))
			record_str = record_str.replace("{device}", device)
			f.write(record_str)
