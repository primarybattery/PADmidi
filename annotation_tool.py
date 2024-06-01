# -*- coding: utf-8 -*-
# @Author  : primarybattery
import os.path
import tkinter
import pygame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
from scipy.interpolate import make_interp_spline
import numpy as np


def fun_pause():
    global timer
    global time_start
    global time_remain
    global pos_music_last
    if mark_started:
        if button_pause['text'] == 'pause':
            button_pause['text'] = 'continue'
            pygame.mixer.music.pause()
            root.after_cancel(timer)
            time_remain = interval_timer - (time.time() - time_start) * 1000
            time_remain = round(time_remain)
            # print(time_remain)
        else:
            button_pause['text'] = 'pause'
            # pos_music_last=pos_scale/1000*length
            time_start = time.time()
            pos_music_last = pos_music_now
            pygame.mixer.music.unpause()
            timer = root.after(time_remain, fun_timer2)
    else:
        fun_start()


def event_pause(event):
    fun_pause()


def fun_start():
    global length
    global timer
    global mark_started
    global y_list
    global time_start
    global temp

    time_start = time.time()
    temp = time_start
    y_list = []
    # mark_started = True
    button_start.config(state=tkinter.DISABLED)
    pygame.mixer.init()
    pygame.mixer.music.load(music_name)
    sound = pygame.mixer.Sound(music_name)
    length = sound.get_length()
    pygame.mixer.music.play()
    timer = root.after(interval_timer, fun_timer2)
    root.after(interval_timer_draw_emo, fun_timer_draw_emo)



def fun_stop():
    global timer
    pygame.mixer.music.stop()
    root.after_cancel(timer)


# def fun_get_emo_timer():
#     global timer_get_emo
#     global timer_draw
#     # x_list.append(scale_x.get())
#     y_list.append(scale_y.get())
#     timer_get_emo = root.after(interval_get_emo, fun_get_emo_timer)


# def fun_timer():
#     global timer
#     global time_start
#     # x_list.append(scale_x.get())
#     y_list.append(scale_y.get())
#     interval = interval_timer // 1000
#     if label_current_emo_type_variable.get() == 'Pleasure':
#         p.plot(range(0, len(y_list) * interval, interval), y_list)
#     elif label_current_emo_type_variable.get() == 'Arousal':
#         a.plot(range(0, len(y_list) * interval, interval), y_list)
#     elif label_current_emo_type_variable.get() == 'Dominance':
#         d.plot(range(0, len(y_list) * interval, interval), y_list)
#
#     canvas.draw()
#     time_start = time.time()
#     timer = root.after(interval_timer, fun_timer)
#     # timer_get_emo = root.after(interval_get_emo, fun_get_emo_timer)
#     # timer_draw=root.after(interval_draw,fun_draw_timer)


def draw_line(sub_figure):
    fig.sca(sub_figure)
    plt.cla()
    plt.xlim(0, 1000)
    plt.ylim(-10, 10)

    sub_figure.vlines(pos_scale, -100, 100, linestyle='--')
    sub_figure.hlines(0, 0, 1000, linestyle='--')


def fun_timer2():
    global pos_scale
    global timer
    global time_start
    global pos_music_now
    # time_start = time.time()

    draw_line(p)
    draw_line(a)
    draw_line(d)
    canvas.draw()

    pos_music_now = pos_music_last + time.time() - time_start
    # music_time = pos_scale / 1000 * length
    # music_time += interval_timer / 1000
    # pos_scale = music_time / length * 1000
    pos_scale = pos_music_now / length * 1000
    # print('{:.2f} {:.2f}'.format(pos_music_now, time.time() - temp))

    scale_x.set(pos_scale)
    timer = root.after(interval_timer, fun_timer2)

    # timer_draw


