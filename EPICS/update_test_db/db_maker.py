fixed_variables = """
record(ai, "temperature:water")
{
	field(DESC, "Water temperature in the fish tank")
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
}

record(ao, "alarm_lim_dynamic:High")
{
    field(DESC, "Test")
    field(PINI, "YES")
    field(OUT, "temperature:oil.HIGH")
}

record(ai, "temperature:oil")
{
    field(DESC, "Oil temperature in the engine")
    field(HSV, "MINOR")
    field(LSV, "MINOR")
}
"""

template_dynamic = """
record(int64in, "rpi4:PTP_slave:{index}")
{
    field(DESC, "PTP slave {index} offset in Raspberry Pi 4")
}

record(int64in, "rpi4:NTP_client:{index}")
{
    field(DESC, "NTP client {index} offset in Raspberry Pi 4")
	field(LOLO, "-500000")
	field(LOW, "-200000")
	field(HIGH, "200000")
	field(HIHI, "500000")
	field(LSV, "MINOR")
	field(HSV, "MINOR")
	field(LLSV, "MAJOR")
	field(HHSV, "MAJOR")
}

record(int64in, "nano2gb:PTP_slave:{index}")
{
    field(DESC, "PTP slave {index} offset in Jetson Nano 2GB")
}

record(int64in, "nano2gb:NTP_client:{index}")
{
    field(DESC, "NTP client {index} offset in Jetson Nano 2GB")
	field(LOLO, "-500000")
	field(LOW, "-200000")
	field(HIGH, "200000")
	field(HIHI, "500000")
	field(LSV, "MINOR")
	field(HSV, "MINOR")
	field(LLSV, "MAJOR")
	field(HHSV, "MAJOR")
}

record(int64in, "nano4gb:PTP_slave:{index}")
{
    field(DESC, "PTP slave {index} offset in Jetson Nano 4GB")
}

record(int64in, "nano4gb:NTP_client:{index}")
{
    field(DESC, "NTP client {index} offset in Jetson Nano 4GB")
	field(LOLO, "-500000")
	field(LOW, "-200000")
	field(HIGH, "200000")
	field(HIHI, "500000")
	field(LSV, "MINOR")
	field(HSV, "MINOR")
	field(LLSV, "MAJOR")
	field(HHSV, "MAJOR")
}
"""

with open("test.db", "w") as f:
    f.write(fixed_variables)
    for i in range(0, 20):
        record_str = template_dynamic.replace("{index}", str(i))
        f.write(record_str)
