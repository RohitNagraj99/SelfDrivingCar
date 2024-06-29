from pynput.keyboard import Key, Listener
import RPi.GPIO as gpio
from picamera import PiCamera
import sys
import termios
import keyboard
import time
import tty
import csv


class Car:
    def __init__(self):
        self.i = 0
        self.camera = PiCamera()
        self.M11 = 15
        self.M12 = 13
        self.M21 = 21
        self.M22 = 23

        gpio.setmode(gpio.BOARD)
        gpio.setup(self.M11, gpio.OUT)
        gpio.setup(self.M12, gpio.OUT)
        gpio.setup(self.M21, gpio.OUT)
        gpio.setup(self.M22, gpio.OUT)

    def forward(self):
        gpio.output(self.M11, True)
        gpio.output(self.M12, False)
        gpio.output(self.M21, True)
        gpio.output(self.M22, False)
        print("Forward")

        time.sleep(0.3)
        gpio.output(self.M11, False)
        gpio.output(self.M12, False)
        gpio.output(self.M21, False)
        gpio.output(self.M22, False)

    def reverse(self):
        gpio.output(self.M11, False)
        gpio.output(self.M12, True)
        gpio.output(self.M21, False)
        gpio.output(self.M22, True)
        print("Reverse")

        time.sleep(0.3)
        gpio.output(self.M11, False)
        gpio.output(self.M12, False)
        gpio.output(self.M21, False)
        gpio.output(self.M22, False)

    def left(self):
        gpio.output(self.M11, True)
        gpio.output(self.M12, False)
        gpio.output(self.M21, False)
        gpio.output(self.M22, False)
        print("Left")

        time.sleep(0.3)
        gpio.output(self.M11, False)
        gpio.output(self.M12, False)
        gpio.output(self.M21, False)
        gpio.output(self.M22, False)

    def right(self):
        gpio.output(self.M11, False)
        gpio.output(self.M12, False)
        gpio.output(self.M21, True)
        gpio.output(self.M22, False)
        print("Right")

        time.sleep(0.3)
        gpio.output(self.M11, False)
        gpio.output(self.M12, False)
        gpio.output(self.M21, False)
        gpio.output(self.M22, False)

    def getch(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


if __name__ == '__main__':
    car = Car()

    move = {'w': car.forward, 'a': car.left,
            's': car.reverse, 'd': car.right, 'e': exit}

    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        while True:
            char = car.getch()
            path = '/home/pi/Documents/images/image_' + str(car.i) + '.jpg'
            car.camera.capture(path)
            car.i += 1

            writer.writerow((path, char))

            move[char]()


# Alternate way of taking keyboard input
# def on_press(key):
#     if key == Key.up:
#         forward()


# def on_release(key):
#     print('{0} release'.format(
#         key))
#     if key == Key.esc:
#         # Stop listener
#         return False


# # Collect events until released
# with Listener(
#         on_press=on_press,
#         on_release=on_release) as listener:
#     listener.join()
