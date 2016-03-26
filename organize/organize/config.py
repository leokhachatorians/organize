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

    def _open_config(self):
        with open('config.json') as config_file:
            self.data = json.load(config_file)

    def back_to_main_display(self, button=None):
        self.main_widget.original_widget = self.main_display

    def back_to_opened_folder_display(self, button):
        self.main_widget.original_widget = self.opened_folder_display

    def back_to_new_extension_display(self, button):
        self.main_widget.original_widget = self.new_extension_display

class MainDisplay(BaseView):
    def __init__(self):
        self._open_config()
        self.palette = [
            ('selected', 'white', 'dark blue'),
            ('save', 'white', 'dark green'),
            ('delete', 'white', 'dark red'),
            ('error', 'default, bold', 'dark red', 'black')]
        self._run()

    def make_intro_display(self):
        bigtext = urwid.BigText("Config", urwid.HalfBlock5x4Font())
        bigtext = urwid.Padding(bigtext, "center", None)

        text = urwid.Text('Customize how you want to organize your files')

        goto_main = urwid.Button(u'Customize')
        urwid.connect_signal(goto_main, 'click', self.main_display)

        exit = urwid.Button(u'Exit')
        urwid.connect_signal(exit, 'click', self.exit)

        body = [bigtext,
                urwid.Text(u'\n'),
                text,
                urwid.AttrMap(goto_main, None, focus_map='save'),
                urwid.AttrMap(exit, None, focus_map='selected')]

        self.top = urwid.ListBox(urwid.SimpleFocusListWalker(body))
        self.main_widget = urwid.Padding(self.top, left=0, right=0)
        self.intro_display = self.main_widget.original_widget

    def _run(self):
        self.make_intro_display()
        self.main_loop = urwid.MainLoop(self.main_widget, self.palette)
        self.main_loop.run()

    def main_display(self, button):
        self.folders = FoldersView(self.main_widget)
        self.folders.make_main_display()

class FoldersView(BaseView):
    def __init__(self, main_widget):
        self.main_widget = main_widget
        self._open_config()

    def create_opened_folder_instance(self, button):
        folder = button.get_label()
        self.opened_folder = OpenedFolderView(folder, self.main_widget, self.main_display)
        self.opened_folder.make_open_folder_display()

    def make_main_display(self, button=None):
        body = []
        body.append(urwid.Text(u'Folders'))

        for a_folder in self.data:
            folder_button = urwid.Button(a_folder)
            urwid.connect_signal(folder_button, 'click', self.create_opened_folder_instance)
            body.append(urwid.AttrMap(folder_button, None, focus_map='selected'))
            body.append(urwid.Divider())

        new_folder =  urwid.Button(u'New Folder')
        urwid.connect_signal(new_folder, 'click', self.make_new_folder_display)

        delete_folder = urwid.Button(u'Delete Folder')
        urwid.connect_signal(delete_folder, 'click', self.delete_folder_display)

        exit_button = urwid.Button(u'Exit')
        urwid.connect_signal(exit_button, 'click', self.exit)

        body.append(urwid.Divider())
        body.append(urwid.AttrMap(new_folder, None, focus_map='selected'))
        body.append(urwid.AttrMap(delete_folder, None, focus_map='selected'))
        body.append(urwid.AttrMap(exit_button, None, focus_map='selected'))

        self.main_widget.original_widget = urwid.ListBox(urwid.SimpleListWalker(body))
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
                urwid.AttrMap(save, None, focus_map='save'),
                urwid.AttrMap(cancel, None, focus_map='selected')]

        self.main_widget.original_widget = urwid.ListBox(urwid.SimpleListWalker(body))

    def on_save_folder_click(self, button):
        if self.check_if_valid_folder():
            self.ask_to_save_folder()

    def check_if_valid_folder(self):
        errors = []
        folder_text = self.new_folder.get_edit_text()

        if len(folder_text) < 1:
            errors.append('You need to enter something')
            self.display_errors(errors, folder=True)
        else:
            if any(char in folder_text for char in ['\0', '/']):
                errors.append('Invalid characters in folder name')

            try:
                if self.data[folder_text]:
                    errors.append('That folder name already exists')
            except:
                pass

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
                urwid.AttrMap(yes, None, focus_map='save'),
                urwid.AttrMap(cancel, None, focus_map='selected')]

        self.main_widget.original_widget = urwid.ListBox(urwid.SimpleListWalker(body))

    def save_folder(self, button):
        self.data[self.new_folder.get_edit_text()] = []
        self.save_config()
        self.make_main_display()
        self.back_to_main_display()

    def delete_folder_display(self, button=None):
        body = []

        text = urwid.Text(u'Delete Folder')
        body.append(text)

        for folder in self.data:
            button = urwid.Button(folder)
            urwid.connect_signal(button, 'click', self.delete_folder)
            body.append(urwid.AttrMap(button, None, focus_map='delete'))

        body.append(urwid.Divider())

        cancel = urwid.Button(u'Cancel')
        urwid.connect_signal(cancel, 'click', self.back_to_main_display)
        body.append(urwid.AttrMap(cancel, None, focus_map='selected'))

        self.main_widget.original_widget = urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def delete_folder(self, button):
        folder = button.get_label()
        self.data.pop(folder, None)

        self.save_config()
        self.make_main_display()
        self.back_to_main_display()

