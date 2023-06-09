# This file was taken from bottles <https://usebottles.com> with the permission from brombinmirko
#
# threading.py
#
# Copyright 2022 brombinmirko <send@mirko.pm>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, in version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import threading
import traceback

from gettext import gettext as _

from gi.repository import GLib


class RunAsync(threading.Thread):
    """
    This class is used to execute a function asynchronously.
    It takes a function, a callback and a list of arguments as input.
    """

    def __init__(self, task_func, callback=None, *args, **kwargs):
        import faulthandler

        faulthandler.enable()

        self.source_id = None
        assert threading.current_thread() is threading.main_thread()

        super(RunAsync, self).__init__(target=self.__target, args=args, kwargs=kwargs)

        self.task_func = task_func

        self.callback = callback if callback else lambda r, e: None
        self.daemon = kwargs.pop("daemon", True)

        self.start()

    def __target(self, *args, **kwargs):
        result = None
        error = None

        print(f"DEBUG: Running async job [{self.task_func}].")

        try:
            result = self.task_func(*args, **kwargs)
        except Exception as exception:
            print(
                "ERROR: while running async job: "
                f"{self.task_func}\nException: {exception}"
            )

            error = exception
            _ex_type, _ex_value, trace = sys.exc_info()
            traceback.print_tb(trace)
            traceback_info = "\n".join(traceback.format_tb(trace))

            print([str(exception), traceback_info])
        self.source_id = GLib.idle_add(self.callback, result, error)
        return self.source_id
