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

import requests
from gi.repository import Gtk, Adw
from davinci_resolver.widgets.tag import DavinciTag
from davinci_resolver.classes.userData import UserData
from davinci_resolver.windows.davinciInstallerWindow import DavinciInstallerWindow

@Gtk.Template(resource_path='/io/github/axtloss/davinciresolver/widgets/entry.ui')
class DavinciEntry(Adw.ActionRow):
    __gtype_name__="DavinciEntry"

    entryBox: Gtk.Box = Gtk.Template.Child()
    button: Gtk.Button = Gtk.Template.Child()

    tagList: list[DavinciTag] = [];

    name: str = ""
    version: str = ""
    url: str = ""
    downloadid: str = ""

    def __init__(self,
            name: str,
            version: str,
            downloadid: str,
            url: str,
            window: Adw.ApplicationWindow,
            **kwargs):

        super().__init__(**kwargs)
        self.name = name
        self.version = version
        self.downloadid = downloadid
        self.url = url
        self.window = window
        self.set_title(self.name)
        self.button.connect('clicked', self.install_davinci)

    def add_tag(self, tag: DavinciTag):
        self.entryBox.prepend(tag)
        self.tagList.append(tag)

    def remove_tag(self, tag: DavinciTag):
        self.entryBox.remove(tag)
        self.tagList.remove(tag)

    def install_davinci(self, _):
        installer=DavinciInstallerWindow(self.window, self.downloadid, self.url)
        installer.present()
        
