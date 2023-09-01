import tkinter as tk
import tkinter.ttk as ttk
from tkinter.font import Font
import tkinter.filedialog as fd
import os
import logic
from typing import Optional
import tkinter.messagebox as msgbox
import shutil

program_title = "Save My Save"
target_options = {
            "sav 문자열 포함": ".*sav.*",
            "*.rpgsave": ".*[.]rpgsave$",
            "*.rvdata": ".*[.]rvdata$",
            "*.rvdata2": ".*[.]rvdata2$",
            "모든 파일": ".*",
            "확장자 직접 입력...": None
        }

class Gui:
    def _make_top_frame(self):
        top_frame = tk.Frame(self.mf)
        top_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        padding = 3

        tk.Label(top_frame, text="타겟 폴더: ").grid(row=0, column=0, pady=padding)
        self.target_directory_path_var = tk.StringVar()
        self.target_directory_path_var.set("선택되지 않음.")
        self.target_dir_entry = tk.Entry(
            top_frame, textvariable=self.target_directory_path_var,
            width=22, state='readonly', readonlybackground='#d7d7d7'
        )
        self.target_dir_entry.grid(row=0, column=1, pady=padding)
        tk.Button(
            top_frame, text="찾아보기...", font=Font(family='돋움', size=9), command=self.controller.set_target_directory
        ).grid(row=0, column=2, padx=3, pady=padding)

        tk.Label(top_frame, text="백업 폴더: ").grid(row=1, column=0, pady=padding)
        self.backup_path_var = tk.StringVar()
        self.backup_path_var.set("타겟 폴더/backup")
        self.backup_dir_entry = tk.Entry(
            top_frame, textvariable=self.backup_path_var,
            width=22, state='readonly', readonlybackground='#d7d7d7'
        )
        self.backup_dir_entry.grid(row=1, column=1, pady=padding)
        tk.Button(
            top_frame, text="찾아보기...", font=Font(family='돋움', size=9), command=self.controller.set_backup_directory
        ).grid(row=1, column=2, padx=3, pady=padding)

    def _do_popup(self, event=None):
        self.controller.auto_refresh()
        if not self.backuped_dir_listbox.get(0, tk.END):
            return
        self.backuped_dir_listbox.selection_clear(0, tk.END)
        self.backuped_dir_listbox.selection_set(self.backuped_dir_listbox.nearest(event.y))
        self.backuped_dir_listbox.activate(self.backuped_dir_listbox.nearest(event.y))
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.popup_menu.grab_release()

    def _make_left_frame(self):
        left_frame = tk.LabelFrame(self.mf, text='백업 버전 목록')
        left_frame.grid(row=1, column=0, sticky='ns', padx=5, pady=5)
        self.backuped_dir_listbox = tk.Listbox(left_frame, height=10, width=18)
        scrbar = tk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.backuped_dir_listbox.yview)
        self.backuped_dir_listbox.config(yscrollcommand=scrbar.set)
        self.popup_menu = tk.Menu(self.backuped_dir_listbox, tearoff=0)
        self.popup_menu.add_command(label="제거",
                                    command=lambda: self.controller.delete_version())
        self.backuped_dir_listbox.bind('<Button-1>', lambda event=None: self.controller.auto_refresh())
        self.backuped_dir_listbox.bind('<Button-3>', self._do_popup)
        scrbar.pack(side='right', fill='y')
        self.backuped_dir_listbox.pack(side='left', expand=True, fill='both')

    def _make_right_frame(self):
        right_frame = tk.Frame(self.mf)
        right_frame.grid(row=1, column=1, sticky='nsw', padx=5, pady=5)

        state_frame = tk.Frame(right_frame, pady=5)
        state_frame.grid(row=0, column=0, sticky='ew')

        self.state_message_var = tk.StringVar()
        self.state_message_var.set("로드되지 않음")
        tk.Label(
            state_frame, textvariable=self.state_message_var, font=Font(family='맑은 고딕', size=10)
        ).pack(fill='x', side='left')

        self.target_option_combobox = ttk.Combobox(right_frame, width=15, state='readonly', height=8)
        self.target_option_combobox.grid(row=1, column=0, sticky='w')

        def combobox_command(event=None):
            self.controller.set_target_option()

        self.target_option_combobox.bind('<<ComboboxSelected>>', combobox_command)

        tk.Frame(right_frame, height=7).grid(row=2, column=0)
        mini_frame = tk.Frame(right_frame)
        mini_frame.grid(row=3, column=0, sticky='ew')
        font = Font(family='돋움', size=9)
        self.which_file_button = tk.Button(
            mini_frame, text='파일 확인', command=self.controller.show_target_files, bg='#cc6', font=font
        )
        self.which_file_button.grid(row=3, column=0, sticky='w')
        tk.Frame(mini_frame, width=2).grid(row=3, column=1)
        self.which_file_button = tk.Button(
            mini_frame, text='폴더 열기', command=self.controller.open_dir, bg='#99f', font=font
        )
        self.which_file_button.grid(row=3, column=2, sticky='w')

        ttk.Separator(right_frame, orient=tk.HORIZONTAL).grid(row=5, column=0, columnspan=2, sticky='ew', pady=7)

        font = Font(family="맑은 고딕", size=11)
        tk.Button(
            right_frame, text='롤백', width=8, font=font, bg='#cf9', command=self.controller.push_rollback_button
        ).grid(row=6, column=0)
        tk.Frame(right_frame, height=5).grid(row=7, column=0)
        tk.Button(
            right_frame, text='백업', width=8, font=font, bg='#f99', command=self.controller.push_backup_button
        ).grid(row=8, column=0)

    def which_directory(self):
        res = fd.askdirectory(parent=self.mf)
        self.mf.deiconify()
        return res

    def __init__(self):
        self.mf = tk.Tk()
        self.mf.title(program_title)
        self.mf.focus()
        self.icon = "icon.ico"
        self.mf.iconbitmap(self.icon)
        self.mf.geometry(
            "310x257+{}+{}".format(self.mf.winfo_screenwidth() // 2 - 155, self.mf.winfo_screenheight() // 2 - 160))
        self.mf.resizable(0, 0)
        self.controller = Contorller(self)
        self._make_top_frame()
        self._make_left_frame()
        self._make_right_frame()
        self.controller.insert_target_option_combobox_list()

    def _list_window(self, list, title: Optional[str] = None, message: Optional[str] = None):
        self.subwindow = tk.Toplevel(self.mf)
        self.subwindow.resizable(0, 0)
        self.subwindow.iconbitmap(self.icon)
        self.subwindow.grab_set()
        self.subwindow.focus()
        if title:
            self.subwindow.title(title)
        if message:
            tk.Label(self.subwindow, text=message).pack(side='top', anchor='w', fill='x', padx=4, pady=4)
        middle_frame = tk.Frame(self.subwindow, bd=5)
        middle_frame.pack(side='top', fill='both', expand=True)
        text = tk.Text(middle_frame, width=35, height=10)
        for idx, element in enumerate(list):
            text.insert(tk.END, element + '\n')
        text['state'] = 'disabled'
        scrbar = tk.Scrollbar(middle_frame, orient='vertical', command=text.yview)
        text['yscrollcommand'] = scrbar.set
        scrbar.pack(side='right', fill='y')
        text.pack(side='left', fill='both', expand=True)

        def destroy(event=None):
            self.subwindow.destroy()

        self.subwindow.bind('<Escape>', destroy)

    def show_list(self, list, title: Optional[str] = None, message: Optional[str] = None):
        self._list_window(list, title, message)
        bottom_frame = tk.Frame(self.subwindow, bd=5)
        bottom_frame.pack(side='bottom')
        tk.Button(bottom_frame, text='확인', width=10, command=self.subwindow.destroy).pack(pady=5)
        self.subwindow.update()
        w, h = self.subwindow.winfo_width(), self.subwindow.winfo_height()
        self.subwindow.geometry("{}x{}+{}+{}".format(w, h, self.mf.winfo_x() + 20, self.mf.winfo_y() + 30))

        def when_enter(event=None):
            self.subwindow.destroy()

        self.subwindow.bind('<Return>', when_enter)
        self.subwindow.mainloop()

    def ask_for_try_backup(self, list, auto_name: str, title: Optional[str] = None, message: Optional[str] = None):
        self._list_window(list, title, message)
        entry_frame = tk.Frame(self.subwindow, bd=5)
        entry_frame.pack(side='top', fill='x')
        self.version_directroy_name_var = tk.StringVar()
        self.version_directroy_name_var.set(auto_name)
        tk.Label(entry_frame, text="백업폴더:").pack(side='left')
        tk.Entry(
            entry_frame, textvariable=self.version_directroy_name_var
        ).pack(side='right', fill='x', expand=True, padx=3)
        bottom_frame = tk.Frame(self.subwindow, bd=5)
        bottom_frame.pack(side='bottom')
        tk.Button(
            bottom_frame, text='백업 진행', bg='#f99', width=10,
            command=self.controller.backup
        ).pack(side='left', padx=5)
        tk.Button(bottom_frame, text='취소', width=10, command=self.subwindow.destroy).pack(side='right', padx=5)
        self.subwindow.update()
        w, h = self.subwindow.winfo_width(), self.subwindow.winfo_height()
        self.subwindow.geometry("{}x{}+{}+{}".format(w, h, self.mf.winfo_x() + 20, self.mf.winfo_y() + 30))

        def when_enter(event=None):
            self.controller.backup()

        self.subwindow.bind('<Return>', when_enter)
        self.subwindow.mainloop()

    def ask_rollback(self, title: Optional[str], src, dst, backup_version_name):
        self.subwindow = tk.Toplevel(self.mf)
        self.subwindow.iconbitmap(self.icon)
        self.subwindow.grab_set()
        self.subwindow.focus()

        if title:
            self.subwindow.title(title)
        window_frame = tk.Frame(self.subwindow, width=20, height=10, bd=8)
        window_frame.pack(fill='both')
        message_frame = tk.Frame(window_frame, width=20, height=10, bd=8)
        message_frame.pack(fill='x')
        font = Font(family='맑은 고딕', size=10, weight='bold')
        tk.Label(message_frame, text=src, font=font, fg='#00f').pack(side='left')
        tk.Label(message_frame, text='의 파일들을 ', font=font).pack(side='left')
        tk.Label(message_frame, text=dst, font=font, fg='#f0f').pack(side='left')
        tk.Label(message_frame, text='에 덮어씁니다.', font=font).pack(side='left')
        self.auto_backup_var = tk.BooleanVar()
        self.auto_backup_var.set(False)
        tk.Checkbutton(
            window_frame, text='현재 파일들을 {}에 백업하기'.format(backup_version_name),
            font=Font(family='맑은 고딕', size=9), variable=self.auto_backup_var
        ).pack(side='top', pady=5, padx=5)
        button_frame = tk.Frame(window_frame)
        button_frame.pack(side='bottom', pady=5)
        tk.Button(
            button_frame, text='롤백하기', width=8, bg='#cf9', command=self.controller.rollback
        ).pack(side='left', anchor='e', padx=4)
        tk.Button(button_frame, text='취소', width=8, command=self.subwindow.destroy).pack(side='right', anchor='w',
                                                                                         padx=4)
        self.subwindow.update()
        w, h = self.subwindow.winfo_width(), self.subwindow.winfo_height()
        self.subwindow.geometry("{}x{}+{}+{}".format(w, h, self.mf.winfo_x() + 20, self.mf.winfo_y() + 50))

        def when_enter(event=None):
            self.controller.rollback()

        def destroy(event=None):
            self.subwindow.destroy()

        self.subwindow.bind('<Return>', when_enter)
        self.subwindow.bind('<Escape>', destroy)

        self.subwindow.mainloop()

    def _set_extension(self):
        self.exist_extension = True

    def show_extension_entry(self):
        self.subwindow = tk.Toplevel(self.mf)
        self.subwindow.iconbitmap(self.icon)
        self.subwindow.grab_set()
        self.subwindow.focus()
        self.subwindow.title("확장자 직접 입력")
        window_frame = tk.Frame(self.subwindow, width=20, height=10, bd=8)
        window_frame.pack(fill='both')
        tk.Label(window_frame, text="확장자:").grid(row=0, column=0)
        self.extension_var = tk.StringVar()
        tk.Entry(window_frame, textvariable=self.extension_var).grid(row=0, column=1)
        button_frame = tk.Frame(window_frame, bd=5)
        button_frame.grid(row=1, column=0, columnspan=2)

        def ok(self):
            self.controller.set_custom_extension(self.extension_var.get())
            self.subwindow.destroy()

        def window_exit(self):
            self.target_option_combobox.current(0)
            self.subwindow.destroy()

        self.subwindow.protocol("WM_DELETE_WINDOW", lambda: window_exit(self))
        tk.Button(
            button_frame, text='확인', width=8, bg='#fcc', command=lambda: ok(self)
        ).pack(side='left', anchor='e', padx=4)
        tk.Button(
            button_frame, text='취소', width=8, command=lambda: window_exit(self)
        ).pack(side='right', anchor='w', padx=4)
        self.subwindow.bind('<Return>', lambda event=None: ok(self))
        self.subwindow.bind('<Escape>', lambda event=None: window_exit(self))

        self.subwindow.update()
        w, h = self.subwindow.winfo_width(), self.subwindow.winfo_height()
        self.subwindow.geometry("{}x{}+{}+{}".format(w, h, self.mf.winfo_x() + 40, self.mf.winfo_y() + 80))
        self.subwindow.mainloop()

    def renew_backup_directory_list(self, dir_list):
        self.dir_list = dir_list
        self.backuped_dir_listbox.delete(0, tk.END)
        for directory in self.dir_list:
            self.backuped_dir_listbox.insert(tk.END, directory)
        self.backuped_dir_listbox.see(tk.END)
        self.state_message_var.set(f"백업 개수: {len(dir_list)}개")

    def set_target_option_combobox_list(self, option_list):
        self.target_option_combobox.config(values=option_list)
        self.target_option_combobox.current(0)

    def mainloop(self):
        self.mf.mainloop()


class Contorller:
    def __init__(self, gui: Gui):
        self.gui = gui
        self.logic = None
        self.target_options = target_options

    def insert_target_option_combobox_list(self):
        self.gui.set_target_option_combobox_list(list(self.target_options.keys()))

    def set_target_directory(self):
        target_directory = self.gui.which_directory()
        if not target_directory:
            return
        target_directory = os.path.abspath(target_directory)
        self.gui.target_directory_path_var.set(target_directory)
        self.gui.target_dir_entry.xview_moveto(1)
        if not os.path.isdir(self.gui.backup_path_var.get()):
            self.gui.backup_path_var.set(os.path.join(target_directory, 'backup'))
            self.gui.backup_dir_entry.xview_moveto(1)
        backup_directory = self.gui.backup_path_var.get()

        self.logic = logic.Logic(
            name_format=self.target_options[self.gui.target_option_combobox.get()],
            target_dir_path=target_directory,
            backup_dir_path=backup_directory
        )

        self.gui.renew_backup_directory_list(self.logic.load_backup_directories())

    def set_backup_directory(self):
        backup_directory = self.gui.which_directory()
        if not backup_directory:
            return
        backup_directory = os.path.abspath(backup_directory)
        self.gui.backup_path_var.set(backup_directory)
        self.gui.backup_dir_entry.xview_moveto(1)
        target_directory = self.gui.target_directory_path_var.get()
        if not os.path.isdir(target_directory):
            return

        self.logic = logic.Logic(
            name_format=self.target_options[self.gui.target_option_combobox.get()],
            target_dir_path=target_directory,
            backup_dir_path=backup_directory
        )

        self.gui.renew_backup_directory_list(self.logic.load_backup_directories())

    def set_target_option(self):
        if not self.logic:
            msgbox.showinfo("알림", "먼저 타겟 폴더를 설정하세요")
            self.gui.target_option_combobox.current(0)
            return
        try:
            name_format = self.target_options[self.gui.target_option_combobox.get()]
        except:
            name_format = None
        if name_format is None:
            self.gui.show_extension_entry()
            return

        target_directory = self.gui.target_directory_path_var.get()
        backup_directory = self.gui.backup_path_var.get()

        self.logic = logic.Logic(
            name_format=name_format,
            target_dir_path=target_directory,
            backup_dir_path=backup_directory
        )

    def set_custom_extension(self, custom_extension):
        if custom_extension:
            try:
                print(custom_extension)
                if '.' in custom_extension:
                    extension = custom_extension.split('.', maxsplit=1)[1]
                else:
                    extension = custom_extension
                name_format = f".*[.]{extension}$"
                self.gui.target_option_combobox.set(f"*.{extension}")
            except:
                msgbox.showerror("오류 발생", "오류가 발생했습니다.")
                self.gui.target_option_combobox.current(0)
                return
        else:
            self.gui.target_option_combobox.current(0)
            return

        print("설정 완료")
        target_directory = self.gui.target_directory_path_var.get()
        backup_directory = self.gui.backup_path_var.get()

        self.logic = logic.Logic(
            name_format=name_format,
            target_dir_path=target_directory,
            backup_dir_path=backup_directory
        )

    def show_target_files(self):
        if self.logic:
            self.gui.show_list(
                self.logic.target_list(),
                "백업 대상 파일", f"\"{self.gui.target_option_combobox.get()}\"은 아래를 포함합니다.", )
        else:
            msgbox.showinfo("알림", "먼저 타겟 폴더를 설정하세요")

    def push_backup_button(self):
        if self.logic:
            self.gui.ask_for_try_backup(self.logic.target_list(), self.logic.get_auto_version_directory_name(),
                                        "백업 확인", "아래의 파일들을 백업하시겠습니까?")
        else:
            msgbox.showinfo("알림", "먼저 타겟 폴더를 설정하세요")

    def push_rollback_button(self):
        listbox_value = self.get_listbox_value()
        if listbox_value:
            self.gui.ask_rollback("롤백 안내", listbox_value,
                                  os.path.basename(self.gui.target_directory_path_var.get()),
                                  self.logic.get_auto_version_directory_name())
        elif self.logic:
            msgbox.showinfo("알림", "목록에서 버전을 선택해주세요.")
        else:
            msgbox.showinfo("알림", "먼저 타겟 폴더를 설정하세요")

    def backup(self):
        self.gui.subwindow.destroy()
        if self.logic.backup(dir_name=self.gui.version_directroy_name_var.get()):
            msgbox.showinfo("성공", f"{self.gui.version_directroy_name_var.get()}에 백업을 완료하였습니다.")
        else:
            msgbox.showerror("오류", "백업을 실패하였습니다.")

        self.gui.renew_backup_directory_list(self.logic.load_backup_directories())

    def rollback(self):
        self.gui.subwindow.destroy()
        message = f"{self.gui.target_option_combobox.get()}의 파일들을 롤백하였습니다."
        if self.gui.auto_backup_var.get():
            if not self.logic.backup(dir_name=self.logic.get_auto_version_directory_name()):
                msgbox.showerror("오류", "롤백 과정중 백업 실패하였습니다.")
            else:
                message = f"백업 후 {self.gui.target_option_combobox.get()}의 파일들을 롤백하였습니다."
        if self.logic.rollback(self.gui.backuped_dir_listbox.get(self.gui.backuped_dir_listbox.curselection()[0])):
            msgbox.showinfo("성공", message)
        else:
            msgbox.showerror("오류", "롤백을 실패하였습니다.")

        self.gui.renew_backup_directory_list(self.logic.load_backup_directories())

    def get_listbox_value(self):
        selected_idx_tuple = self.gui.backuped_dir_listbox.curselection()
        if selected_idx_tuple:
            idx = selected_idx_tuple[0]
            return self.gui.backuped_dir_listbox.get(idx, idx)[0]
        else:
            return None

    def delete_version(self):
        dir_name = self.get_listbox_value()
        if dir_name:
            if msgbox.askyesno("제거 확인", f"{dir_name}을 제거하시겠습니까?"):
                shutil.rmtree(os.path.join(self.gui.backup_path_var.get(), dir_name))
                self.gui.renew_backup_directory_list(self.logic.load_backup_directories())
        else:
            msgbox.showinfo("알림", "버전을 선택하세요")

    def open_dir(self):
        if self.logic:
            dir_name = self.gui.backup_dir_entry.get()
            try:
                os.startfile(dir_name)
            except FileNotFoundError:
                pass
        else:
            msgbox.showinfo("알림", "먼저 타겟 폴더를 설정하세요")

    def auto_refresh(self):
        if self.logic:
            self.gui.renew_backup_directory_list(self.logic.load_backup_directories())


if __name__ == '__main__':
    a = Gui()
    a.mainloop()
