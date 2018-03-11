import json

import sublime
import sublime_plugin


class JsonPrettifyCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if region.empty():
                region = sublime.Region(0, self.view.size())
                select_all = True
            else:
                select_all = False

            data = self.view.substr(region)

            try:
                data = json.loads(data)
            except Exception as exc:
                sublime.status_message(str(exc))
                continue

            data = json.dumps(data, indent=4)
            self.view.replace(edit, region, data)

            if select_all:
                self.view.set_syntax_file(
                    'Packages/JavaScript/JSON.tmLanguage'
                )
