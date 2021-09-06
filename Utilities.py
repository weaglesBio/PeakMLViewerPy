from datetime import datetime
import uuid
import IO.SettingsIO as SettingsIO
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import List

from faker import Factory

# Collection of static helper methods

def format_time_string(time: str) -> str:
    return "{:02d}:{:02d}".format(int(float(time)/60), int(float(time)%60))

def format_time_min(time: str) -> str:
    return int(float(time)/60)

def format_time_sec(time: str) -> str:
    return int(float(time)%60)

def format_time_int(time_string: str) -> int:
    time_split = time_string.split(":")
    min = int(time_split[0])
    sec = int(time_split[1])
    return (min*60) + sec
    #return "{:02d}:{:02d}".format(int(float(time)/60), int(float(time)%60))

def format_time_int_min(time_string: str) -> int:
    time_split = time_string.split(":")
    return int(time_split[0])

def format_time_int_sec(time_string: str) -> int:
    time_split = time_string.split(":")
    return int(time_split[1])

def format_time_datetime(time: float) -> datetime:
    return datetime.fromtimestamp(float(time))

def format_time_from_datetime_int(time_as_dt: datetime) -> int:
    return time_as_dt.minute
    #return datetime.fromtimestamp(float(time))

def format_time_from_datetime_sec(time_as_dt: datetime) -> int:
    return time_as_dt.second

def get_current_time() -> str:
    return datetime.now().strftime("%H:%M:%S.%f")
    #return datetime.now().strftime("%H:%M:%S")

def get_new_uuid() -> str:
    return str(uuid.uuid4())

def get_colours(number: int) -> List[str]:

    default_colours = ['#e6194b', # 1. Red 
            '#3cb44b', # 2. Green
            '#ffe119', # 3. Yellow
            '#4363d8', # 4. Blue
            '#f58231', # 5. Orange
            '#911eb4', # 6. Purple
            '#42d4f4', # 7. Cyan
            '#f032e6', # 8. Magenta
            '#bfef45', # 9. Lime
            '#fabebe', # 10. Pink
            '#469990', # 11. Teal
            '#dcbeff', # 12. Lavender
            '#9a6324', # 13. Brown
            #'#fffac8', # 14. Beige
            '#800000', # 15. Maroon
            '#aaffc3', # 16. Mint
            '#808000', # 17. Olive
            '#ffd8b1', # 18. Apricot
            '#000075', # 19. Navy
            '#a9a9a9', # 20. Grey
            '#167E4A', # 21. Forest Green
            '#470387', # 22. Dark Purple
            '#FF91F7', # 23. Bright Pink
            '#1EFA46', # 24. Bright Green
            '#000000', # 25. Black
            ]

    colours = []

    fake = Factory.create()
    for i in range(number):

        if i < len(default_colours):
            colours.append(default_colours[i])
        else:
            colour_added = False

            while not colour_added:
                new_colour = fake.hex_color()
                if new_colour not in colours:
                    colours.append(new_colour)
                    colour_added = True

    return colours

    # return ['#fabebe', # 1. blank
    #         '#3cb44b', # 2. IPA_Beard
    #         '#3cb44b', # 3. IPA_Bust
    #         '#3cb44b', # 4. IPA_Green
    #         '#3cb44b', # 5. IPA_Hob
    #         '#3cb44b', # 6. IPA_Old
    #         '#3cb44b', # 7. IPA_Punk
    #         '#3cb44b', # 8. IPA_Thorn
    #         '#e6194b', # 9. Lag_Beck
    #         '#e6194b', # 10. Lag_Bud
    #         '#e6194b', # 11. Lag_Cob
    #         '#e6194b', # 12. Lag_Est
    #         '#e6194b', # 13. Lag_Hob
    #         '#e6194b', # 14. Lag_Per
    #         '#e6194b', # 15. Lag_San
    #         '#4363d8', # 16. Port_Brew
    #         '#4363d8', # 17. Port_Coffee
    #         '#4363d8', # 18. Port_Drag
    #         '#4363d8', # 19. Port_Guin
    #         '#4363d8', # 20. Port_Lond
    #         '#4363d8', # 21. Port_Rob
    #         '#4363d8', # 22. Port_White
    #         '#fabebe', # 23. QC
    #         ]

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

def convert_float_to_sf(value, sfnum: int = None) -> str:
    
    if not sfnum:
        # On initialisation settings file may not exist so default to 3 until it is.
        try:
            sfnum = SettingsIO.load_preference_decdp()
        except:
            sfnum = 3

    if value != '':
        decimal_val = float(value)

        if decimal_val < 1000 and decimal_val > -1000:
            return str(round(decimal_val, sfnum))
        else:
            return ("{val:.{fig}e}".format(val=decimal_val, fig=sfnum))
    else:
        return ''

def prettify_xml(etree: ET.Element):
    et_string = ET.tostring(etree)
    md_string = minidom.parseString(et_string)
    return md_string.toprettyxml(indent="\t")

## Debugging methods

def trace(message: str):
    print(" ".join([message, get_current_time()]))
