# X-Control

A small script to map multiple keystrokes to the same joystick knob control. Primarily aimed at HOTAS knobs.

It is the second in my tools for X-Plane. However, you can probably use this with any other simulator or even game without issues.

## Demo of the script (YouTube)

[![X-Control: A Knobster replacement script in Python](https://img.youtube.com/vi/C5tbFqLlYGI/0.jpg)](https://www.youtube.com/watch?v=C5tbFqLlYGI)

## Why I made this script

There is a software named "Air Manager", sold by SimInnovations. It is made for flight simulator enthusiats, and offers quite a number of panels for a large array of planes, including touch screen support.

In addition to the software you can buy an individual piece of hardware named "Knobster". You connect it to your PC via USB.

Then, you start your simulator and AirManager, touch or click some control that is a knob in real life (for example the Altitude dual dials on a Garmin G1000), and turn the Knobster. The change will not only be reflected on the AirManager panel, but also of course in the simulator.

Sounds great, but I found AirManager with 69 EUR a bit too expensive - plus the Knobster, which is an additional 99 EUR. If you want touch screens too and you don't have them, well then these add to the cost on top of that.

## Another solution

In my case, I already have two touch screens, and a HOTAS which has dials clearly inspired from a G1000. On the throttle, there is a dual rotary encoder, and two single encoders.

Normally, you can only map them to do or change a certain value. For example only Altitude or your COM-frequency.

This script changes that.

It effectively enables a few dials on your setup to control multiple things in your cockpit.

## How X-Control works

It basically reads in the configuration file you provide, and then it checks against two things:

- Was a certain "Activator" key combo pressed
- React on the joystick button with the corresponding key combination to be pressed

One can freely change what should be changed or adjusted: altitude, Com frequency, Nav frequency... it is up to you really.

This means you can map any amount of key combos to the same joystick control - you only need to press the key combo to define which keys should be sent. There is no upper limit on that.

## Requirements

- One of these: Windows, Linux (or Unix-like), macOS
- Python 3.13+
- Ability to either create pip packages system wide OR
- Ability to create a Python virtual environment and install pip packages in that environment

**Important note:**
On Windows systems, this script may not require administrative priviliges to use the keyboard module and emulate keypresses. On Linux systems, you may need to run the script using the ```sudo``` command.

## Installation

Either
- clone this repository to a folder of your choice
- download the zip of this repo, and extract it to a folder of your choice

Then, you will need to install the required Python modules. I highly recommend creating a virtual environment within the folder where this script is located, to keep modules separate from other projects or installations you may have.

Navigate to the folder where this script is located, and open a terminal of your choice on your OS.

Next, instruct pip to install the needed modules:

```pip install -f ./requirements.txt```

This will everything you need.

## Usage

In essence, you run the script and tell the script which configration you want to use. In this repo, I have included my working example for my Turtle Beach FlightDeck Throttle.

- Navigate to the folder where this script is located
- Run Python with the script, plus the configuration file you want to use:

```python ./X-Control.py ./NameOfYourConfigFile.json```

## Configuration files

This repo contains a working example for the Turtle Beach FlightDeck Throttle, but chances are you have a different one. It is not too difficult to adjust this to your needs.

The configurations are JSON files. They basically describe the "activators" as I call them, and then which keys are emitted when a certain activator is active.

Put in the joystick ID of pygame first (see below on how to find the ID):

```
{
    "joy_id": 1
}
```

Next, you define the single activator key combinations, and what keys should be pressed if a button-down event was detect from a joystick rotary.

```
{
    "joy_id": 1,
    "triggers":
    [
    ]
}
```

Let's have a look at an example:

```
{
    "joy_id": 1,
    "triggers":
    [
        { "buttons": "31,32", "activator": "alt+shift+f1", "keys": "b,b", "mods": "ctrl,shift" },
        { "buttons": "31,32", "activator": "alt+shift+f2", "keys": "u,u", "mods": "ctrl,shift" }
    ]
}
```

The first row defines:

- monitor buttons 31 and 32 on the joystick (in my case, it's a single rotary encoder on the throttle)
- the activator key combination, I have chosen Alt+Shift+F1
- the virtual keyboard keys to be pressed - "B" in both cases, but Ctrl+B for button 31 and Shift+B for button 32

The second row is almost identical - except it is Alt+Shift+F2 which activates the second entry, and "u" with modifiers should be pressed when this dial is turned.

Have a look at my full sample config to get a complete picture.

## Finding the ID of a joystick

Simply run

```python ./X-Control.py --list```

## Testing a joystick to find its button numbers

Simply run

```python ./X-Control.py --test [joystick_number]```

If you ran the list command before, and the ID of your joystick is 2 for example, you would need to run

```python ./X-Control.py --test 2```

Press buttons and/or turn rotaries - you will see the button number.

And that should help you to build your own config.