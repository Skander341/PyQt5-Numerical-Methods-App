from PyQt5.QtWidgets import QApplication, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
from pickle import load, dump


def is_real(x):
    try:
        float(x)
        return True
    except:
        return False


def k(x, eps):
    return f(x, eps) - g(x)


def g(x):
    return 0.5 * x * x


def f(x, eps):
    return ln(x + 2, eps)



def compute_x(eps):
    x = -1
    xp = 0
    i = 0
    max_iter = 1000

    while abs(x - xp) > eps and i < max_iter:
        xp = x
        x = k(x, eps)
        i += 1

    return x


def ln(x, eps):
    if x <= 0:
        return 0

    n = 0
    s = 0
    s1 = 1

    while abs(2 * s - 2 * s1) > eps:
        s1 = s
        term = (1 / (2 * n + 1)) * power(((x - 1) / (x + 1)), (2 * n + 1))
        s += term
        n += 1

    return 2 * s


def power(a, b):
    if b == 0:
        return 1
    return a * power(a, b - 1)


def find_root(a, b, eps):
    m = (a + b) / 2

    while (b - a) > eps and abs(k(m, eps)) > eps:
        if k(m, eps) * k(a, eps) > 0:
            a = m
        else:
            b = m

        m = (a + b) / 2

    return m


def calculate_bounds():
    ep = w.EPS.text()

    if not (is_real(ep) and 0 < float(ep) < 0.1):
        QMessageBox.critical(w, "Error", "epsilon has to be between 0 and 0.1")
        return

    x = compute_x(float(ep))
    w.a_txt.setText(str(-x))
    w.b_txt.setText(str(x))

    w.liste.addItem(str(find_root(-x, x, float(ep))))


def rectangle(a, b, n, eps):
    h = (b - a) / n
    s = 0
    x = a

    for _ in range(n):
        s += k(x, eps)
        x += h

    return s * h


def trapezoidal(a, b, n, eps):
    h = (b - a) / n
    s = 0
    x = a

    for _ in range(n):
        s += k(x, eps) + k(x + h, eps)
        x += h

    return s * h / 2


def exists(n, eps):
    try:
        file = open("Surface.dat", "rb")
    except:
        return False

    found = False

    while True:
        try:
            e = load(file)
            if e["N"] == n and e["Eps"] == eps:
                found = True
                break
        except:
            break

    file.close()
    return found

def calculate():
    ep = w.EPS.text()
    a = w.a_txt.text()
    b = w.b_txt.text()
    n = w.subdiv.currentText()

    if not (is_real(ep) and 0 < float(ep) < 0.1):
        QMessageBox.critical(w, "Error", "Invalid epsilon")
        return

    if a == "" or b == "":
        QMessageBox.critical(w, "Error", "Invalid bounds")
        return

    if not n.isdecimal():
        QMessageBox.critical(w, "Error", "Invalid n")
        return

    rect = rectangle(float(a), float(b), int(n), float(ep))
    trap = trapezoidal(float(a), float(b), int(n), float(ep))

    if not exists(int(n), float(ep)):
        file = open("Surface.dat", "ab")
        dump({"N": int(n), "Eps": float(ep), "Rect": rect, "Trap": trap}, file)
        file.close()



def minimum():
    ep = w.EPS.text()
    a = w.a_txt.text()
    b = w.b_txt.text()
    n = w.subdiv.currentText()

    if not (is_real(ep) and 0 < float(ep) < 0.1):
        QMessageBox.critical(w, "Error", "Invalid epsilon")
        return

    if a == "" or b == "":
        QMessageBox.critical(w, "Error", "Invalid bounds")
        return

    if not n.isdecimal():
        QMessageBox.critical(w, "Error", "Invalid n")
        return

    rect = rectangle(float(a), float(b), int(n), float(ep))
    trap = trapezoidal(float(a), float(b), int(n), float(ep))

    w.surface.setText(str(min(rect, trap)))



def display():
    w.table.setRowCount(0)

    try:
        file = open("Surface.dat", "rb")
    except:
        return

    i = 0

    while True:
        try:
            e = load(file)

            w.table.insertRow(i)
            w.table.setItem(i, 0, QTableWidgetItem(str(e["N"])))
            w.table.setItem(i, 1, QTableWidgetItem(str(e["Eps"])))
            w.table.setItem(i, 2, QTableWidgetItem(str(e["Rect"])))
            w.table.setItem(i, 3, QTableWidgetItem(str(e["Trap"])))

            i += 1
        except:
            break

    file.close()


app = QApplication([])
w = loadUi("interface.ui")

w.btnbornes.clicked.connect(calculate_bounds)
w.btncalculer.clicked.connect(calculate)
w.btncherche.clicked.connect(minimum)
w.btnmeth.clicked.connect(display)

w.show()
app.exec()
