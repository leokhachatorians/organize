import urwid
from .opened_folder import OpenedFolderView
from .base import BaseView

class FoldersView(BaseView):
    def __init__(self, main_widget):
        super(FoldersView, self).__init__()
        self.main_widget = main_widget
        self.open_config()

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
            urwid.connect_signal(button, 'click', self.verify_delete_folder)
            body.append(urwid.AttrMap(button, None, focus_map='delete'))

        body.append(urwid.Divider())

        cancel = urwid.Button(u'Cancel')
        urwid.connect_signal(cancel, 'click', self.back_to_main_display)
        body.append(urwid.AttrMap(cancel, None, focus_map='selected'))

        self.main_widget.original_widget = urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def verify_delete_folder(self, button):
        self.folder_to_delete = button.get_label()
        text = urwid.Text(u'Delete folder <{}>?'.format(self.folder_to_delete))

        delete = urwid.Button(u'Delete')
        urwid.connect_signal(delete, 'click', self.delete_folder)

        cancel = urwid.Button(u'Cancel')
        urwid.connect_signal(cancel, 'click', self.back_to_main_display)

        body = [text,
                urwid.Divider(),
                urwid.AttrMap(delete, None, focus_map='delete'),
                urwid.AttrMap(cancel, None, focus_map='selected')]

        self.main_widget.original_widget = urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def delete_folder(self, button):
        self.data.pop(self.folder_to_delete, None)

        self.save_config()
        self.make_main_display()
        self.back_to_main_display()
