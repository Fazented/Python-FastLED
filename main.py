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
        
        # Main Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((1, 2), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
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
        
        # Sidebar Components
        
        # UI Scaling switcher label
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w") 
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        # UI Scaling switcher
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        # Appearance switcher
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 10))
        
        # Bottom bar
        
        # Command entry field
        self.command_entry = customtkinter.CTkEntry(self, placeholder_text="Enter Serial Command")
        self.command_entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        # Command send
        self.command_send = customtkinter.CTkButton(master=self, text="Send", fg_color="transparent", border_width=2, command=self.send_command, text_color=("gray10", "#DCE4EE"))
        self.command_send.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")


        # MAIN CONTENT 
        
        # Main Colour Picker
        self.colorpicker = CTkColorPicker(self, width=500, orientation="horizontal", command=lambda e: self.hex_to_rgb(e)) 
        self.colorpicker.grid(row=0, column=1, padx=10, pady=10)
        


        #temporary
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

    # add functions to app

    def hex_to_rgb(self, hex):
        self.colourbutton.configure(border_color=hex)
        hex = hex.lstrip('#')
        rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
        r = str(rgb[0])
        g = str(rgb[1])
        b = str(rgb[2])
        x = "[setRgb," + r + "," + g + "," + b + ",]"
        print(x)
        ser.write(x.encode())
    
    def change_appearance_mode_event(self, new_appearance_mode: str):
        print(f"Appearance Set to {new_appearance_mode}")
        customtkinter.set_appearance_mode(new_appearance_mode)
    
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        print(f"Scaling set to {new_scaling}")
        customtkinter.set_widget_scaling(new_scaling_float)
        
    def send_command(self):
        command = self.command_entry.get() # Take the command from the command_entry field
        
        if command == "":
            pass
        else:
            print(command)
            ser.write(command.encode()) # Encode and send command
        
        self.command_entry.delete(first_index=0, last_index=999999999)
        self.command_send.focus_set()


if __name__ == "__main__":
    app = App()
    app.mainloop()


