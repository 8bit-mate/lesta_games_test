from collections import deque
import timeit

"""
Результаты теста производительности:

CyclicBufferOne среднее время, с: 0.008332187999039889
CyclicBufferTwo среднее время, с: 0.008300502029596828

Выбор конкретной реализации может быть обусловлен многимии факторами: скорость разработки
читаемость кода, необходимость произвольного доступа к элементам (в середине буффера),
необходимость реализации дополнительных методов (таких как pop) и т.д.
"""

class CyclicBufferOne:
    """
    Реализация циклического FIFO-буффера при помощи класса collections.deque().

    Преимущества по сравнению с CyclicBufferTwo:
      - быстро реализуем благодаря тому, что основывается на готовом решении
        collections.deque();
      - компактный код;
      - может быть использован для создания буффера в любой среде, где доступен
        модуль collections.

    Недостатки:
      - может оказаться менее гибким из-за того, что в основе лежит готовое решение;
      - медленный, если требуется произвольный доступ к элементам в середине списка [1].
      
    Источник:
      1 - https://wiki.python.org/moin/TimeComplexity
    """

    def __init__(self, buffer_size):
        self.buffer = deque(maxlen=buffer_size)

    def append(self, item):
        self.buffer.append(item)

    def get_buffer(self):
        return list(self.buffer)

    def peek_top(self):
        """
        Возвращает последний добавленный (самый "верхний") элемент,
        не удаляя элемент из списка.
        """
        if not self.buffer:
            raise IndexError("Список пустой.")
        return self.buffer[-1]

    def peek_bottom(self):
        """
        Возвращает самый старый ("нижний") добавленный элемент, не
        удаляя элемент из списка.
        """
        if not self.buffer:
            raise IndexError("Список пустой.")
        return self.buffer[0]

class CyclicBufferTwo:
    """
    Преимущества:
      - не требуется производить импорт сторонних зависимостей;
      - может быть более гибким решением.

    Недостатки:
      - требует бОльших затрат на реализацию по сравнению с готовыми решениями.
    """

    def __init__(self, buffer_size):
        self.buffer = [0] * buffer_size
        self.size = buffer_size
        self.position = 0
        self.count = 0

    def append(self, item):
        self.buffer[self.position] = item
        self.position = (self.position + 1) % self.size
        if self.count < self.size:
            self.count += 1

    def get_buffer(self):
        if self.count < self.size:
            return self.buffer[:self.count]
        else:
            return self.buffer[self.position:] + self.buffer[:self.position]

    def peek_top(self):
        """
        Возвращает последний добавленный (самый "верхний") элемент,
        не удаляя элемент из списка.
        """
        if self.count == 0:
            raise IndexError("Список пустой.")
        return self.buffer[(self.position - 1) % self.size]

    def peek_bottom(self):
        """
        Возвращает самый старый ("нижний") добавленный элемент, не
        удаляя элемент из списка.
        """
        if self.count == 0:
            raise IndexError("Список пустой.")
        if self.count < self.size:
            return self.buffer[0]
        else:
            return self.buffer[self.position]
          
# Тесты производительности:
def test_buffer_one(buffer_size = 10):
    test_buffer(CyclicBufferOne(buffer_size))

def test_buffer_two(buffer_size = 10):
    test_buffer(CyclicBufferTwo(buffer_size))

def test_buffer(buffer):
    for i in range(900_000):
      buffer.append(i)
      if i % 100 == 0:
          buffer.peek_top()
          buffer.peek_bottom()

def run_test(method_name, statement, setup, runs = 100):
    times = [timeit.timeit(statement, setup=setup) for _ in range(runs)]
    mean_time = sum(times) / len(times)
    print(f"{method_name} среднее время, с: {mean_time}")

run_test("CyclicBufferOne", 'test_buffer_one', 'from __main__ import test_buffer_one')
run_test("CyclicBufferTwo", 'test_buffer_two', 'from __main__ import test_buffer_two')
