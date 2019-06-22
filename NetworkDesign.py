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

from MERTarget import MerCalc
from LineStreams import StreamLine, textSize
from Console import merSoltoText, test
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtWidgets import QWidget


class DrawGridSolution:
    def __init__(self, merCalc: MerCalc, width, height):
        self.mer = merCalc
        self.lineColdInColdSide: list[StreamLine] = []
        self.lineHotInColdSide: list[StreamLine] = []
        self.lineColdInHotSide: list[StreamLine] = []
        self.lineHotInHotSide: list[StreamLine] = []

        self.width = width
        self.height = height

        self.vspace = 40
        self.hspace = 60
        self.spaceAtPinch = 10

        self.circleDia = 20

        self.prepareData()

    def prepareData(self):
        # calculate height area for drawing grid mer
        nStream = len(self.mer.dataColdStream) + len(self.mer.dataHotStream)
        self.heightArea = self.vspace * (nStream + 1)

        # calculate width area for drawing grid mer
        nMatchInColdSide = len(self.mer.matchInColdSide)
        nMatchInHotSide = len(self.mer.matchInHotSide)
        nMatch = nMatchInColdSide + nMatchInHotSide
        self.widthArea = self.hspace * (nMatch + 5) + self.spaceAtPinch

        # finding pinch line position
        lengthXinColdSide = self.hspace * (nMatchInColdSide + 3)
        lengthXinHotSide = self.hspace * (nMatchInHotSide + 2)
        self.startXHotSide = lengthXinHotSide
        self.endXHotSide = 0
        self.startXColdSide = lengthXinHotSide + self.spaceAtPinch
        self.endXColdSide = self.startXColdSide + lengthXinColdSide - self.hspace

    def drawCircle(self, qp: QPainter, xpos, ypos, typeCircle: str):
        """
        draw circle dimana titik referensi atau posisi merupakan center dari circle
        """
        if typeCircle == "heat":
            qp.setPen(QColor(Qt.gray))
            qp.setBrush(QBrush(QColor(Qt.gray)))
        elif typeCircle == "coldUtil":
            qp.setPen(QColor(Qt.blue))
            qp.setBrush(QBrush(QColor(Qt.blue)))
        elif typeCircle == "hotUtil":
            qp.setPen(QColor(Qt.red))
            qp.setBrush(QBrush(QColor(Qt.red)))
        x = xpos - self.circleDia / 2
        y = ypos - self.circleDia / 2
        qp.drawEllipse(x, y, self.circleDia, self.circleDia)

    def drawColdUtil(self, qp: QPainter, i: int, endXColdSide, space):
        if self.mer.streamHotInColdSide[i].heatRemaining > 0:
            x = endXColdSide - self.hspace
            y = space
            self.drawCircle(qp, x, y, "coldUtil")
            qp.setPen(QColor(Qt.black))
            strColdUtil = str(self.mer.streamHotInColdSide[i].heatRemaining)
            textWidth, textHeight = textSize(qp, strColdUtil)
            textPosX = x - textWidth / 2
            textPosY = y + self.circleDia + 2
            qp.drawText(textPosX, textPosY, strColdUtil)

    def drawHotUtil(self, qp: QPainter, i: int, endXHotSide, space):
        if self.mer.streamColdInHotSide[i].heatRemaining > 0:
            x = endXHotSide + self.hspace
            y = space
            self.drawCircle(qp, x, y, "hotUtil")
            qp.setPen(QColor(Qt.black))
            strHotUtil = str(self.mer.streamColdInHotSide[i].heatRemaining)
            textWidth, textHeight = textSize(qp, strHotUtil)
            textPosX = x - textWidth / 2
            textPosY = y + self.circleDia + 2
            qp.drawText(textPosX, textPosY, strHotUtil)

    def drawLineMatch(self, qp: QPainter, x, y1, y2, match):
        qp.drawLine(x, y1, x, y2)
        self.drawCircle(qp, x, y1, "heat")
        self.drawCircle(qp, x, y2, "heat")
        string = str(match.heatLoad)
        twidth, theight = textSize(qp, string)
        qp.setPen(QColor(Qt.black))
        qp.drawText(x - twidth / 2, y2 + self.circleDia, string)

    def drawGS(self, qp: QPainter):
        qp.drawLine(self.startXHotSide, 0, self.startXHotSide, self.heightArea)
        qp.drawLine(self.startXColdSide, 0, self.startXColdSide, self.heightArea)
        i = 0
        space = 0
        # draw hot stream line in cold side
        for streamHot in self.mer.dataHotStream:
            space = space + self.vspace
            if i < len(self.mer.streamHotInColdSide):
                if streamHot.name == self.mer.streamHotInColdSide[i].name:
                    if self.mer.streamHotInColdSide[i].ts == self.mer.tPinchHot:
                        streamLine = StreamLine(
                            self.startXColdSide, space,
                            self.endXColdSide, space,
                            "cold", "hot",
                            self.mer.streamHotInColdSide[i])
                        streamLine.drawStreamLine(qp)
                        self.lineHotInColdSide.append(streamLine)
                        self.drawColdUtil(qp, i, self.endXColdSide, space)
                        i = i + 1
                    else:
                        streamLine = StreamLine(
                            self.startXColdSide + self.hspace, space,
                            self.endXColdSide, space,
                            "cold", "hot",
                            self.mer.streamHotInColdSide[i])
                        streamLine.drawStreamLine(qp)
                        self.lineHotInColdSide.append(streamLine)
                        self.drawColdUtil(qp, i, self.endXColdSide, space)
                        i = i + 1
        # draw cold stream line in cold side
        i = 0
        for streamCold in self.mer.dataColdStream:
            space = space + self.vspace
            if i < len(self.mer.streamColdInColdSide):
                if streamCold.name == self.mer.streamColdInColdSide[i].name:
                    if self.mer.streamColdInColdSide[i].tt == self.mer.tPinchCold:
                        streamLine = StreamLine(self.endXColdSide, space, self.startXColdSide, space, "cold", "cold",
                                                self.mer.streamColdInColdSide[i])
                        streamLine.drawStreamLine(qp)
                        self.lineColdInColdSide.append(streamLine)
                        i = i + 1
                    else:
                        streamLine = StreamLine(
                            self.endXColdSide, space, self.startXColdSide + self.hspace, space, "cold", "cold",
                            self.mer.streamColdInColdSide[i])
                        streamLine.drawStreamLine(qp)
                        self.lineColdInColdSide.append(streamLine)
                        i = i + 1
        # draw hot stream line in hot side
        i = 0
        space = 0
        for streamHot in self.mer.dataHotStream:
            space = space + self.vspace
            if i < len(self.mer.streamHotInHotSide):
                if streamHot.name == self.mer.streamHotInHotSide[i].name:
                    if self.mer.streamHotInHotSide[i].tt == self.mer.tPinchHot:
                        streamLine = StreamLine(
                            self.endXHotSide, space, self.startXHotSide, space, "hot", "hot",
                            self.mer.streamHotInHotSide[i])
                        streamLine.drawStreamLine(qp)
                        self.lineHotInHotSide.append(streamLine)
                        i = i + 1
                    else:
                        streamLine = StreamLine(
                            self.endXHotSide, space, self.startXHotSide - 20, space, "hot", "hot",
                            self.mer.streamHotInHotSide[i])
                        streamLine.drawStreamLine(qp)
                        self.lineHotInHotSide.append(streamLine)
                        i = i + 1
        # draw cold line in hot side
        i = 0
        for streamCold in self.mer.dataColdStream:
            space = space + self.vspace
            if i < len(self.mer.streamColdInHotSide):
                if streamCold.name == self.mer.streamColdInHotSide[i].name:
                    if self.mer.streamColdInHotSide[i].ts == self.mer.tPinchCold:
                        streamLine = StreamLine(
                            self.startXHotSide, space, self.endXHotSide, space, "hot", "cold",
                            self.mer.streamColdInHotSide[i])
                        streamLine.drawStreamLine(qp)
                        self.lineColdInHotSide.append(streamLine)
                        self.drawHotUtil(qp, i, self.endXHotSide, space)
                        i = i + 1
                    else:
                        streamLine = StreamLine(
                            self.startXHotSide - self.hspace, space,
                            self.endXHotSide, space,
                            "hot", "cold",
                            self.mer.streamColdInHotSide[i])
                        streamLine.drawStreamLine(qp)
                        self.lineColdInHotSide.append(streamLine)
                        self.drawHotUtil(qp, i, self.endXHotSide, space)
                        i = i + 1
        # draw stream matching in solution grid
        x = self.startXColdSide + self.hspace
        for match in self.mer.matchInColdSide:
            matchFrom = match.matchFrom
            matchTo = match.matchTo
            for lineHot in self.lineHotInColdSide:
                if matchFrom == lineHot.name:
                    y1 = lineHot.y1
                    for lineCold in self.lineColdInColdSide:
                        if lineCold.name == matchTo:
                            y2 = lineCold.y1
                            self.drawLineMatch(qp, x, y1, y2, match)
            x = x + self.hspace
        x = self.startXHotSide - self.hspace
        for match in self.mer.matchInHotSide:
            matchFrom = match.matchFrom
            matchTo = match.matchTo
            for lineHot in self.lineHotInHotSide:
                if matchFrom == lineHot.name:
                    y1 = lineHot.y1
                    for lineCold in self.lineColdInHotSide:
                        if lineCold.name == matchTo:
                            y2 = lineCold.y1
                            self.drawLineMatch(qp, x, y1, y2, match)
            x = x - self.hspace


class GridMer(QWidget):
    def __init__(self, mer: MerCalc):
        super().__init__()

        self.width = 970
        self.height = 750

        self.drawGridMer = DrawGridSolution(mer, self.width, self.height)
        self.initUI()

    def initUI(self):
        self.resize(self.width, self.height)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawGridMer.drawGS(qp)
        qp.end()


from PyQt5.QtWidgets import QApplication
import sys
if __name__ == "__main__":
    mer = test()
    string = merSoltoText(mer)
    print(string)
    app = QApplication(sys.argv)
    ex = GridMer(mer)
    ex.show()
    sys.exit(app.exec())