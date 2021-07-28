from datetime import datetime
import uuid
import seaborn as sns
import IO.SettingsIO as SettingsIO

# Collection of static helper methods

def format_time_string(time):
    return "{:02d}:{:02d}".format(int(float(time)/60), int(float(time)%60))

def format_time_datetime(time):
    return datetime.fromtimestamp(float(time))

def format_time_hr_int(time):
    date_time = datetime.fromtimestamp(float(time))
    return date_time.hour

def format_time_min_int(time):
    date_time = datetime.fromtimestamp(float(time))
    return date_time.minute

def get_current_time():
    return datetime.now().strftime("%H:%M:%S.%f")
    #return datetime.now().strftime("%H:%M:%S")

def get_datetime_string():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def get_datetime_full_string():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def get_new_uuid():
    return str(uuid.uuid4())

def get_colours(number):
    palette = sns.color_palette(None, number)
    return palette.as_hex()

def to_float(value: str) -> float:
    try:
        val_float = float(value)
    except ValueError:
        return None

    return val_float

def is_float(value: str) -> bool:
    try:
        val_float = float(value)
        if val_float:
            return True
    except ValueError:
        return False

def is_integer(value: str) -> bool:
    try:
        val_float = int(value)
        if val_float:
            return True
    except ValueError:
        return False

def convert_float_to_sf(value, sfnum: int = SettingsIO.load_preference_decdp()):
    
    if value != '':
        decimal_val = float(value)

        if decimal_val < 1000 and decimal_val > -1000:
            return str(round(decimal_val, sfnum))
        else:
            return ("{val:.{fig}e}".format(val=decimal_val, fig=sfnum))
    else:
        return ''




## Debugging methods

def trace(message):
    print(" ".join([message, get_current_time()]))


#test = "AAAAAAAAAAEAAAAC"
#test = "AAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAE="
#measurementids_decoded_bytes = base64.b64decode(test) 
#measurementids = np.frombuffer(measurementids_decoded_bytes, dtype = int)
#print(measurementids)

#raw_time = 646.0380249023438

#cur_result = format_time(raw_time)
#print(cur_result)


#new_result = datetime.fromtimestamp(raw_time)
#new_result = new_result.time()
#print(new_result)

#text = "C:/Users/willi/OneDrive/University/RP2/peakML/Example_file.peakml"

#slice_object = slice(-1, -2, -1)

#print(text[slice_object])

#section = text.slice("/")[0]

#print(section)