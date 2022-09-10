from tkinter import *
from tkinter import messagebox

import time

BLACK = '#000'
WHITE = '#fff'

# PATH_TO_BTN_IMAGE = 'eggs.png'
# PATH_TO_RING_SOUND = 'telephone-ring-03a.wav'
pause_timer_flag = False

root = Tk()
root.title('Timer')
root.geometry('400x600')
root.config(bg=BLACK)
root.resizable(False, False)

heading = Label(root, text='TIMER COUNTDOWN', font='consolas 30 bold', bg=BLACK, fg=WHITE)
heading.pack(pady=10)

Label(root, font=('consolas', 15, 'bold'), text='current time:', bg='papaya whip').place(x=55, y=70)


def dotbox():
    dotbox_time = time.strftime('%H:%M:%S %p')
    current_time.config(text=dotbox_time)
    current_time.after(1000, dotbox)


current_time = Label(root, font=('consolas', 15, 'bold'), text="", fg=BLACK, bg=WHITE)
current_time.place(x=220, y=70)
dotbox()

# timer
hrs = StringVar()
hrs_pos = 60
space_hms = 100
hrs_entry = Entry(root, textvariable=hrs, width=2, font='consolas 50', bg=BLACK, fg=WHITE, bd=2)
hrs_entry.place(x=hrs_pos, y=155)
hrs.set('00')

mins = StringVar()
mins_entry = Entry(root, textvariable=mins, width=2, font='consolas 50', bg=BLACK, fg=WHITE, bd=2)
mins_entry.place(x=hrs_pos + space_hms, y=155)
mins.set('00')

secs = StringVar()
secs_entry = Entry(root, textvariable=secs, width=2, font='consolas 50', bg=BLACK, fg=WHITE, bd=2)
secs_entry.place(x=hrs_pos + space_hms * 2, y=155)
secs.set('00')

Label(root, text='hours', font='consolas 10', bg=BLACK, fg=WHITE).place(x=hrs_pos + 20, y=225)
Label(root, text='mins', font='consolas 10', bg=BLACK, fg=WHITE).place(x=hrs_pos + 20 + space_hms, y=225)
Label(root, text='secs', font='consolas 10', bg=BLACK, fg=WHITE).place(x=hrs_pos + 20 + space_hms * 2, y=225)


def timer(times):
    # times = int(hrs.get()) * 3600 + int(mins.get()) * 60 + int(secs.get())
    # while times > -1:
    if times > -1:
        if not pause_timer_flag:
            # if len(hrs_entry.get()) > 2:
            #     hrs_entry.delete(1, END)
            # if len(mins_entry.get()) > 2:
            #     mins_entry.delete(1, END)
            # if len(secs_entry.get()) > 2:
            #     secs_entry.delete(1, END)
            btn_pause['state'] = 'normal'
            btn_reset['state'] = 'disabled'
            hrs_entry.config(state="disabled")
            mins_entry.config(state="disabled")
            secs_entry.config(state="disabled")
            minute, second = (times // 60, times % 60)
            hour = 0
            if minute > 60:
                hour, minute = (minute // 60, minute % 60)

            if second < 10:
                secs.set(f'0{str(second)}')
            else:
                secs.set(str(second))

            if minute < 10:
                mins.set(f'0{str(minute)}')
            else:
                mins.set(str(minute))

            if hour < 10:
                hrs.set(f'0{str(hour)}')
            else:
                hrs.set(str(hour))

            times -= 1
            # time.sleep(1)

            if times < 0:
                # playsound(PATH_TO_RING_SOUND)
                secs.set('00')
                mins.set('00')
                hrs.set('00')
                btn_start['text'] = 'Start'
                btn_start['state'] = 'normal'
                btn_pause['state'] = 'disabled'
                btn_reset['state'] = 'normal'
                hrs_entry.config(state="normal")
                mins_entry.config(state="normal")
                secs_entry.config(state="normal")
                messagebox.showinfo("", "Your time has expired!")

            # root.update()
            root.after(1000, timer, times)
            # print(times)
        if times > 0:
            btn_start['text'] = 'Running'
            btn_start['state'] = 'disabled'


def pause_time():
    global pause_timer_flag
    if pause_timer_flag:
        pause_timer_flag = False
        btn_pause['text'] = 'Pause'
        timer(int(hrs.get()) * 3600 + int(mins.get()) * 60 + int(secs.get()))
    else:
        pause_timer_flag = True
        btn_pause['text'] = 'Continue'
        btn_reset['state'] = 'normal'


def brush():
    hrs.set('00')
    mins.set('07')
    secs.set('00')


def reset_time():
    global pause_timer_flag
    hrs.set('00')
    mins.set('00')
    secs.set('00')
    pause_timer_flag = False
    btn_start['text'] = 'Start'
    btn_start['state'] = 'normal'
    btn_pause['state'] = 'disabled'
    btn_reset['state'] = 'normal'
    btn_pause['text'] = 'Pause'
    hrs_entry.config(state="normal")
    mins_entry.config(state="normal")
    secs_entry.config(state="normal")


def eggs_time():
    hrs.set('00')
    mins.set('07')
    secs.set('00')


def ten_m_time():
    hrs.set('00')
    mins.set('10')
    secs.set('00')


def thirty_m_time():
    hrs.set('00')
    mins.set('30')
    secs.set('00')


x_pos = 125
btn_start = Button(root, text='Start', bg=WHITE, bd=0, fg=BLACK, width=25, height=3, font='consolas 10 bold',
                   cursor="dotbox",
                   command=lambda: timer(int(hrs.get()) * 3600 + int(mins.get()) * 60 + int(secs.get())))
btn_start.place(x=x_pos - 15, y=300)

btn_pause = Button(root, text='Pause', bg='#ea3548', bd=0, fg=WHITE, width=20, height=2, font='consolas 10 bold',
                   cursor="dotbox",
                   command=pause_time, state='disabled')
btn_pause.place(x=x_pos + 3, y=360)

btn_reset = Button(root, text='Reset', bg='#ea3548', bd=0, fg=WHITE, width=20, height=2, font='consolas 10 bold',
                   cursor="dotbox",
                   command=reset_time)
btn_reset.place(x=x_pos + 3, y=405)

btn_eggs = Button(root, text='Eggs', bg='#06347d', bd=0, fg=WHITE, width=10, height=2, font='consolas 10 bold',
                  cursor="dotbox",
                  command=eggs_time)
btn_eggs.place(x=10, y=500)

btn_10m = Button(root, text='10m', bg='#06347d', bd=0, fg=WHITE, width=10, height=2, font='consolas 10 bold',
                 cursor="dotbox",
                 command=ten_m_time)
btn_10m.place(x=90, y=500)

btn_30m = Button(root, text='30m', bg='#06347d', bd=0, fg=WHITE, width=10, height=2, font='consolas 10 bold',
                 cursor="dotbox",
                 command=thirty_m_time)
btn_30m.place(x=170, y=500)

# image_btn_eggs = PhotoImage(file=PATH_TO_BTN_IMAGE)
# btn_eggs = Button(root, image=image_btn_eggs, bg=WHITE, bd=0, command=brush)
# btn_eggs.place(x=7, y=300)


root.mainloop()
