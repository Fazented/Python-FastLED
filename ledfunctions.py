import customtkinter
import CTkColorPicker
import serial

previous_number = None

# Debug function, for when DebugMode is on
def debug():
    print("LED Functions Imported")



# App Functions

# Serial Sending command, takes all the arguments for a command and sends them
def send_serial(self, command_type, prefix, r, g, b, brightness, led_num, reset):
    # Checks if command is type 1, 2 or 3. Command 1 is rgb for all leds, command 2 is adressable leds, command 3 is just the command with brightness.
    if command_type == 1: 
        command = str(f"[{prefix},{r},{g},{b}]")
    elif command_type == 2:
        command = str(f"[{prefix},{r},{g},{b},{led_num},{reset}]")
    elif command_type == 3:
        command = str(f"[{prefix},{brightness}]")

    try:
        ser.write(command.encode())
    except NameError:
        if DebugMode == False:
            print("Serial Error, make sure \"port\" and \"BaudRate\" is set right, or enable DebugMode")
        else:
            print("Serial Error, unable to send command.")

    if DebugMode:
        print(f"Port is set to {port}")
        print(f"BaudRate is set to {baudRate}")
        print(f"Command Sent: {command}")
        print(f"Command Type: {command_type}")


  # Sets all LEDs to rgb from the colour picker
def set_rgb(self, hex):
    self.colourbutton.configure(border_color=hex)
    hex = hex.lstrip('#')

    # Sets up extra command values
    command_type = 1
    command_prefix = "RGB"            

    # Converts hex to RGB and sets r, g, b values.
    r = int(hex[0:2], 16)
    g = int(hex[2:4], 16)
    b = int(hex[4:6], 16)

    self.send_serial(command_type, command_prefix, r, g, b, False, False, False)


def set_individual(self, hex):
    hex = hex.lstrip('#')

    # Sets up extra command variables
    reset = reset_leds
    led = str(int(self.ledslider.get()))
    command_type = 2
    command_prefix = "Individual"

    # Converts hex to RGB and sets r, g, b values.
    r = int(hex[0:2], 16)
    g = int(hex[2:4], 16)
    b = int(hex[4:6], 16)

    self.send_serial(command_type, command_prefix, r, g, b, False, led, reset)

# Gets position of the LED Slider - Need to make it only send 1 output
def led_picker(self, led_position):
    global previous_number
    led_position = int(led_position)

    # Makes sure only one number is output to console
    if led_position != previous_number:
        print(f"Slider is at position {led_position}")
        previous_number = led_position


  # Sends the command in the command box, bypasses send_serial function
def send_command(self):
    command = self.command_entry.get() # Take the command from the command_entry field
    
    if command == "": #todo make this detect commands and give feedback to the user, like autocorrect
        pass
    else:
        self.send_serial(command)
    
    self.command_entry.delete(first_index=0, last_index=999999999)

    # Sends the serial command, prints debug info is DebugMode is True
    try:
        ser.write(command.encode())
    except NameError:
        if DebugMode == False:
            print("Serial Error, make sure \"port\" and \"BaudRate\" is set right, or enable DebugMode")
        else:
            print("Serial Error, unable to send command.")

    if DebugMode:
        print(f"Port is set to {port}")
        print(f"BaudRate is set to {baudRate}")
        print(f"Command Sent: {command}")
        print(f"Command Type: Custom User Command")