class OpenedFolderView(BaseView):
    def __init__(self, opened_folder, main_widget, main_display):
        self.opened_folder = opened_folder
        self.main_widget = main_widget
        self.main_display = main_display
        self._open_config()

    def make_open_folder_display(self, button=None):
        body = []
        body.append(urwid.Text(u'Folder: ' + self.opened_folder))

        for extensions in self.data[self.opened_folder]:
            body.append(urwid.Text(extensions))

        body.append(urwid.Divider())

        new_extension = urwid.Button(u'Add an Extension')
        urwid.connect_signal(new_extension, 'click', self.make_new_extension_display)
        
        body.append(urwid.AttrMap(new_extension, None, focus_map='selected'))

        delete = urwid.Button(u'Delete an Extension')
        urwid.connect_signal(delete, 'click', self.delete_extension_display)
        body.append(urwid.AttrMap(delete, None, focus_map='selected'))

        go_back = urwid.Button(u'Go Back')
        urwid.connect_signal(go_back, 'click', self.back_to_main_display)
        body.append(urwid.AttrMap(go_back, None, focus_map='selected'))

        self.main_widget.original_widget = urwid.ListBox(urwid.SimpleListWalker(body))
        self.opened_folder_display = self.main_widget

    def make_new_extension_display(self, button):
        text = urwid.Text(u'Add an extension to {}'.format(self.opened_folder))

        self.new_extension = urwid.Edit(u'Extension: ')

        save = urwid.Button(u'Save Excention')
        urwid.connect_signal(save, 'click', self.on_save_extension_click)

        go_back = urwid.Button(u'Go Back')
        urwid.connect_signal(go_back, 'click', self.make_open_folder_display)

        body = [text,
                self.new_extension,
                urwid.Divider(),
                urwid.AttrMap(save, None, focus_map='save'),
                urwid.AttrMap(go_back, None, focus_map='selected')]

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
                urwid.AttrMap(yes, None, focus_map='save'),
                urwid.AttrMap(cancel, None, focus_map='selected')]

        self.main_widget.original_widget = urwid.ListBox(urwid.SimpleListWalker(body))

    def save_extension_to_folder(self, button):
        self.data[self.opened_folder] += [self.new_extension.get_edit_text()]
        self.save_config()
        self.main_widget.original_widget = self.main_display

    def delete_extension_display(self, button):
        body = []

        text = urwid.Text(u'Delete Extension')
        body.append(text)
        body.append(urwid.Divider())

        folder = urwid.Text(self.opened_folder)
        body.append(folder)

        for extension in self.data[self.opened_folder]:
            button = urwid.Button(extension)
            urwid.connect_signal(button, 'click', self.delete_extension)
            body.append(urwid.AttrMap(button, None, focus_map='delete'))

        body.append(urwid.Divider())
        cancel = urwid.Button(u'Cancel')
        urwid.connect_signal(cancel, 'click', self.make_open_folder_display)
        body.append(urwid.AttrMap(cancel, None, focus_map='selected'))

        self.main_widget.original_widget = urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def delete_extension(self, button):
        extension = button.get_label()

        self.data[self.opened_folder].remove(extension)

        self.save_config()
        self.back_to_main_display()

a = MainDisplay()