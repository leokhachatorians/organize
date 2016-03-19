import urwid
import json
import pprint

class ConfigView():
    def __init__(self):
        self._open_config()
        self._run()

    def _open_config(self):
        with open('config.json') as config_file:
            self.data = json.load(config_file)

    def make_main_display(self):
        body = []
        body.append(urwid.Text(u'Folders'))
        body.append(urwid.Divider())

        new_folder_button =  urwid.Button(u'New Folder')
        urwid.connect_signal(new_folder_button, 'click', self._make_new_folder)

        exit_button = urwid.Button(u'Exit')
        urwid.connect_signal(exit_button, 'click', self.exit)
        
        body.append(urwid.Divider())
    
        for a_folder in self.data:
            folder_button = urwid.Button(a_folder)
            urwid.connect_signal(folder_button, 'click', self.make_open_folder_display)
            body.append(folder_button)
            body.append(urwid.Divider())

        body.append(urwid.Divider())
        body.append(new_folder_button)
        body.append(exit_button)

        self.top = urwid.ListBox(urwid.SimpleFocusListWalker(body))
        self.main_widget = urwid.Padding(self.top, left=0, right=0)
        self.main_display = self.main_widget.original_widget

    def make_open_folder_display(self, button):
        body = []
        self.opened_folder = button.get_label()
        body.append(urwid.Text('Folder: ' + self.opened_folder))

        for extensions in self.data[self.opened_folder]:
            body.append(urwid.Text(extensions))

        body.append(urwid.Divider())

        new_extension = urwid.Button(u'Add an Extension')
        urwid.connect_signal(new_extension, 'click', self.make_new_extension_display)
        body.append(new_extension)
        
        delete = urwid.Button(u'Delete an Extension')
        urwid.connect_signal(delete, 'click', self.delete_extension_display)
        body.append(delete)

        go_back = urwid.Button(u'Go Back')
        urwid.connect_signal(go_back, 'click', self.back_to_main_display)
        body.append(go_back)

        exit = urwid.Button(u'Exit')
        urwid.connect_signal(exit, 'click', self.exit)
        body.append(exit)

        self.main_widget.original_widget = urwid.ListBox(urwid.SimpleFocusListWalker(body))
        self.opened_folder_display = self.main_widget.original_widget

    def delete_extension_display(self, button):
        body = []

        text = urwid.Text(u'Delete Extension')
        body.append(text)

        folder = urwid.Text(self.opened_folder)
        body.append(folder)

        for extension in self.data[self.opened_folder]:
            button = urwid.Button(extension)
            urwid.connect_signal(button, 'click', self.delete_extension)
            body.append(button)

        body.append(urwid.Divider())
        cancel = urwid.Button(u'Cancel')
        urwid.connect_signal(cancel, 'click', self.back_to_opened_folder_display)
        body.append(cancel)

        self.main_widget.original_widget = urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def delete_extension(self, button):
        extension = button.get_label()

        self.data[self.opened_folder].remove(extension)

        self.save_config()
        self.back_to_main_display()

    def make_new_extension_display(self, button):
        text = urwid.Text(u'Add an extension to {}'.format(self.opened_folder))

        self.new_extension = urwid.Edit(u'Extension: ')

        save = urwid.Button(u'Save Excention')
        urwid.connect_signal(save, 'click', self.on_save_extension_click)

        go_back = urwid.Button(u'Go Back')
        urwid.connect_signal(go_back, 'click', self.back_to_opened_folder_display)

        body = [text,
                self.new_extension,
                save,
                go_back]
                
        self.main_widget.original_widget = urwid.ListBox(urwid.SimpleListWalker(body))
        self.new_extension_display = self.main_widget.original_widget

    def on_save_extension_click(self, button):
        if self.check_if_valid_extension():
            self.ask_to_save()

    def check_if_valid_extension(self):
        errors = []
        extension_text = self.new_extension.get_edit_text()

        if len(extension_text) <= 1:
            errors.append('You need to enter something')
            self.display_errors(errors)
        else:
            if extension_text[0] != '.' or '/' in extension_text:
                errors.append('That\'s not a valid extension.')
           
            if extension_text in self.data[self.opened_folder]:
                errors.append('That extension already exists in that folder')

            if errors:
                self.display_errors(errors)
            else:
                return True

    def ask_to_save(self):
        text = urwid.Text(u'Add extension <{0}> to <{1}> folder?'.format(
            self.new_extension.get_edit_text(),
            self.opened_folder))

        yes = urwid.Button(u'Yes')
        urwid.connect_signal(yes, 'click', self.save_extension_to_folder)

        cancel = urwid.Button(u'Cancel')
        urwid.connect_signal(cancel, 'click', self.back_to_new_extension_display)

        body = [text,
                yes,
                cancel]
    
        self.main_widget.original_widget = urwid.ListBox(urwid.SimpleListWalker(body))

    def save_extension_to_folder(self, button):
        self.data[self.opened_folder] += [self.new_extension.get_edit_text()]

        self.save_config()

        self.main_widget.original_widget = self.main_display

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
        urwid.connect_signal(go_back, 'click', self.back_to_new_extension_display)
        body.append(go_back)

        self.main_widget.original_widget = urwid.ListBox(urwid.SimpleListWalker(body))

    def save_config(self):
        with open('config.json', 'w') as data:
            json.dump(self.data, data)

    def back_to_main_display(self, button=None):
        self.main_widget.original_widget = self.main_display

    def back_to_opened_folder_display(self, button):
        self.main_widget.original_widget = self.opened_folder_display

    def back_to_new_extension_display(self, button):
        self.main_widget.original_widget = self.new_extension_display
     
    def _run(self):
        self.make_main_display()
        urwid.MainLoop(self.main_widget).run()

    def _make_new_folder(self, button):
        raise urwid.ExitMainLoop()

    def exit(self, button):
        raise urwid.ExitMainLoop()

c = ConfigView()
