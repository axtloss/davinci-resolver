# window.py
#
# Copyright 2023 Unknown
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import os
from urllib import request
from urllib import error as urlerr
from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import Xdp
from gi.repository import XdpGtk4
from davinci_resolver.widgets.entry import DavinciEntry
from davinci_resolver.widgets.tag import DavinciTag
from davinci_resolver.windows.davinciInstallerWindow import DavinciInstallerWindow

@Gtk.Template(resource_path='/io/github/axtloss/davinciresolver/window.ui')
class DavinciResolverWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'DavinciResolverWindow'

    versionList: Gtk.ListBox = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parse_versions_file()
        portal = Xdp.Portal()
        icon="org.gnome.Adwaita1.Demo-symbolic"
        _icon=Gio.Icon.new_for_string("test")

        icon_v = _icon.serialize()
        #token = portal.dynamic_launcher_prepare_install("test", icon_v)
        portal.dynamic_launcher_prepare_install(None, "title", icon_v, Xdp.LauncherType.APPLICATION, None, True, True, None, self.prepare_install_cb)
        #portal.dynamic_launcher_install(
        #    token,
        #    "test.desktop",
        #    """
        #    [Desktop Entry]
        #    Exec=test
        #    Type=Application
        #    Terminal=false
        #    Categories=Application;
        #    Comment=Launch test using Bottles.
        #    Actions=Configure;
        #    [Desktop Action Configure]
        #        Name=Configure in Bottles
        #    Exec=test
        #    """
        #    ).encode("utf-8")

    def prepare_install_cb(self, result, guh):
        portal = Xdp.Portal()
        print("here")
        print(guh)

        ret = portal.dynamic_launcher_prepare_install_finish(guh)
        print(result)
        print(ret)

    def parse_versions_file(self):
        content=""

        try:
            for line in request.urlopen("https://raw.githubusercontent.com/axtloss/davinci-resolver/main/versions.json"):
                content=content+line.decode('utf-8')
            with open(os.getenv('HOME')+'/.var/app/io.github.axtloss.davinciresolver/data/versions.json', 'w') as file:
                file.write(content)
        except urlerr.URLError:
            print('no internet, using cached file')
            with open(os.getenv('HOME')+'/.var/app/io.github.axtloss.davinciresolver/data/versions.json', 'r') as file:
                content=file.read()

        parsed = json.loads(content)
        for entry in parsed.get('versions'):
            gtkEntry = DavinciEntry(name=entry.get('name'), version=entry.get('version'),
                                    url=entry.get('url'), downloadid=entry.get('downloadid'), window=self)
            print(entry.get('downloadid'))
            for tag in entry.get('tags'):
                if tag.strip().lower() == "studio":
                    tag=DavinciTag(labelType=0)
                elif tag.strip().lower() == "beta":
                    tag=DavinciTag(labelType=1)
                gtkEntry.add_tag(tag)
            self.versionList.append(gtkEntry)
            
