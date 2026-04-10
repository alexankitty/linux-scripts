#!/usr/bin/env python3
import json
import signal
import sys
from pathlib import Path
from gi.repository import GLib
import dbus
import dbus.mainloop.glib

def pretty_language(code: str) -> str:
    return {
        "EN": "English", "JA": "Japanese", "ZH": "Chinese",
        "KO": "Korean",  "FR": "French",   "DE": "German",
        "ES": "Spanish", "RU": "Russian",  "AR": "Arabic",
    }.get(code, code)

def get_current() -> dict:
    bus = dbus.SessionBus()
    obj = bus.get_object("org.fcitx.Fcitx5", "/controller")
    iface = dbus.Interface(obj, "org.fcitx.Fcitx.Controller1")
    unique, name, _, native, lang_code, lang, addon, enabled, *_ = iface.CurrentInputMethodInfo()

    unique    = str(unique)
    name      = str(name)
    native    = str(native)
    lang_code = str(lang_code)
    lang      = str(lang).upper()
    addon     = str(addon)
    enabled   = bool(enabled)

    return {
        "uniqueName":     unique,
        "name":           name,
        "nativeName":     native,
        "languageCode":   lang_code,
        "language":       lang,
        "languagePretty": pretty_language(lang),
        "languageBrief":  lang if lang_code.upper() == lang else f"{lang} | {lang_code}",
        "addon":          addon,
        "enabled":        enabled,
        "alt":            addon,
    }

def on_input_method_changed(*args, **kwargs):
    print(json.dumps(get_current()), flush=True)

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()
bus.add_signal_receiver(
    on_input_method_changed,
    signal_name="NewIcon",
    dbus_interface="org.kde.StatusNotifierItem",
    path="/StatusNotifierItem",
)

loop = GLib.MainLoop()

def on_interrupt(*args):
    loop.quit()
    sys.exit(0)

signal.signal(signal.SIGINT, on_interrupt)
signal.signal(signal.SIGTERM, on_interrupt)

# output immediately on start
print(json.dumps(get_current()), flush=True)

loop.run()
