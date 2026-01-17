#!/usr/bin/env python3
"""
QNX GPIO motion monitor (polling)

QNX-specific notes:
- Uses os.open() and os.devctl() against a QNX device-file (e.g. /dev/gpio)
- The DCMD (devctl command) and data layout are driver-specific
- Provide --dcmd at runtime or set GPIO_IOCTL_READ below
- Default behavior assumes sensor outputs 1 when motion is detected
"""

import os
import struct
import time
import sys
import errno
import signal
import argparse

# Optional integration
try:
    import homesecurity
except Exception:
    homesecurity = None

# --------------------
# Defaults
# --------------------

GPIO_DEVICE = "/dev/gpio"
PIN = 17
POLL_INTERVAL = 0.1  # seconds

# Leave None unless you know the correct value from QNX headers
GPIO_IOCTL_READ = None

# Default ABI:
# pin (unsigned int), value (unsigned int)
DEFAULT_STRUCT_FORMAT = "II"

# --------------------
# Signal handling
# --------------------

def sigint_handler(signum, frame):
    print("\nExiting on signal", signum)
    sys.exit(0)

# --------------------
# GPIO helpers
# --------------------

def open_gpio_device(path):
    try:
        return os.open(path, os.O_RDONLY)
    except OSError as e:
        print(f"Failed to open GPIO device '{path}': {e}")
        raise


def read_gpio_pin_devctl(fd, pin, dcmd, struct_fmt):
    """
    Read a GPIO pin using QNX devctl().
    The struct layout MUST match the driver ABI.
    """
    buf = struct.pack(struct_fmt, pin, 0)

    try:
        ret = os.devctl(fd, dcmd, buf)
    except OSError:
        raise

    _, value = struct.unpack(struct_fmt, ret)
    return 1 if value else 0


# --------------------
# Motion monitor
# --------------------

def monitor_motion(device_path, pin, poll_interval, zone, dcmd,
                   struct_fmt, simulate=False):

    if dcmd is None and not simulate:
        print("ERROR: DCMD/devctl value not provided. Use --dcmd or set GPIO_IOCTL_READ.")
        return 2

    fd = None
    try:
        if not simulate:
            fd = open_gpio_device(device_path)
    except OSError:
        print("Cannot proceed without GPIO device.")
        return 1

    print(f"Monitoring GPIO pin {pin} (poll {poll_interval}s)")
    if simulate:
        print("Running in SIMULATION mode")

    last_val = None
    sim_state = 0

    try:
        while True:
            try:
                if simulate:
                    val = sim_state
                    sim_state = 1 - sim_state
                else:
                    val = read_gpio_pin_devctl(fd, pin, dcmd, struct_fmt)

            except OSError as e:
                if e.errno == errno.EINTR:
                    continue

                print(f"GPIO devctl read failed: {e}")

                if e.errno in (errno.EBADF, errno.ENODEV):
                    print("GPIO device unavailable — stopping.")
                    break

                time.sleep(poll_interval)
                continue

            val = 1 if val else 0

            if last_val is None:
                last_val = val

            if last_val == 0 and val == 1:
                ts = time.strftime('%Y-%m-%d %H:%M:%S')
                print(f"ALARM: motion detected on pin {pin} at {ts}")

                if homesecurity is not None:
                    try:
                        sensor = homesecurity.Sensor(zone)
                        homesecurity.trip(sensor)
                    except Exception as e:
                        print(f"homesecurity error: {e}")

            last_val = val
            time.sleep(poll_interval)

    except KeyboardInterrupt:
        print("\nKeyboard interrupt received. Exiting.")
    finally:
        if fd is not None:
            try:
                os.close(fd)
            except Exception:
                pass

    return 0

# --------------------
# Argument parsing
# --------------------

def parse_args():
    p = argparse.ArgumentParser(description="QNX GPIO motion monitor")
    p.add_argument("--device", "-d", default=GPIO_DEVICE,
                   help="GPIO device file (default: /dev/gpio)")
    p.add_argument("--pin", "-p", type=int, default=PIN,
                   help="GPIO pin number")
    p.add_argument("--interval", "-i", type=float, default=POLL_INTERVAL,
                   help="Polling interval (seconds)")
    p.add_argument("--dcmd",
                   help="DCMD/devctl numeric value (hex 0x... or decimal)")
    p.add_argument("--struct-format", default=DEFAULT_STRUCT_FORMAT,
                   help="struct.pack/unpack format (default: 'II')")
    p.add_argument("--simulate", action="store_true",
                   help="Run without GPIO hardware (simulation mode)")
    p.add_argument("--zone", default="default",
                   help="Security zone name")
    return p.parse_args()

# --------------------
# Main
# --------------------

def main():
    signal.signal(signal.SIGINT, sigint_handler)
    signal.signal(signal.SIGTERM, sigint_handler)

    args = parse_args()

    # Resolve DCMD
    dcmd = GPIO_IOCTL_READ
    if args.dcmd:
        try:
            dcmd = int(args.dcmd, 0)
        except ValueError:
            print("Invalid --dcmd value; use hex (0x...) or decimal")
            sys.exit(3)

    rc = monitor_motion(
        device_path=args.device,
        pin=args.pin,
        poll_interval=args.interval,
        zone=args.zone,
        dcmd=dcmd,
        struct_fmt=args.struct_format,
        simulate=args.simulate
    )

    # Ensure an integer exit code is returned to the caller; allow
    # the outer `if __name__` block to call `sys.exit()` with it.
    try:
        return int(rc)
    except Exception:
        return 1


if __name__ == "__main__":
    sys.exit(main())
