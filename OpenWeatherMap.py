import datetime
import pyowm

PyOWM = pyowm.OWM(API_key='91eb722bb4c29a9db3283e6010325939', language="ru")

def GetWindDirectionName(degrees):
    if degrees <= 22.5:
        return "северный"
    elif degrees <= 67.5:
        return "северо-восточный"
    elif degrees <= 112.5:
        return "восточный"
    elif degrees <= 157.5:
        return "юго-восточный"
    elif degrees <= 202.5:
        return "южный"
    elif degrees <= 247.5:
        return "юго-западный"
    elif degrees <= 292.5:
        return "западный"
    elif degrees <= 337.5:
        return "северо-западный"
    else:
        return "северный"


def GetWeatherReport(observation):
    location = observation.get_location()
    weather = observation.get_weather()

    forecastTemperature = PyOWM.daily_forecast(location.get_name(), limit=1).get_forecast().get_weathers()[0].get_temperature(
        "celsius")

    data = dict(
        city=location.get_name(),
        time="{0:%H:%M}".format(datetime.datetime.now()),
        status=weather.get_detailed_status(),
        cloudiness=weather.get_clouds(),
        pressure=round(weather.get_pressure()["press"] * 0.75006375541921),
        currentTemp=round(weather.get_temperature("celsius")["temp"]),
        windSpeed=round(weather.get_wind()["speed"]),
        windDirection=GetWindDirectionName(weather.get_wind()["deg"]),
        nightTemp=round(forecastTemperature["night"]),
        dayTemp=round(forecastTemperature["day"])
    )

    return '''
Погода в городе {city} на сегодня в {time}:
{status}, облачность составляет {cloudiness}%, давление — {pressure} мм рт. ст., температура — {currentTemp}°C.
Ветер {windDirection}, {windSpeed} м/с.
Температура воздуха ночью — {nightTemp}°C, днём — {dayTemp}°C.
    '''.format(**data)

def ChoosePlacename():
    observations = PyOWM.weather_at_places(input('Введите название населенного пункта: '), 'like', 6)

    i = 0
    while i < len(observations):
        print(str(i+1) + '. ' + observations[i].get_location().get_name())
        i += 1

    i = int(input('Введите номер нужного населенного пункта: '))

    return observations[i - 1]


print(GetWeatherReport(ChoosePlacename()))