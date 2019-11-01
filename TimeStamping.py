#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
import tkinter.messagebox
import datetime
from datetime import datetime as dt
import json

# TODO: Get rid of excess variables. A class and related properties could be implemented.
def stampin_manually():
    global time_stampin
    global manual_stampin
    manual_stampin = True
    hour = si1.get()
    minute = si2.get()
    print("Hour: %s\nMinute: %s" % (si1.get(), si2.get()))
    try:
        now = datetime.datetime.now()
        time_stampin = now.replace(hour=int(hour), minute=int(minute))
    except ValueError:
        print('Input is not valid. Please ensure that you use 24-hour time format i.e. 13:37')
        stampin.config(text='Input is not valid. Please ensure \nthat you use 24-hour time format i.e. 13:37', fg="red")
    manual_stamp_in(time_stampin)
    manual_stampin = False
    return


def stampout_manually():
    global time_stampout
    global manual_stampout
    manual_stampout = True
    print("Hour: %s\nMinute: %s" % (so1.get(), so2.get()))
    hour = so1.get()
    minute = so2.get()
    try:
        now = datetime.datetime.now()
        time_stampout = now.replace(hour=int(hour), minute=int(minute))
    except ValueError:
        print('Input is not valid. Please ensure that you use 24-hour time format i.e. 13:37')
        stampout.config(text='Input is not valid. Please ensure \nthat you use 24-hour time format i.e. 13:37', fg="red")
    manual_stamp_out(time_stampout)
    manual_stampout = False
    return


def stamp_in():
    global time_stampin
    global manual_stampin
    time_stampin = datetime.datetime.now()
    stamped_in_date = time_stampin.strftime("%d/%m/%Y")
    stamped_in_time = time_stampin.strftime("%H:%M:%S")
    check_for_duplicate = check_if_timestampin_exists(stamped_in_date)
    if check_for_duplicate:
        stampin.config(fg="red",
                        text='There is already a stamp in for this date')
        return
    msg = 'Stamped in: {}'.format(time_stampin.strftime("%d/%m/%Y, %H:%M:%S"))
    stampin.config(fg="green", text='Stamped in: {}'.format(time_stampin.strftime("%d/%m/%Y, %H:%M:%S")))
    tkinter.messagebox.showinfo("Information", msg)
    check_if_checked_out = check_if_timestampout_exists(stamped_in_date)
    if check_if_checked_out is False and manual_stampin is False:
        with open('testdata.json', 'r') as json_file:
            data = json.load(json_file)
        data['work_day'].append({
            'stampin_date': stamped_in_date,
            'stampin_time': stamped_in_time,
            'stampin_manual': False,
            'stampout_date': '',
            'stampout_time': '',
            'stamptout:manual': False,
            'time_worked': ''
        })
        with open('testdata.json', 'w') as outfile:
            json.dump(data, outfile)
    else:
        with open('testdata.json', 'r') as json_file:
            data = json.load(json_file)
            for t in data['work_day']:
                if t['stampout_date'] == stamped_in_date:
                    print('Found this stampin on the same date: ' + t['stampout_date'] + ', ' + t['stampout_time'])
                    t['stampin_date'] = stamped_in_date
                    t['stampout_time'] = stamped_in_time
            with open('testdata.json', 'w') as outfile:
                json.dump(data, outfile)
            msg = 'Stamped in: {}'.format(time_stampin.strftime("%d/%m/%Y, %H:%M:%S"))
            tkinter.messagebox.showinfo("Information", msg)
            stampout.config(fg="green",
                            text='Stamped in: {}'.format(time_stampin.strftime("%d/%m/%Y, %H:%M:%S")))
            show_time_passed(stamped_in_date)
            return


