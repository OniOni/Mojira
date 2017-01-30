import sys, tty, termios
import time

def getchar(n: int = 1):
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(n)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return ch

class GrowableList(list):

    def grow(self, index):
        if len(self) < index:
            self += [None for _ in range(index - len(self))]

class Screen(object):

    def __init__(self, max_len: int = 80) -> None:
        self._buffer = GrowableList()
        self._buffer.grow(1)
        self._max_len = max_len
        self._line = 0
        self._debug = ""

    def debug(self, msg):
        self._debug += "{}: {}\n".format(time.time(), msg)

    def get_debug_output(self):
        print('-' * 80)
        print(self._debug)
        print('-' * 80)

    def move_up(self, lines: int) -> None:
        fd = sys.stdout.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            self.debug(sys.stdout.buffer.seekable())
            for _ in range(lines):
                self.debug("Going up line {}".format(self._line))
                back = - (len(self._buffer[self._line]) - 1)
                self.debug("Back by {}".format(back))
                sys.stdout.buffer.seek(back, 2)
                self._line -= 1
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def move_down(self, nb_lines: int) -> None:
        self._buffer.grow(len(self._buffer) + nb_lines + 1)
        print('\n' * nb_lines, end='')
        self._line += nb_lines

    def move2line(self, line: int) -> None:
        self.debug("Moving to line {}".format(line))
        if self._line != line:
            nb = line - self._line
            self.debug("Need to move by {}".format(nb))
            if nb > 0:
                self.move_down(nb)
            else:
                self.move_up(abs(nb))
            self._line = line

    def write(self, buf: str, line: int = 0) -> int:
        self.move2line(line)
        self._buffer[line] = buf[:min(len(buf), self._max_len)]
        print(self._buffer[line], end='', flush=True)

        return len(self._buffer)

    def beginning(self) -> None:
        print('\b' * len(self._buffer), end='', flush=True)

    def clear(self, line: int = 0) -> None:
        self.beginning()
        print('' * len(self._buffer), end='')
        self.beginning()

    def read(self, n: int = 1) -> str:
        self.move2line(0)
        c = getchar(n)

        return c

def main():
    screen = Screen()

    try:
        for i in reversed(range(5)):
            time.sleep(1)
            screen.write('line {}'.format(i), line=i)

        screen.write('???', line=0)
    except Exception as e:
        print('\n')
        print(e)
        screen.get_debug_output()

if __name__ == '__main__':
    main()
