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

## First Flight

We're not here to learn to fly... but we need to get our aircraft in the air before we can do much.  The Cub is a fairly forgiving trainer aircraft so will *almost* fly itself.  To take off:

1. Press 9 on the numeric keypad and hold for 5 seconds, to get the throttle all the way open.  (You might see a little red knob move in the cockpit.)
2. Press S and hold for a second to start the engine.
3. Just let the aircraft accelerate.  It might lurch when the back wheel lifts off, but don't worry about staying on the runway - it'll get airborne anyway.  (If you really want to fly it, use 0 and Enter on the numeric keypad to steer using the rudder.)
4. When you get into the air, use the left and right arrow keys to bank, but use only small taps and then back to centre.  Try and keep yourself about level, but don't worry if you climb in a spiral - we just need to gain height.

> Need a breather?  Press P at any time to pause the simulator.

Let's be lazy!  Although the Cub aircraft has almost no avionics, FlightGear provides us with a generic autopilot to control it.  We need to get straight and level, flying south.

1. Press F11 to open the autopilot dialog.
2. Check the button next to "Heading Bug" and enter "180" as the desired heading.
3. Check the box next to "Heading Control"
4. Check the button next to "Vertical Speed" and ensure "0" is entered as the desired value.
5. Check the box next to "Pitch/Altitude Control"
6. Close the autopilot dialog and centre all other controls by pressing 5 on the numeric keypad.

You should now be able to relax as your aircraft flies itself off over the sea (although if you're in San Francisco, watch out for the mountains, and use the vertical speed to climb more if you have to...)
