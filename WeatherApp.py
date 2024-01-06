import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import requests
from datetime import datetime, timezone, timedelta
import customtkinter as ctk

BASE_URL = "https://api.openweathermap.org/data/2.5/"
API_KEY = "xxxx Your API Key xxxx"

PRIMARY_100 = "#F7BF7A"
PRIMARY_200 = "#CFB997"
PRIMARY_300 = "#FDF6FD"
ACCENT_100 = "#6F8AA1"
ACCENT_200 = "#9EB2C2"
TEXT_100 = "#F9F9F9"
TEXT_200 = "#DCDCDC"
BG_100 = "#567189"
BG_200 = "#7B8FA1"
BG_300 = "#3E5975"

class MainWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        master.title("Weather App")
        master.configure(bg=BG_100)

        # 天気情報の取得
        self.weather_info = Weather()
        self.weather_info.get_weather("Tokyo")
        self.set_widget()
    
    def set_widget(self):
        FONT_TITLE = ctk.CTkFont("arial", 32, "bold", "italic")
        FONT_MAIN = ctk.CTkFont("arial", 22)
        FONT_SMALL = ctk.CTkFont("arial", 18)

        # タイトルの配置
        self.title_label = ctk.CTkLabel(self.master, text="Weather App", fg_color=BG_200, text_color=TEXT_100, font=FONT_TITLE, corner_radius=8)
        self.title_label.pack(side=tk.TOP, pady=10, ipadx=20)

        # 検索キーワードフレームの配置 ===========================
        self. city_entry_frame = tk.Frame(self.master, bg=BG_100)
        self. city_entry_frame.pack(side=tk.TOP, pady=5)

        # 都市名ラベル
        self.city_label = tk.Label(self.city_entry_frame, text="City Name:", font=FONT_MAIN, bg=BG_100, fg=TEXT_200)
        self.city_label.pack(side=tk.LEFT, padx=5)

        # 都市名入力欄
        self.city_text = tk.StringVar()
        self.city_entry = ctk.CTkEntry(self.city_entry_frame, width=200, font=FONT_MAIN, fg_color=ACCENT_200, text_color=TEXT_100, textvariable=self.city_text)
        self.city_entry.pack(side=tk.LEFT)

        # Get Weatherボタン
        self.get_button = ctk.CTkButton(self.city_entry_frame, text="Get Weather", font=FONT_SMALL, fg_color=BG_300, text_color=TEXT_200, command=self.get_weather, cursor="hand2", hover_color=ACCENT_100)
        self.get_button.pack(side=tk.LEFT, padx=5)

        # 天気・気温フレームの配置 ===========================
        self.current_weather_frame = ctk.CTkFrame(self.master, fg_color=BG_200)
        self.current_weather_frame.pack(side=tk.LEFT, padx=20, ipadx=5)

        # 現在の天気アイコン
        self.current_weather_canvas = tk.Canvas(self.current_weather_frame, width=128, height=128, bg=PRIMARY_100)
        self.current_weather_canvas.pack(side=tk.TOP, pady=5)

        current_weather_org = Image.open("./images/" + self.weather_info.weather + ".png")
        self.current_weather_icon = current_weather_org.resize((120, 120), Image.LANCZOS)
        self.current_weather_icon = ImageTk.PhotoImage(self.current_weather_icon)
        self.current_weather_canvas.create_image(64, 64, image=self.current_weather_icon)

        # 現在の気温
        self.temp_label = ctk.CTkLabel(self.current_weather_frame, text=f"{self.weather_info.temp}℃", font=FONT_MAIN, fg_color=ACCENT_200, text_color=TEXT_200, corner_radius=8)
        self.temp_label.pack(side=tk.TOP, pady=5, ipadx=10)

        # 湿度・風速・視界フレームの配置 ===========================
        self.current_humid_frame = ctk.CTkFrame(self.master, fg_color=BG_200)
        self.current_humid_frame.pack(side=tk.LEFT, padx=20, pady=5)

        # 都市名
        self.city_name_label = tk.Label(self.current_humid_frame, text=self.weather_info.city_name, width=20, font=FONT_MAIN, bg=BG_200, fg=TEXT_100, cursor="hand2")
        self.city_name_label.pack(side=tk.TOP, pady=5)
        self.city_name_label.bind("<Button-1>", self.open_forecast_window)

        # 湿度
        self.humidity_label = ctk.CTkLabel(self.current_humid_frame, text=f"Humidity: {self.weather_info.humidity} %", font=FONT_SMALL, fg_color=ACCENT_200, text_color=TEXT_200, corner_radius=8)
        self.humidity_label.pack(side=tk.TOP, padx=5, pady=10, ipady=5, expand=True, fill=tk.X)

        # 視界
        self.visibility_label = ctk.CTkLabel(self.current_humid_frame, text=f"Visibility: {self.weather_info.visibility} m", font=FONT_SMALL, fg_color=ACCENT_200, text_color=TEXT_200, corner_radius=8)
        self.visibility_label.pack(side=tk.BOTTOM, padx=5, pady=10, ipady=5, expand=True, fill=tk.X)

        # 風向き画像
        self.wd_canvas = tk.Canvas(self.current_humid_frame, width=32, height=32, bg=PRIMARY_200)
        self.wd_canvas.pack(side=tk.LEFT, padx=5)

        wd_org = Image.open("./images/" + self.weather_info.wind_deg + ".png")
        self.wd_icon = wd_org.resize((30, 30), Image.LANCZOS)
        self.wd_icon = ImageTk.PhotoImage(self.wd_icon)
        self.wd_canvas.create_image(18, 18, image=self.wd_icon)

        # 風向き文字列
        self.wd_label = ctk.CTkLabel(self.current_humid_frame, text=f"{self.weather_info.wind_speed} m/s", font=FONT_SMALL, fg_color=ACCENT_200, text_color=TEXT_200, corner_radius=8)
        self.wd_label.pack(side=tk.LEFT, padx=5, ipady=5, expand=True, fill=tk.X)

    def get_weather(self):
        city_name = self.city_text.get()
        if city_name == "":
            # 都市名に未入力の場合は処理しない
            pass
        else:
            # 天気の取得
            self.weather_info.get_weather(city_name)

            # widgetの初期化
            self.city_entry_frame.pack_forget()
            self.title_label.pack_forget()
            self.current_weather_frame.pack_forget()
            self.current_humid_frame.pack_forget()

            # Widgetの描画
            self.set_widget()

    def open_forecast_window(self, e):
        city_name = self.city_name_label.cget("text")
        if city_name == "":
            # 都市名に未入力の場合は処理しない
            pass
        else:
            forecast_window = ForecastWindow(city_name)

