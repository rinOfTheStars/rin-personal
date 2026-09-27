import os
import subprocess
from typing import Optional

from talon import Context, Module, actions, app

ctx = Context()
mod = Module()

ctx.matches = r"""
os: mac
tag: user.custom-fs
"""

OPEN_CMD_PATH = "/usr/bin/open"

def write_to_clipboard(output : any):
        process = subprocess.Popen(
            "/usr/bin/pbcopy", stdin=subprocess.PIPE)
        process.communicate(output)

def read_from_clipboard():
        return subprocess.check_output("/usr/bin/pbpaste")

@mod.action_class
class Actions:

    def finder_open_in_inner(path: str, app_or_path: str = None) -> Optional[subprocess.CompletedProcess]:
        """INTERNAL"""
        if app_or_path.endswith(".app") and os.path.exists(app_or_path):
            program = app_or_path
        else:
            application = actions.user.get_running_app(app_or_path)
            if not application:
                app.notify(
                    "Couldn't find application",
                    f"Couldn't find a running app named {application}",
                )
                return
            program = application.path
        return subprocess.run(["/usr/bin/open", "-a", program, path], capture_output=True)
        
    def finder_open_in(path: str, app_or_path: str = None):
        """Opens the supplied path within a given running program. macOS only, depends on talon_axkit"""
        old_clipboard = read_from_clipboard()
        actions.key("alt-cmd-c")
        temp_keyboard = read_from_clipboard()
        actions.user.finder_open_in_inner(temp_keyboard, app_or_path)
        write_to_clipboard(old_clipboard)
