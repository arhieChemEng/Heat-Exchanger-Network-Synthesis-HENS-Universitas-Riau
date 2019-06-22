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

from HENS.StreamsData import DataStream
from HENS.MERTarget import MerCalc


def merSoltoText(mer: MerCalc) -> str:
    txt = "Calculation Result of Maximum Energy Recovery Target \n"
    txt = txt + "Data Input: \n"
    txt = txt + "--------------------------------\n"
    txt = txt + "Stream Name" + "\t Ts" + "\t\t Tt" + "\t\t CP \n"
    txt = txt + "--------------------------------\n"
    for _ in mer.dataHotStream:
        txt = txt + str(_.name) + "\t\t\t" + str(_.ts) + "\t\t" + str(_.tt) + "\t\t" + str(_.c) + "\n"
    for _ in mer.dataColdStream:
        txt = txt + str(_.name) + "\t\t\t" + str(_.ts) + "\t\t" + str(_.tt) + "\t\t" + str(_.c) + "\n"
    txt = txt + "--------------------------------\n"
    txt = txt + "Qh Minimum: " + str(mer.qHmin) + "\n"
    txt = txt + "Qc Minimum: " + str(mer.qCmin) + "\n"
    txt = txt + "T Pinch Hot: " + str(mer.tPinchHot) + "\n"
    txt = txt + "T Pinch Cold: " + str(mer.tPinchCold) + "\n"
    txt = txt + "--------------------------------\n"
    txt = txt + "\n"
    txt = txt + "Solution to Grid Diagram\n"
    txt = txt + "-------------------------\n"
    txt = txt + "Match at Cold Side\n"
    txt = txt + "Number of Match = " + str(len(mer.matchInColdSide)) + "\n"
    for match in mer.matchInColdSide:
        txt = txt + "Match from " + match.matchFrom + " To " + str(match.matchTo) + " Heat Load: " + str(match.heatLoad) + "\n"
    for stream in mer.streamHotInColdSide:
        if stream.heatRemaining > 0.0:
            txt = txt + "Cold Utilities : " + str(stream.heatRemaining) + " at " + stream.name + "\n"
    txt = txt + "\n"
    txt = txt + "Match at Hot Side"
    txt = txt + "Number of Match = " + str(len(mer.matchInHotSide)) + "\n"
    for match in mer.matchInHotSide:
        txt = txt + "Match from " + match.matchFrom + " To " + str(match.matchTo) + " Heat Load: " + str(match.heatLoad) + "\n"
    for stream in mer.streamColdInHotSide:
        if stream.heatRemaining > 0.0:
            txt = txt + "Hot Utilities : " + str(stream.heatRemaining) + " at " + stream.name + "\n"
    return txt

def test() -> MerCalc:

    h1 = DataStream(350, 160, 3.2, "h1")
    h2 = DataStream(400, 100, 3.0, "h2")
    h3 = DataStream(110, 60, 8.0, "h3")
    c1 = DataStream(50, 250, 4.5, "c1")
    c2 = DataStream(70, 320, 2.0, "c2")
    c3 = DataStream(100, 300, 3.0, "c3")
    datahot = [h1, h2, h3]
    datacold = [c1, c2, c3]
    mer = MerCalc(datahot, datacold, 10.0)
    return mer


class MerManager:
    def __init__(self, merCalc: MerCalc):
        self.mer = merCalc

    def init(self):
        pass