class ForecastWindow:
    def __init__(self, city_name):
        self.forecast_window = tk.Toplevel(bg=BG_100)
        self.forecast_window.title("Forecast")
        # モーダルウィンドウにする
        self.forecast_window.grab_set()
        self.set_widget(city_name)

    def set_widget(self, city_name):
        FONT_TITLE = ctk.CTkFont("arial", 32, "bold", "italic")
        FONT_MAIN = ctk.CTkFont("arial", 22)
        FONT_SMALL = ctk.CTkFont("arial", 18)

        # タイトル
        self.forecast_title_label = ctk.CTkLabel(self.forecast_window, text="5 day weather forecast", fg_color=BG_200, text_color=TEXT_100, font=FONT_TITLE, corner_radius=8)
        self.forecast_title_label.pack(side=tk.TOP, pady=10, ipadx=10)

       # Closeボタン
        self.close_button = ctk.CTkButton(self.forecast_window, text="Close", fg_color=BG_300, text_color=TEXT_200, font=FONT_SMALL, command=self.close_window, cursor="hand2", hover_color=ACCENT_100)
        self.close_button.pack(side=tk.BOTTOM, padx=5, pady=5)

        # 5日予報の取得
        self.forecast = Forecast()
        self.forecast.get_forecast(city_name)

        # 5つの要素を持つ配列をダミー値0で作成
        self.day_frame = [0]*5
        self.date_label = [0]*5
        self.weather_canvas = [0]*5
        self.temp_label = [0]*5
        self.weather_icon = [0]*5

        for i in range(5):
            self.day_frame[i] = ctk.CTkFrame(self.forecast_window, fg_color=BG_200, width=50, height=50)
            self.day_frame[i].pack(side=tk.LEFT, padx=5, pady=5)

            # 日付
            date_jp = datetime.fromtimestamp(self.forecast.forecast[i].date, tz=timezone(timedelta(hours=9)))
            md = date_jp.strftime("%m/%d")
            day = date_jp.strftime("%a")
            self.date_label[i] = tk.Label(self.day_frame[i], text=f"{md}\n{day}", font=FONT_SMALL, bg=BG_200, fg=TEXT_200)
            self.date_label[i].pack(side=tk.TOP, padx=10)

            # 天気アイコン
            self.weather_canvas[i] = tk.Canvas(self.day_frame[i], width=96, height=96, bg=PRIMARY_100)
            self.weather_canvas[i].pack(side=tk.TOP, pady=5)

            weather_icon_org = Image.open("./images/" + self.forecast.forecast[i].weather +".png")
            self.weather_icon[i] = weather_icon_org.resize((90, 90), Image.LANCZOS)
            self.weather_icon[i] = ImageTk.PhotoImage(self.weather_icon[i])
            self.weather_canvas[i].create_image(50, 50, image=self.weather_icon[i])
            
            # 気温
            self.temp_label[i] = ctk.CTkLabel(self.day_frame[i], text=f"{self.forecast.forecast[i].temp}℃", font=FONT_MAIN, fg_color=ACCENT_100, text_color=TEXT_200, corner_radius=8)
            self.temp_label[i].pack(side=tk.TOP, padx=10, pady=5, ipadx=10)

    def close_window(self):
        self.forecast_window.destroy()

