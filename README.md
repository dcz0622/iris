## IRIS

IRIS (Indoor Route Instruction System) is a wearable device to provide in-building navigation guidance for a
visually-impaired person.



## Setting Up the Raspberry Pi

### Install mpg123 MP3 Player

- `sudo apt-get update`
- `sudo apt-get install alsa-utils mpg123`
- `sudo reboot`
- `sudo modprobe snd_bcm2835`
- `sudo amixer cset numid=3 1`

Here the output is being set to 1, which is analog (headphone jack). Setting the output to 2 switches to HDMI. The
default setting is 0 which is automatic. To change the volume, enter

`amixer set PCM -- 85%`

### Configure the RaspberryPi to Communicate with Arduino Mega

- `sudo systemctl stop serial-getty@ttyAMA0.service`
- `sudo systemctl disable serial-getty@ttyAMA0.service`
- `sudo nano /boot/cmdline.txt`
    - You will see something like: `dwc_otg.lpm_enable=0 console=serial0,115200 console=tty1 root=/dev/mmcblk0p2
      rootfstype=ext4 elevator=deadline fsck.repair=yes root wait`
    - Remove the line: `console=serial0,115200` and save and reboot for changes to take effect.
    - Reference: http://spellfoundry.com/2016/05/29/configuring-gpio-serial-port-raspbian-jessie-including-pi-3/
      #Using_the_serial_port_with_other_hardware

### Clone This Repository

- `cd ~/Desktop`
- `git clone https://github.com/chen-zhuo/IRIS.git`

### Configure the Raspberry Pi to Run a Python File Upon Boot

- Ensure that the boot option is set to “Console Autologin”, and “Wait for Network at Boot” is enabled.
- In Terminal, enter `sudo raspi-config` to enter the configuration panel.
- Add autorun script to the “profile” file
- In Terminal, enter `sudo nano /etc/profile`, and then append your script, for example:
- `cd ~/Desktop/IRIS/RaspberryPi`
- `python3 ~/Desktop/IRIS/RaspberryPi/main.py`



## Tips

### Safely Shut Down or Reboot the Raspberry Pi
- `sudo halt`
- `sudo reboot`

### Viewing RaspberryPi's memory on Mac

- `open afp://192.168.0.104` (use your Raspberry pi's IP address)
- Reference: http://raspberrypituts.com/access-raspberry-pi-files-in-your-os-x-finder/



## References

### Text-To-Speech Audio Files Generator

- http://www.fromtexttospeech.com

### Raspberry Pi GPIO Pins

- https://www.raspberrypi.org/documentation/usage/gpio/
