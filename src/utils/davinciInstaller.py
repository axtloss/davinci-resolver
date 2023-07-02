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
from davinci_resolver.classes.userData import UserData
from davinci_resolver.utils.zipFile import ZipFileCallback

class DavinciInstaller:

    # This value was taken from the davinci resolve aur package
    # https://aur.archlinux.org/packages/davinci-resolve-studio
    # it does not mention how to get this value, but it seems to work
    # for every version currently available
    # TODO: Investigate where this value comes from
    referrerid: str = "69a3995a376441d0ae23711c44370662"

    downloadID: str
    userdata: UserData
    download_url: str
    url: str

    def __init__(self, downloadID: str, userdata: UserData, url: str):
        self.downloadID = downloadID
        if userdata is not None:
            self.userdata = userdata
        else:
            self.userdata = userdata = UserData(firstname="Leonardo",
                                                lastname="da Vinci",
                                                email="leodavinci@monalisa.org", # monalisa.org is a real domain, huh
                                                phone="363-259-518", # randomly generated
                                                country="it",
                                                state="",
                                                city="Anchiano",
                                                product="DaVinci Resolve")
        self.url = url
        self.download_url = self.get_src_url()

    def get_src_url(self):
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
            'Referer': 'https://www.blackmagicdesign.com/support/download/' + self.referrerid + '/Linux',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cookie': '_ga=GA1.2.1849503966.1518103294; _gid=GA1.2.953840595.1518103294',
            'Authority': 'www.blackmagicdesign.com',
        }

        print(self.userdata.get_json())

        response = requests.post(self.url.replace("%ID%", self.downloadID), cookies=cookies, headers=headers, data=self.userdata.get_json())
        return response.content.decode('utf-8')

    def download_installer(self, on_progress):
        on_progress("100")
        return
        os.mkdir(os.getenv('XDG_DATA_HOME')+'/installerCache')
        file_name=os.getenv('XDG_DATA_HOME')+'/installerCache/davinci.zip'
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
                    done = int((dl / total_length) * 100)
                    on_progress(str(done))


    def extract_installer_zip(self, on_progress):
        def calculate_progress(current: int, total: int):
            progress=float(current) / total
            progress=round(progress*100)
            return str(progress)

        with ZipFileCallback(os.getenv('XDG_DATA_HOME')+'/installerCache/davinci.zip', 'r') as zip_file:
            zip_file.extractall(os.getenv('XDG_DATA_HOME')+'/installerCache', progress_callback=lambda current, total: on_progress(calculate_progress(current, total)))


   # def copy_directories(self):

   
