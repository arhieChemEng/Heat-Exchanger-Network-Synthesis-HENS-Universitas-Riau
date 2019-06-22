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
from StreamsGrid import StreamGrid
from MatchDataStream import MatchData


class MerCalc(object):

    def __init__(self,
                 dataHotStream: [DataStream],
                 dataColdStream: [DataStream],
                 dTmin: float):
        """ Constructor for Mer Calculation
        Keyword arguments:
        dataHotStream -- is a list of DataStream type Hot Stream
        dataColdStream -- is a list of DataStream type Cold Stream
        """
        self.dataHotStream = dataHotStream
        self.dataColdStream = dataColdStream
        self.streamHotInColdSide: list[StreamGrid] = []
        self.streamHotInHotSide: list[StreamGrid] = []
        self.streamColdInHotSide: list[StreamGrid] = []
        self.streamColdInColdSide: list[StreamGrid] = []
        # Calculate number of Stream in each data stream
        self.nHotStream = len(self.dataHotStream)
        self.nColdStream = len(self.dataColdStream)
        self.dTmin = dTmin
        self.calculate()
        self.streamMatch()

    def calculate(self):
        """ menyalin data temperatur masing-2 aliran ke intervalT """
        intervalT = []
        for _ in self.dataHotStream:
            intervalT.append(_.ts - self.dTmin)
            intervalT.append(_.tt - self.dTmin)
        for _ in self.dataColdStream:
            intervalT.append(_.ts)
            intervalT.append(_.tt)
        # remove redundant temperature in intervalT
        intervalT = list(set(intervalT))
        intervalT.sort()
        intervalT.reverse()
        listdT = []
        for i in range(len(intervalT) - 1):
            listdT.append(intervalT[i] - intervalT[i + 1])
        # cek temperature interval interception with data stream temperature interval
        listCP = []
        sumCpHot = 0.0
        sumCpCold = 0.0
        for i in range(len(intervalT) - 1):
            for j in range(len(self.dataHotStream)):
                # for data hot ts > tt
                if self.dataHotStream[j].ts - self.dTmin >= intervalT[i] > self.dataHotStream[j].tt - self.dTmin:
                    sumCpHot = sumCpHot + self.dataHotStream[j].c
            for k in range(len(self.dataColdStream)):
                # for data cold ts < tt
                if self.dataColdStream[k].tt >= intervalT[i] > self.dataColdStream[k].ts:
                    sumCpCold = sumCpCold + self.dataColdStream[k].c
            listCP.append(sumCpHot - sumCpCold)
            sumCpHot = 0.0
            sumCpCold = 0.0
        dH = []
        for i in range(len(listCP)):
            dH.append(listCP[i] * listdT[i])
        qcascadeInit = []
        sumQ = 0.0
        for i in range(len(dH)):
            sumQ = sumQ + dH[i]
            qcascadeInit.append(sumQ)
        qcascadeFinal = []
        qHmin = abs(min(qcascadeInit))
        qcascadeFinal.append(qHmin)
        sumQFinal = qHmin
        for i in range(len(qcascadeInit)):
            _ = qcascadeInit[i] + sumQFinal
            qcascadeFinal.append(_)
        qCmin = qcascadeFinal[len(qcascadeFinal) - 1]
        self.qCmin = qCmin
        self.qHmin = qHmin
        minValue = min(qcascadeFinal)
        index = qcascadeFinal.index(minValue)
        self.tPinchCold = intervalT[index]
        self.tPinchHot = self.tPinchCold + self.dTmin

    def streamMatch(self):
        # define stream Hot and Cold

        # Add stream grid in Hot Side
        for i in range(self.nHotStream):
            if self.dataHotStream[i].ts >= self.tPinchHot > self.dataHotStream[i].tt:
                self.streamHotInColdSide.append(
                    StreamGrid(self.tPinchHot, self.dataHotStream[i].tt, self.dataHotStream[i].c,
                               self.dataHotStream[i].name))
            elif self.tPinchHot > self.dataHotStream[i].ts:
                self.streamHotInColdSide.append(
                    StreamGrid(self.dataHotStream[i].ts, self.dataHotStream[i].tt, self.dataHotStream[i].c,
                               self.dataHotStream[i].name))
            if self.dataHotStream[i].tt <= self.tPinchHot < self.dataHotStream[i].ts:
                self.streamHotInHotSide.append(
                    StreamGrid(self.dataHotStream[i].ts, self.tPinchHot, self.dataHotStream[i].c,
                               self.dataHotStream[i].name))
            elif self.tPinchHot < self.dataHotStream[i].tt:
                self.streamHotInHotSide.append(
                    StreamGrid(self.dataHotStream[i].ts, self.dataHotStream[i].tt, self.dataHotStream[i].c,
                               self.dataHotStream[i].name))
        # Add Stream Grid in Cold Side
        for i in range(self.nColdStream):
            if self.dataColdStream[i].ts <= self.tPinchCold < self.dataColdStream[i].tt:
                self.streamColdInHotSide.append(
                    StreamGrid(self.tPinchCold, self.dataColdStream[i].tt, self.dataColdStream[i].c,
                               self.dataColdStream[i].name))
            elif self.tPinchCold < self.dataColdStream[i].ts:
                self.streamColdInHotSide.append(
                    StreamGrid(self.dataColdStream[i].ts, self.dataColdStream[i].tt, self.dataColdStream[i].c,
                               self.dataColdStream[i].name))
            if self.dataColdStream[i].tt >= self.tPinchCold > self.dataColdStream[i].ts:
                self.streamColdInColdSide.append(
                    StreamGrid(self.dataColdStream[i].ts, self.tPinchCold, self.dataColdStream[i].c,
                               self.dataColdStream[i].name))
            elif self.tPinchCold > self.dataColdStream[i].tt:
                self.streamColdInColdSide.append(
                    StreamGrid(self.dataColdStream[i].ts, self.dataColdStream[i].tt, self.dataColdStream[i].c,
                               self.dataColdStream[i].name))

        self.matchInColdSide = []
        self.matchInHotSide = []
        nameCold = ''
        nameHot = ''
        heatload = 0.0
        for streamHot in self.streamHotInColdSide:
            for streamCold in self.streamColdInColdSide:
                if streamHot.c >= streamCold.c:
                    if not nameCold == streamCold.name and not nameHot == streamHot.name:
                        if streamHot.heat <= streamCold.heat:
                            heatload = streamHot.heat
                        else:
                            heatload = streamCold.heat
                        streamHot.addHeatIn(heatload)
                        streamCold.addHeatIn(heatload)
                        self.matchInColdSide.append(MatchData(streamHot.name, streamCold.name, heatload, True))
                        nameHot = streamHot.name
                        nameCold = streamCold.name

        nameHot = ''
        nameCold = ''
        for streamHot in self.streamHotInHotSide:
            for streamCold in self.streamColdInHotSide:
                if streamHot.c <= streamCold.c:
                    if not nameHot == streamHot.name and not nameCold == streamCold.name:
                        if streamHot.heat <= streamCold.heat:
                            heatload = streamHot.heat
                        else:
                            heatload = streamCold.heat
                        streamHot.addHeatIn(heatload)
                        streamCold.addHeatIn(heatload)
                        self.matchInHotSide.append(MatchData(streamHot.name, streamCold.name, heatload, True))
                        nameHot = streamHot.name
                        nameCold = streamCold.name

        for streamHot in self.streamHotInColdSide:
            for streamCold in self.streamColdInColdSide:
                if not streamHot.matchTarget and not streamCold.matchTarget:
                    if streamHot.haveMatch or streamCold.haveMatch:
                        if streamHot.heatRemaining <= streamCold.heatRemaining:
                            heatload = streamHot.heatRemaining
                        else:
                            heatload = streamCold.heatRemaining
                        streamHot.addHeatIn(heatload)
                        streamCold.addHeatIn(heatload)
                        self.matchInColdSide.append(MatchData(streamHot.name, streamCold.name, heatload, False))

        for streamHot in self.streamHotInHotSide:
            for streamCold in self.streamColdInHotSide:
                if not streamHot.matchTarget and not streamCold.matchTarget:
                    if streamHot.haveMatch or streamCold.haveMatch:
                        if streamHot.heatRemaining <= streamCold.heatRemaining:
                            heatload = streamHot.heatRemaining
                        else:
                            heatload = streamCold.heatRemaining
                        streamHot.addHeatIn(heatload)
                        streamCold.addHeatIn(heatload)
                        self.matchInHotSide.append(MatchData(streamHot.name, streamCold.name, heatload, False))

    def printResult(self):
        # self._setIntervalT()
        print("Calculation Result of Maximum Energy Recovery Target")
        print("Data Input: ")
        print("--------------------------------------------------------------------")
        print("Stream Name" + "\t Ts" + "\t Tt" + "\t CP")
        print("--------------------------------------------------------------------")
        for _ in self.dataHotStream:
            print(str(_.name) + "\t\t" + str(_.ts) + "\t" + str(_.tt) + "\t" + str(_.c))
        for _ in self.dataColdStream:
            print(str(_.name) + "\t\t" + str(_.ts) + "\t" + str(_.tt) + "\t" + str(_.c))
        print("--------------------------------------------------------------------")
        print("Qh Minimum: " + str(self.qHmin))
        print("Qc Minimum: " + str(self.qCmin))
        print("T Pinch Hot: " + str(self.tPinchHot))
        print("T Pinch Cold: " + str(self.tPinchCold))
        print("--------------------------------------------------------------------")
        print()
        print("Solution to Grid Diagram")
        print("-------------------------")
        print("Match at Cold Side")
        print("Number of Match = " + str(len(self.matchInColdSide)))
        for match in self.matchInColdSide:
            print("Match from " + match.matchFrom + " To " + str(match.matchTo) + " Heat Load: " + str(match.heatLoad))
        for stream in self.streamHotInColdSide:
            if stream.heatRemaining > 0.0:
                print("Cold Utilities : " + str(stream.heatRemaining) + " at " + stream.name)
        print()
        print("Match at Hot Side")
        print("Number of Match = " + str(len(self.matchInHotSide)))
        for match in self.matchInHotSide:
            print("Match from " + match.matchFrom + " To " + str(match.matchTo) + " Heat Load: " + str(match.heatLoad))
        for stream in self.streamColdInHotSide:
            if stream.heatRemaining > 0.0:
                print("Hot Utilities : " + str(stream.heatRemaining) + " at " + stream.name)
