from tkinter import * 
from tkinter import messagebox
from configparser import ConfigParser
from PIL import ImageTk, Image
import requests

url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

def search():
    city = city_text.get()
    weather = get_weather(city)
    if(weather):
        location_lbl['text'] = weather[0]+","+weather[1]
        temp_lbl['text'] = str(weather[2])+"°C / "+str(weather[3])+"°F"
        weather_lbl['text'] = str(weather[5])
    else:
        messagebox.showerror(title = 'Error!', message='City Not Found')
        



config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']


#information needed to extract from API call 
# from json we will use 
# Temperature - F and celcuis , city_name, weather condition, 
# Icon name 
def get_weather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        json_data = result.json()
        city_name = json_data['name']
        country = json_data['sys']['country']
        temp_celcius = float(json_data['main']['temp']) - 273.15 
        temp_farenheit = (temp_celcius*(9/5)) + 32
        icon = json_data['weather'][0]['icon']
        weather = json_data['weather'][0]['main']
        final = (city_name, country , round(temp_celcius,2) , round(temp_farenheit,2), icon, weather)
        return final
    else:
        return None



app = Tk()
app.title('Weather App')
app.geometry('350x500')

city_text = StringVar()
city_entry  = Entry(app, textvariable=city_text)
city_entry.pack()

search_btn = Button(app, text = "search weather", width=12, command=search)
search_btn.pack()

location_lbl = Label(app, text='Location', font=('bold', 20))
location_lbl.pack()


canvas = Canvas(app, width = 200, height = 200)      
canvas.pack()      
img = PhotoImage(file="C:/Users/shubh/Desktop/Projects/Weather_app/icons/default.png")      
canvas.create_image(20,20, anchor=NW, image=img)  
# image1.pack(side = "bottom", fill = "both", expand = "yes")

temp_lbl = Label(app, text='temperature', font=(15))
temp_lbl.pack()

weather_lbl = Label(app , text = 'weather', font=(14))
weather_lbl.pack()


app.mainloop()
