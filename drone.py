import time

# Дрон и его действия
class Drone:
    def __init__(self, location_name, base_coords):
        self.base_coords = base_coords
        self.current_coords = base_coords
        self.location_name = "База"
        self.altitude = 0

    # Поднимаем дрон на заданную высоту
    def takeoff(self, altitude):
        print(f"Поднимаемся до высоты {altitude} метров\nНачало миссии")
        time.sleep(2)  # Имитация времени на подъем
        self.altitude = altitude

    # Летим в заданные координаты и зависаем там
    def fly_to(self, location_name, coords):
        print(f"\nЛетим в локацию '{location_name}' в координатах: {coords}")
        time.sleep(5)  # Имитация времени на перелет
        self.current_coords = coords
        print(f"Прилетели в локацию '{location_name}'")

    # Выполняем круговую съемку с шагом 60 градусов
    def panoramic_shot(self, location_name):
        print("Выполняем круговую съемку с шагом 60 градусов")
        for angle in range(0, 300, 60):
            print(f"\t{location_name}_{angle}.png")
            time.sleep(1)  # Имитация времени на съемку

    # Снижаемся
    def land(self):
        print("Снижаемся и завершаем полет")
        self.altitude = 0
        time.sleep(2)  # Имитация времени на спуск
