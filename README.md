# control_tutorial

Control tutorial examples using Flightgear simulator.

We're using aircraft as a case study for control because the dynamics responses are interesting but, 
for the trainer aircraft we'll experiment with, quite forgiving.  We'll use [FlightGear](https://www.flightgear.org/) as its free, makes a good 
job of representing the aircraft dynamics, and provides an easy back door for interfacing with external programs.
We will implement those programs in Python, using a custom interface class provided in this project.

## Install me!

Start by cloning this repository somewhere on your PC: `git clone https://github.com/arthurrichards77/control_tutorial.git`

## Getting started with FlightGear

Try running FlightGear with the Cub aircraft using `fgfs --aircraft=Cub --timeofday=morning --telnet=5051`

> If you get `Command fgfs not found` then you'll need to install FlightGear using `sudo apt install flightgear`.  Ask 
> staff to help if you're on one of our PCs.

> If you get `Requested aircraft (Cub) not found` then FlightGear is OK but hasn't come with the Cub aircraft model.  
> Different versions seem to ship with different aircraft as standard.  You'll need to download it yourself.  
> Move to a convenient folder, ideally the folder for this tutorial, and do the following:
> ```
> wget http://mirrors.ibiblio.org/flightgear/ftp/Aircraft/J3Cub.zip
> unzip J3Cub.zip
> ```
> Then you'll need to tell FlightGear where to find it when you run it:
> ```
> fgfs --aircraft=Cub --fg-aircraft=<directory where J3Cub was unzipped> --timeofday=morning --telnet=5051
> ```

> The 'timeofday' bit ensures you have daylight.  Otherwise FlightGear uses the real time at the simulated location - and it's dark in the Pacific.
> The 'telnet' bit opens a server port for us to access and manipulate the simulator data - this is the back door for Python. 

If all that worked, you should be looking at a bright yellow aircraft cockpit on a runway, either in Hawaii or San Francisco.

![Ready for takeoff](https://github.com/arthurrichards77/control_tutorial/raw/master/.screenshots/Screenshot%20from%202019-10-10%2009-35-38.png)

## First Flight

We're not here to learn to fly... but we need to get our aircraft in the air before we can do much.  The Cub is a fairly forgiving trainer aircraft so will *almost* fly itself.  To take off:

1. Press 9 on the numeric keypad and hold for 5 seconds, to get the throttle all the way open.  (You might see a little red knob move in the cockpit.)
2. Press S and hold for a second to start the engine.
3. Just let the aircraft accelerate.  It might lurch when the back wheel lifts off, but don't worry about staying on the runway - it'll get airborne anyway.  (If you really want to fly it, use 0 and Enter on the numeric keypad to steer using the rudder.)
4. When you get into the air, use the left and right arrow keys to bank, but use only small taps and then back to centre.  Try and keep yourself about level, but don't worry if you climb in a spiral - we just need to gain height.

> Need a breather?  Press P at any time to pause the simulator.

![Flying](https://github.com/arthurrichards77/control_tutorial/raw/master/.screenshots/Screenshot%20from%202019-10-10%2009-38-07.png)

Let's be lazy!  Although the Cub aircraft has almost no avionics, FlightGear provides us with a generic autopilot to control it.  We need to get straight and level, flying south.

1. Press F11 to open the autopilot dialog.
2. Check the button next to "Heading Bug" and enter "180" as the desired heading.
3. Check the box next to "Heading Control"
4. Check the button next to "Vertical Speed" and ensure "0" is entered as the desired value.
5. Check the box next to "Pitch/Altitude Control"
6. Close the autopilot dialog and centre all other controls by pressing 5 on the numeric keypad.

![Autopilot](https://github.com/arthurrichards77/control_tutorial/raw/master/.screenshots/Screenshot%20from%202019-10-10%2009-45-32.png)

You should now be able to relax as your aircraft flies itself off over the sea (although if you're in San Francisco, watch out for the mountains, and use the vertical speed to climb more if you have to...)

> That should be it for the simulator.  I recommend you pause it when not experimenting.  If you crash, hit Shift+Esc to reset and start again from takeoff.

## Setting up Python environment

We're going to need a few specialist bits in Python.  Specifically, we're going to use Python 3 and the Jupyter Notebook.  Installing different packages across different versions of Python can get really ugly - so we'll use a virtual environment to keep a tidy little Python world just for this activity.  To get set up:
```
python3 -m venv venv
source venv/bin/activate
pip list
```
You should now see a little `(venv)` tag before your linux prompt.  The result of `pip list` should be almost nothing.  Where did all your Python packages go?  The virtual environment has its own set of packages and we'll install just the ones we need.

> You only need to create the venv once.  If you open a new terminal, just run the `source venv/bin/activate` bit again.  If you want to get out again, type `deactivate`.

> Problems?  You might need to install pip for Python 3.  Try `sudo apt install python3-pip`.

Time to install the Python bits we need in our virtual environment.
```
pip install --upgrade pip
pip install scipy numpy matplotlib jupyter
```
For everything that follows, you should be in the virtual environment.

## Time to close a loop

Look inside the file `vs_p.py` (meaning vertical speed, proportional control) using your favorite text editor (`gedit`? `nano`?) to view it.

First, the FlightGear client module is loaded and we make a new client.  We also turn off the autopilot pitch loop.
```python
from fgclient import FgClient
c = FgClient()
c.ap_pitch_off()
```
Next, we start an infinite loop.  The `c.tic()` call starts a timer in the client.  We are going to try a step change in vertical speed: the desired value `vs_des` jumps from 0 to 5 after 10 steps.
```
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
```
  vs = c.vertical_speed_fps()
  c.set_elevator(-0.01*(vs_des - vs))
```
Finally we print the speed, just to watch, and then check the timer.  The `toc(0.5)` call means *wait until 0.5 seconds have passed since I last called tic()*.  It allows for the fact that talking to FlightGear burns some time.
```
  print(vs)
  c.toc(0.5)
```

Run the file using `python vs_p.py` and watch your aircraft.  Did you see it climb?  Kill vs_p.py again using Ctrl+C.  To turn the autopilot back on and get yourself straight and level again, use `python apreset.py`.

To see what happened in more detail, the client logs all the signals for us.  Use `ls logs` to see what's in the log file directory.  Files are tagged with the date and time they were started, so you should be able to choose the latest one.  To view the results as a graph, use `python fgplot.py logs/fglog<date and time of your log>.csv`.

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

Again, mess around with the gains, and identify which key measures (stability, overshoot, rise time, steady state error) are affected.

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

Investigate the effect of the gain on this term, *i.e.* the *derivative gain*.  Make sure you look at the aileron signal as well as the heading.

### PID

With the proportional and derivative gains at values you like, re-introduce the integral gain to your heading controller.  What is the effect?

This controller with all three elements is a standard and common type of controller: Proportional + Integral + Derivative or PID for short.

### Tuning

Can you tune your gains to achieve heading control to the following specification for a 15 degree heading change?
* Rise time (time to first reach 90% of step) less than 5s
* Overshoot <15% (i.e. go no more than 15% of 15 degrees beyond the target heading)
* Settling time (time to converge within 5% of the steo around the target heading) less than 20s

If this can't be done, how close can you get?  What must I compromise on?
