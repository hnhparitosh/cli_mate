import customtkinter as ctk
import tkintermapview as tkmap
from geopy.geocoders import Nominatim
import cli_mate

ctk.set_appearance_mode('system')
ctk.set_default_color_theme('blue')


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title('GUI-Mate for CLI-Mate')
        self.geometry('800x600')
        self.minsize(800, 600)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)

        self.marker = None
        self.geolocator = Nominatim(user_agent='geoapiExercises')
    
        # create two frames in the window
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.left_frame = ctk.CTkFrame(master=self,width=200, corner_radius=0, fg_color=None)
        self.left_frame.grid(row=0, column=0, padx=0, pady=0, sticky='nsew')

        self.right_frame = ctk.CTkFrame(master=self, corner_radius=0)
        self.right_frame.grid(row=0, column=1,rowspan=1, padx=0, pady=0, sticky='nsew')

        # left frame

        # create label for displaying the city name and weather details from cli_mate
        self.city_label = ctk.CTkLabel(master=self.left_frame, text='City Name', anchor='w')
        self.city_label.grid(row=0, column=0, padx=(20, 20), pady=(20, 0))

        self.weather_label = ctk.CTkLabel(master=self.left_frame, text='Weather Details', anchor='w')
        self.weather_label.grid(row=1, column=0, padx=(20, 20), pady=(20, 0))

        # right frame

        #  create map view
        self.map_view = tkmap.TkinterMapView(master=self.right_frame, corner_radius=0)
        self.map_view.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky='nsew')
        self.marker = self.map_view.set_marker(28.644800, 77.216721)

        self.map_view.add_left_click_map_command(self.add_marker_event)

        # set default values of map widget
        self.map_view.set_address("New Delhi")
        self.map_view.set_zoom(5)
        self.map_view.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)


    def add_marker_event(self, coords):
        self.marker.delete()
        self.marker = self.map_view.set_marker(coords[0], coords[1])
        location = self.geolocator.geocode(f'{coords[0]},{coords[1]}')
        location = self.geolocator.reverse(f'{coords[0]},{coords[1]}')
        print(location.raw)

    def on_closing(self, event=0):
        self.destroy()

    
        





    def start(self):
        self.mainloop()

if __name__ == '__main__':
    app = App()
    app.start()


