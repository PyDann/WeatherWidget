import json
import requests
import pyto_ui as ui
from UIKit import UIDevice
from datetime import timedelta
from datetime import datetime as dt

def get_weather():
	key = 'cde16970543bfe66b5ae315481806e1c'
	lat = '47.4824'
	lon = '-120.3978'
	url = 'https://api.darksky.net/forecast/{0}/{1},{2}'
	req = requests.get(url .format (key, lat, lon))
	api = req.json()

	cur = api['currently']
	frc = api['daily']
	now = int(dt.timestamp(dt.now()))

	dat = {
	'currently': cur,
	'forecast': frc,
	'stamp': now
	}

	with open('wthr.json', 'w+') as f:
		json.dump(dat, f)

	return dat

def need_update():
	now = dt.timestamp(dt.now())
	try:
		with open('wthr.json', 'r') as f:
			api = json.load(f)
		old_stamp = api['stamp']
		last_update = ((now - old_stamp) / 60)
		if last_update > 15:
			return True
		else:
			return False
	except IOError:
	#No Data File Found
		return True

if need_update():
	api = get_weather()
else:
	with open('wthr.json', 'r') as f:
		api = json.load(f)

emj = {
"fog": "☁️",
"wind": "💨",
"rain": "🌧",
"snow": "❄️",
"sunny": "☀️",
"clear": "☀️",
"sleet": "🌨",
"cloudy": "☁️",
"clear-day": "☀️",
"clear-night": "☁️",
"partly-cloudy-day": "🌤",
"partly-cloudy-night": "☁️"
}

max = 'temperatureMax'
min = 'temperatureMin'
frc = 'forecast'

view = ui.View()

today = dt.now()

icon = ui.Label()
icon.alpha = 1.0
icon.text = emj[api['currently']['icon']]
icon.font = ui.Font.system_font_of_size(45)
icon.size_to_fit()
icon.center = (40, 35)
view.add_subview(icon)

temp = ui.Label()
temp.alpha = 0.8
temp.text = str(round(api['currently']['temperature']))
temp.text += '°'
temp.font = ui.Font.system_font_of_size(30)
temp.size_to_fit()
temp.center = (40, 72)
view.add_subview(temp)

#Day of Week - ex: Monday
today_dow = ui.Label()
today_dow.alpha = 0.8
today_dow.text = today.strftime('%A').upper()
today_dow.font = ui.Font.system_font_of_size(10)
today_dow.size_to_fit()
today_dow.center = (100, 5)
view.add_subview(today_dow)

#Day of Month - ex: 14
today_dom = ui.Label()
today_dom.alpha = 0.8
today_dom.text = str(today.day)
today_dom.font = ui.Font.system_font_of_size(45)
today_dom.size_to_fit()
today_dom.center = (100, 35)
view.add_subview(today_dom)

hi_label = ui.Label()
hi_label.alpha = 0.8
hi_label.text = '↑'
hi_label.font = ui.Font.system_font_of_size(10)
hi_label.size_to_fit()
hi_label.center = (85, 65)
view.add_subview(hi_label)

today_hi = ui.Label()
today_hi.alpha = 0.8
today_hi.text = str(round(api[frc]['data'][0][max]))
today_hi.text += '°'
today_hi.font = ui.Font.system_font_of_size(10)
today_hi.size_to_fit()
today_hi.center = (105, 65)
view.add_subview(today_hi)

lo_label = ui.Label()
lo_label.alpha = 0.4
lo_label.text = '↓'
lo_label.font = ui.Font.system_font_of_size(10)
lo_label.size_to_fit()
lo_label.center = (85, 80)
view.add_subview(lo_label)

today_lo = ui.Label()
today_lo.alpha = 0.4
today_lo.text = str(round(api[frc]['data'][0][min]))
today_lo.text += '°'
today_lo.font = ui.Font.system_font_of_size(10)
today_lo.size_to_fit()
today_lo.center = (105, 80)
view.add_subview(today_lo)

#Icon Spacing
device = str(UIDevice.currentDevice.model)

if device == 'iPad':
	w = 40
if device == 'iPhone':
	w = 45

for i in range(1, 7):
	day = (today + timedelta(days=i))

	dayofweek = ui.Label()
	dayofweek.alpha = 0.4
	dayofweek.text = day.strftime('%a').upper()
	dayofweek.font = ui.Font.system_font_of_size(10)
	dayofweek.size_to_fit()
	dayofweek.center = (105+(w*i), 5)
	view.add_subview(dayofweek)
			
	dayofmonth = ui.Label()
	dayofmonth.alpha = 0.8
	dayofmonth.text = str(day.day)
	dayofmonth.font = ui.Font.system_font_of_size(14)
	dayofmonth.size_to_fit()
	dayofmonth.center = (105+(w*i), 24)
	view.add_subview(dayofmonth)

	icon = ui.Label()
	icon.text = emj[api[frc]['data'][i]['icon']]
	icon.size_to_fit()
	icon.center = (105+(w*i), 45)
	view.add_subview(icon)

	hi = ui.Label()
	hi.alpha = 0.8
	hi.text = str(round(api[frc]['data'][i][max]))
	hi.text += '°' 
	hi.font = ui.Font.system_font_of_size(10)
	hi.size_to_fit()
	hi.center = (105+(w*i), 65)
	view.add_subview(hi)
	
	lo = ui.Label()
	lo.alpha = 0.4
	lo.text = str(round(api[frc]['data'][i][min]))
	lo.text += '°'
	lo.font = ui.Font.system_font_of_size(10)
	lo.size_to_fit()
	lo.center = (105+(w*i), 80)
	view.add_subview(lo)

ui.show_view(view, ui.PRESENTATION_MODE_WIDGET)