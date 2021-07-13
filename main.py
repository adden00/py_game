import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
import sys


root = tk.Tk()
bg_color = 'azure'
root['bg'] = bg_color
root.title('Тренажер для закрепления навыков программирования')
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
btns_col_count = 2


def open_file(f_name=None):
    if f_name is None:
        ft_name = fd.askopenfilename()
    else:
        ft_name = f_name
    if ft_name != '':
        t_box.config(state='normal')
        t_box.delete('1.9', 'end')
        t_box.insert('end', '\n')
        f = open(ft_name, 'r')
        for line in f:
            line = line.strip()
            t_box.insert('end', f'{line}\n')
        f.close()
        t_box.config(state='disabled')


def main_fun(f_b_name=None):
    if f_b_name is None:
        f_name = fd.askopenfilename()
    else:
        f_name = f_b_name
    if f_name != '':
        arr = []
        for eli in root.winfo_children():
            if eli not in safe_list:
                eli.destroy()
        btns = []
        res_arr = []
        f = open(f_name, 'r')
        i = 0
        arr.clear()
        for line in f:
            if line != 'def prog():\n':
                i += 1
                line = line.replace('\n', '')
                arr.append(line)

        f.close()

        lbl = tk.Label(root, anchor='w', text='Выберите фрагменты кода в правильном порядке:',
                       font='Times 14', bg=bg_color)
        lbl.grid(row=2, column=0, padx=0, pady=5, columnspan=3)

        t_input_box = tk.Text(root, width=96, height=13, font='Times 11')
        create_buttons(arr, res_arr, i, btns_col_count, t_input_box, btns)
        t_input_box.grid(row=4, column=0, padx=15, pady=10, columnspan=4)
        t_input_box.insert('end', 'КОД: \n')
        t_input_box.config(state='disabled')
        btn_check = tk.Button(root, text='Проверить', font='Times 15',
                              command=lambda: check_answer(arr, res_arr, t_input_box, f_name, btns))
        btn_check.grid(row=5, column=0, padx=20, pady=10, columnspan=2)
        btn_rem = tk.Button(root, text='Очистить ввод', font='Times 15',
                            command=lambda: remove_text(t_input_box, res_arr, btns))
        btn_rem.grid(row=5, column=2, padx=20, pady=10, columnspan=2)


def create_buttons(arr, res_arr, i, col_count, t_input_box, btns):
    scr_btn = tk.Canvas(root, bg=bg_color, bd=2,
                        highlightbackground=bg_color)
    scr_btn.grid(row=3, column=0, padx=20, pady=10, columnspan=4)
    sort_arr = sorted(arr)
    for it in range(i):
        btns.append(tk.Button(scr_btn, width=int(90/col_count), text=sort_arr[it], font='Times 10', anchor="w",
                    bg='#F0F0F0', command=lambda par=it: onclick(arr, res_arr, par, t_input_box, btns)))
        btns[it].grid(column=int(it % col_count), row=int(it / col_count))


def onclick(arr, res_arr,  it, t_input_box, btns):
    res_arr.append(sorted(arr)[it])
    t_input_box.config(state='normal')
    t_input_box.insert('end', f'{sorted(arr)[it]}\n')
    t_input_box.config(state='disabled')
    btns[it].config(state='disabled')
    btns[it]['bg'] = 'lightgray'


def check_answer(arr, res_arr, t_input_box, f_name, btns):

    sys.path.append('./examples/')
    if arr == res_arr:
        messagebox.showinfo('message', 'Congratulation! Now click "OK" and check program work in your console!')
        m_name = f_name[f_name.rfind('/')+1:-3]
        module = __import__(m_name)
        module.prog()

    else:
        messagebox.showerror('message', 'Wrong! Please try again!')
        remove_text(t_input_box, res_arr, btns)


def remove_text(t_input_box, res_arr, btns):
    t_input_box.config(state='normal')
    t_input_box.delete('1.4', 'end')
    t_input_box.insert('end', '\n')
    t_input_box.config(state='disabled')
    for btn in btns:
        btn.config(state='normal')
        btn['bg'] = '#F0F0F0'
    res_arr.clear()


def sample_run():
    open_file('./examples/test.txt')
    main_fun('./examples/test.py')


def sample_run2():
    open_file('./examples/test2.txt')
    main_fun('./examples/test2.py')


safe_list = []

btn_add = tk.Button(root, text='открыть файл задания', font='Times 10', command=open_file)
btn_add.grid(row=0, column=0, padx=18, pady=10)
safe_list.append(btn_add)

t_box = tk.Text(root, width=96, height=5, font='Times 11')
t_box.grid(row=1, padx=15, pady=10, columnspan=4)
t_box.insert('end', 'Задание: \n')
t_box.config(state='disabled')
safe_list.append(t_box)

btn_addCode = tk.Button(root, text='загрузить скрипт', font='Times 10', command=main_fun)
btn_addCode.grid(row=0, column=1, padx=18, pady=10)
safe_list.append(btn_addCode)

btn_example1 = tk.Button(root, text='Открыть тестовое задание 1', font='Times 10', command=sample_run)
btn_example1.grid(row=0, column=2, padx=18, pady=10)
safe_list.append(btn_example1)

btn_example2 = tk.Button(root, text='Открыть тестовое задание 2', font='Times 10', command=sample_run2)
btn_example2.grid(row=0, column=3, padx=18, pady=10)
safe_list.append(btn_example2)

root.mainloop()
