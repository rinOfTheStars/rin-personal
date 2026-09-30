import os
import subprocess

from talon import Context, Module, actions, app, clip

ctx = Context()
mod = Module()

ctx.matches = r"""
os: mac
tag: user.custom-fs
"""

@mod.action_class
class Actions:

    def finder_open_in_inner(path: str, app_or_path: str = None) -> subprocess.CompletedProcess | None :
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
        old_clipboard = clip.get()
        actions.key("alt-cmd-c")
        temp_keyboard = clip.get()
        result = actions.user.finder_open_in_inner(temp_keyboard, app_or_path)
        if result is not None:
                if result.returncode != 0:
                    app.notify(
                        "Open in app failure",
                        f"open command w/ args {result.args} exited with code {result.returncode}, check talon logs for details"
                    )
                    print(result.stdout)
        else:
            app.notify(
                "WTF??",
                f"open command returned None??? Report this!!!"
            )
        clip.set(old_clipboard)
