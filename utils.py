import os
import subprocess

import sublime


def get_selected_line_nos(view):
    return (
        view.rowcol(view.sel()[0].begin())[0] + 1,
        view.rowcol(view.sel()[0].end())[0] + 1,
    )


def get_line_no(view):
    return view.rowcol(view.sel()[0].begin())[0] + 1


def get_buffer(view):
    return view.substr(sublime.Region(0, view.size()))


def run(command, cwd=None):
    if cwd is None:
        cwd = get_cwd()

    output = subprocess.check_output(command, cwd=cwd)
    output = output.decode('utf-8')
    output = output.strip()
    return output


def get_cwd():
    window = sublime.active_window()
    view = window.active_view()

    if view:
        file_name = view.file_name()

        if file_name:
            return os.path.dirname(file_name)

    folders = window.folders()

    if len(folders) > 0:
        return folders[0]
    else:
        return os.path.expanduser('~')
