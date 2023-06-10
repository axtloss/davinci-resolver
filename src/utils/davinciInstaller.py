# davinciInstaller.py
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

import os
import sys
import requests
import zipfile

class DavinciInstaller:

    download_url: str

    def __init__(self, download_url: str):
        self.download_url = download_url

    def download_installer(self):
        os.mkdir(os.getenv('HOME')+'/.var/app/io.github.axtloss.davinciresolver/data/installerCache')
        file_name=os.getenv('HOME')+'/.var/app/io.github.axtloss.davinciresolver/data/installerCache/davinci.zip'
        with open(file_name, "wb") as f:
            print("Downloading %s" % file_name)
            response = requests.get(self.download_url, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None: # no content length header
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )
                    sys.stdout.flush()


    def extract_installer_zip(self):
        with zipfile.ZipFile(os.getenv('HOME')+'/.var/app/io.github.axtloss.davinciresolver/data/installerCache/davinci.zip', 'r') as zip_file:
            zip_file.extractall(os.getenv('HOME')+'/.var/app/io.github.axtloss.davinciresolver/data/installerCache')
            
