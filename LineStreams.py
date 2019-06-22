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

from StreamsGrid import StreamGrid


"""


Drawing MER Grid solution into PyQt5 widget


"""
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QPainter, QColor, QBrush, QPolygon


def textSize(qp: QPainter, text: str):
    rect: QRect = QRect()
    rect = qp.boundingRect(rect, Qt.PlainText, text)
    textWidth = rect.width()
    textHeight = rect.height()
    return textWidth, textHeight


class StreamLine:
    def __init__(self, x1, y1, x2, y2, side: str, typeStream: str, streamGrid: StreamGrid):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.side = side
        self.typeStream = typeStream
        self.streamGrid = streamGrid
        self.name = self.streamGrid.name

    @staticmethod
    def drawArrow(qp: QPainter, x1, y1, x2, y2, x3, y3):
        points = QPolygon([
            QPoint(x1, y1),
            QPoint(x2, y2),
            QPoint(x3, y3)
        ])
        qp.drawPolygon(points)

    def drawStreamLine(self, qp: QPainter):
        ts = str(self.streamGrid.ts)
        tt = str(self.streamGrid.tt)
        ts_width, ts_height = textSize(qp, ts)
        tt_width, tt_height = textSize(qp, tt)

        if self.side == "hot" and self.typeStream == "hot":
            qp.setPen(QColor(Qt.red))
            qp.drawLine(self.x1, self.y1, self.x2, self.y2)
            qp.setBrush(QBrush(QColor(Qt.red)))
            self.drawArrow(qp, self.x2 - 10, self.y2 - 5,
                           self.x2, self.y2,
                           self.x2 - 10, self.y2 + 5)
            qp.drawText(self.x1, self.y1 - 2, ts)
            qp.drawText(self.x2 - tt_width - 10, self.y2 - 2, tt)

        if self.side == "hot" and self.typeStream == "cold":
            qp.setPen(QColor(Qt.blue))
            qp.drawLine(self.x1, self.y1, self.x2, self.y2)
            qp.setBrush(QBrush(QColor(Qt.blue)))
            self.drawArrow(qp, self.x2 + 10, self.y2 - 5,
                           self.x2, self.y2,
                           self.x2 + 10, self.y2 + 5)
            qp.drawText(self.x1 - ts_width, self.y1 - 2, ts)
            qp.drawText(self.x2 + 10, self.y2 - 2, tt)

        if self.side == "cold" and self.typeStream == "hot":
            qp.setPen(QColor(Qt.red))
            qp.drawLine(self.x1, self.y1, self.x2, self.y2)
            qp.setBrush(QBrush(QColor(Qt.red)))
            self.drawArrow(qp, self.x2 - 10, self.y2 - 5,
                           self.x2, self.y2,
                           self.x2 - 10, self.y2 + 5)
            qp.drawText(self.x1, self.y1 - 2, ts)
            qp.drawText(self.x2 - tt_width - 10, self.y2 - 2, tt)

        if self.side == "cold" and self.typeStream == "cold":
            qp.setPen(QColor(Qt.blue))
            qp.drawLine(self.x1, self.y1, self.x2, self.y2)
            self.drawArrow(qp, self.x2 + 10, self.y2 - 5,
                           self.x2, self.y2,
                           self.x2 + 10, self.y2 + 5)
            qp.drawText(self.x1 - ts_width, self.y1 - 2, ts)
            qp.drawText(self.x2 + 10, self.y2 - 2, tt)