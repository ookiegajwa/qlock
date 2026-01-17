import homesecurity
import smbus
import time

# Define the I2C address of the PCF8574 I/O expander connected to the LCD
I2C_ADDR = 0x27

# LCD configuration constants
LCD_WIDTH = 16  # Number of characters per line
LCD_CHR = 1  # Data mode
LCD_CMD = 0  # Command mode
LCD_LINE_1 = 0x80  # Address for the first line
LCD_LINE_2 = 0xC0  # Address for the second line
LCD_BACKLIGHT = 0x00  # Backlight off (set to 0x08 to turn it on)
ENABLE = 0b00000100  # Enable bit to latch data

# Timing delays
E_PULSE = 0.0005  # Enable pulse duration
E_DELAY = 0.0005  # Delay between operations

bus = smbus.SMBus(1)

def lcd_init():
    global update_thread, LCD_BACKLIGHT
    lcd_byte(0b00110011, LCD_CMD)  # Reset sequence
    lcd_byte(0b00110010, LCD_CMD)  # Set to 4-bit mode
    lcd_byte(0b00000110, LCD_CMD)  # Set cursor move direction (left to right)
    lcd_byte(0b00001100, LCD_CMD)  # Display ON, cursor OFF, blink OFF
    lcd_byte(0b00101000, LCD_CMD)  # Function set: 2 lines, 5x8 font
    lcd_byte(0b00000001, LCD_CMD)  # Clear display
    time.sleep(E_DELAY)

    LCD_BACKLIGHT = 0x08
    lcd_byte(0x01, LCD_CMD)


def lcd_byte(bits, mode):
    """Sends a byte to the LCD in 4-bit mode."""
    bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT      # Upper nibble
    bits_low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT  # Lower nibble

    bus.write_byte(I2C_ADDR, bits_high)   # Send high bits
    lcd_toggle_enable(bits_high)

    bus.write_byte(I2C_ADDR, bits_low)    # Send low bits
    lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
    """Pulse the enable bit to latch data into the LCD."""
    time.sleep(E_DELAY)
    bus.write_byte(I2C_ADDR, (bits | ENABLE))   # Enable high
    time.sleep(E_PULSE)
    bus.write_byte(I2C_ADDR, (bits & ~ENABLE))  # Enable low
    time.sleep(E_DELAY)

def lcd_string(message, line):
    """Displays a message on the specified LCD line."""
    message = message.ljust(LCD_WIDTH, " ")  # Pad message with spaces to fill line
    lcd_byte(line, LCD_CMD)                 # Set cursor to the specified line
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)  # Send each character

async def marquee_smooth(message, line, delay=0.3, cycles=3):
    """Displays a scrolling marquee effect on the specified LCD line."""
    if len(message) < LCD_WIDTH:
        message = message.ljust(LCD_WIDTH)  # Pad if message is short

    scroll_text = message + " " * LCD_WIDTH  # Add space for smooth scrolling
    length = len(message) + LCD_WIDTH        # Total scroll length

    for cycle in range(cycles):              # Repeat for given number of cycles
        for pos in range(length):
            window = ""                      # Window of characters to show
            for i in range(LCD_WIDTH):
                window += scroll_text[(pos + i) % len(scroll_text)]
            lcd_string(window, line)         # Show scrolling window
            time.sleep(delay)                # Wait between steps

# -- Main events --

tripped_sensors = []
line1 = ""
line2 = ""
scroll_offset = 0
scroll_current = ""
scroll_old = ""

def on_arm():
    update_status()

def on_disarm():
    update_status()

def on_alarm():
    update_status()

def on_trip(sensor: homesecurity.Sensor):
    tripped_sensors.append(sensor)
    update_status()

def on_clear(sensor: homesecurity.Sensor):
    tripped_sensors.remove(sensor)
    update_status()

def update_status():
    global line1, line2, scroll_offset, scroll_current, scroll_old
    if homesecurity.state == 0:
        if len(tripped_sensors) == 0:
            line1 = "Ready"
            line2 = ""
        else:
            line1 = "Not ready"
            line2 = "Fault: "
            for sensor in tripped_sensors:
                line2 += sensor.zone + "; "
    elif homesecurity.state == 1:
        line1 = "Armed"
        line2 = "Secure"
    else:
        line1 = "ALARM"
        line2 = "In: "
        for sensor in homesecurity.alarm:
            line2 += sensor.zone + "; "

    lcd_string(line1, LCD_LINE_1)

    if line2 != scroll_old:
        scroll_offset = 0
        scroll_current = line2
        scroll_old = line2

    if len(line2) < LCD_WIDTH:
        lcd_string(line2, LCD_LINE_2)
    else:
        lcd_string(scroll_current, LCD_LINE_2)
        scroll_current = scroll_current[1:] + scroll_current[0]
