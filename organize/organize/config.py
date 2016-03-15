import urwid
import json
import pprint
    

def open_config():
    with open('config.json') as file:
        data = json.load(file)

    return data

def test():
    with open('config.json') as f:
        data = json.load(f)\
    
    for folder in data:
        print(folder)
        for items in data[folder]:
            print(items)


data = open_config()

def make(data):
    body = [urwid.Text(u'TEST'), urwid.Divider()]

    for _ in data:
        folder = urwid.Text(_)
        body.append(folder)
        for i in data[_]:
            a = urwid.Text(i)
            body.append(a)
        body.append(urwid.Divider())

    btn = urwid.Button(u'Exit')
    urwid.connect_signal(btn, 'click', exit_program)
    body.append(btn)
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def exit_program(button):
    raise urwid.ExitMainLoop()

main = urwid.Padding(make(data), left=2, right=2)
top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
    align='center', width=('relative', 60),
    valign='middle',height=('relative', 60),
    min_width=20, min_height=9)
urwid.MainLoop(top).run()
