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
from davinci_resolver.classes.userData import UserData

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
    referrerid: str = "69a3995a376441d0ae23711c44370662"

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

    def add_tag(self, tag: DavinciTag):
        self.entryBox.prepend(tag)
        self.tagList.append(tag)

    def remove_tag(self, tag: DavinciTag):
        self.entryBox.remove(tag)
        self.tagList.remove(tag)

    def get_src_url(userdata: UserData):

        cookies = {
            '_ga': 'GA1.2.1849503966.1518103294',
            '_gid': 'GA1.2.953840595.1518103294',
        }

        headers = {
            'Host': 'www.blackmagicdesign.com',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://www.blackmagicdesign.com',
            'Content-Type': 'application/json;charset=UTF-8',
            'Referer': 'https://www.blackmagicdesign.com/support/download/' + self.refferrerid + '/Linux',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Authority': 'www.blackmagicdesign.com',
        }

        data = userdata.get_json()

        response = requests.post('http://' + self.url.replace("%", self.downloadid), cookies=cookies, headers=headers, data=data)
