import os

beginning = """<?xml version="1.0" encoding="UTF-8"?>
<engineconfig>
  <group>
    <name>Test</name>
"""

end_sentence = """
  </group>
</engineconfig>
"""

template_static = """
    <channel>
      <name>pva://temperature:water</name>
      <monitor/>
      <period>1.0</period>
    </channel>
    <channel>
      <name>pva://temperature:oil</name>
      <monitor/>
      <period>1.0</period>
    </channel>
"""

template_dynamic_device = """
    <channel>
      <name>pva://{device}:PTP_slave</name>
      <monitor/>
      <period>0.5</period>
    </channel>
    <channel>
      <name>pva://{device}:PTP_freq</name>
      <monitor/>
      <period>0.5</period>
    </channel>
    <channel>
      <name>pva://{device}:NTP_host</name>
      <monitor/>
      <period>0.1</period>
    </channel>
"""

template_dynamic_all = """
    <channel>
      <name>pva://{device}:NTP_client:{index}</name>
      <monitor/>
      <period>0.1</period>
    </channel>
"""

ROOT = os.getcwd()
os.chdir(ROOT + "/archive-engine")

devices = ["rpi4", "nano2gb", "nano4gb"]

with open("Test.xml", "w") as f:
  f.write(beginning)

  f.write(template_static)

  # for device in devices:
  #   record_device = template_dynamic_device.replace("{device}", device)
  #   record_str = template_dynamic_all.replace("{device}", device)
  #   f.write(record_device)

  #   for i in range(0,20):
  #     record_str_save = record_str.replace("{index}", str(i))
  #     f.write(record_str_save)

  f.write(end_sentence)
