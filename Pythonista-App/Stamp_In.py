import ui
import datetime
from datetime import datetime as dt
import json

def stamp_in(stampin_label): 
    global time_stampin
    global manual_stampin
    time_stampin = datetime.datetime.now()
    stamped_in_date = time_stampin.strftime("%d/%m/%Y")
    stamped_in_time = time_stampin.strftime("%H:%M:%S")
    check_for_duplicate = check_if_timestampin_exists(stamped_in_date)
    msg = 'There is already a stamp in for this date'
    if check_for_duplicate:
    	textlabel = v['stampin_label']
    	textlabel.text = msg
    
    msg = 'Stamped in: {}'.format(time_stampin.strftime("%d/%m/%Y, %H:%M:%S"))
    textlabel = v['stampin_label']
    textlabel.text = msg
    
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
            'stampout_manual': False,
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
            textlabel = v['stampin_label']
            textlabel.text = msg
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
        msg = 'Error. A stamp in for the same date already exists'
        textlabel = v['stampin_label']
        textlabel.text = msg
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
                'stampout_manual': False,
                'time_worked': ''
            })
        with open('testdata.json', 'w') as outfile:
            json.dump(data, outfile)
            msg = 'Stamped in: {}'.format(time_stampin.strftime("%d/%m/%Y, %H:%M:%S"))
            textlabel = v['stampin_label']
            textlabel.text = msg
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
                    textlabel = v['stampin_label']
                    textlabel.text = msg
                    show_time_passed(stamped_in_date)
                    return


def stamp_out(stampout_label):
    global time_stampout
    global time_stampin
    time_stampout = datetime.datetime.now()
    stamped_out_date = time_stampout.strftime("%d/%m/%Y")
    stamped_out_time = time_stampout.strftime("%H:%M:%S")
    stamped_in_already = check_if_timestampin_exists(stamped_out_date)
    stamped_out_already = check_if_timestampout_exists(stamped_out_date)
    if stamped_out_already:
        print('Error. A stamp out for the same date already exists')
        msg='There is already a stamp out for this date'
        textlabel = v['stampout_label']
        textlabel.text = msg
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
                    textlabel = v['stampout_label']
        textlabel.text = msg
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
        'stampout_manual': False,
        'time_worked': ''
    })
    with open('testdata.json', 'w') as outfile:
        json.dump(data, outfile)
        msg = 'Stamped out: {}'.format(time_stampout.strftime("%d/%m/%Y, %H:%M:%S"))
        textlabel = v['stampout_label']
        textlabel.text = msg
        return


def manual_stamp_out(time):
    global time_stampout
    time_stampout = time
    stamped_out_date = time_stampout.strftime("%d/%m/%Y")
    stamped_out_time = time_stampout.strftime("%H:%M:%S")
    check_for_duplicate = check_if_timestampout_exists(stamped_out_date)
    if check_for_duplicate:
        print('Duplicate stamp in found!')
        msg = 'There is already a stamp out for this date'
        textlabel = v['stampout_label']
        textlabel.text = msg
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
                'stampout_manual': True,
                'time_worked': ''
            })
        with open('testdata.json', 'w') as outfile:
            json.dump(data, outfile)
            msg = 'Stamped out: {}'.format(time_stampout.strftime("%d/%m/%Y, %H:%M:%S"))
            textlabel = v['stampout_label']
            textlabel.text = msg
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
                    textlabel = v['stampout_label']
                    textlabel.text = msg
                    show_time_passed(stamped_out_date)
                    return


def toggle_switch(in_out_toggle_label):
	global is_switch_on
	if is_switch_on == True:
		is_switch_on = False
		textlabel = v['in_out_toggle_label']
		textlabel.text = 'Stamp Out'
	else:
		is_switch_on = True
		textlabel = v['in_out_toggle_label']
		textlabel.text = 'Stamp In'


def check_what_is_toggled(submit_button_input):
	global is_switch_on
	textfield_hour.end_editing()
	textfield_minute.end_editing()
	if is_switch_on is True:
		stampin_manually()
	else:
		stampout_manually()
		

def stampin_manually():
    global time_stampin
    global manual_stampin
    manual_stampin = True
    hour = textfield_hour.text
    minute = textfield_minute.text
    print("Hour: %s\nMinute: %s" % (hour, minute))
    try:
        now = datetime.datetime.now()
        time_stampin = now.replace(hour=int(hour), minute=int(minute))
    except ValueError:
        print('Input is not valid. Please ensure that you use 24-hour time format i.e. 13:37')
        msg = 'Input is not valid. Please ensure \nthat you use 24-hour time format i.e. 13:37'
        textlabel = v['stampin_label']
        textlabel.text = msg
    manual_stamp_in(time_stampin)
    manual_stampin = False
    return


def stampout_manually():
    global time_stampout
    global manual_stampout
    manual_stampout = True
    print("Hour: %s\nMinute: %s" % (textfield_hour.text, textfield_minute.text))
    hour = textfield_hour.text
    minute = textfield_minute.text
    try:
        now = datetime.datetime.now()
        time_stampout = now.replace(hour=int(hour), minute=int(minute))
    except ValueError:
        print('Input is not valid. Please ensure that you use 24-hour time format i.e. 13:37')
        msg = 'Input is not valid. Please ensure \nthat you use 24-hour time format i.e. 13:37'
        textlabel = v['stampout_label']
        textlabel.text = msg
    manual_stamp_out(time_stampout)
    manual_stampout = False
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
            msg ="Time passed: %d hours, %d minutes and %d seconds" % (
    hours[0], minutes[0], seconds[0])
            textlabel = v['summarized_label']
            textlabel.text = msg
            t['time_worked'] = str(time_elapsed)
            with open('testdata.json', 'w') as outfile:
                json.dump(data, outfile)


def show_hide_close_button(sender):
	print('Testing if it was possible to remove the keyboard this way')
	closebutton.background_color = "red"
	closebutton.title = "Clear"
	closebutton.tint_color = "white"
	closebutton.enabled = True
	

def on_exit_button_click(sender):
	textfield_hour.end_editing()
	textfield_minute.end_editing()
	closebutton.background_color = "transparent"
	closebutton.title = ""
	closebutton.tint_color = "transparent"
	closebutton.enabled = False
	textfield_hour.text = ""
	textfield_minute.text = ""


def getInput(view):
    input_hour = textfield_hour.text
    input_minute = textfield_minute.text
    if len(input_hour) >= 2:
    	textfield_hour.end_editing()
    if len(input_minute) >= 2:
    	textfield_minute.end_editing()
    return input


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


def create_new_json_file():
        data = {}
        data['work_day'] = []
        data['work_day'].append({
            'stampin_date': '2019/02/10',
            'stampin_time': '07:37:00',
            'stampin_manual': False,
            'stampout_date': '2019/02/10',
            'stampout_time': '14:37:00',
            'stampout_manual': True,
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


check_json_file()
v = ui.load_view('My_UI')
v.background_color="#6F4368"
textfield_hour = v['hour_textfield']
textfield_hour.keyboard_type=ui.KEYBOARD_DECIMAL_PAD
textfield_minute = v['minute_textfield']
textfield_minute.keyboard_type=ui.KEYBOARD_DECIMAL_PAD
#textfield_minute.clear_button_mode="always"
closebutton = v['close_keyboard_button']
closebutton.enabled = False

v.present('sheet')

time_stampout = 0
time_stampin = 0
is_switch_on = True
manual_stampin = False
manual_stampout = False

while True:
	getInput(v)







