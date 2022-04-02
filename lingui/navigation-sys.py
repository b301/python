# lingui_navigation_sys.py
#
# __name__ >> b301
# __date__ >> 2.4.22
# __student__ >> b406
#
# todo:
# frame to scroll in


import tkinter
from tkinter import messagebox


BUTTON_HEIGHT = 50
BUTTON_WIDTH = 130


def main() -> None:
    root = tkinter.Tk()

    buttons = create_buttons(root)

    tkinter.Button(master=root, text="Delete all...", command=lambda x = buttons: delete_buttons(x)).pack()

    root.mainloop()


def create_buttons(master: tkinter.Frame) -> list:
    _FILE_ICON = tkinter.PhotoImage(file=".\\file.ico")
    _DIRECTORY_ICON = tkinter.PhotoImage(file=".\\directory.ico")
    FILE_ICON = _FILE_ICON.subsample(3, 3)
    DIRECTORY_ICON = _DIRECTORY_ICON.subsample(3, 3)

    with open(".\\ls.txt", 'r') as f:
        data = f.read()
        directories = ls_to_list(data)
    
    buttons = []
    x = 0
    y = 0
    for directory_name, type in directories:
        if type == 'd':
            directory_button = tkinter.Button(master=master, image=DIRECTORY_ICON, text=directory_name,command=lambda x = directory_name: print(x),
             width=BUTTON_WIDTH, height=BUTTON_HEIGHT, fg="green", compound="top")
            directory_button.image = DIRECTORY_ICON
        else:
            directory_button = tkinter.Button(master=master, image=FILE_ICON, text=directory_name, command=lambda x = directory_name: read_file(master,x),
             width=BUTTON_WIDTH, height=BUTTON_HEIGHT, fg="black", compound="top")
            directory_button.image = FILE_ICON
        directory_button.place(x=1.3*x, y=1.3*y)
        
        x += BUTTON_WIDTH
        if x == 4 * BUTTON_WIDTH:
            x = 0
            y += BUTTON_HEIGHT

        buttons.append(directory_button)
    
    print("APP >>> Created Buttons")
    return buttons


def delete_buttons(buttons: list) -> None:
    for button in buttons:
        button.destroy()

    print("APP >>> Deleted buttons")
    return


def ls_to_list(ls: str) -> list:
    files = ls.split('\n')[1:]

    _files = []
    for file in files:
        attributes = file.split()
        if 'd' in attributes[0]:
            _files.append((attributes[-1], 'd'))
        else:
            _files.append((attributes[-1], 'f'))

    return _files


def read_file(master: tkinter.Tk, title: str, content: str) -> None:
    _POP_WIDTH = 400
    _POP_HEIGHT = 600
    
    pop_up = tkinter.Toplevel(master)
    pop_up.geometry(f"{_POP_WIDTH}x{_POP_HEIGHT}")
    pop_up.title(title)
    pop_up.resizable(False, False)

    text = tkinter.Text(pop_up, width=_POP_WIDTH, height=_POP_HEIGHT)
    text.insert(tkinter.END, content)
    text.config(state="disabled")
    text.pack()

    return


if __name__ == "__main__":
    main()
