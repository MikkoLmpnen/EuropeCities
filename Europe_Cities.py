# -*- coding: utf-8 -*-
# Mikko Lampinen, Tampere
# May, 2021
# The program asks Cities of Europe to locate them in the map, by clicking as near the right location
# and as quickly you can.

from tkinter import *
import math
import random
from time import time
import codecs

class City:

    def __init__(self, lat, long, name):
        self.latitude = lat
        self.longitude = long
        self.name = name

    def get_name(self):
        return self.name


#           F U N C T I O N S   I N   A L P H A B E T I C A L   O R D E R

def ask_city():
    global index
    global taken
    global total_pts
    global canvas_clicked
    global t1
    global latitude
    global longitude

# asks 10 cities

    if index < 10:
        ask_btn.config(state=DISABLED)  # cant accidentally ask another city before answered
        if index < 1:
            taken = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # DON'T ASK THE SAME CITY TWICE

        city_asked_before = False
        random_city = random.randint(1, 103)
        for counter in range(0, 10):
            if taken[counter] == random_city:
                city_asked_before = True

        if not city_asked_before:
            taken[index] = random_city

            header2_txt = str(index + 1) + ". " + city[random_city].get_name()
            header2.config(text=header2_txt)
            label1.config(text="")
            label2.config(text="")
            label3.config(text="")
            label4.config(text="")
            label5.config(text="")

            latitude = city[random_city].latitude
            longitude = city[random_city].longitude

            t1 = time()
            delay = 0
            while delay < 2:
                delay = delta_t()

            canvas_clicked = False
            index += 1
            t1 = time()

        else:
            ask_city()

# AFTER 10 CITIES ASKED DISPLAYS BEST SCORES AND NAMES AND CHECK IF CURRENT SCORE IS TOP 5

    else:
        player_name = name.get()
        player_name = player_name.replace(";", " ")
        if len(player_name) > 10:
            player_name = player_name[:10]

        header2_txt = "Top 5 scores! (Your score:" + str(total_pts) + ")"
        best_details = []
        with codecs.open("best_of_europe.csv", "r", "utf8") as bestfile:
            for row in bestfile:
                best_details = row.split(";")

        for i in range(0, 16, 2):
            best_pts = int(best_details[i])
        # best_details[0] = 1.score, best_details[1] = 1.name, best_details[2] = 2.score, best_details[3] = 2.name, etc.

            if total_pts > best_pts and total_pts > 0:
                best_details.insert(i, str(total_pts))  # insert total points into top 5 to index i
                best_details.insert(i + 1, player_name)  # e.g. 950,Mikko,945,Lotta,930,Liina,etc.
                total_pts = -1  # points down, so it dont insert points twice,
                # (total_points = -1) is also a "sign" to save top 5

        # DISPLAY TOP 5
        label1_txt = "1. " + best_details[0] + (17 - 2 * len(best_details[0])) * " " + best_details[1]
        label2_txt = "2. " + best_details[2] + (17 - 2 * len(best_details[2])) * " " + best_details[3]
        label3_txt = "3. " + best_details[4] + (17 - 2 * len(best_details[4])) * " " + best_details[5]
        label4_txt = "4. " + best_details[6] + (17 - 2 * len(best_details[6])) * " " + best_details[7]
        label5_txt = "5. " + best_details[8] + (17 - 2 * len(best_details[8])) * " " + best_details[9]

        header2.config(text=header2_txt)
        label1.config(text=label1_txt)
        label2.config(text=label2_txt)
        label3.config(text=label3_txt)
        label4.config(text=label4_txt)
        label5.config(text=label5_txt)

    # SAVING NEW TOP 5 ????

        if total_pts == -1:         # total points has been in top 5
            txt_to_save = ""
            for item in best_details:
                txt_to_save += item + ";"

            with codecs.open("best_of_europe.csv", "w", "utf8") as writefile:  # write new top 5
                writefile.write(txt_to_save)

        new_game()


def bigger_map():
    global pplatitude
    pplatitude += 0.5
    new_map()


def canvas_click(event):
    global canvas_clicked
    global label1
    global label3
    global label5
    global total_pts
    ask_btn.config(state=NORMAL)  # can ask new city from now on

    if not canvas_clicked:                  # cant click twice
        canvas_clicked = True
        answer_time = delta_t()

    # POINTS THE RIGHT SPOT WITH RED CIRCLE

        right_y = convert_to_y(latitude)
        right_x = convert_to_x(latitude, longitude)
        canvas.create_oval(right_x - 2, right_y - 2, right_x + 2, right_y + 2, fill="red")

    # PINPOINTS THE ANSWER

        click_x = event.x
        click_y = event.y
        pin_x = click_x + 10                                           # pin_x and pin_y are for pinpoint line
        pin_y = click_y - 15
        canvas.create_line(click_x, click_y, pin_x, pin_y)
        canvas.create_oval((pin_x - 2, pin_y - 3, pin_x + 3, pin_y + 2), fill="blue")

    # CONVERTS CLICKED Y AND X TO LATITUDE AND LONGITUDE

        pplongitude = pplatitude * math.cos(latitude * math.pi / squash_north)
        click_latitude = convert_to_latitude(click_y)
        click_longitude = convert_to_longitude(click_x, pplongitude)

    # CALCULATING DISTANCE OF CLICKED POSITION AND RIGHT LOCATION (KM)

        kmy = (latitude - click_latitude) * 10000 / 90  # distance y component
        north_latitude = click_latitude
        if latitude < click_latitude:
            north_latitude = latitude
        kmx = (longitude - click_longitude) * 10000 * math.cos(north_latitude * math.pi / 180) / 90

        distance = math.sqrt((kmy * kmy) + (kmx * kmx))  # pythagoras is close enough
        distance = int(distance)

    # CALCULATING POINTS

        max_points = 150
        seconds = int(max_points * answer_time) / 100
        pts = int(150 - int(distance / 3) - int(10 * seconds))
        if pts < 0:
            pts = 0
        total_pts += pts

    # DISPLAYS THE CALCULATION AND POINTS
        label2_txt = "-" + str(int(distance / 3)) + " pts (distance " + str(distance) + " km)    "
        label3_txt = "-" + str(int(10 * seconds)) + " pts (time " + str(seconds) + " s)    "
        label5_txt = str(pts) + " pts, total " + str(total_pts) + " pts       "
        label1.config(text= str(max_points) + " pts (max)")
        label2.config(text=label2_txt)
        label3.config(text=label3_txt)
        label4.config(text="________________")
        label5.config(text=label5_txt)


