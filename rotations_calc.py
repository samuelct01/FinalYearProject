from gpiozero import MotionSensor
import time
turbineid = 1 #chane this for each turbine.
irs = MotionSensor(4)
rotation = 0
seconds = 20
turbine_circumfrence = 20 #actuall value will be added when the turbines are made
end = time.time() + seconds # will run this for a decided amount of time when it comes to testing 

while time.time() < end:
    if irs.motion_detected:
        rotation +=1


per_second = rotation/seconds
turbinespeed = per_second * turbine_circumfrence
