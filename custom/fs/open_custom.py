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
        
    def finder_open_in(local_path: str, app_target: str = None):
        """Opens the supplied local_path within a given running program. macOS only, depends on talon_axkit"""
        current_path = actions.user.file_manager_current_path()
        target_path = os.path.join(current_path, local_path)
        target_path = os.path.abspath(target_path)
        # print("target_path: " + target_path)
        if app_target.endswith(".app") and os.path.exists(app_target):
            app_path = app_target
        else:
            application = actions.user.get_running_app(app_target)
            if not application:
                app.notify(
                    "Couldn't find application",
                    f"Couldn't find a running app named {application}",
                )
                app_path = None
            app_path = application.path
        if app_path is not None:
            result = subprocess.run(["/usr/bin/open", "-a",app_path , target_path], capture_output=True)
        else:
            result = None
        if result is not None:
                if result.returncode != 0:
                    app.notify(
                        "Open in app failure",
                        f"open command w/ args {result.args} exited with code {result.returncode}, check talon logs for details"
                    )
                    print("Stdout code is " + str(result.returncode))
        else:
            if app_path is not None:
                app.notify(
                    "Unexpected behavior",
                    "app_target is valid while open command returned None; this should never happen?"
                )
                print("app_target is valid while open command returned None; this should never happen?")
