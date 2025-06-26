import turtle as t
import math
import xml.etree.ElementTree as ET

collided = False
cockpit_coor = (680.0, 21.0)
escape_pod_coor = (-409.0, -19.0)


def draw_line(point1: tuple[float, float], point2: tuple[float, float]) -> None:
    """
    Menggambar garis antar 2 titik
    Note: Pastikan turtle dimulai dan diakhirkan dengan penup
    """
    # TODO lengkapi kode tersebut
    t.penup()
    t.goto(point1)
    t.pendown()
    t.goto(point2)
    t.penup()


def process_movement(direction: str, distance: float) -> None:
    """
    Memproses perintah movement
    """
    global collided
    if collided:
        t.goto(cockpit_coor)
        collided = False
        return

    # TODO lengkapi kode tersebut
    if direction == "up":
        t.setheading(90)
    elif direction == "down":
        t.setheading(270)
    elif direction == "left":
        t.setheading(180)
    elif direction == "right":
        t.setheading(0)
    t.forward(distance)

    if collided:
        t.goto(cockpit_coor)
        collided = False
        return


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
    Mengecek apakah turtle menabrak dinding
    (tabrakan terjadi jika jarak turtle dengan dinding kurang dari 5)
    """
    # TODO lengkapi kode tersebut
    return distance_to_line_segment(turtle_point, line_start, line_end) < 5


def draw_grid(size: int, spacing: int) -> None:
    """
    Menggambarkan grid persegi dari (-size, -size) hingga (size, size)
    secara instan dengan warna #d3d3d3
    """
    # TODO lengkapi kode tersebut
    t.tracer(0)
    old_color = t.color()
    t.color("#d3d3d3")
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
    t.color(old_color[0])
    t.update()
    t.tracer(1)


def parse_point_string(point_Str: str) -> list[tuple[float, float]]:
    """
    Mengubah string koordinat menjadi list dari tuple points
    Ex. "12.34,56.78 87.65,43.21" -> [(12.34, 56.78), (87.65, 43.21)]
    """

    # TODO lengkapi kode tersebut
    points_list = []
    point_pairs = point_Str.strip().split()
    for pair in point_pairs:
        x_str, y_str = pair.split(",")
        x = float(x_str)
        y = float(y_str)
        points_list.append((x, y))
    return points_list


def draw_maze() -> list[tuple[tuple[float, float], tuple[float, float]]]:
    """
    Menggambar skema pesawat dari ship_map.svg secara instan
    Mengembalikan garis-garis pada skema pesawat
    """
    line_list = []
    xml_tree = ET.parse("ship_map.svg")
    namespaces = {"ns": "http://www.w3.org/2000/svg"}
    namespace_length = len(namespaces["ns"]) + 2
    for element in xml_tree.iterfind(".//ns:*", namespaces):
        match element.tag[namespace_length:]:
            case "polyline":
                points = parse_point_string(element.attrib["points"])
                for i in range(len(points) - 1):
                    line_list.append([points[i], points[i + 1]])
            case "line":
                x1 = float(element.attrib["x1"])
                x2 = float(element.attrib["x2"])
                y1 = float(element.attrib["y1"])
                y2 = float(element.attrib["y2"])
                line_list.append([(x1, y1), (x2, y2)])
            case "polygon":
                points = parse_point_string(element.attrib["points"])
                for i in range(len(points) - 1):
                    line_list.append([points[i], points[i + 1]])
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
    y_offset = 550
    t.tracer(0)
    for line in line_list:
        line[0] = (line[0][0] * scale + x_offset, -line[0][1] * scale + y_offset)
        line[1] = (line[1][0] * scale + x_offset, -line[1][1] * scale + y_offset)
        draw_line(line[0], line[1])
    for line in line_list:
        draw_line(line[0], line[1])
    t.update()
    t.tracer(1)
    return line_list


def init_screen() -> t._Screen:
    """
    Initialisasi turtle Screen dengan
    - Setup window seukuran 1500x1000
    - Title "COSMIC Escape Simulator"
    Lalu kembalikan objek Screen tersebut
    """
    # TODO lengkapi kode tersebut
    screen = t.Screen()
    screen.setup(width=1500, height=1000)
    t.title("COSMIC Escape Simulator")
    return screen


if __name__ == "__main__":
    screen = init_screen()

    draw_grid(1000, 10)
    line_list = draw_maze()

    t.goto(cockpit_coor)
    t.showturtle()
    t.penup()

    def check_all_collisions():
        global collided
        for line in line_list:
            if is_collided(t.pos(), line[0], line[1]):
                print("Dinding tertabrak! Kembali ke titik awal...")
                collided = True
                break
        screen.ontimer(check_all_collisions, 5)  # Call again after 10 ms

    # OPTIONAL
    # Buat callback ke onscreenclick() agar memudahkan perhitungan koordinat
    def buttonclick(x, y):
        print("You clicked at this coordinate({0},{1})".format(x, y))

    # onscreen function to send coordinate
    t.onscreenclick(buttonclick, 1)

    # OPTIONAL
    # Buat callback ke onkey() untuk mengetes setiap gerakan dengan keyboard
    screen.onkey(lambda: process_movement("up", 10), "Up")
    screen.onkey(lambda: process_movement("down", 10), "Down")
    screen.onkey(lambda: process_movement("left", 10), "Left")
    screen.onkey(lambda: process_movement("right", 10), "Right")
    screen.listen()

    movement_path: list[tuple[str, float]] = []

    check_all_collisions()  # Pengecekan tabrakan dimulai

    for movement in movement_path:
        direction = movement[0]
        distance = movement[1]
        process_movement(direction, distance)
        if math.dist(t.pos(), escape_pod_coor) < 10:
            print("Berhasil kabur!")
            exit(0)

    print("Path tidak mencapai destinasi...")
    t.done()
