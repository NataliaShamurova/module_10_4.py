import queue
import threading
import time
import random


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None



class Guest(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        # Гость ожидает случайное количество времени от 3 до 10 секунд
        time_wait = random.randint(3,10)
        time.sleep(time_wait)

class Cafe:
    def __init__(self, *tables):
        self.tables = list(tables)
        self.queue = queue.Queue()


    # прибытие гостей
    def guest_arrival(self, *guests):
        for guest in guests:
            seated = False
            for table in self.tables:
                if table.guest is None:
                    table.guest = guest
                    print(f"{guest.name} сел(-а) за стол номер {table.number}")

                    # Запускаем поток гостя
                    guest.start()
                    seated = True
                    break
            if not seated:
                self.queue.put(guest)
                print(f'{guest.name} в очереди')


    # процесс обслуживания гостей
    def discuss_guests(self):
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                if table.guest:
                    if not table.guest.is_alive():
                        print(f'{table.guest.name} поел(-а) и ушёл(ушла)')
                        print(f'Стол номер {table.number} свободен')
                        table.guest = None

            if not self.queue.empty():
                for table in self.tables:
                    if table.guest is None:
                        guest_from_queue = self.queue.get()
                        table.guest = guest_from_queue

                        print(f"{guest_from_queue.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")
                        guest_from_queue.start()
                        break


# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()