import customtkinter
import CTkColorPicker
import serial

# Debug function, for when DebugMode is on
def debug():
    print("App Functions Imported")


# App Functions
def change_appearance_mode_event(self, new_appearance_mode: str):
    print(f"Appearance Set to {new_appearance_mode}")
    customtkinter.set_appearance_mode(new_appearance_mode)

def change_scaling_event(self, new_scaling: str):
    new_scaling_float = int(new_scaling.replace("%", "")) / 100
    print(f"Scaling set to {new_scaling}")
    customtkinter.set_widget_scaling(new_scaling_float)
