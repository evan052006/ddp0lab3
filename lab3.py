import turtle as t
import math
import random
import xml.etree.ElementTree as ET


def draw_line(point1: tuple[float, float], point2: tuple[float, float]) -> None:
    """Draw a line between two points."""
    t.penup()
    t.goto(point1)
    t.pendown()
    t.goto(point2)
    t.penup()


def process_movement(direction: str, distance: float) -> None:
    """Process movement commands."""
    if direction == "up":
        t.setheading(90)
    elif direction == "down":
        t.setheading(270)
    elif direction == "left":
        t.setheading(180)
    elif direction == "right":
        t.setheading(0)
    t.forward(distance)


def distance_to_line_segment(
    point: tuple[float, float],
    line_start: tuple[float, float],
    line_end: tuple[float, float],
) -> float:
    """
    Mengembalikan jarak terdekat suatu titik (point) ke segment garis tertentu
    """
    px = point[0]
    py = point[1]
    x1 = line_start[0]
    y1 = line_start[1]
    x2 = line_end[0]
    y2 = line_end[1]

    if x1 == x2 and y1 == y2:
        return math.hypot(px - x1, py - y1)

    dx = x2 - x1
    dy = y2 - y1
    length_squared = dx * dx + dy * dy
    t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / length_squared))

    proj_x = x1 + t * dx
    proj_y = y1 + t * dy

    return math.hypot(px - proj_x, py - proj_y)


def is_collided(
    turtle_point: tuple[float, float],
    line_start: tuple[float, float],
    line_end: tuple[float, float],
) -> bool:
    """
    Mengecek apakah turtle  menabrak dinding
    (implementasi oleh mentee)
    """
    return distance_to_line_segment(turtle_point, line_start, line_end) < 2.5


def draw_grid(size: int, spacing: int) -> None:
    """
    Draw a grid with given size and spacing
    """

    t.penup()

    # Draw vertical lines
    for x in range(-size, size + 1, spacing):
        t.goto(x, -size)
        t.pendown()
        t.goto(x, size)
        t.penup()

    # Draw horizontal lines
    for y in range(-size, size + 1, spacing):
        t.goto(-size, y)
        t.pendown()
        t.goto(size, y)
        t.penup()

def parse_point_string(point_Str: str) -> list[tuple[float, float]]:
    '''
    Turns coordinate strings to list of tuple points
    Ex. "12.34,56.78 87.65,43.21" -> [(12.34, 56.78), (87.65, 43.21)]
    '''
    def parse_points(val):
        return tuple(map(float, val.split(",")))
    return list(map(parse_points, point_Str.split()))

def draw_maze() -> list[tuple[tuple[float, float], tuple[float, float]]]:
    """
    Menggambar skema pesawat dari ship_map.svg 
    Mengembalikan garis-garis pada skema pesawat
    """
    line_list = []
    xml_tree = ET.parse('ship_map.svg')
    namespace_length = len("{http://www.w3.org/2000/svg}")
    for element in xml_tree.iter():
        match element.tag[namespace_length:]:
            case "polyline":
                points = parse_point_string(element.attrib["points"])
                for i in range(len(points)-1):
                    line_list.append([points[i], points[i+1]])
            case "line":
                x1 = float(element.attrib["x1"])
                x2 = float(element.attrib["x2"])
                y1 = float(element.attrib["y1"])
                y2 = float(element.attrib["y2"])
                line_list.append([(x1, y1), (x2, y2)])
            case "polygon":
                points = parse_point_string(element.attrib["points"])
                for i in range(len(points)-1):
                    line_list.append([points[i], points[i+1]])
                line_list.append([points[-1], points[0]])
            case "rect":
                x = float(element.attrib["x"])
                y = float(element.attrib["y"])
                width = float(element.attrib["width"])
                height = float(element.attrib["height"])
                line_list.append([(x, y), (x + width, y)])
                line_list.append([(x + width, y), (x + width, y + height)])
                line_list.append([(x, y + height), (x + width, y + height)])
                line_list.append([(x, y), (x, y + height)])
    scale = 1.1
    x_offset = -750
    y_offset = -500
    for line in line_list:
        line[0] = (line[0][0] * scale + x_offset, line[0][1] * scale + y_offset)
        line[1] = (line[1][0] * scale + x_offset, line[1][1] * scale + y_offset)
        draw_line(line[0], line[1])
    return line_list

if __name__ == "__main__":

    screen = t.Screen()
    screen.setup(width=800, height=600)

    t.title("Maze Explorer")
    t.speed(0)
    t.hideturtle()

    t.tracer(0)
    t.color("#d3d3d3")
    t.pendown()
    draw_grid(1000, 10)
    t.penup()
    t.color("black")
    line_list = draw_maze()
    t.tracer(1)
    t.update()
    
    home_coor = (-410.0,69)
    t.goto(home_coor)
    t.showturtle()
    t.shapesize(2, 2)
    t.penup()

    def check_all_collisions():
        for line in line_list:
            if is_collided(t.pos(), line[0], line[1]):
                print("Collision detected!")
                t.goto(home_coor)  # Reset position to the center
                break
        screen.ontimer(check_all_collisions, 10)  # Call again after 10 ms

    # self defined function to print coordinate
    def buttonclick(x, y):
        print("You clicked at this coordinate({0},{1})".format(x, y))

    # onscreen function to send coordinate
    t.onscreenclick(buttonclick, 1)

    screen.onkey(lambda: process_movement("up", 10), "Up")
    screen.onkey(lambda: process_movement("down", 10), "Down")
    screen.onkey(lambda: process_movement("left", 10), "Left")
    screen.onkey(lambda: process_movement("right", 10), "Right")
    screen.listen()

    check_all_collisions()  # Start the recurring collision check

    t.done()
