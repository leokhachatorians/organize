import urwid
import json

class ConfigView():
    def __init__(self):
        self._open_config()
        self._run()

    def _open_config(self):
        with open('config.json') as config_file:
            self.data = json.load(config_file)

    def make_main_display(self, button=None):
        body = []
        body.append(urwid.Text(u'Folders'))

        for a_folder in self.data:
            folder_button = urwid.Button(a_folder)
            urwid.connect_signal(folder_button, 'click', self.make_open_folder_display)
            body.append(folder_button)
            body.append(urwid.Divider())

        new_folder =  urwid.Button(u'New Folder')
        urwid.connect_signal(new_folder, 'click', self.make_new_folder_display)

        delete_folder = urwid.Button(u'Delete Folder')
        urwid.connect_signal(delete_folder, 'click', self.delete_folder_display)

        exit_button = urwid.Button(u'Exit')
        urwid.connect_signal(exit_button, 'click', self.exit)
        
        body.append(urwid.Divider())
        body.append(new_folder)
        body.append(delete_folder)
        body.append(exit_button)

        self.top = urwid.ListBox(urwid.SimpleFocusListWalker(body))
        self.main_widget = urwid.Padding(self.top, left=0, right=0)
        self.main_display = self.main_widget.original_widget

    def make_new_folder_display(self, button):
        text = urwid.Text(u'Make a New Folder')

        self.new_folder = urwid.Edit(u'Folder Name: ')
        
        save = urwid.Button(u'Save Folder')
        urwid.connect_signal(save, 'click', self.on_save_folder_click)

        cancel = urwid.Button(u'Cancel')
        urwid.connect_signal(cancel, 'click', self.back_to_main_display)

        body = [text,
                urwid.Divider(),
                self.new_folder,
                urwid.Divider(),
                save,
                cancel]

        self.main_widget.original_widget = urwid.ListBox(urwid.SimpleListWalker(body))

    def on_save_folder_click(self, button):
        if self.check_if_valid_folder():
            self.ask_to_save_folder()

    def check_if_valid_folder(self):
        errors = []
        folder_text = self.new_folder.get_edit_text()

        if len(folder_text) < 1:
            errors.append('You need to enter something')
            self.display_errors(errors)
        else:
            if any(char in folder_text for char in ['\0', '/']):
                errors.append('Invalid characters in folder name')

            if errors:
                self.display_errors(errors, folder=True)
            else:
                return True

    def ask_to_save_folder(self):
        text = urwid.Text('Create new folder <{0}>?'.format(
            self.new_folder.get_edit_text()))

        yes = urwid.Button(u'Yes')
        urwid.connect_signal(yes,'click', self.save_folder)
        
        cancel = urwid.Button(u'Cancel')
        urwid.connect_signal(cancel, 'click', self.back_to_main_display)

        body = [text,
                yes,
                cancel]

        self.main_widget.original_widget = urwid.ListBox(urwid.SimpleListWalker(body))

    def save_folder(self, button):
        self.data[self.new_folder.get_edit_text()] = []
        self.save_config()
        self.main_widget.original_widget = self.main_display

    def delete_folder_display(self, button=None):
        body = []

        text = urwid.Text(u'Delete Folder')
        body.append(text)

        for folder in self.data:
            button = urwid.Button(folder)
            urwid.connect_signal(button, 'click', self.delete_folder)
            body.append(button)
        
        body.append(urwid.Divider())

        cancel = urwid.Button(u'Cancel')
        urwid.connect_signal(cancel, 'click', self.back_to_main_display)
        body.append(cancel)

        self.main_widget.original_widget = urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def delete_folder(self, button):
        folder = button.get_label()
        self.data.pop(folder, None)

        self.save_config()
        #self.make_main_display()
        self.update()
        #self.back_to_main_display()
        #self.delete_folder_display()
        self.make_main_display()
        self.back_to_main_display()

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

    def display_errors(self, errors, folder=False):
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
        if folder:
            urwid.connect_signal(go_back, 'click', self.back_to_main_display)
        else:
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
        self.main_loop = urwid.MainLoop(self.main_widget)
        self.main_loop.run()

    def update(self):
        self.main_loop.draw_screen()

    def exit(self, button):
        raise urwid.ExitMainLoop()

c = ConfigView()
