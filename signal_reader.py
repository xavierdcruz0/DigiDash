from bcr_mcp3008 import MCP3008


class SignalReader():
    def __init__(self, **config):

        self.channel = config.get("channel")
        self.device = config.get("device")
        self.adc = MCP3008(device=self.device)
    
    def sample_signal(self):
        return self.adc.readData(self.channel)



if __name__ == '__main__':
    import time
    import json

    CONFIG_PATH = 'config1.json'

    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)

    REFRESH_RATE = 0.1

    sr = SignalReader(**config)

    while True:
        # print(f"Signal value: {sr.sample_signal()}", end="\r")
        print(f"Signal value: {sr.sample_signal()}")

        time.sleep(REFRESH_RATE)
