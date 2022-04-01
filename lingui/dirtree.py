import tkinter


DIRECTORIES = ["/home", "/var", "/bin", "/root", "/etc", "/usr"]


def main() -> None:
    root = tkinter.Tk()

    buttons = create_buttons(root, DIRECTORIES)

    tkinter.Button(master=root, text="Delete all...", command=lambda x = buttons: delete_buttons(x)).pack()

    root.mainloop()


def create_buttons(master: tkinter.Frame, directories: list) -> list:
    buttons = []
    for directory_name in directories:
        directory_button = tkinter.Button(master=master, text=directory_name, command=lambda x = directory_name: print(x))
        directory_button.pack()
        buttons.append(directory_button)
    
    print(">>> Created Buttons")
    return buttons


def delete_buttons(buttons: list) -> None:
    for button in buttons:
        print("beep")
        button.destroy()
        print("bop")

    print(">>> Deleted buttons")
    return


if __name__ == "__main__":
    main()
