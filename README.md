![](onair.png)

OnAir status indicator for macOS camera usage with a Keyboard Maestro trigger.
==

This is based off of the work of henrik242 at https://github.com/henrik242/OnAir

Using a menubar indicator and Keyboard Maestro triggers to turn on/off a light bulb

**Please make sure you add the correct KM UUIDs to change the light status.**

To get the UUID, find the macro for "Off" and "On" and right-click Copy as > Copy as UUID

```
usage: OnAirKM.py &
```

Building the app
--

```
pip3 install -r requirements.txt
```

This installs the appropriate Python module requirements.

Planned improvements:
- Settings file so you don't have to hard-code the KM UUIDs
- Compile as Mac app per henrik242 repo

Thanks to
--

- <https://github.com/henrik242/OnAir>
- <https://github.com/jaredks/rumps>
- <https://camillovisini.com/article/create-macos-menu-bar-app-pomodoro/>
