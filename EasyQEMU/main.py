from sys import exit
if __name__!='__main__':exit()

# import library
import tkinter as tk
from subprocess import getoutput, check_output, DEVNULL
import tkinter.filedialog
import pathlib
import os
import threading
import time
import signal
from tkinter.messagebox import showerror


# initial
if os.name == 'nt':
    print("This tool only design for Linux!")
    input()
    exit()

# var
home = getoutput("echo $HOME")
qemu_name = ["aarch64", "arm", "x86_64", "i386"]
tmp_for_long_path = ""
is_running = 0
machine = ""

class bin:
    def is_file(file):
        return pathlib.Path(file).is_file()
    def is_dir(dir):
        return pathlib.Path(dir).is_dir()
    def browse(initialdir=globals()["home"], title="EasyQEMU", file_name="qemu", file_type="*"):
        return tkinter.filedialog.askopenfilename(initialdir = initialdir, title = title, filetypes = [(file_name, file_type)])
    def real_path(file_or_dir):
        return os.path.realpath(file_or_dir)
    def kill_process():
        if hasattr(signal, 'SIGKILL'):
            os.kill(os.getpid(), signal.SIGKILL)
        else:
            os.kill(os.getpid(), signal.SIGABRT)
        return
    def report_callback_exception(self, exc, val, tb):
        showerror("Program error", message=str(val))
    
def refresh_qemu(add=""):
    new = find_qemu_path()
    if add:
        globals()["tmp_for_long_path"] = str(add)
        if len(str(add)) > 50:
            add = str("../" + str(add).split("/")[-1])
        tmp = get_qemu_arch(globals()["tmp_for_long_path"])
        qemu.set(add + " ({})".format(tmp))
        new.append(add + " ({})".format(tmp))
    else:
        return
    globals()["option_menu_qemu"]['menu'].delete(0, 'end')
    for choice in new:
        globals()["option_menu_qemu"]['menu'].add_command(label=choice, command=tk._setit(globals()["qemu"], choice))
    return

def auto_refresh():
    tmp = ""
    while 1:
        try:
            if tmp != globals()["qemu"].get():
                tmp = globals()["qemu"].get()
                for k in globals()["obf"]:
                    globals()[k].config(text="")
                for k in globals()["obf_data"]:
                    globals()[k] = ""
        except RuntimeError:
            bin.kill_process()
        time.sleep(1)

def browse_qemu():
    if (globals()["tmp_for_long_path"]):
        a = bin.browse("/".join(globals()["tmp_for_long_path"].split("/")[:-1]))
    else:
        a = bin.browse()
    print(a)
    if (str(a) != "") and (bin.is_file(str(a))):
        refresh_qemu(bin.real_path(str(a)))
    return

def get_qemu_arch(file):
    try:
        arch = check_output("{} --help".format(file), stderr=DEVNULL, shell=True, timeout=1).decode()
    except:
        return "unknown"
    for i in globals()["qemu_name"]:
        if "qemu-system-{}".format(i) in arch:
            return i
    return "unknown"

def get_list_in_qemu(txt):
    tmp = []
    test = getoutput(globals()["qemu"].get() + " " + txt + " help").split("\n")[1:]
    for i in test:
        tmp.append(i.split()[0])
    return tmp

def change_text_running():
    globals()["button_run_qemu"].config(text="STOP")
    globals()["button_run_qemu"].config(command= lambda : stop_qemu(qemu.get()))
    globals()["button_machine"]["state"] = "disabled"
    globals()["option_menu_qemu"].configure(state="disabled")
    globals()["button_browse_qemu"]["state"] = "disabled"
    return

def while_running():
    while globals()["is_running"] == 1:
        time.sleep(1)

    globals()["button_run_qemu"].config(text="RUN")
    globals()["button_run_qemu"].config(command= lambda : run_qemu(qemu.get()))
    globals()["button_machine"]["state"] = "normal"
    globals()["option_menu_qemu"].configure(state="normal")
    globals()["button_browse_qemu"]["state"] = "normal"
    return

def stop_qemu(qemu):
    os.system("kill -9 $(pgrep -f {})".format(qemu.split("/")[-1]))

def execute_qemu(cmd):
    os.system(cmd)
    globals()["is_running"] = 0
    return

def run_qemu(cmd):
    cmd += " -M {} ".format(globals()["machine"])
    globals()["is_running"] = 1
    change_text_running()
    threading.Thread(target=while_running, args=()).start()
    threading.Thread(target=execute_qemu, args=(cmd,)).start()
    return

def find_qemu_path():
    qemu_path = []
    for i in globals()["qemu_name"]:
        try:
            tmp = bin.real_path(getoutput("which qemu-system-{}".format(i)))
        except:
            continue
        if (tmp != ""):
            qemu_path.append(tmp)
    return qemu_path

def open_vm():
    file = bin.browse(initialdir=globals()["home"], title="EasyQEMU", file_name="Config VM", file_type="vmconfig")
    pass

def save_vm():
    pass

def new_vm():
    pass

def test_pass():
    return

    
def choose_option(options,textbox,var,text):
    if(options == []):
        return
    globals()["root_options"] = tk.Tk()

    tkvar = tk.StringVar(globals()["root_options"])

    tkvar.set('choose')

    def on_selection(value):
        globals()[textbox].config(text=value)
        globals()[var] = value
        globals()["root_options"].destroy()

    popupMenu = tk.OptionMenu(globals()["root_options"], tkvar, *options, command = on_selection)
    tk.Label(globals()["root_options"], text=text).grid(row=0, column=0)
    popupMenu.grid(row=1, column =0)

    globals()["root_options"].mainloop()


# main
### tk.Tk.report_callback_exception = bin.report_callback_exception
window = tk.Tk()
window.title("EasyQEMU")
window.geometry("640x320")
window.resizable(width=False, height=False)
window_bottom = tk.Frame(window)
window_bottom.pack(side="bottom")

# menubar
menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label = "New VM", command = new_vm)
filemenu.add_command(label = "Open VM", command = open_vm)
filemenu.add_command(label = "Save VM", command = save_vm)
filemenu.add_separator()
filemenu.add_command(label = "Exit", command = bin.kill_process)
menubar.add_cascade(label = "File", menu = filemenu)
window.config(menu = menubar)

qemu = tk.StringVar(window)
qemu.set("Choose qemu")

# label
label_machine_type = tk.Label(window, text='VM: ', font=('Arial', 12, 'bold'))
label_machine_type.place_forget()
label_machine_type.place(x=10,y=10)

label_machine_type = tk.Label(window, text='Machine: ')
label_machine_type.place_forget()
label_machine_type.place(x=10,y=40)

# option

option_menu_qemu = tk.OptionMenu(window_bottom, qemu, *find_qemu_path())
option_menu_qemu.pack(side = "left")

# button
button_browse_qemu = tk.Button(window_bottom, text='Browse qemu', command=browse_qemu)
button_browse_qemu.pack(side = "left")

button_run_qemu = tk.Button(window_bottom, text='RUN', command= lambda : run_qemu(qemu.get()))
button_run_qemu.pack(side = "right")

button_machine = tk.Button(window, text='',command= lambda : choose_option(get_list_in_qemu("-M"),"button_machine", "machine", "Machine:"))
button_machine.place_forget()
button_machine.place(x=80,y=35)

button_test = tk.Button(window_bottom, text='test',command= lambda : choose_option(["sdad"]))
button_test.pack(side = 'left')

obf = ["button_machine"]
obf_data = ["machine"]
threading.Thread(target=auto_refresh,args=()).start()

window.mainloop()