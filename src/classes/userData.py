# userData.py
#
# Copyright 2023 axtloss <axtlos@getcryst.al>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License only.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-only

class UserData:

    firstname: str
    lastname: str
    email: str
    phone: str
    country: str
    state: str
    city: str
    product: str

    def __init__(
            self,
            firstname: str,
            lastname: str,
            email: str,
            phone: str,
            country: str,
            state: str,
            city: str,
            product: str):

        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone = phone
        self.country = country
        self.state = state
        self.city = city
        self.product = product