def fun_timer_draw_emo():
    global p_x_smooth, p_y_smooth, a_x_smooth, a_y_smooth, d_x_smooth, d_y_smooth
    if len(data_p[0]) > 3:
        p_x_smooth = np.linspace(data_p[0][0], data_p[0][-1], 100)
        p_y_smooth = make_interp_spline(data_p[0], data_p[1])(p_x_smooth)
        p.plot(p_x_smooth, p_y_smooth, color='pink')
    if len(data_a[0]) > 3:
        a_x_smooth = np.linspace(data_a[0][0], data_a[0][-1], 100)
        a_y_smooth = make_interp_spline(data_a[0], data_a[1])(a_x_smooth)
        a.plot(a_x_smooth, a_y_smooth, color='lightgreen')
    if len(data_d[0]) > 3:
        d_x_smooth = np.linspace(data_d[0][0], data_d[0][-1], 100)
        d_y_smooth = make_interp_spline(data_d[0], data_d[1])(d_x_smooth)
        d.plot(d_x_smooth, d_y_smooth, color='lightblue')
    p.plot(data_p[0], data_p[1], marker='o', markersize=8, color='red')
    a.plot(data_a[0], data_a[1], marker='o', markersize=8, color='green')
    d.plot(data_d[0], data_d[1], marker='o', markersize=8, color='blue')
    canvas.draw()
    root.after(interval_timer_draw_emo, fun_timer_draw_emo)


# def fun_draw_timer():
#     global timer_get_emo
#     global timer_draw
#     plt.plot(range(0,len(y_list)*3,3),y_list)
#     canvas.draw()
#     # timer_draw=Timer(3, fun_draw_timer)
#     # timer_draw.start()
#     timer_draw=root.after(interval_draw,fun_draw_timer)

def fun_save_emo_data():
    global p_x_smooth, p_y_smooth, a_x_smooth, a_y_smooth, d_x_smooth, d_y_smooth
    try:
        with open(os.path.join(dir_annotation, music_name.split('\\')[-1]) + '.txt', 'w') as fp:
            # fp.write('valence='+str(x_list))
            fp.write('\np_x=' + str(data_p[0]))
            fp.write('\np_y=' + str(data_p[1]))
            fp.write('\na_x=' + str(data_a[0]))
            fp.write('\na_y=' + str(data_a[1]))
            fp.write('\nd_x=' + str(data_d[0]))
            fp.write('\nd_y=' + str(data_d[1]))

            fp.write('\np_x_fitting=' + str(p_x_smooth))
            fp.write('\np_y_fitting=' + str(p_y_smooth))
            fp.write('\na_x_fitting=' + str(a_x_smooth))
            fp.write('\na_y_fitting=' + str(a_y_smooth))
            fp.write('\nd_x_fitting=' + str(d_x_smooth))
            fp.write('\nd_y_fitting=' + str(d_y_smooth))
            print('successfully saved')
        label_show_save_info['text'] = '保存成功'
    except:
        label_show_save_info['text'] = '保存出错！'


# def fun_key(event):
#     char = event.char
#     keycode = event.keycode
#     if keycode == 32:  # 空格
#         fun_pause()
#     elif char == 'w':
#         scale_y.set(scale_y.get() + 1)
#     elif char == 's':
#         scale_y.set(scale_y.get() - 1)
#     # elif char=='a':
#     #     scale_x.set(scale_x.get() - 1)
#     # elif char=='d':
#     #     scale_x.set(scale_x.get() + 1)
#     # print(event.char,event.keycode)


def event_press_button1(event):
    pygame.mixer.music.stop()
    root.after_cancel(timer)


def event_release_button1(event):
    global timer
    global pos_scale
    global pos_music_last
    global pos_music_now
    global time_start
    pos_scale = scale_x.get()
    pos_music_now = pos_scale / 1000 * length
    time_start = time.time() - pos_music_now
    pos_music_last = 0
    pygame.mixer.music.play()
    pygame.mixer.music.set_pos(pos_music_now)
    if button_pause['text'] == 'pause':
        fun_timer2()
    else:
        # print('pause')
        pygame.mixer.music.pause()
        draw_line(p)
        draw_line(a)
        draw_line(d)
        canvas.draw()
    # timer = root.after(interval_timer, fun_timer2)


