# davinciInstallerWindow.py
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

import json
import os
from urllib import request
from urllib import error as urlerr
from gi.repository import Adw
from gi.repository import Gtk
from davinci_resolver.classes.userData import UserData
from davinci_resolver.utils.davinciInstaller import DavinciInstaller

@Gtk.Template(resource_path='/io/github/axtloss/davinciresolver/windows/davinciInstallerWindow.ui')
class DavinciInstallerWindow(Adw.ApplicationWindow):

    __gtype_name__ = "DavinciInstallerWindow"

    installerStack: Gtk.Stack = Gtk.Template.Child()
    anonymousRegister: Gtk.Button = Gtk.Template.Child()
    regularRegister: Gtk.Button = Gtk.Template.Child()
    selectPage: Adw.StatusPage = Gtk.Template.Child()
    registerPage: Adw.StatusPage = Gtk.Template.Child()
    registerButtons: Gtk.ActionBar = Gtk.Template.Child()
    cancelButton: Gtk.Button = Gtk.Template.Child()
    registerButton: Gtk.Button = Gtk.Template.Child()

    firstNameEntry: Adw.EntryRow = Gtk.Template.Child()
    lastNameEntry: Adw.EntryRow = Gtk.Template.Child()
    emailEntry: Adw.EntryRow = Gtk.Template.Child()
    phoneEntry: Adw.EntryRow = Gtk.Template.Child()
    countrySelection: Adw.ComboRow = Gtk.Template.Child()
    cityEntry: Adw.EntryRow = Gtk.Template.Child()

    downloadID: str
    url: str

    def __init__(self, window: Adw.ApplicationWindow, downloadID: str, url: str,  **kwargs):
        super().__init__(**kwargs)
        self.window = window
        self.downloadID = downloadID
        self.url = url
        self.set_transient_for(self.window)
        self.regularRegister.connect('clicked', self.register)
        self.cancelButton.connect('clicked', self.cancelRegister)
        self.registerButton.connect('clicked', self.on_register)
        self.anonymousRegister.connect('clicked', self.on_anonymous_register)
        self.populate_country()


    def register(self, _):
        self.installerStack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT)
        self.installerStack.set_visible_child(self.registerPage)
        self.registerButtons.set_revealed(True)

    def cancelRegister(self, _):
        self.installerStack.set_transition_type(Gtk.StackTransitionType.SLIDE_RIGHT)
        self.installerStack.set_visible_child(self.selectPage)
        self.registerButtons.set_revealed(False)

    def on_anonymous_register(self, _):
        installer = DavinciInstaller(self.downloadID, None, self.url)
        installer.download_installer()
        installer.extract_installer_zip()

    def on_register(self, _):
        selected_country = self.countries.get_string(self.countrySelection.get_selected())

        data = UserData(firstname=self.firstNameEntry.get_text(),
                        lastname=self.lastNameEntry.get_text(),
                        email=self.emailEntry.get_text(),
                        phone=self.phoneEntry.get_text(),
                        country=self.parsed.get(selected_country),
                        state="", # can be kept empty
                        city=self.cityEntry.get_text(),
                        product="DaVinci Resolve")

        installer = DavinciInstaller(self.downloadID, data, self.url)
        installer.download_installer()
        installer.extract_installer_zip()


    def populate_country(self):
        self.countries = Gtk.StringList()
        content=""
        try:
            for line in request.urlopen("https://raw.githubusercontent.com/axtloss/davinci-resolver/tmpdev/countries.json"):
                content=content+line.decode('utf-8')
            with open(os.getenv('HOME')+'/.var/app/io.github.axtloss.davinciresolver/data/countries.json', 'w') as file:
                file.write(content)
        except urlerr.URLError:
            print('no internet, using cached file')
            with open(os.getenv('HOME')+'/.var/app/io.github.axtloss.davinciresolver/data/countries.json', 'r') as file:
                content=file.read()

        self.parsed = json.loads(content)
        for country in self.parsed:
            self.countries.append(country)

        self.countrySelection.set_model(self.countries)
        
