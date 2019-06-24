#    This file is part of Heat Exchanger Network Synthesis (HENS) - Universitas Riau.
#
#    Heat Exchanger Network Synthesis (HENS) - Universitas Riau is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Heat Exchanger Network Synthesis (HENS) - Universitas Riau is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Foobar.  If not, see <https://www.gnu.org/licenses/>.


from StreamsData import DataStream


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
