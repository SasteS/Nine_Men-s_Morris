"""
Modul sadrži implementaciju reda na osnovu liste.
"""


class QueueError(Exception):
    """
    Klasa modeluje izuzetke vezane za klasu Queue.
    """
    pass


class Queue(object):
    """
    Klasa modeluje red na osnovu liste.
    """
    def __init__(self, capacity=10):
        """
        Konstruktor.

        Argument:
        - `capacity`: inicijalni broj raspoloživih mesta
        """
        # broj elemenata u redu
        self._size = 0

        # indeks prvog elementa reda
        self._first = 0

        # broj mesta u redu
        self.__capacity = capacity
        self._data = [None]*self.__capacity
    
    #setter za kapacitet
    def get_capacity(self):
        return self.__capacity


    def __len__(self): #RADI ONO STO BI INACE RADIO  niz.len()
        return self._size

    def is_empty(self): #vraca true/false?
        """
        Metoda proverava da li je red prazan.
        """
        return self._size == 0

    def first(self):
        """
        Metoda omogućava pristup prvom elementu reda.
        """
        if self.is_empty():
            raise QueueError('Red je prazan.')
        return self._data[self._first]

    def dequeue(self):
        """
        Metoda izbacuje prvi element iz reda.
        """
        if self.is_empty():
            raise QueueError('Red je prazan.')

        element = self._data[self._first]

        # brisanje se vrši postavljanjem sadržaja na vrednost None
        self._data[self._first] = None

        # pomeranje indeksa prvog elementa
        self._first = (self._first+1) % self.__capacity
        self._size -= 1

        # kapacitet se polovi kada je popunjeno manje od 1/4 kapaciteta
        if 0 < self._size < self.__capacity//4:
            self._resize(self.__capacity//2)

        return element

    def enqueue(self, e):
        """
        Metoda vrši dodavanje elementa u red.

        Argument:
        - `e`: novi element
        """
        # dupliranje kapaciteta ukoliko je red popunjen
        if self._size == self.__capacity:
            self._resize(2*self.__capacity)

        # indeks novog elementa (prvi iza trenutno poslednjeg)
        index = (self._first+self._size) % self.__capacity
        self._data[index] = e
        self._size += 1

    def _resize(self, capacity):
        """
        Metoda vrši skaliranje kapaciteta reda.

        Argument:
        - `capacity`: novi kapacitet
        """
        current_data = self._data
        current_first = self._first

        # kreira se "prazna" lista sa zadatim brojem mesta
        self._data = [None]*capacity

        # prepisivanje trenutnog sadržaja u novu listu
        for k in range(self._size):
            self._data[k] = current_data[current_first]
            current_first = (current_first+1) % len(current_data)

        self._first = 0
        self.__capacity = capacity

if __name__ == '__main__':
    queue = Queue()
    print(queue.get_capacity())
    queue.enqueue(3)
    queue.enqueue(8)
    queue.enqueue(1)
    print(len(queue))
    print(queue.first())

    queue.dequeue()
    print(len(queue))

    print(queue.first())
    print(queue.is_empty())
