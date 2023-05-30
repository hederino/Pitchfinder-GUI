import json

A4_MIN, A4_DEFAULT, A4_MAX = 400.0, 440.0, 500.0

default_settings = {"a4": A4_DEFAULT, "do_re_mi_toggled": False}
filename = "settings.json" 

try:
    with open(filename, "r") as f:
        settings = json.load(f)
except:
    settings = default_settings     


def save_settings(a4, toggled):
    dump_settings = {"a4": a4, "do_re_mi_toggled": toggled}
    with open(filename, "w") as f:
        json.dump(dump_settings, f)

