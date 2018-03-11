import ast

import sublime_plugin

from .utils import get_line_no, get_buffer, run


last_args = []


class PytestSuiteCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        run_pytest(self.view)


class PytestLastFailedCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        run_pytest(self.view, ['--lf'])


class PytestReRunCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        run_pytest(self.view, last_args)


class PytestFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        test_file_name = self.view.file_name()

        if not test_file_name:
            return

        run_pytest(self.view, [test_file_name])


class PytestFunctionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        test_file_name = self.view.file_name()

        if not test_file_name:
            return

        line_no = get_line_no(self.view)
        code = get_buffer(self.view)
        test_function_name = get_test_function_name(code, line_no)

        if test_function_name is None:
            return

        test_nodeid = '{test_file_name}::{test_function_name}'.format(
            test_file_name=test_file_name,
            test_function_name=test_function_name,
        )

        run_pytest(self.view, [test_nodeid])


def get_test_function_name(code, line_no):
    tree = ast.parse(code)

    func_node = None

    for node in ast.iter_child_nodes(tree):
        if not isinstance(node, ast.FunctionDef):
            continue

        func_node = node

        if node.lineno > line_no:
            break

    if not func_node:
        return None

    return func_node.name


def get_project_root():
    return run(['pipenv', '--where'])


def run_pytest(view, args=[]):
    global last_args
    last_args = args

    project_root = get_project_root()

    command = ['pipenv', 'run', 'pytest', '-v'] + args
    view.window().run_command('exec', {
        'cmd': command,
        'working_dir': project_root,
    })
