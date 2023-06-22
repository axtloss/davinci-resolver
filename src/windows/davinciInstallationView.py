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

    downloadProgress: Gtk.Label = Gtk.Template.Child()
    downloadSpinner: Gtk.Spinner = Gtk.Template.Child()

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


    def update_download_progress(self, progress: str):
        GLib.idle_add(self.downloadProgress.set_label,progress+"%")

    def download_resolve(self):
        self.installer.download_installer(on_progress=self.update_download_progress)

    def begin_installation(self, installer: DavinciInstaller):
        self.installer = installer
        RunAsync(self.download_resolve)

        