def manual_stamp_in(time):
    global time_stampin
    time_stampin = time
    stamped_in_date = time_stampin.strftime("%d/%m/%Y")
    stamped_in_time = time_stampin.strftime("%H:%M:%S")
    check_for_duplicate = check_if_timestampin_exists(stamped_in_date)
    if check_for_duplicate:
        print('Duplicate stamp in found!')
        print('Error. A stamp in for the same date already exists')
        stampin.config(fg="red",
                        text='There is already a stamp out for this date')
        return
    check_if_checked_out = check_if_timestampout_exists(stamped_in_date)
    if check_if_checked_out and manual_stampin is False:
        ('Error message here...')
        return
    if check_if_checked_out is False and manual_stampin is True:
        with open('testdata.json', 'r') as json_file:
            data = json.load(json_file)
            data['work_day'].append({
                'stampin_date': stamped_in_date,
                'stampin_time': stamped_in_time,
                'stampin_manual': True,
                'stampout_date': '',
                'stampout_time': '',
                'stamptout:manual': False,
                'time_worked': ''
            })
        with open('testdata.json', 'w') as outfile:
            json.dump(data, outfile)
            msg = 'Stamped in: {}'.format(time_stampin.strftime("%d/%m/%Y, %H:%M:%S"))
            stampin.config(fg="green", text='Stamped in: {}'.format(time_stampin.strftime("%d/%m/%Y, %H:%M:%S")))
            tkinter.messagebox.showinfo("Information", msg)
    else:
        with open('testdata.json', 'r') as json_file:
            data = json.load(json_file)
            for t in data['work_day']:
                if t['stampout_date'] == stamped_in_date:
                    print('Found this stampin on the same date: ' + t['stampout_date'] + ', ' + t['stampout_time'])
                    t['stampin_date'] = stamped_in_date
                    t['stampin_time'] = stamped_in_time
                    with open('testdata.json', 'w') as outfile:
                        json.dump(data, outfile)
                    msg = 'Stamped in: {}'.format(time_stampin.strftime("%d/%m/%Y, %H:%M:%S"))
                    tkinter.messagebox.showinfo("Information", msg)
                    stampout.config(fg="green",
                                    text='Stamped in: {}'.format(time_stampin.strftime("%d/%m/%Y, %H:%M:%S")))
                    show_time_passed(stamped_in_date)
                    return


def stamp_out():
    global time_stampout
    global time_stampin
    time_stampout = datetime.datetime.now()
    stamped_out_date = time_stampout.strftime("%d/%m/%Y")
    stamped_out_time = time_stampout.strftime("%H:%M:%S")
    stamped_in_already = check_if_timestampin_exists(stamped_out_date)
    stamped_out_already = check_if_timestampout_exists(stamped_out_date)
    if stamped_out_already:
        print('Error. A stamp out for the same date already exists')
        stampout.config(fg="red",
                        text='There is already a stamp out for this date')
        return
    if stamped_in_already:
        print('Found stamp in')

        with open('testdata.json', 'r') as json_file:
            data = json.load(json_file)
        for t in data['work_day']:
            if t['stampin_date'] == stamped_out_date:
                print('Found this stampout on the same date: ' + t['stampin_date'] + ', ' + t['stampin_time'])
                t['stampout_date'] = stamped_out_date
                t['stampout_time'] = stamped_out_time
        with open('testdata.json', 'w') as outfile:
                    json.dump(data, outfile)
                    msg = 'Stamped out: {}'.format(time_stampout.strftime("%d/%m/%Y, %H:%M:%S"))
                    tkinter.messagebox.showinfo("Information", msg)
                    stampout.config(fg="green",
                                    text='Stamped out: {}'.format(time_stampout.strftime("%d/%m/%Y, %H:%M:%S")))
        show_time_passed(stamped_out_date)
        return
    with open('testdata.json', 'r') as json_file:
        data = json.load(json_file)
    data['work_day'].append({
        'stampin_date': '',
        'stampin_time': '',
        'stampin_manual': True,
        'stampout_date': stamped_out_date,
        'stampout_time': stamped_out_time,
        'stamptout_manual': False,
        'time_worked': ''
    })
    with open('testdata.json', 'w') as outfile:
        json.dump(data, outfile)
        msg = 'Stamped out: {}'.format(time_stampout.strftime("%d/%m/%Y, %H:%M:%S"))
        tkinter.messagebox.showinfo("Information", msg)
        stampout.config(fg="green", text='Stamped out: {}'.format(time_stampout.strftime("%d/%m/%Y, %H:%M:%S")))
        return


