import urwid
from .base import BaseView

class OpenedFolderView(BaseView):
    def __init__(self, opened_folder, main_widget, main_display):
        self.opened_folder = opened_folder
        self.main_widget = main_widget
        self.main_display = main_display
        self.open_config()

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
        self.opened_folder_display = self.main_widget.original_widget

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
            urwid.connect_signal(button, 'click', self.verify_delete_extension)
            body.append(urwid.AttrMap(button, None, focus_map='delete'))

        body.append(urwid.Divider())
        cancel = urwid.Button(u'Cancel')
        urwid.connect_signal(cancel, 'click', self.make_open_folder_display)
        body.append(urwid.AttrMap(cancel, None, focus_map='selected'))

        self.main_widget.original_widget = urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def verify_delete_extension(self, button):
        self.extension_to_delete = button.get_label()

        text = urwid.Text(u'Delete extension <{}>?'.format(
            self.extension_to_delete))

        delete = urwid.Button(u'Delete')
        urwid.connect_signal(delete, 'click', self.delete_extension)

        cancel = urwid.Button(u'Cancel')
        urwid.connect_signal(cancel, 'click', self.back_to_opened_folder_display)

        body = [text,
            urwid.Divider(),
            urwid.AttrMap(delete, None, focus_map='delete'),
            urwid.AttrMap(cancel, None, focus_map='selected')]

        self.main_widget.original_widget = urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def delete_extension(self, button):
        self.data[self.opened_folder].remove(self.extension_to_delete)

        self.save_config()
        self.back_to_main_display()
