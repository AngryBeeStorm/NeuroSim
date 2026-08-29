class LIFneuron:
    def __init__(self):
        self.v_rest = -70.0
        self.v_threshold = -55.0
        self.v_reset = -70.0
        self.tau = 10.0

        self.voltage = self.v_reset