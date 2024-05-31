import customtkinter
from CTkColorPicker import *
from PIL import Image
import serial

# Change them based on your arduino configuration
port = "COM3"
baudRate = "9600"
#todo - add try except for SerialException'

# Set ser as serial port COM3 at 9600 baud rate
ser = serial.Serial(port, baudRate)

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("810x600")
        self.minsize(400, 300)
        self.maxsize(1200, 850)
        self.title("PyLED")

        def hex_to_rgb(hex):
            self.colourbutton.configure(border_color=hex)
            hex = hex.lstrip('#')
            rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
            r = str(rgb[0])
            g = str(rgb[1])
            b = str(rgb[2])
            x = "[setRgb," + r + "," + g + "," + b + ",]"
            print(x)
            ser.write(x.encode())
            
        def send_command(command):
            print(command)
            #ser.write(command.encode())
        
        # Configure UI Grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((1, 2), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        # app widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0) # sidebar
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="PyLED", font=customtkinter.CTkFont(size=20, weight="bold")) # Sidebar Header
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w") # UI Scaling Label
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event) # UI Scaling Switcher
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"], command=self.change_appearance_mode_event) # Appearance Switcher
        self.appearance_mode_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 10))
        
        #Bottom bar
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Enter Serial Command") # Command Entry
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        
        self.main_button_1 = customtkinter.CTkButton(master=self, text="Send", fg_color="transparent", border_width=2, command=send_command(1), text_color=("gray10", "#DCE4EE")) # Command Send
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
            
            
        #Main Content 
        self.colorpicker = CTkColorPicker(self, width=500, orientation="horizontal", command=lambda e: hex_to_rgb(e)) # Colour Picker
        self.colorpicker.grid(row=0, column=1, padx=10, pady=10)
        
        self.colourbutton = customtkinter.CTkButton(self.sidebar_frame, width=28, border_width=5, corner_radius=10, state="disabled", text=" ", fg_color="transparent", command=self.button_click)
        self.colourbutton.grid(row=3, column=0, padx=20, pady=10)




        #Placeholder Buttons
#        self.button = customtkinter.CTkButton(self, text="test button 1", command=self.button_click)
#        self.button.grid(row=0, column=0, padx=20, pady=10)
#
#        self.button = customtkinter.CTkButton(self, text="test button 2", command=self.button_click)
#        self.button.grid(row=0, column=1, padx=20, pady=10)
#        self.button = customtkinter.CTkButton(self, text="test button 3", command=self.button_click)
#        self.button.grid(row=0, column=2, padx=10, pady=10)
#
#        self.button = customtkinter.CTkButton(self, text="test button 4", command=self.button_click)
#        self.button.grid(row=1, column=1, padx=10, pady=10)
#        self.button = customtkinter.CTkButton(self, text="test button 5", command=self.button_click)
#        self.button.grid(row=1, column=2, padx=10, pady=10)
#
#        self.button = customtkinter.CTkButton(self, text="test button 6", command=self.button_click)
#        self.button.grid(row=2, column=1, padx=10, pady=10)
#        self.button = customtkinter.CTkButton(self, text="test button 7", command=self.button_click)
#        self.button.grid(row=2, column=2, padx=10, pady=10)

    # add methods to app
    def button_click(self):
        print("Button Pressed")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        print(f"Appearance Set to {new_appearance_mode}")
        customtkinter.set_appearance_mode(new_appearance_mode)
    
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        print(f"Scaling set to {new_scaling}")
        customtkinter.set_widget_scaling(new_scaling_float)
        



if __name__ == "__main__":
    app = App()
    app.mainloop()


