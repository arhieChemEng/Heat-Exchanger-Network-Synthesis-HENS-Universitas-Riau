from HENS.StreamsData import DataStream


class StreamGrid(DataStream):
    """docstring for """

    def __init__(self, ts, tt, c, name):
        super().__init__(ts, tt, c, name)
        self.heat = abs(ts - tt) * c
        self.heatRemaining = self.heat
        self.matchTarget = False
        self.haveMatch = False

    def addHeatIn(self, heatIn):
        self.heatRemaining = self.heatRemaining - heatIn
        if self.heatRemaining == 0.0:
            self.matchTarget = True
        self.haveMatch = True