def check_if_new_mark(data, x, y):
    # 返回-1产生新点，否则返回需要修改的点在数据中的位置序号
    if len(data[0]) == 0:
        return -1
    x_list = [abs(a - x) for a in data[0]]
    y_list = [abs(a - y) for a in data[1]]
    distance = [a * a + b * b for a, b in zip(x_list, y_list)]
    # print(distance)
    if min(distance) < 20:
        near_pos = distance.index(min(distance))

        return near_pos
    else:
        return -1


def event_undo(event):
    if mark_last_changed_data[0]:
        mark_last_changed_data[0][0].pop(mark_last_changed_data[1])
        mark_last_changed_data[0][1].pop(mark_last_changed_data[1])


def event_click_canvas(event):
    x = event.x
    y = event.y
    i = 0
    if x >= pos_p[0][0] and x <= pos_p[1][0]:  # x在坐标轴内

        if y <= pos_p[0][1] and y >= pos_p[1][1]:
            pos_ = pos_p
            data_ = data_p
        elif y <= pos_a[0][1] and y >= pos_a[1][1]:
            pos_ = pos_a
            data_ = data_a
        elif y <= pos_d[0][1] and y >= pos_d[1][1]:
            pos_ = pos_d
            data_ = data_d
        else:
            return
        related_x = (x - pos_[0][0]) / (pos_[1][0] - pos_[0][0]) * 1000
        related_y = 10 - (y - pos_[1][1]) / (pos_[0][1] - pos_[1][1]) * 20

        mark = check_if_new_mark(data_, related_x, related_y)
        if -1 == mark:
            if data_[0] == [] and data_[1] == []:
                data_[0].append(related_x)
                data_[1].append(related_y)
            else:
                while i < len(data_[0]) and data_[0][i] < related_x:
                    i += 1
                data_[0].insert(i, related_x)
                data_[1].insert(i, related_y)

                mark_last_changed_data[1] = i
            # print(data_[0], data_[1])
        else:
            data_[0][mark] = related_x
            data_[1][mark] = related_y
            mark_last_changed_data[1] = mark
        mark_last_changed_data[0] = data_


def fun_clear_mode():
    if button_clear_mode['text'] == '当前:删除模式':
        button_clear_mode['text'] = '当前:标记模式'
        root.unbind('<Button-1>')
        root.bind('<Button-1>', event_clear_mode)
    else:
        button_clear_mode['text'] = '当前:删除模式'
        root.bind('<Button-1>', event_click_canvas)


def event_clear_mode(event):
    x = event.x
    y = event.y
    # print(x,y)
    if x >= pos_p[0][0] and x <= pos_p[1][0]:  # x在坐标轴内
        if y <= pos_p[0][1] and y >= pos_p[1][1]:
            pos_ = pos_p
            data_ = data_p
        elif y <= pos_a[0][1] and y >= pos_a[1][1]:
            pos_ = pos_a
            data_ = data_a
        elif y <= pos_d[0][1] and y >= pos_d[1][1]:
            pos_ = pos_d
            data_ = data_d
        else:
            return
        if len(data_[0]) == 0:
            return -1
        x = (x - pos_[0][0]) / (pos_[1][0] - pos_[0][0]) * 1000
        y = 10 - (y - pos_[1][1]) / (pos_[0][1] - pos_[1][1]) * 20
        x_list = [abs(a - x) for a in data_[0]]
        y_list = [abs(a - y) for a in data_[1]]
        distance = [a * a + b * b for a, b in zip(x_list, y_list)]
        # print(distance)
        if distance.count(min(distance)) == 1 and min(distance) < 30:
            mark = distance.index(min(distance))
            data_[0].pop(mark)
            data_[1].pop(mark)