def manual_stamp_out(time):
    global time_stampout
    time_stampout = time
    stamped_out_date = time_stampout.strftime("%d/%m/%Y")
    stamped_out_time = time_stampout.strftime("%H:%M:%S")
    check_for_duplicate = check_if_timestampout_exists(stamped_out_date)
    if check_for_duplicate:
        print('Duplicate stamp in found!')
        stampout.config(fg="red",
                        text='There is already a stamp out for this date')
        return
    check_if_checked_in = check_if_timestampin_exists(stamped_out_date)
    if check_if_checked_in and manual_stampout is False:
        ('Error message here...')
        return
    if check_if_checked_in is False and manual_stampout is True:
        with open('testdata.json', 'r') as json_file:
            data = json.load(json_file)
            data['work_day'].append({
                'stampin_date': '',
                'stampin_time': '',
                'stampin_manual': True,
                'stampout_date': stamped_out_date,
                'stampout_time': stamped_out_time,
                'stamptout:manual': True,
                'time_worked': ''
            })
        with open('testdata.json', 'w') as outfile:
            json.dump(data, outfile)
            msg = 'Stamped out: {}'.format(time_stampout.strftime("%d/%m/%Y, %H:%M:%S"))
            stampout.config(fg="green", text='Stamped out: {}'.format(time_stampout.strftime("%d/%m/%Y, %H:%M:%S")))
            tkinter.messagebox.showinfo("Information", msg)
    else:
        with open('testdata.json', 'r') as json_file:
            data = json.load(json_file)
            for t in data['work_day']:
                if t['stampin_date'] == stamped_out_date:
                    print('Found this stampin on the same date: ' + t['stampin_date'] + ', ' + t['stampin_time'])
                    t['stampout_date'] = stamped_out_date
                    t['stampout_time'] = stamped_out_time
                    with open('testdata.json', 'w') as outfile:
                        json.dump(data, outfile)
                    msg = 'Stamped out: {}'.format(time_stampout.strftime("%d/%m/%Y, %H:%M:%S"))
                    tkinter.messagebox.showinfo("Information", msg)
                    stampout.config(fg="green",
                                    text='Stamped out: {}'.format(time_stampout.strftime("%d/%m/%Y, %H:%M:%S")))
                    show_time_passed(stamped_out_date)
                    return


def show_time_passed(timestamp):
    global time_stampin
    global time_stampout
    with open('testdata.json', 'r') as json_file:
        data = json.load(json_file)
    for t in data['work_day']:
        if t['stampout_date'] == timestamp:
            print('Found in this directory: ' + t['stampout_date'] + ', ' + t['stampout_time'])
            stampin_combined = t['stampin_date'] + ', ' + t['stampin_time']
            time_stampin = dt.strptime(stampin_combined, "%d/%m/%Y, %H:%M:%S")
            stampout_combined = t['stampout_date'] + ', ' + t['stampout_time']
            time_stampout = dt.strptime(stampout_combined, "%d/%m/%Y, %H:%M:%S")
            time_elapsed = time_stampout - time_stampin
            duration_in_seconds = time_elapsed.total_seconds()
            days = divmod(duration_in_seconds, 86400)  # Get days (without [0]!)
            hours = divmod(days[1], 3600)  # Use remainder of days to calc hours
            minutes = divmod(hours[1], 60)  # Use remainder of hours to calc minutes
            seconds = divmod(minutes[1], 1)  # Use remainder of minutes to calc seconds
            show_time_passed_label.config(text="Time passed: %d hours, %d minutes and %d seconds" % (
                hours[0], minutes[0], seconds[0]))
            t['time_worked'] = str(time_elapsed)
            with open('testdata.json', 'w') as outfile:
                json.dump(data, outfile)


def create_json_file():
    data = {}
    data['work_day'] = []
    data['work_day'].append({
        'stampin_date': '2019/01/10',
        'stampin_time': '08:37:00',
        'stampin_manual': False,
        'stampout_date': '2019/01/10',
        'stampout_time': '13:37:00',
        'stamptout_manual': True,
        'time_worked': '05:00:00'
    })

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)


