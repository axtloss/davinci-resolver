# installationView.py
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

from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import GLib
from davinci_resolver.utils.runAsync import RunAsync
from davinci_resolver.utils.davinciInstaller import DavinciInstaller

@Gtk.Template(resource_path='/io/github/axtloss/davinciresolver/windows/davinciInstallationView.ui')
class DavinciInstallationView(Adw.Bin):

    __gtype_name__ = "DavinciInstallationView"

    downloadRow: Adw.ActionRow = Gtk.Template.Child()
    downloadProgress: Gtk.Label = Gtk.Template.Child()
    downloadSpinner: Gtk.Spinner = Gtk.Template.Child()

    extractRow: Adw.ActionRow = Gtk.Template.Child()
    extractProgress: Gtk.Label = Gtk.Template.Child()
    extractSpinner: Gtk.Spinner = Gtk.Template.Child()

    installExpander: Adw.ExpanderRow = Gtk.Template.Child()

    copySpinner: Gtk.Spinner = Gtk.Template.Child()
    copyIcon: Gtk.Spinner = Gtk.Template.Child()

    rawUtilitiesSpinner: Gtk.Spinner = Gtk.Template.Child()
    rawUtilitiesIcon: Gtk.Image = Gtk.Template.Child()

    desktopSpinner: Gtk.Spinner = Gtk.Template.Child()
    desktopIcon: Gtk.Image = Gtk.Template.Child()

    def __init__(self, window: Adw.ApplicationWindow, **kwargs):
        super().__init__(**kwargs)
        self.window = window

    def __update_download_progress(self, progress: str):
        GLib.idle_add(self.downloadProgress.set_label, progress+"%")

    def __update_extraction_progress(self, progress: str):
        GLib.idle_add(self.extractProgress.set_label, progress+"%")

    def __download_resolve(self):
        GLib.idle_add(self.downloadRow.set_icon_name, "")
        GLib.idle_add(self.downloadSpinner.set_spinning, True)
        self.installer.download_installer(on_progress=self.__update_download_progress)
        GLib.idle_add(self.downloadSpinner.set_spinning, False)
        GLib.idle_add(self.downloadRow.set_icon_name, "test-pass-symbolic")

        self.__extract_resolve()

    def __extract_resolve(self):
        GLib.idle_add(self.extractRow.set_icon_name, "")
        GLib.idle_add(self.extractSpinner.set_spinning, True)
        self.installer.extract_installer_zip(on_progress=self.__update_extraction_progress)
        GLib.idle_add(self.extractSpinner.set_spinning, False)
        GLib.idle_add(self.extractRow.set_icon_name, "test-pass-symbolic")

    def begin_installation(self, installer: DavinciInstaller):
        self.installer = installer
        RunAsync(self.__download_resolve)

        
