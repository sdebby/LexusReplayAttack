# Lexus - replay attack.
## Or how I hacked my Lexus car.

### Hacking a car remote control key using replay attack.

## Background:
Car remote controls keys use "rolling codes" - means each code sent from the remote control to the car is single use, unique and hard to guess.

The way open the car is to capture the remote code, on sterile environment (with no car around), this way we can ensure that the cade will not be "blacklisted" by the car.

After we captured and saved the code, then we can reply this to the car.

## The equipment:
1. [RTL-SDR](https://www.rtl-sdr.com/) (Software Define Radio) dongle with 16 cm antenna 
2. Raspberry pi 3
   1. LED and switch soldered to GPIO.
   2. Antenna soldered to GPIO.
   3. [RPITX](https://github.com/F5OEO/rpitx) software installation on raspberry pi.
3. Power bank.
   
## The process:
1. First we need to find the remote control transmission frequency. This can be done by searching for the remote control FCC no. to get frequency range. I hade an educated guess that it will be around 868 MHz
2. Connecting the RTL-SDR dongle to the computer. Using SDR# software to identify the exact frequency.
3. **Found** the exact frequency is 867.8625 MHz
4. Then connecting the SDR dongle to the raspberry pi, connecting to the pi using SSH, and recording the remote control codes using rpitx:

```bash
sudo rtl_sdr -s 250000 -g 35 -f 867.8625e6 lexus_open.iq 
```
5. Connecting the SDR dongle back to the computer, and using SDR# software to listen to the frequency.
6. From the raspberry pi, transmitting the recorded codes
```bash
sudo sendiq -s 250000 -f 867.8625e6 -t u8 -i lexus_open.iq 
```
7. Validating on computer that the message is sent.
8. Writing a python script that will run the transmission code when pressing the button on the raspberry pi.
9. Adding the python script to run on boot.
```bash
crontab -e
Adding this:
@reboot python RPI_replay.py
```
10. Testing it on real.
11. ***KABOOM*** 

## **VIDEO**

[![](https://markdown-videos-api.jorgenkh.no/youtube/_qoDBIqu0Zc)](https://youtu.be/_qoDBIqu0Zc)

## Mitigation:
A good mitigation will by 2 way hand shake - like using NTLM authentication.

When paring the remote keys with the car system, a secret key will be exchanged.

Opening the car with a remote key will have the following steps:

1. remote control car key will send a rolling code to the car.
2. The car then will send a random message back to the remote.
3. The remote control car key will encrypt the message using pre defined key, and send it back to the car.
4. The car then decrypt the message with the key and validate massage integrity.
