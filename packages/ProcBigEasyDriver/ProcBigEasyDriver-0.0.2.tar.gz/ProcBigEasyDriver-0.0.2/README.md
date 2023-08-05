# Processed_PI_BigEasyDriver
Python class for continuous rotation of a PI controller regulated stepper motor in a separate process

## Install
pip install ProcBigEasyDriver

## Usage
Here's how this thing works. Once you initialize the object a second process is opened which toggles the step pin up and down at whatever interval is needed to reach to specified motor RPM. This is regulated by a PI controller. The speed and the microstepping regime used can be changed at anytime from the main process. The main process keeps control of the enable pin allowing the motor activity to be gated in the main process. 

### Basics
      import ProcBigEasyDriver as pbed
      from time import sleep
      
      #Init a stepper that turns at 10 rpm with no microstepping
      Stepper = pbed.ProcBigEasyDriver(step, direction, ms1, ms2, ms3, enable,
                                       microstepping=1, rpm=10, steps_per_rev=200,
                                       Kp=0.2, Ki=0.1)
                                       
      #Enable the big easy driver FETs
      Stepper.enable()
      
      #Let it go for 10s
      sleep(10)
      
      #Change the microstepping
      Stepper.set_microstep(2)
      sleep(10)
      
      #Speed it up to 20 rpm
      Stepper.set_rpm(20)
      sleep(10)
      
      #Stop the wheel (but keep the object active) for 10s
      Stepper.disable()
      sleep(10)
      
      #Turn it back on
      Stepper.enable()
      sleep(10)
      
      #Stop the wheel and release the pins (kill the object)
      Stepper.stop()
      
## Contributors
Code was written and is maintained by (Matt Davenport)[https://github.com/mattisabrat/] (mdavenport@rockefeller.edu)
