# QLock

![QLock logo](/img/qlock.webp)

QLock is a customizable and extensible home security system built on QNX and Python. This proof-of-concept is set up by `main.py` and run on a QNX Raspberry Pi as root with `python3 main.py`.

## Inspiration

We always found it impressive how QNX powers so many important computers in our lives, from medical equipment, to cars, to trains. We brought it upon ourselves to bring the the power of a resilient and modular Realtime OS like QNX into the home security landscape, so we built QLock.
 
## What it does

QLock secures your home by automatically locking doors when armed and monitors for any suspicious activities using its various sensors, like motion detectors and door sensors. The current status of the system is easily available to the homeowner through simple traffic light-style indicator lights and a screen.

## How we built it

We built QLock using the Realtime operating system, QNX, running on the Raspberry PI 5 Single Board Computer. The application running the security system itself is written in Python.

## Challenges we ran into

We aspired to add RFID key funcionality as well as camera capture, but we ran into challenges getting the SPI bus working as well as getting camera capture working.

## Accomplishments that we're proud of

This is the first time that any of us has worked with QNX in any way, as well as being our first hackathon for most of us, both of which we are proud of.

## What we learned

We learned the basics of QNX and how this operating system is used for critical software applications around the globe. We also learned what Hackathons are all about, how we might improve further in future events, and had fun while doing it!

## What's next for QLock

In the future we have plans for incorporating an RFID key system as well as a smart camera monitoring system that highlights intruders, as well as smart home integration to popular systems like HomeAssistant. We’d also like to incorporate software such as sentry to scale future development and Elevenlabs for smart warnings incorporating their AI tools.
