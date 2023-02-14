from bcr_mcp3008 import MCP3008
import time
import math


class SignalReader():
    def __init__(self, **config):
        pass
    
    def sample_signal(self):
        raise NotImplementedError
    

class SignalReaderMCP3008(SignalReader):
    def __init__(self, **config):
        self.channel = config.get("channel")
        self.device = config.get("device")
        self.adc = MCP3008(device=self.device)
    
    def sample_signal(self):
        return self.adc.readData(self.channel)
    

class SignalReaderDummy(SignalReader):

    def __init__(self, **config):
        self.channel = config.get("channel")
        self.device = config.get("device")

        class DummySignalGenerator():
            def __init__(self):
                self.creation_time = time.time()
        
            def readData(self, channel):
                return (math.cos(time.time()-self.creation_time) + 1) * 512

        self.adc = DummySignalGenerator()
        
    
    def sample_signal(self):
        return self.adc.readData(self.channel)


if __name__ == '__main__':
    import time
    import json

    CONFIG_PATH = 'config1.json'

    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)

    REFRESH_RATE = 0.1

    # sr = SignalReaderMCP3008(**config)
    sr = SignalReaderDummy(**config)

    while True:
        # print(f"Signal value: {sr.sample_signal()}", end="\r")
        print(f"Signal value: {sr.sample_signal()}")

        time.sleep(REFRESH_RATE)
