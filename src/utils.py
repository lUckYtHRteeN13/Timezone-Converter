from datetime import datetime

now = datetime.now().strftime("%m")

def time_filter(func):
    def wrapper(self, key):
        if key.isdigit() and len(key) <= 2:
            return func(self, key)

        elif key is "":
            return True

        else:
            return False
    
    return wrapper

def pt_converter(hour, minute, reverse=False):
	diff = -7
	day = 0
	
	if reverse:
		return int(hour) + abs(diff), minute

	hour = int(hour) + diff

	if int(hour) < 0:
		hour = 24 + int(hour)
		day -= 1
	
	if int(hour) > 24:
		hour = hour - 24
		day += 1
		
	return int(hour), minute, day

def mt_converter(hour, minute, reverse=False):
	diff = -6
	day = 0

	if reverse:
		return int(hour) + abs(diff), minute

	hour = int(hour) + diff

	if int(hour) < 0:
		hour = 24 + int(hour)
		day -= 1

	if int(hour) > 24:
		hour = hour - 24
		day += 1

	return int(hour), minute, day

def ct_converter(hour, minute, reverse=False):
	diff = -5
	day = 0

	if reverse:
		return int(hour) + abs(diff), minute

	hour = int(hour) + diff

	if int(hour) < 0:
		hour = 24 + int(hour)
		day -= 1

	if int(hour) > 24:
		hour = hour - 24
		day += 1

	return int(hour), minute, day

def et_converter(hour, minute, reverse=False):
	day = 0
	diff = -4

	if reverse:
		return int(hour) + abs(diff), minute

	hour = int(hour) + diff

	if hour < 0:
		hour += 24
		day -= 1

	if hour > 24:
		hour -= 24
		day += 1

	return int(hour), minute, day

def utc_converter(hour, minute, reverse=False):
	diff = 0
	day = 0

	if reverse:
		return int(hour) + abs(diff), minute

	hour = int(hour) + diff

	if int(hour) < 0:
		hour = 24 + int(hour)
		day -= 1

	if int(hour) > 24:
		hour = hour - 24
		day += 1

	return int(hour), minute, day

def jst_converter(hour, minute, reverse=False):
	diff = 9
	day = 0

	if reverse:
		return int(hour) + -abs(diff), minute

	hour = int(hour) + diff

	if int(hour) < 0:
		hour = 24 + int(hour)
		day -= 1

	if int(hour) > 24:
		hour = hour - 24
		day += 1

	return int(hour), minute, day

if __name__ == "__main__":
	print(et_converter(23, 3))