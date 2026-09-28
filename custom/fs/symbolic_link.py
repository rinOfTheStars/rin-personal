import os
import subprocess
from typing import Optional

from talon import Context, Module, actions, app

ctx = Context()
mod = Module()

ctx.matches = r"""
os: mac
app: finder
"""

def write_to_clipboard(output : any):
        process = subprocess.Popen(
            "/usr/bin/pbcopy", stdin=subprocess.PIPE)
        process.communicate(output)

def read_from_clipboard():
        return subprocess.check_output("/usr/bin/pbpaste")

@mod.action_class
class Actions:

    def symlink_active_to_clipboard(direction: bool, name: str):
        """Symlinks active directory to or from the directory or file in the clipboard"""
        here = actions.user.file_manager_current_path()
        possibly_there = read_from_clipboard()
        if os.path.exists(possibly_there):
            result = None
            actual_name = None
            if name == "":
                if direction:
                    actual_name = os.path.basename(here).decode()
                else:
                    actual_name = os.path.basename(possibly_there).decode()
                result = actions.user.symlink(here, possibly_there, direction, actual_name)
            else:
                result = actions.user.symlink(here, possibly_there, direction, name)
            
            if result is not None:
                if reason != 0:
                    app.notify(
                        "Symlink failure",
                        f"symlink command w/ args {result.args} exited with code {result.returncode}, check talon logs for details"
                    )
                    print(result.stdout)
                else :
                    print(f"Successfully created a symlink w/ args {result.args}")
        else:
            app.notify(
                "Bad clipboard contents (not path)",
                f"String {possibly_there} is not a valid path!"
            )

            

    def symlink(here: str, there: str, direction: bool, name: str) -> subprocess.CompletedProcess | None :
        """Creates a symlink"""
        # ls -s ORIGINAL SYMLINK_PATH
        if direction:
            # 'forward' (from here to there)
            if os.path.isdir(there):
                symlink_path = there + "/" + name
                return subprocess.run(["/bin/ln", "-s", here, symlink_path], capture_output=True)
            else:
                app.notify(
                "Bad clipboard contents (not dir)",
                f"String {possibly_there} is not a valid directory!"
                )
                return None
        else:
            # 'reverse' (from there to here)
            # can be from a file, unlike forward mode
            symlink_path = here + "/" + name
            return subprocess.run(["/bin/ln", "-s", there, symlink_path], capture_output=True)