def fun_confirm_user_name(window, user_name):
    # print(user_name)
    global dir_annotation
    dir_annotation='annotation/user_name'
    if not os.path.exists(dir_annotation):
        os.mkdir(dir_annotation)
    label_user_name['text'] = '用户名：{}'.format(user_name)
    window.destroy()


def fun_change_user_name():
    window_change_user_name = tkinter.Tk()
    label = tkinter.Label(window_change_user_name, text='用户名：')
    # entry_textvariable=tkinter.StringVar()
    entry = tkinter.Entry(window_change_user_name, width=10)

    button_confirm = tkinter.Button(window_change_user_name, text='确定',
                                    command=lambda: fun_confirm_user_name(window_change_user_name, entry.get()))
    label.pack()
    entry.pack()
    button_confirm.pack()
    window_change_user_name.mainloop()


def get_user_name():
    if os.path.exists('user_name.txt'):
        with open('user_name.txt', 'r') as fp:
            user_name = fp.read()
    else:
        with open('user_name.txt', 'w') as fp:
            user_name = 'aaa'
            fp.write(user_name)
    return user_name


def fun_exit():
    # fun_save_emo_data()
    root.destroy()


def fun_press_p():
    global label_current_emo_type_variable
    try:
        fun_stop()
    except:
        pass
    label_current_emo_type_variable.set('Pleasure')
    fun_start()


def fun_press_a():
    global label_current_emo_type_variable
    try:
        fun_stop()
    except:
        pass

    label_current_emo_type_variable.set('Arousal')
    fun_start()


def fun_press_d():
    global label_current_emo_type_variable
    try:
        fun_stop()
    except:
        pass

    label_current_emo_type_variable.set('Dominance')
    fun_start()


def fun_previous():
    pass


def fun_next():
    # label_show_music_num_textvariable.set('已标注{}，剩余{}'.format(len(os.listdir(dir_annotation)),len(file_list)))
    pygame.mixer.music.stop()

    fun_exit()
    try:
        # print(__file__)
        os.system('python {}'.format(__file__))
    except:
        os.system('start annotation_type2.exe')


def form_player_list():
    all_file_list = [os.path.join(dir_dataset, filename) for filename in os.listdir(dir_dataset)]
    for filename in os.listdir(dir_annotation):
        annotated = os.path.join(dir_annotation, filename)[:-4].split('\\')[-1]
        # print(all_file_list)
        for filepath in all_file_list:
            if annotated == filepath.split('\\')[-1]:
                all_file_list.remove(filepath)

    return all_file_list


def event_print_music_name(event):
    print(music_name)
    label_select_music['text'] = music_name


def fun_select_music():
    global music_name

    annotation_path=os.path.normpath(entry_select_music.get())
    music_name = os.path.join(dir_dataset,annotation_path.split('\\')[-1].split('.')[0]+'.ogg')
    annotation_list=get_annotation(entry_select_music.get())
    if annotation_list==None:
        label_show_music_name['text'] = music_name+'不存在！'
        return
    label_show_music_name['text'] = music_name
    data_p[0] = annotation_list[0]
    data_p[1] = annotation_list[1]
    data_a[0] = annotation_list[2]
    data_a[1] = annotation_list[3]
    data_d[0] = annotation_list[4]
    data_d[1] = annotation_list[5]
    # p_x_fitting= annotation_list[6]
    # p_y_fitting= annotation_list[7]
    # a_x_fitting= annotation_list[8]
    # a_y_fitting= annotation_list[9]
    # d_x_fitting= annotation_list[10]
    # d_y_fitting= annotation_list[11]

