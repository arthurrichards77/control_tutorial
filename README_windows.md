# control_tutorial

This is the Windows version!  See also the [Linux version](README.md).

Control tutorial examples using FlightGear simulator.

We're using aircraft as a case study for control because the dynamics responses are interesting but, 
for the trainer aircraft we'll experiment with, quite forgiving.  We'll use [FlightGear](https://www.flightgear.org/) as its free, makes a good 
job of representing the aircraft dynamics, and provides an easy back door for interfacing with external programs.
We will implement those programs in Python, using a custom interface class provided in this project.

## Installation

See also the [instruction video](https://youtu.be/k22bB9KeypE) on Youtube.

### Git

Download via (https://git-scm.com/download/win) and install following the instructions.

### Anaconda

Download via (https://www.anaconda.com/products/individual) and make sure you include the Spyder IDE (I think it's included by default).

### FlightGear

*Watch out for all the ads on the website!* They all masquerade as download links.

Install FlightGear by visiting (https://www.flightgear.org/download/) and selecting the Windows version.  You'll be bounced to SourceForge for the download, and it may help to click 'Problems Downloading' and change to a UK mirror.  Time for a cup of tea: it's quite a big install.

### Python FlightGear Interface

Clone this repository somewhere on your PC: `git clone https://github.com/arthurrichards77/control_tutorial.git`

### The Allegro 2000 Aircraft

Run FlightGear and select the Aircraft tab in the start-up wizard.  Click Browse at the top centre and click Add Default Hangar over on the right.  You should see lots of aircraft.  Unselect the Filter option at the top left and then scroll down to Allegro 2000 (Wheels).  CLick install.

## Getting in the Air

### First Run and Testing

Start FlightGear from the Start menu and then
* In the aircraft tab, select the Allegro 2000
* In the location tab, choose Honolulu airport and runway 04L
* In the environment tab, ensure time says Morning
* In the settings tab, ensure that option `--props=5051` is included in the big command line box at the bottom
* Click Fly

Now, run Spyder by looking under ANaconda in your Start menu.  Once inside, load `test_interface.py` from your cloned `control_tutorial` folder and run it by pressing F5.  You should see numbers appear, changing but very close to zero, and if you go back over to FlightGear and press `H` (for head-up display) you should see an indicator move over on the left.  These mean, respectively, that Python is able to read your vertical speed and fiddle with your elevator.

![Ready for takeoff](https://github.com/arthurrichards77/control_tutorial/raw/master/.screenshots/Screenshot%202020-11-30%2015_03_52.png)

Kill the python script by pushing Ctrl+C in the console on the bottom right.  Now load `fgplot.py` and run it by pressing F5.  You should see a plot similar to the one below, either in a new window or in the Plots tab of the top right window pane.  You can run `fgplot.py` at any time, and the last set of signals both read from and written to FlightGear will be plotted for you.

![Test data plot](https://github.com/arthurrichards77/control_tutorial/raw/master/.screenshots/test_figure.png)

### First Flight

We're not here to learn to fly... but we need to get our aircraft in the air before we can do much.  The Allegro is a fairly forgiving trainer aircraft so will *almost* fly itself.  To take off:

1. Press 9 on the numeric keypad and hold for 5 seconds, to get the throttle all the way open.  (You might see a little knob move in the cockpit.)
2. Press } three times to turn on the ignition.
2. Press S and hold for a second to start the engine.
2. Press Shift+B to take the brake off.
3. Just let the aircraft accelerate and after about five seconds, hit the down arrow twice, and you should take to the air.  (If you really want to fly it, use 0 and Enter on the numeric keypad to steer using the rudder.)
4. When you get into the air, use the left and right arrow keys to bank, but use only small taps and then back to centre.  Try and keep yourself about level, but don't worry if you climb in a spiral - we just need to gain height.

> Need a breather?  Press P at any time to pause the simulator.

![Flying](https://github.com/arthurrichards77/control_tutorial/raw/master/.screenshots/takeoff.png)

Let's be lazy!  Although the Allegro aircraft has minimal avionics, FlightGear provides us with a generic autopilot to control it.  We need to get straight and level, flying north.

1. Press F11 to open the autopilot dialog.
2. Check the button next to "Heading Bug" and enter "0" as the desired heading.
3. Check the box next to "Heading Control"
4. Check the button next to "Vertical Speed" and ensure "0" is entered as the desired value.
5. Check the box next to "Pitch/Altitude Control"
6. Close the autopilot dialog and centre all other controls by pressing 5 on the numeric keypad.

![Autopilot](https://github.com/arthurrichards77/control_tutorial/raw/master/.screenshots/autopilot.png)

You should now be able to relax as your aircraft flies itself off over the island and out to sea (although watch out for the mountains, and use the vertical speed to climb more if you have to...)

> That should be it for the simulator.  I recommend you pause it when not experimenting.  If you crash, hit Shift+Esc to reset and start again from takeoff.

## Time to close a loop

Look inside the file `vs_p.py` (meaning vertical speed, proportional control) in Spyder.

First, the FlightGear client module is loaded and we make a new client.  We also turn off the autopilot pitch loop.
```python
from fgclient import FgClient
c = FgClient()
c.ap_pitch_off()
```
Next, we start an infinite loop.  The `c.tic()` call starts a timer in the client.  We are going to try a step change in vertical speed: the desired value `vs_des` jumps from 0 to 5 after 10 steps.
```python
kk = 0
while True:
  kk+=1
  c.tic()
  if kk>10:
    vs_des = 5.0
  else:
    vs_des = 0.0
```
Now a simple proportional controller.  Get the vertical speed, find the error between that and the desired vertical speed, and set the elevator to a multiple of that error.  The multiplier here, `-0.01`, is known as the *proportional gain*.  It's slightly weird for it to be negative: but in FlightGear, negative elevator points you upwards.
```python
  vs = c.vertical_speed_fps()
  c.set_elevator(-0.01*(vs_des - vs))
```
Finally we print the speed, just to watch, and then check the timer.  The `toc(0.5)` call means *wait until 0.5 seconds have passed since I last called tic()*.  It allows for the fact that talking to FlightGear burns some time.
```python
  print(vs)
  c.toc(0.5)
```

Run the file using F5 and watch your aircraft.  Did you see it climb?  Kill vs_p.py again using Ctrl+C.  To turn the autopilot back on and get yourself straight and level again, run `apreset.py`.

To see what happened in more detail, the client logs all the signals for us.  Use `ls logs` to see what's in the log file directory.  Files are tagged with the date and time they were started, so you should be able to choose the latest one.  To view the results as a graph, use `fgplot.py logs/fglog<date and time of your log>.csv`.  As a shortcut, `fgplot.py` will just use the last log created.

![Result plot](https://github.com/arthurrichards77/control_tutorial/raw/master/.screenshots/Figure_1.png)

### Time to do some work

Play around with the proportional gain and investigate its effect.  Pay particular attention to:
* Stability: do we converge at all?
* Overshoot: how far the other side to we go first?
* Time to reach target  - the *rise time* - even if shooting past it
* Steady state error: how close to 5 FPS do we get?

## Challenges

### PI control

Add *integral action* to your vertical speed controller, *i.e.* add a term to the control signal proportional to the integral of all past errors.

> No need to be too worried about accuracy: a simple cumulative sum of the errors will do for the integral.

Again, mess around with the gains, and identify which key measures (stability, overshoot, rise time, steady state error) are affected.  Here's an example of how it can work.

![PI example result](https://github.com/arthurrichards77/control_tutorial/raw/master/.screenshots/Figure_vs_pi.png)

### Nested control

Take your best vertical speed controller and add an *outer loop* that chooses the desired VS to control the altitude to a particular target.

> * Use `c.altitude_ft()` to retrieve the altitude
> * Just use small steps, say 10-50 feet.
> * Consider putting limits on what VS can be requested by the outer loop.

Mess around with the gain on the outer loop and evaluate the results, especially considering the rise times of the VS control and the altitude control.

> Sadly, the interface with the FlightGear telnet server seems pretty slow, and it can take more than 1/10th of a second to fetch or send a piece of data.  You might start seeing "overrun" messages with the nested loop, when you have to get altitude as well as vertical speed.  Try increasing the time step in the `toc()` call to stop the messages.

### Heading control

Adapt the VS controller to use heading control.  *Set the integral gain to zero to begin, but leave the code in place.*  Use `c.heading_deg()` to get the heading and `c.set_aileron(x)` to control the banking.

> This should be a disaster, weaving around the sky in ever-increasing oscillations.  Why?

### Derivative control

Add derivative action to your heading controller, *i.e.* add a term in the control signal that is proportional to the rate of change of the heading.  

> Again, no need to be too worried about accurate differentiation: you can just use simple differencing.

Investigate the effect of the gain on this term, *i.e.* the *derivative gain*.  Make sure you look at the aileron signal as well as the heading.  Here's an example.

![Example heading control result using PD](https://github.com/arthurrichards77/control_tutorial/raw/master/.screenshots/Figure_hdg_pd.png)

### PID

With the proportional and derivative gains at values you like, re-introduce the integral gain to your heading controller.  What is the effect?

This controller with all three elements is a standard and common type of controller: Proportional + Integral + Derivative or PID for short.

### Tuning

Can you tune your gains to achieve heading control to the following specification for a 15 degree heading change?
* Rise time (time to first reach 90% of step) less than 5s
* Overshoot <15% (i.e. go no more than 15% of 15 degrees beyond the target heading)
* Settling time (time to converge within 5% of the steo around the target heading) less than 20s

If this can't be done, how close can you get?  What must I compromise on?
