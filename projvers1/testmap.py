import folium
import os
import webbrowser
filepath = 'templates/map.html'

m = folium.Map(location = [1.290270, 103.851959], zoom_start=15)

folium.Marker([1.37982, 103.848995]).add_to(m)
folium.Marker([1.33349, 103.772830]).add_to(m)

m.save(filepath)
webbrowser.open('file://' + filepath)