def get_annotation(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as fp:
        annotation = fp.readlines()

    for index, line in enumerate(annotation):
        if line.find('p_x=') != -1:
            p_x_index = index
        elif line.find('p_y=') != -1:
            p_y_index = index
        elif line.find('a_x=') != -1:
            a_x_index = index
        elif line.find('a_y=') != -1:
            a_y_index = index
        elif line.find('d_x=') != -1:
            d_x_index = index
        elif line.find('d_y=') != -1:
            d_y_index = index
        elif line.find('p_x_fitting=') != -1:
            p_x_fitting_index = index
        elif line.find('a_x_fitting=') != -1:
            a_x_fitting_index = index
        elif line.find('d_x_fitting=') != -1:
            d_x_fitting_index = index
        elif line.find('p_y_fitting=') != -1:
            p_y_fitting_index = index
        elif line.find('a_y_fitting=') != -1:
            a_y_fitting_index = index
        elif line.find('d_y_fitting=') != -1:
            d_y_fitting_index = index
    annotation_list = []
    annotation.append('')
    for start, end in zip(
            [p_x_index, p_y_index, a_x_index, a_y_index, d_x_index, d_y_index, p_x_fitting_index, p_y_fitting_index,
             a_x_fitting_index, a_y_fitting_index, d_x_fitting_index, d_y_fitting_index],
            [p_y_index, a_x_index, a_y_index, d_x_index, d_y_index, p_x_fitting_index, p_y_fitting_index,
             a_x_fitting_index, a_y_fitting_index, d_x_fitting_index, d_y_fitting_index, -1]):
        data = []
        for line in annotation[start:end]:

            line = line[:-1].split('[')[-1].split(']')[0]
            line=line.split(',')
            if len(line)==1:
                line=line[0]
                line = line.split()
            else:
                pass
            line = [float(i) for i in line]
            data += line
        annotation_list.append(data)

    return annotation_list





root = tkinter.Tk()
root.geometry('1920x1080')
# root.bind('<Key>',fun_key)

canvas = None
fig = plt.figure(figsize=(15, 7.5), dpi=100)

p = fig.add_subplot(311)
plt.xlim(0, 1000)
plt.ylim(-10, 10)
# plt.title('P',x=1.05,y=0.4)
a = fig.add_subplot(312)
plt.xlim(0, 1000)
plt.ylim(-10, 10)
# plt.title('A',x=1.05,y=0.4)

d = fig.add_subplot(313)
plt.xlim(0, 1000)
plt.ylim(-10, 10)
# plt.title('D',x=1.05,y=0.4)

canvas = FigureCanvasTkAgg(fig, root)
root.bind('<Button-1>', event_click_canvas)
root.bind('<BackSpace>', event_undo)
root.bind('<space>', event_pause)
# root.bind('<k>', event_print_music_name)
pos_p = [(189, 261), (1350, 91)]
pos_a = [(189, 465), (1350, 294)]
pos_d = [(189, 670), (1350, 499)]
data_p = [[], []]
data_a = [[], []]
data_d = [[], []]


# test_label=tkinter.Label(text='o')
# plt.xlim(0,300)

class Scale(tkinter.Scale):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pos = 0


# scale_y = tkinter.Scale(root, from_=100, to=-100,tickinterval=10,length=700)
scale_x = Scale(root, from_=0, to=1000, length=1194, orient=tkinter.HORIZONTAL, tickinterval=100, label='time')
scale_x.bind('<ButtonPress-1>', event_press_button1)
scale_x.bind('<ButtonRelease-1>', event_release_button1)
button_start = tkinter.Button(root, text='start', bg='lightyellow', width=10, command=fun_start)
button_stop = tkinter.Button(root, text='stop', bg='lightyellow', width=10, command=fun_stop)
button_pause = tkinter.Button(root, text='pause', bg='lightyellow', width=10, command=fun_pause)
button_save = tkinter.Button(root, text='save', bg='lightyellow', width=10, command=fun_save_emo_data)
button_exit = tkinter.Button(root, fg='red', bg='lightyellow', font=('', 30), text='退出', relief='raised',
                             command=fun_exit)
button_previous = tkinter.Button(root, text='上一首', command=fun_previous)
button_next = tkinter.Button(root, text='下一首', command=fun_next)
label_pleasure = tkinter.Label(root, text='Pleasure\n愉悦度')
label_arousal = tkinter.Label(root, text='Arousal\n强度')
label_dominance = tkinter.Label(root, text='Dominance\n主导程度')
button_clear_mode = tkinter.Button(root, text='当前:删除模式', bg='lightyellow', width=10, command=fun_clear_mode)
label_current_emo_type_variable = tkinter.StringVar(value='Pleasure')
label_current_emo_type = tkinter.Label(root, textvariable=label_current_emo_type_variable, font=('', 10))
label_show_music_num_textvariable = tkinter.StringVar(value='已标注{},剩余{}')
label_show_music_num = tkinter.Label(root, textvariable=label_show_music_num_textvariable)
label_music_name_variable = tkinter.StringVar(value='当前音乐：')
label_music_name = tkinter.Label(root, width=30, background='lightyellow', anchor='w',
                                 textvariable=label_music_name_variable)
label_show_save_info = tkinter.Label(root, fg='red')
label_user_name = tkinter.Label(root, bg='lightblue', text='用户名：new')
button_change_user_name = tkinter.Button(root, text='change user name', command=fun_change_user_name)
introduction = '      说明\n\n横轴为时间，\n\n纵轴为情感强度数值，取值(-10,10)\n\n可以使用wasd控制，空格暂停，点击start开始'
label_introduction = tkinter.Label(root, justify='left', font=('', 13), bg='lightyellow', width=25, height=20,
                                   text=introduction, wraplength=170)
label_show_music_name = tkinter.Label(root, text='')
entry_select_music = tkinter.Entry(root, width=20, bg='lightyellow')
entry_select_music.insert(0,'original_annotation/1/midi_000.txt')
label_select_music = tkinter.Label(root, text='输入音乐名称：')
button_select_music = tkinter.Button(root, text='确定', command=fun_select_music)

scale_x.place(x=170, y=700)
button_start.place(x=400, y=10)
button_clear_mode.place(x=500, y=10)
button_pause.place(x=400, y=50)
button_save.place(x=500, y=50)
button_exit.place(x=1400, y=600)
label_pleasure.place(x=50, y=150)
label_arousal.place(x=50, y=350)
label_dominance.place(x=50, y=550)
canvas.get_tk_widget().place(x=0, y=0)
# label_music_name.place(x=600,y=10)
label_user_name.place(x=1100, y=10)
# label_show_user_name.place(x=1150, y=10)
button_change_user_name.place(x=1200, y=10)
button_previous.place(x=600, y=10)
button_next.place(x=650, y=10)
label_show_music_num.place(x=600, y=50)
label_show_save_info.place(x=750, y=10)
entry_select_music.place(x=1370, y=100)
label_select_music.place(x=1370, y=70)
button_select_music.place(x=1370, y=130)
label_show_music_name.place(x=1370, y=40)
# label_introduction.place(x=1250,y=100)
# label_current_emo_type.place(x=600,y=730)


interval_get_emo = 3000
interval_draw = 3000
interval_timer = 100
interval_timer_draw_emo = 100
timer_get_emo = None
timer_draw = None
timer = None
time_remain = time.time()
time_start = None
mark_started = False
mark_last_changed_data = [None, None]  # [哪一个数据，修改位置]
pos_scale = 0
pos_music_now = 0
pos_music_last = 0
temp = None
# input(time_now)


y_list = []
x_list = []

dir_dataset = 'ogg_music'
dir_annotation = 'annotation/new'
if not os.path.exists(dir_annotation):
    os.mkdir(dir_annotation.split('/')[0])
    os.mkdir(dir_annotation)

file_list = form_player_list()

if file_list:
    music_name = file_list[0]
else:

    music_name = None

label_show_music_num_textvariable.set('已标注{},剩余{}'.format(len(os.listdir(dir_annotation)), len(file_list)))

pygame.mixer.init()
root.mainloop()
