import board
import asyncio


if __name__ == '__main__':
    O = board.Board(size=900, n=1)
    O.draw()
    A = board.Board(size=900, n=2)
    A.draw()
    B = board.Board(size=900, n=4)
    B.draw()
    C = board.Board(size=900, n=5)
    C.draw()
