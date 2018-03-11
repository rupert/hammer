import sublime_plugin

from .utils import get_cwd


class Flake8FileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        clear_window(self.view.window())
        run_flake8(self.view.window(), [self.view.file_name()])


class Flake8ProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        clear_window(self.window)
        run_flake8(self.window)


def clear_window(window):
    for view in window.views():
        clear_view(view)


def clear_view(view):
    view.erase_phantoms('exec')


def run_flake8(window, args=[]):
    command = ['pipenv', 'run', 'flake8'] + args
    window.run_command('exec', {
        'cmd': command,
        'file_regex': '^(.+):([0-9]+):([0-9]+): (.*)$',
        'working_dir': get_cwd(),
    })
