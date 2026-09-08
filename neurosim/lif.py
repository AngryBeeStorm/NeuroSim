class LIFneuron:
    def __init__(self):
        # time measured in milliseconds, voltage in millivolts
        self.v_rest = -70.0
        self.v_threshold = -55.0
        self.v_reset = -70.0
        self.tau = 10.0
        self.dt = 1.0  # (ms) milliseconds

        self.voltage = self.v_reset

    def step(self, current):
        dv = (
            -(self.voltage - self.v_rest)
            + current
        ) / self.tau

        self.voltage += dv * self.dt

        display_voltage = self.voltage
        spiked = False

        if self.voltage >= self.v_threshold:
            display_voltage = self.v_threshold
            self.voltage = self.v_reset
            spiked = True

        return spiked, display_voltage