from datetime import datetime, timedelta
import os

now = datetime.now().strftime("%m %A")
today_yr = datetime.now().strftime("%Y")

app_path = os.path.abspath(os.getcwd())
imgs_path = os.path.join(app_path, "imgs")
SWITCH_IMG = os.path.join(imgs_path, "switch.png")
ICON_IMG = os.path.join(imgs_path, "icon.ico")

TIMEZONES_ABBR = [ 
	("PST", "PDT"), 
	("MST", "MDT"), 
	("CST", "CDT"), 
	("EST", "EDT"), 
	("AST", "ADT"), 
	("BRT", None), 
	("FNT", None), 
	("AZOT", None), 
	("GMT", None), 
	("CET", "CEST"), 
	("EET", "EEST"), 
	("MSK", None), 
	("GST", None), 
	("PKT", None), 
	("CAT", None), 
	("ICT", None), 
	("HKT", None), 
	("JST", None), 
	("AEST", "AEDT"), 
	("SBT", None), 
	("NZST", "NZDT") 
	]
TIMEZONE = {}

time_format = 24
day_type = None

def set_day_type(value):
	global day_type
	day_type = value

def set_time_format(value):
	global time_format
	time_format = value

def get_n_sunday(month, n=0):
	sundays = []
	date = datetime(int(today_yr), month, 1)
	date_cpy = date

	while date_cpy.month == month:

		if date_cpy.weekday() == 6:
			sundays.append(date_cpy.day)

		date_cpy += timedelta(days=1)

	return date.month, sundays[n]

def is_day_light(start, end):
    start_month, start_day = start
    end_month, end_day = end
    
    current_date = datetime.now()
    start_date = datetime(int(today_yr), start_month, start_day)
    end_date = datetime(int(today_yr), end_month, end_day)
    
    return current_date >= start_date and current_date <= end_date

def time_filter(func):
    def wrapper(self, key):
        if key.isdigit() and len(key) <= 2:
            return func(self, key)

        elif key is "":
            return True

        else:
            return False
    
    return wrapper

def convert(hour, minute, diff, reverse=False):
	global time_format, day_type
	day = 0

	if reverse:
		if diff > 0:
			return int(hour) + -abs(diff), minute
		else:
			return int(hour) + abs(diff), minute

	hour = int(hour) + diff

	if int(hour) < 0:
		hour = time_format + int(hour)
		day -= 1

	if int(hour) >= time_format:
		hour = hour - time_format
		day += 1

	return int(hour), minute, day

def get_offset(start:tuple, end:tuple, offset:int):
	month_start, sun_1 = start 
	month_end, sun_2 = end
	offset+=1 if is_day_light(get_n_sunday(month_start, sun_1), get_n_sunday(month_end, sun_2)) else offset
	return offset

for index, timezone in enumerate(TIMEZONES_ABBR):
	offset = index - 8
	start_date, end_date = None, None

	if timezone[1] == None:
		TIMEZONE[timezone[0]] = offset
		continue

	if offset <= -4 and is_day_light(get_n_sunday(3, 1), get_n_sunday(11, 0)):
		TIMEZONE[timezone[1] + " (Daylight Saving)"] = offset + 1
	
	elif 0 < offset <= 2 and is_day_light(get_n_sunday(3, -1), get_n_sunday(10, -1)):
		TIMEZONE[timezone[1] + " (Daylight Saving)"] = offset + 1
	
	elif offset == 10 and is_day_light(get_n_sunday(10, 0), get_n_sunday(4, 0)):
		TIMEZONE[timezone[1] + " (Daylight Saving)"] = offset + 1

	elif offset == 12 and is_day_light(get_n_sunday(9, -1), get_n_sunday(4, 0)):
		TIMEZONE[timezone[1] + " (Daylight Saving)"] = offset + 1
	
	else:
		TIMEZONE[timezone[0]] = offset

print(TIMEZONE)