import folium

# https://www.youtube.com/watch?v=QpBmO35pmVE
# https://python-visualization.github.io/folium/quickstart.html
# https://python-graph-gallery.com/312-add-markers-on-folium-map/
# https://georgetsilva.github.io/posts/mapping-points-with-folium/

# declaration for now
filepath = 'templates/map.html'
# latitude = [1.405264, 1.4067, 1.3942];
# longitude = [103.902097, 103.9022, 103.9130];
# name = ['Punggol', 'Waterway Point', 'Punggol Plaza'];

# Create base map with starting location
# latitude, longitude
# Starting location - Punggol MRT
m = folium.Map(location=[1.4052, 103.9024], zoom_start=15, tiles='openstreetmap', icon=folium.Icon(color="red"))

# Get cordinates and plot
# change name if needed (shortest and quickest)
shortest_dist = folium.GeoJson(shortest, name = "Shortest Distance", style_function=style_function, icon=folium.Icon(color="blue"))
shortest_dist.add_to(m)

quickest_route = folium.GeoJson(quickest, name = "Shortest Distance", style_function=style_function, icon=folium.Icon(color="blue"))
quickest_route.add_to(m)

# Add lines
# folium.PolyLine(name, color="red", weight=2.5, opacity=1).add_to(m)
m.save(filepath)


# pgmap = fol.folium.Map(location=[1.403948, 103.909048], tiles='openstreetmap', zoom_start=15, truncate_by_edge=True)
#
# style_function = lambda feature: dict(
#     color="#FFD97B",
#     weight=1,
#     opacity=0.8)
#
# driveGraphL = fol.GeoJson(driveEdge, name="Public Roads", style_function=style_function)
# driveGraphL.add_to(pgmap)
#
# walkEdgeL = fol.GeoJson(walkEdge, name="Walking Path",  style_function=style_function)
# walkEdgeL.add_to(pgmap)
#
# lrtGraphL = fol.GeoJson(lrtEdge, name="LRT Track",  style_function=style_function)
# lrtGraphL.add_to(pgmap)
#
# fol.GeoJson(plotBuildingNodes, name='Buildings',  style_function=style_function).add_to(pgmap)
# fol.LayerControl(collapsed=True).add_to(pgmap)
#
# logoIcon = fol.features.CustomIcon('images/siticon.png', icon_size=(40, 40))
# SITtooltip = fol.Marker(location=[1.413006, 103.913249], popup='<strong>SIT New Punggol Campus</strong>', icon=logoIcon)
# SITtooltip.add_to(pgmap)
# fol.Marker(location=[getService(i)[2], getService(i)[3]], popup=getService(i)[1], icon=fol.Icon(color='red', icon='info-sign')).add_to(pgmap)
# print(getService(i)[5])
# print(getService(i)[6])
# # end point
# fol.Marker(location=[getService(i)[5], getService(i)[6]], popup=getService(i)[4], icon=fol.Icon(color='red', icon='info-sign')).add_to(pgmap)