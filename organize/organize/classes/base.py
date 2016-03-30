import urwid
import json

class BaseView():
    def save_config(self):
        with open('config.json', 'w') as data:
            json.dump(self.data, data, indent=4, sort_keys=True)

    def display_errors(self, errors, folder=False):
        body = []
        big_text = urwid.BigText("Error!", urwid.HalfBlock5x4Font())
        big_text = urwid.Padding(big_text, 'center', None)
        body.append(big_text)
        body.append(urwid.Text(u'\n'))

        for error in errors:
            the_error = urwid.Text(('error', error))
            body.append(the_error)

        body.append(urwid.Text(u'\n\n'))

        go_back = urwid.Button(u'Go Back')

        if folder:
            urwid.connect_signal(go_back, 'click', self.back_to_main_display)
        else:
            urwid.connect_signal(go_back, 'click', self.back_to_new_extension_display)
        body.append(urwid.AttrMap(go_back, None, focus_map='selected'))

        self.main_widget.original_widget = urwid.ListBox(urwid.SimpleListWalker(body))

    def exit(self, button):
        raise urwid.ExitMainLoop()

    def open_config(self):
        with open('config.json') as config_file:
            self.data = json.load(config_file)

    def back_to_main_display(self, button=None):
        self.main_widget.original_widget = self.main_display

    def back_to_opened_folder_display(self, button):
        self.main_widget.original_widget = self.opened_folder_display

    def back_to_new_extension_display(self, button):
        self.main_widget.original_widget = self.new_extension_display