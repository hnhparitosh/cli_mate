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
        self.geometry('900x700')
        self.minsize(800, 600)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)

        self.marker = None
        self.geolocator = Nominatim(user_agent='geoapiExercises')

        # set default font
        self.default_font = ctk.CTkFont(family='Robot', size=20)
        self.big_font = ctk.CTkFont(family='Robot', size=24)
    
        # create two frames in the window
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=5)
        self.grid_rowconfigure(0, weight=1)

        self.left_frame = ctk.CTkFrame(master=self,width=200, corner_radius=0, fg_color=None)
        self.left_frame.grid(row=0, column=0, padx=0, pady=0, sticky='nsew')

        self.right_frame = ctk.CTkFrame(master=self, corner_radius=0)
        self.right_frame.grid(row=0, column=1,rowspan=1, padx=0, pady=0, sticky='nsew')

        # left frame
        self.left_frame.grid_columnconfigure(0, weight=1)
        # self.right_frame.grid_columnconfigure(1, weight=1)
        self.left_frame.grid_rowconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(1, weight=1)
        self.left_frame.grid_rowconfigure(2, weight=1)
        self.left_frame.grid_rowconfigure(3, weight=1)
        self.left_frame.grid_rowconfigure(4, weight=1)

        # create a label for current weather, temperature, wind speed, humidity and pressure
        self.current_weather_label = ctk.CTkLabel(master=self.left_frame, text='Current Weather:\n🌤️', anchor='w',font=self.default_font)
        self.current_weather_label.grid(row=0, column=0, padx=(20, 20), pady=(20, 0))

        self.temperature_label = ctk.CTkLabel(master=self.left_frame, text='Temperature:\n🌡️', anchor='w',font=self.default_font)
        self.temperature_label.grid(row=1, column=0, padx=(20, 20), pady=(20, 0))

        self.wind_speed_label = ctk.CTkLabel(master=self.left_frame, text='Wind Speed:\n💨', anchor='w',font=self.default_font)
        self.wind_speed_label.grid(row=2, column=0, padx=(20, 20), pady=(20, 0))

        self.humidity_label = ctk.CTkLabel(master=self.left_frame, text='Humidity:\n💧', anchor='w',font=self.default_font)
        self.humidity_label.grid(row=3, column=0, padx=(20, 20), pady=(20, 0))

        self.pressure_label = ctk.CTkLabel(master=self.left_frame, text='Pressure:\n🧊', anchor='w',font=self.default_font)
        self.pressure_label.grid(row=4, column=0, padx=(20, 20), pady=(20, 20))

        # right frame
        self.right_frame.grid_columnconfigure(0, weight=1)
        # self.right_frame.grid_columnconfigure(1, weight=1)
        self.right_frame.grid_rowconfigure(0, weight=0)
        self.right_frame.grid_rowconfigure(1, weight=1)

        # create a label for the city name
        self.city_name_label = ctk.CTkLabel(master=self.right_frame, text='📍 New Delhi, India', anchor='w',font=self.big_font)
        self.city_name_label.grid(row=0, column=0, padx=20, pady = 20)


        #  create map view
        self.map_view = tkmap.TkinterMapView(master=self.right_frame, corner_radius=0)
        self.map_view.grid(row=1, column=0,columnspan=2, padx=(0, 0), pady=(0, 0), sticky='nsew')
        
        self.map_view.add_left_click_map_command(self.add_marker_event)

        # set default values of map widget
        self.map_view.set_address("New Delhi")
        self.map_view.set_zoom(5)
        self.marker = self.map_view.set_marker(28.644800, 77.216721)
        self.get_weather_details((28.644800, 77.216721))
        self.map_view.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

    # function to get weather details of the city and display it in the left frame
    def get_weather_details(self, coords):
        weather_data = cli_mate.get_weather_by_coords(coords[0], coords[1])
        
        if weather_data:
            self.current_weather_label.configure(text='Current Weather:\n🌤️ '+str(weather_data['weather'][0]['main']))
            self.temperature_label.configure(text='Temperature:\n🌡️ '+str(weather_data['main']['temp'])+'°C')
            self.wind_speed_label.configure(text='Wind Speed:\n💨 '+str(weather_data['wind']['speed'])+' m/s')
            self.humidity_label.configure(text='Humidity:\n💧 '+str(weather_data['main']['humidity'])+'%')
            self.pressure_label.configure(text='Pressure:\n🧊 '+str(weather_data['main']['pressure'])+' hPa')
            # type emoji for Atmospheric pressure

        else:
            self.current_weather_label.configure(text='Current Weather:\n🌤️ --')
            self.temperature_label.configure(text='Temperature:\n🌡️ -- °C')
            self.wind_speed_label.configure(text='Wind Speed:\n💨 -- m/s')
            self.humidity_label.configure(text='Humidity:💧\n -- %')
            self.pressure_label.configure(text='Pressure:\n🧊 -- hPa')


    def add_marker_event(self, coords):
        self.marker.delete()
        self.marker = self.map_view.set_marker(coords[0], coords[1])
        location_data = self.geolocator.reverse(f'{coords[0]},{coords[1]}', language='en')
        
        #  get only state name from the location data
        try:
            location = location_data.raw['address']['state_district']+','+location_data.raw['address']['state']+','+location_data.raw['address']['country']
        except:
            location = location_data.raw['address']['state']+','+location_data.raw['address']['country']
    
        self.city_name_label.configure(text='📍 '+location)
        self.get_weather_details(coords)
        # print(location.raw)

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()

if __name__ == '__main__':
    app = App()
    app.start()


