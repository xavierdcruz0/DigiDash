import time
from bcr_mcp3008 import MCP3008

adc0 = MCP3008(device=0)

# seconds
refresh_rate = 1 

while True:
    value0 = adc0.readData(0)

    print(f"Current value = {value0}", end="\r")

    time.sleep(refresh_rate)