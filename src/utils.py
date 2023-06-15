from datetime import datetime, timedelta
import os
from typing import Literal

now = datetime.now().strftime("%m %A")
today_yr = datetime.now().strftime("%Y")

app_path = os.path.abspath(os.getcwd())
imgs_path = os.path.join(app_path, "imgs")
SWITCH_IMG = os.path.join(imgs_path, "switch.png")
ICON_IMG = os.path.join(imgs_path, "icon.png")

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
time_indication = "am"

def set_indication(value:str) -> None:
    global time_indication
    time_indication = value

def twentyfour_to_twelve(hour:int) -> tuple[int, str]: # Need to Test This
    indication = "am"
    
    if 24 > hour >= 12:
        indication = "pm"

    hour = ((hour - 1) % 12) +1
    
    return hour, indication

def twelve_to_twentyfour(hour:int, indication:str) -> int: # 00:00 = 12:00 A.m. 12:00 = 12:00 P.m.
    
    if hour == 12 and indication == "am":
        hour -= 12
    elif indication == "pm" and hour != 12:
        hour += 12

    hour = ((hour) % 24) 
    return hour

def set_time_format(value:int) -> None:
	global time_format
	time_format = value

def get_n_sunday(month:int, n_sunday:int=0) -> tuple[int, int]:
    sundays = []
    date = datetime(int(today_yr), month, 1)
    date_cpy = date

    while date_cpy.month == month:

        if date_cpy.weekday() == 6:
            sundays.append(date_cpy.day)

        date_cpy += timedelta(days=1)

    return date.month, sundays[n_sunday]

def is_day_light(start:tuple[int, int], end:tuple[int, int]) -> bool:
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

def convert(hour: int, time_diff1: int, time_diff2: int) -> tuple[int, Literal[1, -1, 0]]:
    
    day = 0
    if time_format == 12:
        hour = twelve_to_twentyfour(hour, time_indication)

    new_hr = (hour + (time_diff1 * -1)) + time_diff2
    
    if new_hr > 23:
        day += 1
    elif new_hr < 0:
        day -= 1
    new_hr = new_hr % 24

    return new_hr, day

def get_offset(start:tuple, end:tuple, offset:int) -> int:
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

