from datetime import datetime


def format_time_string(time):
    return "{:02d}:{:02d}".format(int(float(time)/60), int(float(time)%60))

def format_time_datetime(time):
    return datetime.fromtimestamp(float(time))

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