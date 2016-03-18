import urwid
import json
import pprint

def open_config():
    with open('config.json') as file:
        data = json.load(file)

    return data

data = open_config()

class Jsonify():
    def _try(self, o):
        try:
            return o.__dict__
        except:
            return str(o)

    def to_json(self):
        return json.dumps(self,
                default=lambda o: self._try(o),
                sort_keys=True,
                indent=0,
                separators=(',',':')).replace('\n','')

class ConfigView():
    def __init__(self, data):
        self.data = data
        self.layout = {}
        self._run()

    def make_main_display(self):
        self.body = [urwid.Text(u'Folders'), urwid.Divider()]

        new_folder_button =  urwid.Button(u'New Folder')
        urwid.connect_signal(new_folder_button, 'click', self._make_new_folder)

        exit_button = urwid.Button(u'Exit')
        urwid.connect_signal(exit_button, 'click', self.exit)
        
        save_button = urwid.Button(u'Save')
        #urwid.connect_signal(save_button, 'click', self.save_changes)

        self.body.append(urwid.Divider())
    
        for a_folder in self.data:
            folder_button = urwid.Button(a_folder)
            urwid.connect_signal(folder_button, 'click', self.make_open_folder_display)
            self.body.append(folder_button)
            self.body.append(urwid.Divider())

        self.body.append(urwid.Divider())
        self.body.append(new_folder_button)
        self.body.append(save_button)
        self.body.append(exit_button)
        self.top = urwid.ListBox(urwid.SimpleFocusListWalker(self.body))
        self.main_widget = urwid.Padding(self.top, left=0, right=0)
        self.main_display = self.main_widget.original_widget

    def make_open_folder_display(self, button):
        body = []
        folder = button.get_label()
        body.append(urwid.Text(folder))

        for formats in self.data[folder]:
            body.append(urwid.Text(formats))

        body.append(urwid.Divider())

        new_format_button = urwid.Button(u'Add a Format')
        urwid.connect_signal(new_format_button, 'click', self.make_new_format_display)
        body.append(new_format_button)
        
        go_back = urwid.Button(u'Go Back')
        urwid.connect_signal(go_back, 'click', self.back_to_main_display)
        body.append(go_back)

        exit = urwid.Button(u'Exit')
        urwid.connect_signal(exit, 'click', self.exit)
        body.append(exit)

        self.main_widget.original_widget = urwid.ListBox(urwid.SimpleFocusListWalker(body))
        self.opened_folder_display = self.main_widget.original_widget

    def make_new_format_display(self, button):
        body = []

        text = urwid.Text(u'Add a Format')
        body.append(text)

        self.new_format = urwid.Edit(u'Format: ')
        body.append(self.new_format)

        save = urwid.Button(u'Save Format')
        urwid.connect_signal(save, 'click', self.on_save_format_click)
        body.append(save)

        go_back = urwid.Button(u'Go Back')
        urwid.connect_signal(go_back, 'click', self.back_to_opened_folder_display)
        body.append(go_back)

        self.main_widget.original_widget = urwid.Overlay(
            urwid.ListBox(urwid.SimpleListWalker(
                body)),
            urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                align='center', width=('relative', 100),
                valign='middle', height=('relative', 75),
                min_width=20, min_height=9)
        self.new_format_display = self.main_widget.original_widget

    def on_save_format_click(self, button):
        if self.check_if_valid_format():
            self.ask_to_save()

    def check_if_valid_format(self):
        errors = []
        format_text = self.new_format.get_edit_text()

        if len(format_text) < 1:
            errors.append('You need to enter something')
            self.display_errors(errors)
        else:
            if format_text[0] != '.' or '/' in format_text:
                errors.append('That\'s not a valid extension.')
            
            if errors:
                self.display_errors(errors)
            else:
                return True

    def display_errors(self, errors):
        body = []
        big_text = urwid.BigText("Error!", urwid.HalfBlock5x4Font())
        big_text = urwid.Padding(big_text, 'center', None)
        body.append(big_text)
        body.append(urwid.Text(u'\n'))

        for error in errors:
            the_error = urwid.Text(error)
            body.append(the_error)

        body.append(urwid.Text(u'\n\n'))

        go_back = urwid.Button(u'Go Back')
        urwid.connect_signal(go_back, 'click', self.back_to_new_format_display)
        body.append(go_back)

        self.main_widget.original_widget = urwid.Overlay(
            urwid.ListBox(urwid.SimpleListWalker(
                body)),
            urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                align='center', width=('relative', 100),
                valign='middle', height=('relative', 75),
                min_width=20, min_height=9)

    def back_to_main_display(self, button):
        self.main_widget.original_widget = self.main_display

    def back_to_opened_folder_display(self, button):
        self.main_widget.original_widget = self.opened_folder_display

    def back_to_new_format_display(self, button):
        self.main_widget.original_widget = self.new_format_display
     
    def _run(self):
        self.make_main_display()
        urwid.MainLoop(self.main_widget).run()

    def _make_new_folder(self, button):
        raise urwid.ExitMainLoop()

    def exit(self, button):
        raise urwid.ExitMainLoop()

c = ConfigView(data)
