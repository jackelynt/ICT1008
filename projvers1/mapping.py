import folium

# Base map location
filepath = 'templates/basemap.html'

# Creation of base map to show when application is ran
m = folium.Map(location = [1.290270, 103.851959], zoom_start=15)

# Markers to plot for show
folium.Marker([1.37982, 103.848995]).add_to(m)
folium.Marker([1.33349, 103.772830]).add_to(m)

# Save map to reference code (basemap.html) to app.py
m.save(filepath)