import threading
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Gesture Recognition'))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'utils'))
from base_recognition import operate_recognition


def print_hi(name):
    print(f'Ez a master branch {name}')


if __name__ == '__main__':
    print_hi('Szar3')
    # threading.Thread(target=operate_recognition).start()

