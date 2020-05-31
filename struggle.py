from threading import Thread
from time import sleep

def _find_getch():
    try:
        import termios
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch

    # POSIX system. Create and return a getch that manipulates the tty.
    import sys, tty
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    return _getch

class struggle:
    def __init__(self, time=10):
        self.time = time #s
        self.c = True
        self.getch = _find_getch()
        self.string = ""
        self.rate = 0
    def _timer(self):
        sleep(self.time)
        self.c = False
        return
    def _keycounter(self):
        while self.c:
            self.string += self.getch()
        return
    def _reset(self):
        self.c = True
        self.rate = 0
    def struggle(self):
        """Initiates a struggle! param: time (seonds) return: rate in keys/second"""
        thread = Thread(target = s._timer)
        thread2 = Thread(target = s._keycounter)

        for i in ["3", "2", "1", "Start!"]:
            sleep(1)
            print(i)

        thread.start()
        thread2.start()
        thread.join()
        self.rate = len(s)/10

if __name__ == "__main__":
    s = struggle()
    thread = Thread(target = s._timer)
    thread2 = Thread(target = s._keycounter)

    for i in ["3", "2", "1", "Start!"]:
        sleep(1)
        print(i)

    thread.start()
    thread2.start()
    thread.join()
    print(s.rate)