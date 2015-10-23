fsactioneditor
==============

FS-UAE custom input actions editor for Linux


### Requirements ###
- [Linux](http://www.whylinuxisbetter.net)
- [fs-uae](http://fs-uae.net)
- Python 3 + [PyQt5](https://riverbankcomputing.com/software/pyqt/intro)
  Use your package manager (e.g. for Debian/Ubuntu install python3-pyqt5, for Arch python-pyqt5).
  If you already have fs-uae-launcher installed, you don't need to install pyqt5 again.



### Installation/Start ###
- Using git:
```
git clone https://github.com/sonnenscheinchen/fsactioneditor.git
cd fsactioneditor
./fsactioneditor
```

- or download the zip archive:
```
wget https://github.com/sonnenscheinchen/fsactioneditor/archive/master.zip
unzip master.zip
cd fsactioneditor-master
./fsactioneditor
```


### Usage ###
If you want to add custom actions to an existing configuration, you need to load it first.
If you want to map a key-/joystick action enable the "capture" toggle button, press a key/button or move your joystick. The event name is displayed below.
Note that the names of the keys are based on the english keyboard layout, so they might look wrong, but trust me, they are not. :-)
Now choose a desired Amiga action using the combo boxes below and click the "add" button to add the action to your config.
If you are done, don't forget to save!


### Bugs/Limitations ###
- More than one controller with the same name has not been tested (might not work at all)