class Weather:
    def __init__(self):
        self.city_name = ""
        self.temp = 0
        self.weather = ""
        self.humidity = 0
        self.wind_deg = ""
        self.wind_speed = 0
        self.visibility = 0
        self.date = 0

    def get_weather(self, city_name):
        url = BASE_URL + "weather"
        response = requests.get(
            url,
            params={'q': city_name, 'appid': API_KEY, 'units': 'metric'})

        if response.status_code == 200:
            response_json = response.json()
            self.city_name = response_json["name"]
            self.temp = response_json["main"]["temp"]
            self.weather = response_json["weather"][0]["main"]
            self.humidity = response_json["main"]["humidity"]
            deg = int(response_json["wind"]["deg"])
            if (deg >= 0 and deg < 23) or (deg > 338):
                self.wind_deg = "N"
            elif deg >= 23 and deg < 68:
                self.wind_deg = "NE"
            elif deg >= 68 and deg < 113:
                self.wind_deg = "E"
            elif deg >= 113 and deg < 158:
                self.wind_deg = "SE"
            elif deg >= 158 and deg < 203:
                self.wind_deg = "S"
            elif deg >= 203 and deg < 248:
                self.wind_deg = "SW"
            elif deg >= 248 and deg < 293:
                self.wind_deg = "W"
            elif deg >= 293 and deg < 338:
                self.wind_deg = "NW"
            self.wind_speed = response_json["wind"]["speed"]
            self.visibility = response_json["visibility"]

        else:
            self.city_name = ""

class Forecast:
    def __init__(self):
        self.forecast = []

    def get_forecast(self, city_name):
        url = BASE_URL + "forecast"
        response = requests.get(
            url,
            params={'q': city_name, 'appid': API_KEY, 'units': 'metric'})

        if response.status_code == 200:
            response_json = response.json()
            for i in range(5):
                weather = Weather()
                weather.date = response_json["list"][i*8]["dt"]
                weather.weather = response_json["list"][i*8]["weather"][0]["main"]
                weather.temp = response_json["list"][i*8]["main"]["temp"]
                self.forecast.append(weather)

def close_window():
    root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    mainWindow = MainWindow(master=root)
    root.protocol("WM_DELETE_WINDOW", close_window)
    mainWindow.mainloop()