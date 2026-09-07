class IzhikevichNeuron:

    def __init__(
        self,
        a=0.02,
        b=0.2,
        c=-65.0,
        d=8.0
    ):
        self.a = a # recovery time scale
        self.b = b # how strongly recovery responds to voltage
        self.c = c # voltage reset after spike
        self.d = d # how much recovery increases after a spike

        self.v = -65.0
        self.u = self.b * self.v

    def step(self, current):
        for _ in range(2):
            dv = (
                0.04 * self.v**2
                + 5 * self.v
                + 140
                - self.u
                + current
            )

            self.v += 0.5 * dv

        du = self.a * (
            self.b * self.v
            - self.u
        )

        self.u += du

        spike = False
        display_voltage = self.v

        if self.v >= 30:
            display_voltage = 30.0

            self.v = self.c
            self.u += self.d

            spike = True

        return spike, display_voltage