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

class DataStream:
    """docstring for """

    def __init__(self, ts, tt, c, name):
        self.ts = ts
        self.tt = tt
        self.c = c
        self.name = name