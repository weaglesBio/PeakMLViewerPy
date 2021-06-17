from datetime import datetime
import numpy as np
import base64
import uuid
import seaborn as sns

def format_time_string(time):
    return "{:02d}:{:02d}".format(int(float(time)/60), int(float(time)%60))

def format_time_datetime(time):
    return datetime.fromtimestamp(float(time))

def get_current_time():
    return datetime.now().strftime("%H:%M:%S")

def get_new_uuid():
    return uuid.uuid4()

def get_colours(number):
    palette = sns.color_palette(None, number)
    return palette.as_hex()

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