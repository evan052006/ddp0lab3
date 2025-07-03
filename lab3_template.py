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
    ...


def process_movement(direction: str, distance: float) -> None:
    """
    Menggerakkan turtle berdasarkan perintah movement (up, down, left, right)
    """
    # TODO lengkapi kode tersebut
    ...


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

    # TODO: Jika tertabrak, ulang dari awal (dan reset tracker ke posisi cockpit_coor)
    # Hint: gunakan is_collided() untuk mengecek tabrakan dan gunakan variabel variabel global
    ...

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

    # TODO: Gambar garis tracker turtle dari posisi lama (old_position) ke posisi saat ini
    ...

    # TODO: Jika tertabrak, ulang dari awal (dan reset tracker ke posisi cockpit_coor)
    # Hint: gunakan is_collided() untuk mengecek tabrakan dan gunakan variabel variabel global
    ...

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
    (tabrakan terjadi jika jarak turtle dengan dinding kurang dari 5)
    """
    # TODO lengkapi kode tersebut
    ...


def draw_grid(size: int, spacing: int) -> None:
    """
    Menggambarkan grid persegi dari (-size, -size) hingga (size, size)
    secara instan dengan warna #d3d3d3
    """
    # TODO lengkapi kode tersebut
    ...

def parse_point_string(point_Str: str) -> list[tuple[float, float]]:
    """
    Mengubah string koordinat menjadi list dari tuple points
    Ex. "12.34,56.78 87.65,43.21" -> [(12.34, 56.78), (87.65, 43.21)]
    """

    # TODO lengkapi kode tersebut
    ...


def draw_maze() -> list[tuple[tuple[float, float], tuple[float, float]]]:
    """
    Menggambar skema pesawat dari ship_map.cosmic secara instan
    Mengembalikan garis-garis pada skema pesawat
    """
    line_list = []
    xml_tree = ET.parse("ship_map.cosmic")  # Load .cosmic sebagai pohon xml
    namespaces = {"ns": "http://cosmic.cs"}  # Set namespace cosmic
    # Format namespace {<namespace>}<tag> (abaikan < dan >)
    # maka +2 kurung luar
    namespace_length = len(namespaces["ns"]) + 2
    # Gunakan library untuk list semua elemen dibawah namespace cosmic
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
    ...


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
            if is_collided(t.pos(), line[0], line[1]) and not collided:
                print("Dinding tertabrak! Kembali ke titik awal...")
                collided = True
                break
        screen.ontimer(check_all_collisions, 1)  # Call again after 1 ms


    # Set fokus pada turtle screen
    screen.listen()

    check_all_collisions()  # Pengecekan tabrakan dimulai

    # Penggambaran dipercepat
    t.speed(0)
    t.delay(0)


    # TODO: Proses setiap gerakan (up, down, left, right, end)
    # Hint 1: berhasil keluar apabila turtle berjarak kurang dari 25 pixel dari escape_pod_coor, gunakan math.dist
    # Hint 2: Cetak "Berhasil kabur!" apabila berhasil keluar
    ...

    t.done()