def create_new_json_file():
        data = {}
        data['work_day'] = []
        data['work_day'].append({
            'stampin_date': '2019/02/10',
            'stampin_time': '07:37:00',
            'stampin_manual': False,
            'stampout_date': '2019/02/10',
            'stampout_time': '14:37:00',
            'stamptout_manual': True,
            'time_worked': '07:00:00'
        })
        with open('testdata.json', 'w') as outfile:
            json.dump(data, outfile)


def check_json_file():
    try:
        with open('testdata.json', 'r') as json_file:
            data = json.load(json_file)
    except:
        print('No JSON-file found. Creating testdata.JSON')
        create_new_json_file()


def check_if_timestampout_exists(timestamp):
    with open('testdata.json', 'r') as json_file:
        data = json.load(json_file)
    for t in data['work_day']:
        if t['stampout_date'] == timestamp:
            print('Found this stampout on the same date: ' + t['stampout_date'] + ', ' + t['stampout_time'])
            return True
        else:
            print('Found no stampout')
    return False


def check_if_timestampin_exists(timestamp):
    with open('testdata.json', 'r') as json_file:
        data = json.load(json_file)
    for t in data['work_day']:
        if t['stampin_date'] == timestamp:
            print('Found this stampout on the same date: ' + t['stampin_date'] + ', ' + t['stampin_time'])
            return True
        else:
            print('Found no stampin')
    return False
#create_new_json_file()
#create_json_file()
check_json_file()
#Use these methods to generate and read
root = tkinter.Tk()
root.configure(background='#424242')
time_stampin = 0
time_stampout = 0
manual_stampin = False
manual_stampout = False
root.title('Time Stamp')
#logo = tkinter.PhotoImage(file="logo.png")
#w1 = tkinter.Label(root, image=logo).pack(side="top")
info_label = tkinter.Label(root, fg="white", text='Stamp in and out below', bg="#424242")
info_label.pack()
btn = tkinter.Button(root, text="Stamp in", padx=5, pady=5, width=10,
                     command=stamp_in, bg='orange')
btn.pack(pady=10)
stampin = tkinter.Label(root, fg="green", bg="#424242")
stampin.pack()
btn2 = tkinter.Button(root, text="Stamp out", padx=5, pady=5, width=10,
                      command=stamp_out, bg='orange')
btn2.pack(pady=10)
stampout = tkinter.Label(root, fg="green", bg="#424242")
stampout.pack()

stampin_manual_label = tkinter.Label(root, fg="white", text='Use the hours and minutes form to enter the \ntime(clockwise) you were supposed to be stamped in', bg="#424242")
stampin_manual_label.pack()
tkinter.Label(root,
         text="Hour", bg='#424242', fg='white').pack()
si1 = tkinter.Entry(root, width=10)
si1.pack(padx=4, pady=4)
tkinter.Label(root,
         text="Minute", bg='#424242', fg='white').pack()
si2 = tkinter.Entry(root, width=10)
si2.pack(padx=4, pady=4)
tkinter.Button(root,
          text='Submit', command=stampin_manually, padx=2, pady=2, width=10, bg='orange').pack()
stampout_manual_label = tkinter.Label(root, fg="white", text='Use the hours and minutes form to enter the \ntime(clockwise) you were supposed to be stamped out', bg="#424242")
stampout_manual_label.pack()
tkinter.Label(root,
         text="Hour", bg='#424242', fg='white').pack()
so1 = tkinter.Entry(root, width=10)
so1.pack(padx=4, pady=4)
tkinter.Label(root,
         text="Minute", bg='#424242', fg='white').pack()
so2 = tkinter.Entry(root, width=10)
so2.pack(padx=4, pady=4)
tkinter.Button(root,
          text='Submit', command=stampout_manually, padx=2, pady=2, width=10, bg='orange').pack()
show_time_passed_label = tkinter.Label(root, fg="white", bg="#424242")
show_time_passed_label.pack()


root.geometry('300x600+300+250')
root.mainloop()
