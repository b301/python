# lingui_navigation_sys.py
#
# __name__ >> b301
# __date__ >> 2.4.22
# __student__ >> b406
#
# todo:
#


import tkinter


BUTTON_HEIGHT = 50
BUTTON_WIDTH = 130
BUTTONS = []


def main() -> None:
    root = tkinter.Tk()

    # call the delete_buttons() and then create_buttons() after a cd ...
    # create the buttons [based at ~ (f"/home/{USER}")

    # change directory >> delete_buttons(), change the directory, ls and then call ls_to_list() on the
    # output. then call create_buttons on the frame, files
    # should be good to go from here :D
    #
    # when you click on a file, you should call cat on the file and read it, redirect the output to
    # read_file() which will open a popup window with the contents.

    root.mainloop()


def create_buttons(master: tkinter.Frame, ls: str) -> None:
    global BUTTONS
    delete_buttons(BUTTONS)
    _FILE_ICON = tkinter.PhotoImage(file=".\\file.ico")
    _DIRECTORY_ICON = tkinter.PhotoImage(file=".\\directory.ico")
    FILE_ICON = _FILE_ICON.subsample(3, 3)
    DIRECTORY_ICON = _DIRECTORY_ICON.subsample(3, 3)

    # todo: fix the parameter to the output of a ls -la after a cd 
    _files = ls_to_list(ls)

    buttons = []
    x = 0
    y = 0
    for directory_name, type, perm in _files:
        if type == 'd':
            directory_button = tkinter.Button(master=master, image=DIRECTORY_ICON,
             text=directory_name,command=lambda x = directory_name: print(x),
              width=BUTTON_WIDTH, height=BUTTON_HEIGHT, fg="purple", compound="top")
            directory_button.image = DIRECTORY_ICON
        else:
            directory_button = tkinter.Button(master=master, image=FILE_ICON,
             text=directory_name, command=lambda x = directory_name: read_file(master, x),
              width=BUTTON_WIDTH, height=BUTTON_HEIGHT, fg="red", compound="top")
            directory_button.image = FILE_ICON
        directory_button.place(x=1.05*x, y=1.1*y)
        
        x += BUTTON_WIDTH
        if x == 6 * BUTTON_WIDTH:
            x = 0
            y += BUTTON_HEIGHT

        buttons.append(directory_button)
    
    BUTTONS = buttons
    return


def delete_buttons(buttons: list) -> None:
    for button in buttons:
        button.destroy()

    return


def ls_to_list(ls: str) -> list:
    files = ls.split('\n')[1:]

    _files = []
    for file in files:
        attributes = file.split()
        if 'd' in attributes[0]:
            _files.append((attributes[-1], 'd', True if attributes[0][7] == 'r' else False))
        else:
            _files.append((attributes[-1], 'f', True if attributes[0][7] == 'r' else False))

    return _files


def read_file(master: tkinter.Tk, title: str, content: str) -> None:
    _POP_WIDTH = 1080
    _POP_HEIGHT = 720

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
