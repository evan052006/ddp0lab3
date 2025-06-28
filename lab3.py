import turtle as t
import math
import xml.etree.ElementTree as ET

moving = False
collided = False
cockpit_coor = (350.0, 10.0)
escape_pod_coor = (-250.0, -10.0)
trail: list[tuple[tuple[float, float], tuple[float, float]]] = []
line_list: list[tuple[tuple[float, float], tuple[float, float]]] = []
tracker = t.Turtle()
tracker.color("blue")
tracker.hideturtle()


def draw_line(
    point1: tuple[float, float], point2: tuple[float, float], turtle: t.Turtle
) -> None:
    """
    Menggambar garis antar 2 titik
    Note: Pastikan turtle dimulai dan diakhirkan dengan penup
    """
    # TODO lengkapi kode tersebut
    turtle.penup()
    turtle.goto(point1)
    turtle.pendown()
    turtle.goto(point2)
    turtle.penup()


def process_movement(direction: str, distance: float) -> None:
    """
    Menggerakkan turtle berdasarkan perintah movement
    """
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


def move(direction: str, distance: float) -> None:
    """
    Memproses dan mendeteksi setiap gerakan turtle
    """
    # Keyword global agar variabel berikut bisa diakses dari scope local
    global collided, moving, trail, cockpit_coor

    # Move dibatalkan jika masih ada movement lain
    if moving:
        return

    moving = True

    # Jika tertabrak, ulang dari awal (dan reset tracker)
    if collided:
        t.goto(cockpit_coor)
        tracker.clear()
        collided = False
        moving = False
        return

    # Simpan posisi sebelum gerakan
    old_position = t.position()
    old_angle = t.heading()

    # Proses gerakan (turtle digerakkan)
    process_movement(direction, distance)

    new_angle = t.heading()

    if old_angle != new_angle:
        trail.append(old_position)
        marker = t.Turtle(shape="circle")
        marker.turtlesize(0.25)
        marker.penup()
        marker.goto(old_position)
        marker.stamp()

    # Gambar tracker turtle
    new_position = t.position()
    t.tracer(0)
    draw_line(old_position, new_position, tracker)
    t.tracer(1)
    t.update()

    # Kita cek collision lagi
    if collided:
        t.goto(cockpit_coor)
        tracker.clear()
        collided = False
        moving = False
        return

    moving = False


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
    (tabrakan terjadi jika jarak turtle dengan dinding kurang dari 1)
    """
    # TODO lengkapi kode tersebut
    return distance_to_line_segment(turtle_point, line_start, line_end) < 1


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
    xml_tree = ET.parse("ship_map.svg")  # Load .svg sebagai pohon xml
    namespaces = {"ns": "http://www.w3.org/2000/svg"}  # Set namespace svg
    # Format namespace {<namespace>}<tag> (abaikan < dan >)
    # maka +2 kurung luar
    namespace_length = len(namespaces["ns"]) + 2
    # Gunakan library untuk list semua elemen dibawah namespace svg
    for element in xml_tree.iterfind(".//ns:*", namespaces):
        # Ambil tagnya saja (skip namespace dan kurung kurawal)
        match element.tag[namespace_length:]:
            case "polyline":
                # Polyline adalah beberapa garis dihubungkan satu sama lain
                points = parse_point_string(element.attrib["points"])
                for i in range(len(points) - 1):
                    line_list.append([points[i], points[i + 1]])
            case "line":
                # Line adalah 1 garis
                x1 = float(element.attrib["x1"])
                x2 = float(element.attrib["x2"])
                y1 = float(element.attrib["y1"])
                y2 = float(element.attrib["y2"])
                line_list.append([(x1, y1), (x2, y2)])
            case "polygon":
                # Polygon adalah polyline dimana titik akhir dan awal terhubung
                points = parse_point_string(element.attrib["points"])
                for i in range(len(points) - 1):
                    line_list.append([points[i], points[i + 1]])
                line_list.append([points[-1], points[0]])
            case "rect":
                # Rectangle = persegi panjang
                x = float(element.attrib["x"])
                y = float(element.attrib["y"])
                width = float(element.attrib["width"])
                height = float(element.attrib["height"])
                line_list.append([(x, y), (x + width, y)])
                line_list.append([(x + width, y), (x + width, y + height)])
                line_list.append([(x, y + height), (x + width, y + height)])
                line_list.append([(x, y), (x, y + height)])
    scale = 0.6
    x_offset = -440
    y_offset = 300
    # Fungsi tracer mengnonaktifkan update otomatis layar secara sementara
    t.tracer(0)
    for line in line_list:
        # Gambar setiap garis berdasarkan offset dan scale
        line[0] = (line[0][0] * scale + x_offset, -line[0][1] * scale + y_offset)
        line[1] = (line[1][0] * scale + x_offset, -line[1][1] * scale + y_offset)
        draw_line(line[0], line[1], t)
    t.update()  # Update layar secara manual
    t.tracer(1)  # Aktifkan lagi update otomatis layar
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
    screen.setup(width=800, height=600)
    t.title("COSMIC Escape Simulator")
    return screen


if __name__ == "__main__":
    # Inisialisasi layar
    screen = init_screen()

    # Gambar grid dan pesawat
    draw_grid(1000, 10)
    line_list = draw_maze()

    # Inisasi turtle
    t.goto(cockpit_coor)
    t.showturtle()
    t.penup()

    # Mendefinisikan pengecekan tabrakan terharap semua garis
    def check_all_collisions():
        global collided
        for line in line_list:
            if is_collided(t.pos(), line[0], line[1]):
                print("Dinding tertabrak! Kembali ke titik awal...")
                collided = True
                break
        screen.ontimer(check_all_collisions, 10)  # Call again after 10 ms

    # OPTIONAL
    # Buat callback ke onscreenclick() agar memudahkan perhitungan koordinat
    def buttonclick(x, y):
        print("You clicked at this coordinate({0},{1})".format(x, y))

    # onscreen function to send coordinate
    t.onscreenclick(buttonclick, 1)

    # OPTIONAL
    # Buat callback ke onkey() untuk mengetes setiap gerakan dengan keyboard
    # screen.onkey(lambda: process_movement("up", 10), "Up")
    # screen.onkey(lambda: process_movement("down", 10), "Down")
    # screen.onkey(lambda: process_movement("left", 10), "Left")
    # screen.onkey(lambda: process_movement("right", 10), "Right")

    # Set fokus pada turtle screen
    screen.listen()

    movement_path = [
        ("left", 60),
        ("up", 30),
        ("left", 70),
        ("down", 20),
        ("left", 80),
        ("up", 20),
        ("left", 20),
        ("up", 10),
        ("left", 40),
        ("down", 80),
        ("right", 30),
        ("down", 15),
        ("left", 40),
        ("down", 15),
        ("right", 60),
        ("down", 10),
        ("left", 70),
        ("down", 10),
        ("left", 70),
        ("down", 20),
        ("left", 40),
        ("up", 60),
        ("right", 30),
        ("up", 30),
        ("left", 30),
        ("up", 100),
        ("left", 10),
        ("up", 20),
        ("right", 90),
        ("down", 30),
        ("right", 30),
        ("up", 30),
        ("right", 20),
        ("down", 30),
        ("right", 30),
        ("up", 50),
        ("left", 180),
        ("up", 30),
        ("right", 50),
        ("up", 20),
        ("left", 240),
        ("up", 20),
        ("right", 240),
        ("up", 10),
        ("left", 260),
        ("up", 20),
        ("right", 250),
        ("up", 20),
        ("left", 270),
        ("down", 20),
        ("left", 20),
        ("down", 40),
        ("right", 10),
        ("down", 10),
        ("right", 20),
        ("down", 20),
        ("right", 140),
        ("down", 60),
        ("right", 30),
        ("down", 90),
        ("right", 10),
        ("down", 70),
        ("left", 20),
        ("down", 90),
        ("right", 90),
        ("down", 70),
        ("left", 90),
        ("down", 10),
        ("left", 20),
        ("up", 40),
        ("left", 80),
        ("up", 40),
        ("right", 80),
        ("up", 60),
        ("left", 70),
        ("up", 20),
        ("right", 40),
        ("up", 160),
        ("left", 20),
        ("down", 20),
        ("left", 20),
        ("up", 20),
        ("left", 40),
        ("down", 20),
        ("left", 20),
        ("up", 20),
        ("left", 30),
        ("down", 20),
        ("left", 40),
        ("down", 80),
        ("right", 30),
        ("up", 60),
        ("right", 125),
        ("down", 100),
        ("left", 105),
        ("up", 80),
        ("right", 90),
        ("down", 60),
        ("left", 70),
        ("up", 40),
        ("right", 40),
        ("down", 20),
        ("left", 10),
    ]

    check_all_collisions()  # Pengecekan tabrakan dimulai

    # Penggambaran dipercepat
    t.speed(0)
    t.delay(0)

    # Proses setiap gerakan
    for movement in movement_path:
        direction = movement[0]
        distance = movement[1]
        move(direction, distance)
        while moving:
            continue
        if math.dist(t.pos(), escape_pod_coor) < 2:
            print(trail)
            print("Berhasil kabur!")
            t.done()
            exit(0)

    print("Path tidak mencapai destinasi...")
    t.done()
