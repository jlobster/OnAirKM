#!/usr/bin/env python3

import os
import platform
import re
import threading
import time
import webbrowser
import rumps

macos_version = int(platform.mac_ver()[0][:2])

class OnAir(object):
    def __init__(self):
        self.app = rumps.App("OnAir", "⚪")
        self.menuToggle = rumps.MenuItem("Turn on", callback=self.on_air)
        self.app.menu.add(self.menuToggle)
        self.app.menu.add(rumps.MenuItem("About OnAir…", callback=self.open_onair_url))
        self.menubar_blinker_active = False
        self.camera_state_updater_active = True

    def run(self):
        threading.Thread(target=self.camera_state_updater, daemon=True).start()
        self.app.run()

    def log(self, msg):
        print("%s" % msg)

    def camera_state_updater(self):  # Corrected the indentation here
        self.log("camera_state_updater()")
        predicate = 'subsystem == "com.apple.UVCExtension" and composedMessage contains "Post PowerLog"'
        extraopts = ""
        searchexpr = "guid:(.+)]"
        onitem = "Start"
        offitem = "Stop"
        if macos_version == 12:
            predicate = 'eventMessage contains "Post event kCameraStream"'
            extraopts = "--style ndjson"
            searchexpr = 'VDCAssistant_Device_GUID\\\\" = \\\\"(.+)\\\\";'
            onitem = "= On;"
            offitem = "= Off;"
        if macos_version >= 13:
            predicate = 'eventMessage contains "Cameras changed to"'
            extraopts = "--style ndjson"
            searchexpr = '"Cameras changed to (\[.*\])",'
            onitem = "to [ControlCenter"
            offitem = "to []"
        log_stream = os.popen("""/usr/bin/log stream %s --predicate '%s'""" % (extraopts, predicate), "r")
        cameras = dict()
        while self.camera_state_updater_active:
            item = log_stream.readline()
            self.log("reading '%s'" % item.strip())
            if item == "":
                self.log("log stream died")
                break
            match = re.search(searchexpr, item)
            if match is not None:
                device = match.group(1) if macos_version < 13 else "dummy"
                if onitem in item:
                    cameras[device] = True
                elif offitem in item:
                    cameras[device] = False
                else:
                    self.log("Unknown activity: %s" % item)
                self.log(cameras)
                if any(cameras.values()):
                    self.log("Camera %s is on" % device)
                    self.on_air()
                else:
                    self.log("Camera %s is off" % device)
                    self.off_air()
        self.log("camera_state_updater() done")

    @staticmethod
    def open_onair_url(callback_sender=None):
        webbrowser.open_new_tab("https://github.com/henrik242/OnAir")

    def on_air(self, callback_sender=None):
        self.log("on_air()")
        os.system("""osascript -e 'tell application "Keyboard Maestro Engine" to do script "ON AIR MACRO UUID HERE"'""")
        # os.system("""osascript -e 'tell application "Keyboard Maestro Engine" to do script "ON AIR MACRO NAME HERE"'""")
        self.menubar_blinker_active = True
        threading.Thread(target=self.menubar_blinker, daemon=True).start()
        self.menuToggle.title = "Turn off"
        self.menuToggle.set_callback(callback=self.off_air)
        self.log("on_air() done")

    def off_air(self, callback_sender=None):
        self.log("off_air()")
        os.system("""osascript -e 'tell application "Keyboard Maestro Engine" to do script "OFF AIR MACRO UUID HERE"'""")
        # os.system("""osascript -e 'tell application "Keyboard Maestro Engine" to do script "OFF AIR MACRO NAME HERE"'""")
        self.menubar_blinker_active = False
        self.menuToggle.title = "Turn on"
        self.menuToggle.set_callback(callback=self.on_air)
        self.log("off_air() done")

    def menubar_blinker(self):
        self.log("menubar_blinker()")
        green = True
        while self.menubar_blinker_active:
            self.app.title = "🟢" if green else "⚪️"
            time.sleep(1)
            green = not green
        self.app.title = "⚪"
        self.log("menubar_blinker() done")

if __name__ == "__main__":
    app = OnAir()
    app.run()
