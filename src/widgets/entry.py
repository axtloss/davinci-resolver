# entry.py
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

from gi.repository import Gtk, Adw
from davinci_resolver.widgets.tag import DavinciTag

@Gtk.Template(resource_path='/io/github/axtloss/davinciresolver/widgets/entry.ui')
class DavinciEntry(Adw.ActionRow):
    __gtype_name__="DavinciEntry"

    entryBox: Gtk.Box = Gtk.Template.Child()
    button: Gtk.Button = Gtk.Template.Child()

    tagList: list[DavinciTag] = [];

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_tag(self, tag: DavinciTag):
        self.entryBox.prepend(tag)
        self.tagList.append(tag)

    def remove_tag(self, tag: DavinciTag):
        self.entryBox.remove(tag)
        self.tagList.remove(tag)
