import urwid
from .base import BaseView
from .closed_folders import FoldersView

class MainDisplay(BaseView):
    def __init__(self):
        super(MainDisplay, self).__init__()
        self.open_config()
        self.palette = [
            ('selected', 'white', 'dark blue'),
            ('save', 'white', 'dark green'),
            ('delete', 'white', 'dark red'),
            ('error', 'default, bold', 'dark red', 'black')]

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

    def run(self):
        self.make_intro_display()
        self.main_loop = urwid.MainLoop(self.main_widget, self.palette)
        self.main_loop.run()

    def main_display(self, button):
        self.folders = FoldersView(self.main_widget)
        self.folders.make_main_display()
