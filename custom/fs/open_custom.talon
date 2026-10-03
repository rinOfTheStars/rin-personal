os: mac
app: finder
tag: user.file_manager
and tag: user.custom-fs
-
open {user.file_manager_files} in <user.launch_applications>$:
    user.finder_open_in(user.file_manager_files, user.launch_applications)
open {user.file_manager_files} in <user.running_applications>$:
    user.finder_open_in(user.file_manager_files, user.running_applications)
open {user.file_manager_directories} in <user.launch_applications>$:
    user.finder_open_in(user.file_manager_directories, user.launch_applications)
open {user.file_manager_directories} in <user.running_applications>$:
    user.finder_open_in(user.file_manager_directories, user.running_applications)