def convert_to_latitude(y):
    return (height - y) / pplatitude + min_latitude


def convert_to_longitude(x, pplong):
    return (x - canvas_center) / pplong + mid_longitude


def convert_to_y(lat):
    return (min_latitude - lat) * pplatitude + height


def convert_to_x(lat, long):
    pplongitude = pplatitude * math.cos(lat * math.pi / squash_north)  # pixels per longitude
    return (long - mid_longitude) * pplongitude + canvas_center


def delta_t():
    t2 = time()
    dt = t2 - t1
    return dt


def draw(filename):
    points = []
    with open(filename + ".csv", "r") as map_data:

        for row in map_data:
            details = row.split(",")
            if details[0] != "draw":

                latitude_from_file = float(details[0])
                longitude_from_file = float(details[1])

                y = convert_to_y(latitude_from_file)
                x = convert_to_x(latitude_from_file, longitude_from_file)

                points.append(x)
                points.append(y)

            # if row begins with "draw"
            else:
                if details[2] == "polygon":
                    canvas.create_polygon(points, fill=details[1])

                if details[2] == "line":
                    canvas.create_line(points, fill=details[1])

                points.clear()


def load_cities():
    global city
    city = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    details = []
    i = 0
    with codecs.open("eu_cities.csv", "r", "utf8") as townfile:
        for row in townfile:
            if i != 0:
                details = row.split(",")
                file_latitude = float(details[0])
                file_longitude = float(details[1])
                name_of_city = details[2]
                city[i] = City(file_latitude, file_longitude, name_of_city)
            i = i + 1

def new_game():
    global index
    global total_pts
    index = 0
    total_pts = 0
    new_map()


def new_map():
    frame_width = 0
    canvas.create_rectangle(frame_width, frame_width, width - frame_width, height - frame_width, fill="cyan")

    draw("europe1")
    draw("islands")
    draw("borders")
    draw("rivers")
    draw("lakes")


def smaller_map():
    global pplatitude
    pplatitude = pplatitude - 0.5
    new_map()


# _________________________________________________________________________
# M A I N   P R O G R A M_________________________________________________
# _________________________________________________________________________

root = Tk()
root.title("Europe cities")
width = 850
height = 649
root.geometry("1580x810")

min_latitude = 33                               # latitude at canvas bottom
pplatitude = 16.5                                 # pixels per one latitude degree
mid_longitude = 14                              # longitude <mid_longitude> is...
canvas_center = 400                             # at <canvas_center> px at canvas
canvas_clicked = True                           # cant answer before asked
squash_north = 200  # if 180 degrees (the right value) then squashes north too much. If 250deg, then skandinavia too big

canvas = Canvas(root, width=width, height=height, bg="yellow")
ask_btn = Button(root, text="Ask new city", command=ask_city)
bigger_btn = Button(root, text="Bigger map", command=bigger_map, bg="cyan")
smaller_btn = Button(root, text="Smaller map", command=smaller_map, bg="cyan")
label_enter_name = Label(root, font=("Helvetica", 12), text="Enter your name below:")
name = Entry(root)
name.insert(0, "Mikko")

header1 = Label(root, font=("Helvetica", 22), text="Cities of Europe")
header2 = Label(root, font=("Helvetica", 18), text="")
label1 = Label(root, font=("Helvetica", 16), text="")
label2 = Label(root, font=("Helvetica", 16), text="")
label3 = Label(root, font=("Helvetica", 16), text="")
label4 = Label(root, font=("Helvetica", 16), text="")
label5 = Label(root, font=("Helvetica", 16), text="")

canvas.grid(row=0, column=0, rowspan=18)
bigger_btn.grid(row=0, column=0, padx=20, pady=5, sticky="NW")
smaller_btn.grid(row=7, column=0, padx=20, pady=5, sticky="NW")
ask_btn.grid(row=4, column=0, padx=30, sticky="NW")
label_enter_name.grid(row=1, column=1, sticky="NW", padx=10, pady=10)
name.grid(row=2, column=1, sticky="NW", padx=10, pady=0)
header1.grid(row=0, column=1, sticky="NW", padx=10, pady=10)
header2.grid(row=3, column=1, sticky="NW", padx=10, pady=10)
label1.grid(row=4, column=1, sticky="NW", padx=10, pady=5)
label2.grid(row=5, column=1, sticky="NW", padx=10, pady=5)
label3.grid(row=6, column=1, sticky="NW", padx=10, pady=5)
label4.grid(row=7, column=1, sticky="NW", padx=10, pady=5)
label5.grid(row=8, column=1, sticky="NW", padx=10, pady=5)

canvas.bind("<Button-1>", canvas_click)
load_cities()
new_game()

root.mainloop()