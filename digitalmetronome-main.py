# DIGITAL METRONOME BY GOATHUR
# INTERFACES WITH I2C TO LCD SCRIPT BY GIGAFIDE

import machine
import utime
from machine import Pin
from picozero import Speaker
from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
# note: plug micro usb-c module onto pin 40 & gnd pin
#button control
switch_up = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_UP)
switch_down = machine.Pin(28, machine.Pin.IN, machine.Pin.PULL_UP)
power_switch = machine.Pin (14, machine.Pin.IN, machine.Pin.PULL_DOWN) #plug power switch onto pin 36 (3v3 out)

#define metronome sound: plays initially at 60 BPM
speaker = Speaker(15)
beat_time = 0.15
rest_time = 0.8
displayed_value = 60
metronome_thok = ["c4", beat_time]
speed_change_time = 0.05
speed_change_sound =["f5", speed_change_time]

#i2c lcd configuration : configuration from RPI-PICO-I2C-LCD library by n0n3nt1ty
I2C_ADDR     = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
lcd.clear() #initially clears everything for blank screen

while True:
    if power_switch.value() == True:
    
        #base display
        lcd.move_to(6,0)
        lcd.backlight_on()
        lcd.putstr("BPM:")
        lcd.move_to(5,1)
        lcd_value_disp = " " + str(displayed_value) + " "
        lcd.putstr(lcd_value_disp)
        speaker.play(metronome_thok)
        
        #button controls for metronome
        if switch_up.value() == 0:
            utime.sleep(0.25)  #pauses metronome sound when BPM is being changed
            speaker.play(speed_change_sound)
            displayed_value = displayed_value + 1
            rest_time = rest_time - 0.017
        
        elif switch_down.value() == 0:
            utime.sleep(0.25) #pauses metronome sound when BPM is being changed
            speaker.play(speed_change_sound)
            displayed_value = displayed_value - 1
            rest_time = rest_time + 0.017
        utime.sleep(rest_time)
        
    elif power_switch.value() == False:
        lcd.clear()
        lcd.backlight_off()
    
    
   
    
