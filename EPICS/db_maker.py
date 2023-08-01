fixed_variables = """
record(ai, "temperature:water")
{
	field(DESC, "Water temperature in the fish tank")
    field(VAL, "34")
	field(LOLO, "10")
	field(LOW, "20")
	field(HIGH, "80")
	field(HIHI, "100")
	field(LSV, "MINOR")
	field(HSV, "MINOR")
	field(LLSV, "MAJOR")
	field(HHSV, "MAJOR")
}

record(ao, "alarm_lim_dynamic:Low")
{
    field(DESC, "Test")
    field(PINI, "YES")
    field(OUT, "temperature:oil.LOW")
    field(VAL, "12")
}

record(ao, "alarm_lim_dynamic:High")
{
    field(DESC, "Test")
    field(PINI, "YES")
    field(OUT, "temperature:oil.HIGH")
    field(VAL, "72")
}

record(ai, "temperature:oil")
{
    field(DESC, "Oil temperature in the engine")
    field(HSV, "MINOR")
    field(LSV, "MINOR")
    field(VAL, "33")
}

record(bi, "rpi4:finish_all")
{
	field(DESC, "Finish OPC UA Server in Raspberry Pi 4")
    field(ZNAM, "False")
    field(ONAM, "True")
    field(VAL, "0")
}

record(bi, "nano2gb:finish_all")
{
	field(DESC, "Finish OPC UA Server in Jetson Nano 2GB")
    field(ZNAM, "False")
    field(ONAM, "True")
    field(VAL, "0")
}

record(bi, "nano4gb:finish_all")
{
	field(DESC, "Finish OPC UA Server in Jetson Nano 4GB")
    field(ZNAM, "False")
    field(ONAM, "True")
    field(VAL, "0")
}

record(aai, "rpi4:PTP_slaves")
{
    field(DESC, "PTP slaves offset in Raspberry Pi 4")
    field(FTVL, "INT64")
    field(NELM, "20")
}

record(aai, "rpi4:NTP_clients")
{
    field(DESC, "NTP clients offset in Raspberry Pi 4")
    field(FTVL, "INT64")
    field(NELM, "20")
}

record(aai, "nano2gb:PTP_slaves")
{
    field(DESC, "PTP slaves offset in Nano 2GB")
    field(FTVL, "INT64")
    field(NELM, "20")
}

record(aai, "nano2gb:NTP_clients")
{
    field(DESC, "NTP clients offset in Nano 2GB")
    field(FTVL, "INT64")
    field(NELM, "20")
}

record(aai, "nano4gb:PTP_slaves")
{
    field(DESC, "PTP slaves offset in Nano 4GB")
    field(FTVL, "INT64")
    field(NELM, "20")
}

record(aai, "nano4gb:NTP_clients")
{
    field(DESC, "NTP clients offset in Nano 4GB")
    field(FTVL, "INT64")
    field(NELM, "20")
}

record(aai, "rpi4:NTP_clients_up")
{
    field(DESC, "NTP clients ON/OFF")
    field(FTVL, "INT64")
    field(NELM, "20")
}

record(aai, "nano2gb:NTP_clients_up")
{
    field(DESC, "NTP clients ON/OFF")
    field(FTVL, "INT64")
    field(NELM, "20")
}

record(aai, "nano4gb:NTP_clients_up")
{
    field(DESC, "NTP clients ON/OFF")
    field(FTVL, "INT64")
    field(NELM, "20")
}
"""

template_dynamic = """
record(int64in, "{device}:PTP_slave:{index}")
{
    field(DESC, "PTP slave {index} offset in {device}")
}

record(calc, "{device}:NTP_client:{index}")
{
    field(DESC, "NTP client {index} offset in {device}")
	field(SCAN, ".1 second")
	field(INPA, "{device}:NTP_clients.VAL[{index}]")
	field(CALC, "A")
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
"""

devices = ["rpi4", "nano2gb", "nano4gb"]
with open("test.db", "w") as f:
	f.write(fixed_variables)
	for i in range(0, 20):
		for device in devices:
			record_str = template_dynamic.replace("{index}", str(i))
			record_str = record_str.replace("{device}", device)
			f.write(record_str)
