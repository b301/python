import tkinter
from tkinter import font


DIRECTORIES = ["/home", "/var", "/bin", "/root", "/etc", "/usr", "/averylongdirectoryname"]
BUTTON_HEIGHT = 2
BUTTON_WIDTH = 16


def main() -> None:
    root = tkinter.Tk()
    _font = font.Font(family="Fira Code", size=10)
    
    buttons = create_buttons(root, _font)

    tkinter.Button(master=root, text="Delete all...", command=lambda x = buttons: delete_buttons(x)).pack()

    root.mainloop()


def create_buttons(master: tkinter.Frame, _font: font.Font) -> list:
    directories = []
    
    buttons = []
    x = 0
    y = 0
    for directory_name, type in directories:
        if type == 'd':
            color = "green"
        else:
            color = "black"

        directory_button = tkinter.Button(master=master, text=directory_name, command=lambda x = directory_name: print(x), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, fg=color, font=_font)
        directory_button.place(x=8.5*x, y=28*y)
        
        x += BUTTON_WIDTH
        if x == 4 * BUTTON_WIDTH:
            x = 0
            y += BUTTON_HEIGHT

        buttons.append(directory_button)
    
    print(">>> Created Buttons")
    return buttons


def delete_buttons(buttons: list) -> None:
    for button in buttons:
        button.destroy()

    print(">>> Deleted buttons")
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


if __name__ == "__main__":
    main()
