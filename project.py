import requests
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import io
import datetime

API_KEY = "86135ec9a332de6650e92d2aabce798e"  # Replace with your OpenWeatherMap API key
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

# Utility function to fetch weather data
def get_weather(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to update GUI with weather info
def show_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name")
        return

    data = get_weather(city)
    if data:
        update_ui(data)
    else:
        messagebox.showerror("Error", "City not found or network issue")

# Function to update interface
def update_ui(data):
    city_name = data['name']
    country = data['sys']['country']
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    condition = data['weather'][0]['description'].title()
    icon_code = data['weather'][0]['icon']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    pressure = data['main']['pressure']
    time = datetime.datetime.now().strftime("%A, %d %B %Y | %I:%M %p")

    location_label.config(text=f"Weather in {city_name}, {country}")
    time_label.config(text=time)

    weather_details = (
        f"Temperature: {temp} °C\n"
        f"Feels Like: {feels_like} °C\n"
        f"Condition: {condition}\n"
        f"Humidity: {humidity}%\n"
        f"Wind Speed: {wind_speed} m/s\n"
        f"Pressure: {pressure} hPa"
    )
    result_label.config(text=weather_details)

    # Fetch and display weather icon
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
    icon_response = requests.get(icon_url)
    if icon_response.status_code == 200:
        img_data = icon_response.content
        img = Image.open(io.BytesIO(img_data))
        img = img.resize((100, 100))
        photo = ImageTk.PhotoImage(img)
        icon_label.config(image=photo)
        icon_label.image = photo
    else:
        icon_label.config(image='')
        icon_label.image = None

# GUI Setup
root = tk.Tk()
root.title("Live Weather App")
root.geometry("500x600")
root.config(bg="#282c34")
root.resizable(False, False)

# Styling
style = ttk.Style()
style.theme_use('clam')

# Top Frame (Title)
top_frame = tk.Frame(root, bg="#3c4043")
top_frame.pack(fill="x")

app_title = tk.Label(
    top_frame,
    text="☁️ Live Weather App ☀️",
    font=("Helvetica", 20, "bold"),
    bg="#3c4043",
    fg="white",
    pady=10
)
app_title.pack()

# Search Frame
search_frame = tk.Frame(root, bg="#282c34")
search_frame.pack(pady=20)

city_entry = tk.Entry(search_frame, font=("Helvetica", 14), width=25, justify='center')
city_entry.grid(row=0, column=0, padx=10)

search_btn = tk.Button(
    search_frame,
    text="Get Weather",
    command=show_weather,
    font=("Helvetica", 12),
    bg="#61dafb",
    fg="black",
    activebackground="#21a1f1",
    relief="flat",
    padx=10,
    pady=5
)
search_btn.grid(row=0, column=1)

# Output Frame
output_frame = tk.Frame(root, bg="#282c34")
output_frame.pack(pady=10)

location_label = tk.Label(
    output_frame,
    text="",
    font=("Helvetica", 16, "bold"),
    fg="white",
    bg="#282c34"
)
location_label.pack()

time_label = tk.Label(
    output_frame,
    text="",
    font=("Helvetica", 12),
    fg="gray",
    bg="#282c34"
)
time_label.pack()

icon_label = tk.Label(
    output_frame,
    bg="#282c34"
)
icon_label.pack(pady=10)

result_label = tk.Label(
    output_frame,
    text="",
    font=("Helvetica", 12),
    fg="white",
    bg="#282c34",
    justify="left"
)
result_label.pack()

# Footer
footer = tk.Label(
    root,
    text="Made with ❤️ using Python & OpenWeatherMap API",
    font=("Helvetica", 10),
    fg="gray",
    bg="#282c34"
)
footer.pack(side="bottom", pady=10)

root.mainloop()