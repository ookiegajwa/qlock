# QNX GPIO Motion Monitor — Run Instructions

**Purpose**: This repository contains `gpio_motion_monitor.py`, a Python 3 script that polls a GPIO pin via the QNX device-file model and prints an alarm message on a LOW→HIGH (rising-edge) transition (default pin 17).

**File**: [gpio_motion_monitor.py](gpio_motion_monitor.py#L1)

**Quick Run (on the QNX target)**
- **Copy the script to the target** (replace user@target):

```bash
scp gpio_motion_monitor.py user@target:/home/user/
```

- **On the target, ensure Python 3 is installed** (QNX package manager or cross-deploy). Then make it executable and run with the DCMD value from your GPIO header:

```bash
chmod +x gpio_motion_monitor.py
# Example run (placeholder DCMD 0xDEADBEEF) — replace with real DCMD
./gpio_motion_monitor.py --dcmd 0xDEADBEEF --pin 17 --interval 0.1
```

**How to determine the correct DCMD/ioctl and data layout**
- On QNX, GPIO driver commands are normally defined in target headers (e.g. `/usr/include/sys/gpio.h` or vendor-specific headers). Look for `#define` names referencing `DCMD` or `GPIO`.
- Useful commands on the QNX target to locate definitions:

```bash
grep -R "gpio" /usr/include 2>/dev/null | sed -n '1,200p'
grep -R "DCMD" /usr/include/sys 2>/dev/null | sed -n '1,200p'
```

- Open the header that defines the read command (example path may vary):

```bash
cat /usr/include/sys/gpio.h | sed -n '1,240p'
```

- If the header uses macros like `_DCMD_MISC(...)`, you must expand/compute the numeric value; often the driver vendor documentation or header comments show the final value. If you paste the header snippet here I can compute or embed the numeric constant for you.

**struct-format / ABI**
- `gpio_motion_monitor.py` accepts `--struct-format` to specify the `struct.pack/unpack` format string used for packing the pin number and unpacking the returned value. Default is `'I'` (unsigned int). If your driver uses a struct (e.g., `struct gpio_read { unsigned int pin; unsigned int value; }`), set `--struct-format` accordingly or modify the script to use a custom pack/unpack sequence.

**Example: run with a known ABI**
- If the driver expects a single unsigned int (pin) and returns an unsigned int (value), run:

```bash
./gpio_motion_monitor.py --dcmd 0x12345678 --pin 17 --interval 0.2 --struct-format I
```

**Permissions and device path**
- Ensure the user running the script has permission to open the GPIO device file (often `/dev/gpio` or driver-specific path). Use `ls -l /dev/gpio*` to inspect.

**Troubleshooting**
- If the script prints `ERROR: DCMD/ioctl value not provided.`, provide `--dcmd` or edit the `GPIO_IOCTL_READ` constant in the script.
- If `fcntl.ioctl` raises `ENODEV` or `EBADF`, verify the device path and that the driver is loaded.
- If read values look incorrect, try different `--struct-format` values (e.g., `H`, `I`, `L`) or adapt the script to pack/unpack a custom struct.

**Next steps I can help with**
- Embed the exact DCMD and struct layout if you paste the header snippet here.
- SSH-run the script on your QNX target if you grant access details or provide command outputs (header contents, `ls -l /dev`) and I will tailor the script.

--
Generated to help deploy `gpio_motion_monitor.py` on a QNX Neutrino target. If you want, paste the GPIO header snippet and I'll update the script with the resolved DCMD and ABI.
