import folium

def UpdateMap(RouteList):
    filepath = 'templates/map.html'
    #use to centralise the map
    centralLong = (RouteList[len(RouteList)-1][3] + RouteList[0][3]) / 2
    centralLat = (RouteList[len(RouteList)-1][2] + RouteList[0][2]) / 2
    m = folium.Map(location=[centralLong, centralLat], zoom_start=15)
    ##loop all items in list
    prevPoint = 0
    prevMark = "None"
    for Co in RouteList:
        if (Co[0] == "HDB"):
            #add marker for HDB
            folium.Marker([Co[3], Co[2]], popup="HDB!",
                          icon=folium.Icon(color='blue', icon='fas fa-building', prefix='fa'), tooltip=Co[1], zoom_start=30).add_to(m)
        elif(Co[0] == "Bus"):
            #add marker for
            folium.Marker([Co[3], Co[2]], popup="Bus!",
                          icon=folium.Icon(color='red', icon='fas fa-bus', prefix='fa'), tooltip=Co[1], zoom_start=30).add_to(m)
        else:
            # add marker for
            folium.Marker([Co[3], Co[2]], popup="MRT/LRT!",
                          icon=folium.Icon(color='green', icon='fas fa-subway', prefix='fa'), tooltip=Co[1], zoom_start=30).add_to(m)

        if prevPoint == 0:
            # on first run it will add prevPoint for drawing of line
            prevPoint = (Co[3], Co[2])
            prevMark = Co[0]
        else:
            # joins the last point to the current point to draw line
            points = [prevPoint, (Co[3], Co[2])]
            if (prevMark == "Bus" and Co[0] == "Bus"):
                folium.PolyLine(points, color="Blue").add_to(m)
                prevPoint = (Co[3], Co[2])
            elif (prevMark == "MRT" and Co[0] == "MRT"):
                folium.PolyLine(points, color="Red").add_to(m)
                prevPoint = (Co[3], Co[2])
            elif (prevMark == "LRT" and Co[0] == "LRT"):
                folium.PolyLine(points, color="purple").add_to(m)
                prevPoint = (Co[3], Co[2])
            else:
                folium.PolyLine(points, color="green").add_to(m)
                prevPoint = (Co[3], Co[2])

        # if prevPoint == 0:
        #     #on first run it will add prevPoint for drawing of line
        #     prevPoint = (Co[1], Co[2])
        #     prevMark = Co[0]
        # else:
        #     #joins the last point to the current point to draw line
        #     points = [prevPoint, (Co[1], Co[2])]
        #     folium.PolyLine(points, color="blue").add_to(m)
        #     prevPoint = (Co[1], Co[2])

    m.save(filepath)
    return ("nothing")