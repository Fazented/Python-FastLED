import customtkinter
import CTkColorPicker
import serial
import time
#from tkfontawesome import icon_to_image

DebugMode = True  # Set to True to enable debugging tools

# Change these based on your arduino configuration
port = "/dev/ttyACM0"
baudRate = "115200"

Num_LEDS = 14 # Set this to the number of leds you have
Num_LEDS = Num_LEDS - 1  # this -1 is because i wrote the arduino code wrong
# i should probably fix this...

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
        self.geometry("700x575")
        self.minsize(700, 575)
        self.maxsize(700, 575)
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
        self.testcolours = customtkinter.CTkButton(self.sidebar_frame, text="Test LEDs", anchor="w", command=self.functions.leds_test)
        self.testcolours.grid(row=5, column=0, padx=20, pady=(10, 0))
        # UI Scaling switcher label
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w") 
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        # UI Scaling switcher
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.functions.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        # Appearance switcher
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"], command=self.functions.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 10))

        
        # Bottom bar (likely being removed)
        
        # # Command entry field
        # self.command_entry = customtkinter.CTkEntry(self, placeholder_text="Enter Serial Command")
        # self.command_entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        # # Command send
        # self.command_send = customtkinter.CTkButton(master=self, text="Send", fg_color="transparent", border_width=2, command=self.functions.send_command, text_color=("gray10", "#DCE4EE"))
        # self.command_send.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")



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
        tab1.grid_columnconfigure((0, 1), weight=0)
        tab1.grid_rowconfigure(0, weight=1)

        self.colorpicker = CTkColorPicker.CTkColorPicker(tab1, width=500, orientation="horizontal", command=lambda hex: self.functions.set_rgb(hex))
        self.colorpicker.grid(row=0, column=0, padx=10, pady=(10,0), sticky="nsew")
        
        self.colour_buttons = customtkinter.CTkFrame(tab1, width=100, corner_radius=0)
        self.colour_buttons.grid(row=0, column=1, sticky="n")

        self.red_button = customtkinter.CTkButton(self.colour_buttons, text=" ", width=27, fg_color="#ff1e02", hover_color="#7e2e00", command=self.functions.red_preset)
        self.red_button.grid(row=0, column=0, pady=(90, 5), sticky="nsw")

        self.orange_button = customtkinter.CTkButton(self.colour_buttons, text=" ", width=27, fg_color="#ff8208", hover_color="#b25b00", command=self.functions.orange_preset)
        self.orange_button.grid(row=1, column=0, pady=5, sticky="nsw")

        self.yellow_button = customtkinter.CTkButton(self.colour_buttons, text=" ", width=27, fg_color="#ffff00", hover_color="#b2b200", command=self.functions.yellow_preset)
        self.yellow_button.grid(row=2, column=0, pady=5, sticky="nsw")

        self.green_button = customtkinter.CTkButton(self.colour_buttons, text=" ", width=27, fg_color="#37f600", hover_color="#00a918", command=self.functions.green_preset)
        self.green_button.grid(row=3, column=0, pady=5, sticky="nsw")

        self.blue_button = customtkinter.CTkButton(self.colour_buttons, text=" ", width=27, fg_color="#0282ff", hover_color="#005bb2", command=self.functions.blue_preset)
        self.blue_button.grid(row=4, column=0, pady=5, sticky="nsw")

        self.purple_button = customtkinter.CTkButton(self.colour_buttons, text=" ", width=27, fg_color="#7403ff", hover_color="#762a7d", command=self.functions.purple_preset)
        self.purple_button.grid(row=5, column=0, pady=5, sticky="nsw")

        self.white_button = customtkinter.CTkButton(self.colour_buttons, text=" ", width=27, fg_color="#ffffff", hover_color="#b2b2b0", command=self.functions.white_preset)
        self.white_button.grid(row=6, column=0, pady=5, sticky="nsw")


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

    # Sends RGB values to the arduino
    def send_rgb(self, prefix, r, g, b):
        command_type = "RGB"
        command = str(f"[{prefix}, {r},{g},{b}]")
        
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
         
    # sends a preset command, for animations like "rainbow" etc
    def send_preset(self, preset):
        command_type = "Preset"
        command = str(f"[{preset}]")
        
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

        command_prefix = "RGB"            

        # Converts hex to RGB and sets rgb values.
        r = int(hex[0:2], 16)
        g = int(hex[2:4], 16)
        b = int(hex[4:6], 16)

        self.send_rgb(command_prefix, r, g, b)

    # Sends serial to an individual LED and resets others depending if reset = true or false
    def send_individual(self, prefix, r, g, b, led_num, reset):
        if reset:
            command = str(f"[{prefix},{r},{g},{b},{led_num},1]")
        else:
            command = str(f"[{prefix},{r},{g},{b},{led_num},0]")

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

    # takes hex code from the colour picker and sends it to the send_individual function
    def set_individual(self, hex):
        hex = hex.lstrip('#')

        # Sets up extra command variables
        reset = reset_leds
        led = str(int(self.app.ledslider.get()))
        command_prefix = "I" # I means Individual

        # Converts hex to RGB and sets r, g, b values.
        r = int(hex[0:2], 16)
        g = int(hex[2:4], 16)
        b = int(hex[4:6], 16)

        self.slider_command = [command_prefix, r, g, b, led, reset]

        self.send_individual(command_prefix, r, g, b, led, reset)

    # The individual LED picker. takes a position from the slider and updates the set_individual command with an LED address
    def led_picker(self, led_position):
        global previous_number
        led_position = int(led_position)

        # Makes sure only one number is output to console
        if led_position != previous_number:
            print(f"Slider is at position {led_position}")
            previous_number = led_position
            # print(f"Slider Command: {self.slider_command}")

            if self.slider_command is not None:
                self.slider_command[5] = led_position
                print(self.slider_command)
                self.send_individual(self.slider_command[0], self.slider_command[1], self.slider_command[2], self.slider_command[3], self.slider_command[4], self.slider_command[5])
            else:
                if DebugMode:
                    print(f"Individual LED command is not set. Currently {self.slider_command}")

    # Preset colour buttons
    def red_preset(self):
        self.send_rgb("RGB", 255, 0, 0)
        if DebugMode:
            print("Red Preset Selected")

    def orange_preset(self):
        self.send_rgb("RGB", 255, 127, 0)
        if DebugMode:
            print("Orange Preset Selected")

    def yellow_preset(self):
        self.send_rgb("RGB", 255, 255, 0)
        if DebugMode:
            print("Yellow Preset Selected")

    def green_preset(self):
        self.send_rgb("RGB", 0, 255, 0)
        if DebugMode:
            print("Green Preset Selected")

    def blue_preset(self):
        self.send_rgb("RGB", 0, 0, 255)
        if DebugMode:
            print("Blue Preset Selected")

    def purple_preset(self):
        self.send_rgb("RGB", 200, 0, 255)
        if DebugMode:
            print("Purple Preset Selected")

    def white_preset(self):
        self.send_rgb("RGB", 255, 255, 255)
        if DebugMode:
            print("White Preset Selected")


    # Tests each colour of the leds 5 times
    def leds_test(self):
        if DebugMode:
            print("Test Colours selected!")

        presets = [
            self.red_preset,
            self.orange_preset,
            self.yellow_preset,
            self.green_preset,
            self.blue_preset,
            self.purple_preset,
            self.white_preset
        ]
    
        for _ in range(5):  # Loop 5 times
            for preset in presets:
                preset()  # Call the preset method
                time.sleep(0.5)

        self.send_rgb("RGB", 0, 0, 0) #Turns LEDs off after button pressed



# Main App loop
if __name__ == "__main__":
    app = App()
    app.mainloop()
