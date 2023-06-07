# tag.py
#
# Copyright 2023 axtlos <axtlos@disroot.org>
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

from gi.repository import Gtk

@Gtk.Template(resource_path='/io/github/axtloss/davinciresolver/widgets/tag.ui')
class DavinciTag(Gtk.Label):

    __gtype_name__="DavinciTag"

    def __init__(self, labelType: int, **kwargs):
        """
        Init class for DavinciTag
        Parameters:
        labelType (int): What the tag should represent, 0 for studio and 1 for beta
        """
        super().__init__(**kwargs)
        if labelType == 0:
            self.add_css_class("studioTag")
            self.set_label("Studio")
        else:
            self.add_css_class("betaTag")
            self.set_label("Beta")
