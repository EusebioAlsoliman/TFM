from pvaccess import Channel

EPICS_channel_NTP_up = Channel("nano2gb" + ":NTP_clients_up")
array_got = str(EPICS_channel_NTP_up.get())[45:86]
array_got = array_got.replace("[", "")
array_got = array_got.replace("]", "")
array_got = array_got.replace(",", "")
array_got = list(array_got)
array_got = [eval(i) for i in array_got]
print(array_got)

array = [0] * 20

EPICS_channel_NTP_up.put(array)