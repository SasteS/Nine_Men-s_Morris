"""
Modul sadrži implementaciju stabla.
"""
from operator import indexOf
from queue import Queue


class TreeNode(object):
    """
    Klasa modeluje čvor stabla.
    """
    __slots__ = 'parent', 'children', 'data'

    def __init__(self, data):
        """
        Konstruktor.

        Argument:
        - `data`: podatak koji se upisuje u čvor
        """
        self.parent = None
        self.children = []
        self.data = data

    def is_root(self):
        """
        Metoda proverava da li je čvor koren stabla.
        """
        return self.parent is None

    def is_leaf(self):
        """
        Metoda proverava da li je čvor list stabla.
        """
        return len(self.children) == 0

    def add_child(self, x):
        """
        Metoda dodaje potomka čvoru.

        Argument:
        - `x`: čvor potomak
        """
        # kreiranje dvosmerne veze između čvorova
        x.parent = self
        self.children.append(x)


class Tree(object):
    """
    Klasa modeluje stablo.
    """
    def __init__(self):
        self.root = None

    def is_empty(self):
        """
        Metoda proverava da li stablo ima elemenata.
        """
        return self.root is None

    def depth(self, x):
        """
        Metoda izračunava dubinu zadatog čvora.

        Argument:
        - `x`: čvor čija dubina se računa
        """
        if x.is_root():
            return 0
        else:
            return 1 + self.depth(x.parent)

    def _height(self, x):
        """
        Metoda izračunava visinu podstabla sa zadatim korenom.

        Argument:
        - `x`: koren posmatranog podstabla
        """
        if x.is_leaf():
            return 0
        else:
            return 1 + max(self._height(c) for c in x.children)

    def height(self):
        return self._height(self.root)

    def preorder(self, x):
        """
        Preorder obilazak po dubini

        Najpre se vrši obilazak roditelja a zatim svih njegovih potomaka.

        Argument:
        - `x`: čvor od koga počinje obilazak
        """
        if not self.is_empty():
            print(x.data)
            for c in x.children:
                self.preorder(c)

    def postorder(self, x):
        """
        Postorder obilazak po dubini

        Najpre se vrši obilazak potomaka a zatim i roditelja

        Argument:
        - `x`: čvor od koga počinje obilazak
        """
        if not self.is_empty():
            for c in x.children:
                self.postorder(c)
            print(x.data)

    def breadth_first(self):
        """
        Metoda vrši obilazak stabla po širini.
        """
        to_visit = Queue()
        to_visit.enqueue(self.root)
        while not to_visit.is_empty():
            e = to_visit.dequeue()
            print(e.data)

            for c in e.children:
                to_visit.enqueue(c)

if __name__ == '__main__':
    # instanca stabla
    t = Tree()
    t.root = TreeNode(0)
    
    # kreiranje relacija između novih čvorova
    a = TreeNode(1)
    b = TreeNode(2)
    c = TreeNode(3)
    d = TreeNode(4)
    e = TreeNode(5)

    a.add_child(c)
    a.add_child(d)
    c.add_child(e)
    t.root.add_child(a)
    t.root.add_child(b)
    print(t.depth(e))
    
    print("awd " + str(a.children[a.children.index(c)].data))