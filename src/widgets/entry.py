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
from davinci_resolver.utils.davinciInstaller import DavinciInstaller

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

    # This value was taken from the davinci resolve aur package
    # https://aur.archlinux.org/packages/davinci-resolve-studio
    # it does not mention how to get this value, but it seems to work
    # for every version currently available
    # TODO: Investigate where this value comes from
    refferrerid: str = "69a3995a376441d0ae23711c44370662"

    def __init__(self,
            name: str,
            version: str,
            downloadid: str,
            url: str,
            **kwargs,):

        super().__init__(**kwargs)
        self.name = name
        self.version = version
        self.downloadid = downloadid
        self.url = url
        self.set_title(self.name)
        self.button.connect('clicked', self.install_davinci)

    def add_tag(self, tag: DavinciTag):
        self.entryBox.prepend(tag)
        self.tagList.append(tag)

    def remove_tag(self, tag: DavinciTag):
        self.entryBox.remove(tag)
        self.tagList.remove(tag)

    def install_davinci(self, _):

        # This is placeholder data, used for everyone who uses davinciresolver
        # TODO: evaluate if it would make sense to let the user enter this information themselves (optional)
        # Issue is that the country and state are a bit of work to implement
        # since the countries are a set list, and the state only applies to specific countries
        # futhermore, it seems like the country uses some special codes that are not displayed in the main page
        userdata = UserData(
            firstname="Leonardo",
            lastname="da Vinci",
            email="leodavinci@monalisa.org",
            phone="363-259-518",
            country="it",
            state="",
            city="Anchiano",
            product="DaVinci Resolve"
        )
        cookies = {
            '_ga': 'GA1.2.1849503966.1518103294',
            '_gid': 'GA1.2.953840595.1518103294',
        }

        headers = {
            'Host': 'www.blackmagicdesign.com',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://www.blackmagicdesign.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Content-Type': 'application/json;charset=UTF-8',
            'Referer': 'https://www.blackmagicdesign.com/support/download/' + self.refferrerid + '/Linux',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cookie': '_ga=GA1.2.1849503966.1518103294; _gid=GA1.2.953840595.1518103294',
            'Authority': 'www.blackmagicdesign.com',
        }

        response = requests.post(self.url.replace("%ID%", self.downloadid), cookies=cookies, headers=headers, data=userdata.get_json())
        installer = DavinciInstaller(download_url=response.content.decode('utf-8'))
        installer.download_installer()
        installer.extract_installer_zip()
