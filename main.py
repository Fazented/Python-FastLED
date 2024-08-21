import customtkinter
import CTkColorPicker
import serial

DebugMode = True  # Set to True to enable debugging tools

# Change these based on your arduino configuration
port = "/dev/ttyACM0"
baudRate = "115200"

Num_LEDS = 14 - 1  # Set this to the number of leds you have, -1 is because i wrote the arduino code wrong

reset_leds = True  # Will make leds reset or stay the same if addressable leds are addressed

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

# Set ser as serial port and baud rate, as defined above
try:
    ser = serial.Serial(port, baudRate)
except serial.serialutil.SerialException:
    print("Serial Error, make sure port and Baudrate is set right, or enable DebugMode")

previous_number = None  # Used for making LED picker smoother, sending fewer commands over serial

# Prints debug info if DebugMode is True
if DebugMode:
    print(f"Port is set to: {port}")
    print(f"BaudRate is set to: {baudRate}")
    print(f"Reset LEDs set to: {reset_leds}")
    print(f"Number of LEDs: {Num_LEDS}")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.functions = AppFunctions(self)  # Create an instance of AppFunctions and pass App instance
        self.geometry("1000x675")
        #self.minsize(400, 300)
        #self.maxsize(1200, 850)
        self.title("PyLED")

        # Window Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure((1, 2), weight=0)


        # Sidebar frame
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        # Sidebar logo frame
        self.logo_frame = customtkinter.CTkFrame(self.sidebar_frame, width=100, fg_color="#212121", corner_radius=0)
        self.logo_frame.grid(row=0, column=0, sticky="nsew")
        # Sidebar title
        self.logo_label = customtkinter.CTkLabel(self.logo_frame, text="PyLED", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=1, padx=0, pady=(10, 10))
        # Sidebar logo (its just a button lol)
        self.colourbutton = customtkinter.CTkButton(self.logo_frame, width=30, border_width=6, corner_radius=10, state="disabled", text=" ", fg_color="transparent")
        self.colourbutton.grid(row=0, column=0, padx=(35, 10), pady=10)

        # Other Sidebar Components

        # self.tabs_frame = customtkinter.CTkFrame(self, width=80, fg_color="#4a4a49", corner_radius=10)
        # self.tabs_frame.grid(row=0, column=0, sticky="s")

        # self.tab_button = customtkinter.CTkButton(self.tabs_frame, text="RGB Control", anchor="w")
        # self.tab_button.grid(row=0,column=0, padx=5, pady=(5, 0))

        # self.tab_button2 = customtkinter.CTkButton(self.tabs_frame, text="Addressable Control", fg_color="#4a4a49", hover_color="#696969", anchor="w")
        # self.tab_button2.grid(row=1,column=0, padx=5, pady=(5, 0))

        # self.tab_button3 = customtkinter.CTkButton(self.tabs_frame, text="Effects", fg_color="#4a4a49", hover_color="#696969", anchor="w")
        # self.tab_button3.grid(row=2,column=0, padx=5, pady=(5, 0))

        # self.tab_button4 = customtkinter.CTkButton(self.tabs_frame, text="Settings", fg_color="#4a4a49", hover_color="#696969", anchor="w")
        # self.tab_button4.grid(row=3,column=0, padx=5, pady=(5, 5))

        # LED off button
        self.led_off_button = customtkinter.CTkButton(self.sidebar_frame, text="LEDs Off", anchor="w", command=self.functions.leds_off)
        self.led_off_button.grid(row=5, column=0, padx=20, pady=(10, 0))
        # UI Scaling switcher label
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w") 
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        # UI Scaling switcher
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.functions.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        # Appearance switcher
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"], command=self.functions.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 10))

        
        # Bottom bar
        
        # Command entry field
        self.command_entry = customtkinter.CTkEntry(self, placeholder_text="Enter Serial Command")
        self.command_entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        # Command send
        self.command_send = customtkinter.CTkButton(master=self, text="Send", fg_color="transparent", border_width=2, command=self.functions.send_command, text_color=("gray10", "#DCE4EE"))
        self.command_send.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")



        # MAIN CONTENT 
        
        # Tabs
        self.tabview = customtkinter.CTkTabview(self, width=500)
        self.tabview.grid(row=0, column=1, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.grid_columnconfigure(1, weight=1) # Makes tabview expand horizontal
        self.grid_rowconfigure(0, weight=1)    # Makes tabview expand vertical

        self.tabview.add("RGB Control")
        self.tabview.add("Addressable Control")
        self.tabview.add("Effects")
        self.tabview.add("Artnet Input")
        self.tabview.add("Config")
        self.tabview.add("Help")

        self.tabview.set("RGB Control")


        # Main Tab 1 (RGB Control) content
        tab1 = self.tabview.tab("RGB Control")
        tab1.grid_columnconfigure((0, 1, 2), weight=1)
        tab1.grid_rowconfigure(0, weight=1)

        self.colorpicker = CTkColorPicker.CTkColorPicker(tab1, width=500, orientation="horizontal", command=lambda hex: self.functions.set_rgb(hex))
        self.colorpicker.grid(row=0, column=1, padx=10, pady=10, sticky="ew")


        # Tab 2 (Addressable Control) content 

        tab2 = self.tabview.tab("Addressable Control")
        tab2.grid_columnconfigure((0, 1, 2), weight=1)
        tab2.grid_rowconfigure(0, weight=1)

        self.individual_picker = CTkColorPicker.CTkColorPicker(tab2, width=500, orientation="horizontal", command=lambda e: self.functions.set_individual(e))
        self.individual_picker.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.ledslider = customtkinter.CTkSlider(tab2, from_=0, to=Num_LEDS, orientation="vertical", height=500, width=25, number_of_steps=Num_LEDS, command=self.functions.led_picker)
        self.ledslider.grid(row=0, column=2, padx=10, pady=10, sticky="ns")


        # Tab 3 (Effects) content

        tab3 = self.tabview.tab("Effects")
        tab3.grid_columnconfigure((0, 1, 2), weight=1)
        tab3.grid_rowconfigure(0, weight=1)

        self.label_tab3 = customtkinter.CTkLabel(tab3, text="Effects Tab")
        self.label_tab3.pack(padx=20, pady=20)
        self.button_tab3 = customtkinter.CTkButton(tab3, text="Test Button, but again")
        self.button_tab3.pack(padx=20, pady=10)


        # Tab 4 (Artnet Input) content

        tab4 = self.tabview.tab("Artnet Input")
        tab4.grid_columnconfigure((0, 1, 2), weight=1)
        tab4.grid_rowconfigure(0, weight=1)

        self.label_tab4 = customtkinter.CTkLabel(tab4, text="Artnet Input Tab")
        self.label_tab4.pack(padx=20, pady=20)
        self.button_tab4 = customtkinter.CTkButton(tab4, text="Test Button, but again")
        self.button_tab4.pack(padx=20, pady=10)


        # Tab 5 (Config) content

        tab5 = self.tabview.tab("Config")
        tab5.grid_columnconfigure((0, 1, 2), weight=1)
        tab5.grid_rowconfigure(0, weight=1)

        self.label_tab5 = customtkinter.CTkLabel(tab5, text="Config Tab")
        self.label_tab5.pack(padx=20, pady=20)
        self.button_tab5 = customtkinter.CTkButton(tab5, text="Test Button, but again")
        self.button_tab5.pack(padx=20, pady=10)


        # Tab 6 (Help) content

        tab6 = self.tabview.tab("Help")
        tab6.grid_columnconfigure((0, 1, 2), weight=1)
        tab6.grid_rowconfigure(0, weight=1)

        self.label_tab6 = customtkinter.CTkLabel(tab6, text="Help Tab")
        self.label_tab6.pack(padx=20, pady=20)
        self.button_tab6 = customtkinter.CTkButton(tab6, text="Test Button, but again")
        self.button_tab6.pack(padx=20, pady=10)


# Contains all the functions for the app to run
class AppFunctions:
    def __init__(self, app):
        self.app = app
        self.slider_command = None

    def change_appearance_mode_event(self, new_appearance_mode: str):
        print(f"Appearance Set to {new_appearance_mode}")
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        print(f"Scaling set to {new_scaling}")
        customtkinter.set_widget_scaling(new_scaling_float)

    # LED/Serial control functions

    # Serial Sending command, takes all the arguments for a command and sends them
    def send_serial(self, command_type, prefix, r, g, b, brightness, led_num, reset):
        # Checks if command is type 1, 2 or 3. Command 1 is rgb for all leds, command 2 is addressable leds, command 3 is just the command with brightness.
        if command_type == 1: 
            command = str(f"[{prefix},{r},{g},{b}]")
        elif command_type == 2:
            if reset:
                command = str(f"[{prefix},{r},{g},{b},{led_num},1]")
            else:
                command = str(f"[{prefix},{r},{g},{b},{led_num},0]")
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
        self.app.colourbutton.configure(border_color=hex)
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
        led = str(int(self.app.ledslider.get()))
        command_type = 2
        command_prefix = "I"

        # Converts hex to RGB and sets r, g, b values.
        r = int(hex[0:2], 16)
        g = int(hex[2:4], 16)
        b = int(hex[4:6], 16)

        self.slider_command = [command_type, command_prefix, r, g, b, False, led, reset]

        self.send_serial(command_type, command_prefix, r, g, b, True, led, reset)


    # Gets position of the LED Slider
    def led_picker(self, led_position):
        global previous_number
        led_position = int(led_position)

        # Makes sure only one number is output to console
        if led_position != previous_number:
            print(f"Slider is at position {led_position}")
            previous_number = led_position
            # print(f"Slider Command: {self.slider_command}")

            if self.slider_command is not None:
                self.slider_command[6] = led_position
                print(self.slider_command)
                self.send_serial(self.slider_command[0], self.slider_command[1], self.slider_command[2], self.slider_command[3], self.slider_command[4], self.slider_command[5], self.slider_command[6], self.slider_command[7])
            else:
                if DebugMode:
                    print(f"Individual LED command is not set. Currently {self.slider_command}")


    def leds_off(self):
        if DebugMode:
            print("LED off was switched")
        self.send_serial(2, "RGB", 0, 0, 0, False, False, False)


    # Sends the command in the command box, bypasses send_serial function
    def send_command(self):
        command = self.app.command_entry.get()  # Take the command from the command_entry field
        
        if command == "":  # todo make this detect commands and give feedback to the user, like autocorrect
            pass
        else:
            self.send_serial(command)

        self.app.command_entry.delete(first_index=0, last_index=999999999)

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


if __name__ == "__main__":
    app = App()
    app.mainloop()
