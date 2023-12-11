import ttkbootstrap as ttk
from tkinter import filedialog
import os
import subprocess


class auto_pyinstaller:
    def __init__(self, root):
        self.root = root
        self.folder_var, self.icon_file_var, self.name_file_var, self.file_top_path, self.file_name = ttk.StringVar(), ttk.StringVar(), ttk.StringVar(), ttk.StringVar(), ttk.StringVar()
        self.name_var, self.icon_var = ttk.BooleanVar(), ttk.BooleanVar()
        self.run_window_var, self.clear_file_var = ttk.BooleanVar(), ttk.BooleanVar()
        self.command_display_var = ttk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        # 主框架
        tab = ttk.Frame(self.root, width=750, height=520)
        tab.pack_propagate(False)
        tab.pack()
        # 顶层框架
        title_frame = ttk.Frame(tab, width=700, height=60)
        title_frame.pack_propagate(False)
        title = ttk.Label(title_frame, text='Auto-Pyinstaller', font=('Arial', 22, "bold"), foreground='Blue')
        dividing_line1 = ttk.Separator(title_frame, bootstyle="primary")
        title_frame.pack(pady=10), title.pack(anchor='w'), dividing_line1.pack(fill='x', pady=5)
        # 子框架1
        child1_frame = ttk.Frame(tab, width=700, height=100)
        child1_frame.grid_propagate(False)
        child1_frame.pack()
        file_url = ttk.Label(child1_frame, text='打包文件', bootstyle="primary")
        file_path = ttk.Entry(child1_frame, width=50, textvariable=self.folder_var, state="readonly", bootstyle="primary")
        file_open_path = ttk.Button(child1_frame, text='Browse', command=lambda: self.open_file_input("0"), width=10, takefocus=False)
        file_url.grid(row=0, column=0, padx=5, pady=5), file_path.grid(row=0, column=1, padx=5), file_open_path.grid(row=0, column=2, padx=15)
        file_format = ttk.Label(child1_frame, text='生成格式', bootstyle="primary")
        file_format.grid(row=1, column=0, padx=5, pady=5)
        open_file_button = ttk.Button(child1_frame, text='Open File', command=self.open_input, width=10, takefocus=False)
        self.combobox = ttk.Combobox(child1_frame, values=["one_file", "one_dir"], state="readonly", bootstyle="primary")
        self.combobox.current(0), self.mouse()
        self.combobox.grid(row=1, column=1, padx=5, pady=5, sticky='nsew'), open_file_button.grid(row=1, column=2, padx=15)
        # 子框架2
        child2_frame = ttk.Frame(tab, width=700, height=100)
        child2_frame.grid_propagate(False)
        child2_frame.pack()
        icon_frame = ttk.Frame(child2_frame, width=700, height=40)
        name_frame = ttk.Frame(child2_frame, width=700, height=40)
        icon_frame.grid_propagate(False), name_frame.grid_propagate(False)
        icon_frame.grid(row=0), name_frame.grid(row=1)
        icon = ttk.Label(icon_frame, text='图标', bootstyle="primary")
        icon_button = ttk.Checkbutton(icon_frame, variable=self.icon_var, command=self.icon_frame_display, bootstyle="success-square-toggle")
        self.icon_entry = ttk.Entry(icon_frame, width=44, textvariable=self.icon_file_var, state="readonly", bootstyle="primary")
        self.icon_open_path = ttk.Button(icon_frame, text='Browse', command=lambda: self.open_file_input("1"), width=10, takefocus=False)
        icon.grid(row=0, column=0, padx=20, pady=5), icon_button.grid(row=0, column=1, padx=5)
        name = ttk.Label(name_frame, text='名称', bootstyle="primary")
        name_button = ttk.Checkbutton(name_frame, variable=self.name_var, command=self.name_frame_display, bootstyle="success-square-toggle")
        self.name_entry = ttk.Entry(name_frame, width=44, bootstyle="primary")
        self.name_open = ttk.Button(name_frame, text='ok', command=lambda: self.command_display_var.set(self.command_display.get()+' -n '+self.name_entry.get()) if '-n' not in self.command_display.get() else None, width=10, takefocus=False)
        name.grid(row=0, column=0, padx=20, pady=5), name_button.grid(row=0, column=1, padx=5)
        # 子框架3
        child3_frame = ttk.Frame(tab, width=700, height=60)
        child3_1_frame = ttk.Frame(child3_frame, width=350, height=60)
        child3_2_frame = ttk.Frame(child3_frame, width=350, height=60)
        child3_frame.grid_propagate(False), child3_frame.pack(), child3_1_frame.grid_propagate(False), child3_2_frame.grid_propagate(False)
        run_command_window = ttk.Label(child3_1_frame, text='运行命令窗口', bootstyle="primary")
        run_window_button = ttk.Checkbutton(child3_1_frame, variable=self.run_window_var, command=self.add_command, bootstyle="success-square-toggle")
        child3_1_frame.grid(row=0, column=0, padx=20), run_command_window.grid(row=0, column=0, padx=20), run_window_button.grid(row=0, column=1)
        clear_superfluous_file = ttk.Label(child3_2_frame, text='清理多余文件', bootstyle="primary")
        clear_file_button = ttk.Checkbutton(child3_2_frame, variable=self.clear_file_var, bootstyle="success-square-toggle")
        child3_2_frame.grid(row=0, column=1), clear_superfluous_file.grid(row=0, column=2, padx=20), clear_file_button.grid(row=0, column=3)
        # 子框架4
        child4_frame = ttk.Frame(tab, width=700, height=80)
        child4_frame.pack_propagate(False)
        command_title = ttk.Label(child4_frame, text='Command', font=('Arial', 14, "bold"), foreground='light green')
        self.command_display = ttk.Entry(child4_frame, width=80, textvariable=self.command_display_var, state="readonly", bootstyle="primary")
        child4_frame.pack(), command_title.pack(anchor='w'), self.command_display.pack()
        # 执行
        child5_frame = ttk.Frame(tab, width=700, height=60)
        child5_frame.pack_propagate(False)
        run_command = ttk.Button(child5_frame, text="Run Command", command=self.open_cmd_window, width=12, takefocus=False)
        child5_frame.pack(pady=15), run_command.pack(side='right')

    def open_cmd_window(self):
        if self.clear_file_var.get():
            f = str(self.file_name)
            if '-n' in self.command_display.get():
                f = self.name_entry.get()
            remove = 'rd /s /q build&&del {}.spec'.format(os.path.splitext(f)[0])
            command = 'cd /d {}&&{}&&{}&&pause&&exit'.format(str(self.file_top_path), self.command_display.get(), remove)
        else:
            command = 'cd /d {}&&{}&&pause&&exit'.format(str(self.file_top_path), self.command_display.get())
        subprocess.run(['start', 'cmd', '/k', command], shell=True)

    def add_command(self):
        if self.run_window_var.get():
            if '-w' in self.command_display.get():
                self.command_display_var.set(self.command_display.get()[0:self.command_display.get().find(" -w")]+self.command_display.get()[self.command_display.get().find(" -w")+3:])
        else:
            if '-w' not in self.command_display.get():
                self.command_display_var.set(self.command_display.get()+' -w')

    def open_input(self):
        folder_path = os.path.abspath(str(self.file_top_path)+'/dist')
        if os.path.exists(folder_path):
            os.startfile(folder_path)

    def open_file_input(self, t):
        file_path = filedialog.askopenfilename()
        if file_path:
            if t == "0":
                self.file_top_path, self.file_name = os.path.split(file_path)
                file_format_dict = {"one_file": "-F", "one_dir": "-D"}
                file_format_option = file_format_dict[self.combobox.get()]
                self.folder_var.set(file_path), self.command_display_var.set('pyinstaller {} '.format(file_format_option)+self.file_name + ' -w')
            else:
                self.icon_file_var.set(file_path), self.icon_file_var.set(file_path)
                self.command_display_var.set(self.command_display.get()+' -i '+file_path) if '-i' not in self.command_display.get() else None

    def mouse(self):
        def disable_scroll(event):
            return "break"
        self.combobox.bind("<MouseWheel>", disable_scroll)

    def icon_frame_display(self):
        if self.icon_var.get():
            self.icon_entry.grid(row=0, column=2, padx=10)
            self.icon_open_path.grid(row=0, column=3, padx=10)
        else:
            self.icon_entry.grid_forget()  # 隐藏
            self.icon_open_path.grid_forget()
            if '-i' in self.command_display.get():
                self.command_display_var.set(self.command_display.get()[0:self.command_display.get().find("-i")])

    def name_frame_display(self):
        if self.name_var.get():
            self.name_entry.grid(row=0, column=2, padx=10)
            self.name_open.grid(row=0, column=3, padx=10)
        else:
            self.name_entry.grid_forget()  # 隐藏
            self.name_open.grid_forget()
            if '-n' in self.command_display.get():
                self.command_display_var.set(self.command_display.get()[0:self.command_display.get().find("-n")])


if __name__ == '__main__':
    root = ttk.Window(title='Auto Pyinstaller', themename='cosmo', size=(750, 520), position=(400, 250), resizable=None)
    app = auto_pyinstaller(root)
    root.mainloop()
