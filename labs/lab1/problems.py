import math


class Problems:
    @staticmethod
    def solve1(text):
        """
        :param text: string
        :return: string care contine ultimul cuvant dpdv alfabetic
        """
        return sorted(text.split())[-1]

    @staticmethod
    def solve2(a, b):
        """
        :param a: lista cu cele 2 coordonate ale primului punct
        :param b: lista cu cele 2 coordonate ale celui de-al doilea punct
        :return: distanta euclidiana dintre cele 2 puncte
        """
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    @staticmethod
    def solve3(v1, v2):
        """
        :param v1: vector
        :param v2: vector
        :return: produsul scalar al vectorilor
        """
        produs = 0
        for i in range(len(v1)):
            if v1[i] != 0 and v2[i] != 0:
                produs += v1[i] * v2[i]
        return produs

    @staticmethod
    def solve4(text):
        """
        :param text: string
        :return: lista cu cuvintele care apar o singura data in text
        """
        # text = text.split()
        # return [word for word in text if text.count(word) == 1]

        text = sorted(text.split())
        current_index = 1
        delete_current = False
        current_word = text[0]
        while current_index < len(text):
            if text[current_index] == current_word:
                delete_current = True
                text = text[:current_index] + text[current_index + 1:]
            else:
                current_word = text[current_index]
                if delete_current:
                    text = text[:current_index - 1] + text[current_index:]
                else:
                    current_index += 1
                delete_current = False
        return text

    @staticmethod
    def solve5(lista):
        """
        :param lista: lista cu n numere, din intervalul 1 : n-1, astfel incat
                    o singura valoare se repeta
        :return: numarul care se repeta
        """
        list_sum = 0
        for x in lista:
            list_sum += x
        length = len(lista)
        return length - (((length * (length + 1)) / 2) - list_sum)

    @staticmethod
    def solve6(lista):
        """
        :param lista: lista cu n numere
        :return: elementul care apare de mai mult de n/2 ori
        """
        lista = sorted(lista)
        length = len(lista)
        current_nr = lista[0]
        current_count = 1
        for nr in lista[1:]:
            if nr != current_nr:
                current_count = 1
                current_nr = nr
            else:
                current_count += 1
                if current_count > length // 2:
                    return current_nr

    @staticmethod
    def solve7(lista, k):
        """
        :param lista: lista de numere
        :param k: int
        :return: al k-lea cel mai mare element
        """
        return sorted(lista)[-k]

    @staticmethod
    def solve8(n):
        """
        :param n: int
        :return: lista cu numerele de la 1 la n reprezentate binar
        """
        lista = []
        current = 1
        for i in range(n):
            lista += [current]
            current = Utils.increment_binary(current)
        return lista

    @staticmethod
    def solve9(matrice, perechi):
        """
        :param matrice: matrice de numere
        :param perechi: perechi de coordonate a 2 elemente din matrice
        :return: lista cu sumele submatricelor identificate de fiecare pereche
        """
        """ brute
                sume = []
                for pereche in perechi:
                    suma = 0
                    x1, x2, y1, y2 = pereche[0][0], pereche[1][0], pereche[0][1], pereche[1][1]
                    for i in range(x1, x2 + 1):
                        for j in range(y1, y2 + 1):
                            suma += matrice[i][j]
                    sume += [suma]
                return sume
        """

        sume = []
        n = len(matrice)
        m = len(matrice[0])
        for i in range(n):
            for j in range(m):
                if i > 0:
                    matrice[i][j] += matrice[i - 1][j]
                if j > 0:
                    matrice[i][j] += matrice[i][j - 1]
                if i > 0 and j > 0:
                    matrice[i][j] -= matrice[i - 1][j - 1]

        for pereche in perechi:
            x1, x2, y1, y2 = pereche[0][0], pereche[1][0], pereche[0][1], pereche[1][1]
            if x1 > x2 or (x1 == x2 and y1 > y2):
                x1, x2, y1, y2 = x2, x1, y2, y1
            suma = matrice[x2][y2]
            if x1 > 0:
                suma -= matrice[x1 - 1][y2]
            if y1 > 0:
                suma -= matrice[x2][y1 - 1]
            if x1 > 0 and y1 > 0:
                suma += matrice[x1 - 1][y1 - 1]
            sume += [suma]
        return sume

    @staticmethod
    def solve10(matrice):
        """
        :param matrice: matrice de elemente binare sortate crescator pe linii
        :return: indexul liniei care contine cele mai multe elemente de 1
        """
        for j in range(len(matrice[0])):
            for i in range(len(matrice)):
                if matrice[i][j] == 1:
                    return i + 1
        return 1

    @staticmethod
    def solve11(matrice):
        """
        Inlocuieste cu 1 intr-o matrice toate aparitiile de 0 inconjurate de 1
        :param matrice: matrice cu elemente binare
        :return: matricea schimbata
        """
        Utils.dfs_wrapper11(matrice, len(matrice), len(matrice[0]))
        return matrice


class Utils:
    @staticmethod
    def dfs_wrapper11(matrice, n, m):
        # facem dfs de la marginile matricii unde gasim 0
        for j in range(m):
            if matrice[0][j] == 0:
                Utils.dfs11(matrice, 0, j, n, m)
            if matrice[n - 1][j] == 0:
                Utils.dfs11(matrice, n - 1, j, n, m)
        for i in range(n):
            if matrice[i][0] == 0:
                Utils.dfs11(matrice, i, 0, n, m)
            if matrice[i][m - 1] == 0:
                Utils.dfs11(matrice, i, m - 1, n, m)

        # unde avem 0 nu se poate ajunge din margine, deci schimbam in 1
        for i in range(n):
            for j in range(m):
                if matrice[i][j] == 0:
                    matrice[i][j] = 1
        # avem -1 in pozitiile in care s-a ajuns din margine, deci schimbam in 0
        for i in range(n):
            for j in range(m):
                if matrice[i][j] == -1:
                    matrice[i][j] = 0

    @staticmethod
    def dfs11(matrice, i, j, n, m):
        # suntem pe un element al matricii care e 0 si are drum catre margine
        # de aici trecem si la vecinii lui care sunt 0 ca sa ii 'marcam'
        matrice[i][j] = -1
        for (x, y) in Utils.get_vecini(i, j, n, m):
            if matrice[x][y] == 0:
                Utils.dfs11(matrice, x, y, n, m)

    @staticmethod
    def get_vecini(i, j, n, m):
        # returneaza lista cu perechi de coordonate care indica vecini ai elementului (i, j)
        vecini = []
        if i + 1 < n:
            vecini += [(i + 1, j)]
        if i - 1 >= 0:
            vecini += [(i - 1, j)]
        if j + 1 < m:
            vecini += [(i, j + 1)]
        if j - 1 >= 0:
            vecini += [(i, j - 1)]
        return vecini

    @staticmethod
    def increment_binary(x):
        if x % 2 == 0:
            x += 1
        else:
            nr = 1
            y = x
            while y % 10 == 1:
                y //= 10
                x -= nr
                nr *= 10
            x += nr
        return x
