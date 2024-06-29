from gpiozero import Robot
from pynput.keyboard import Key, Listener
import RPi.GPIO as gpio
from picamera import PiCamera
import curses
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
        self.M21 = 22
        self.M22 = 24

        gpio.setmode(gpio.BOARD)
        gpio.cleanup()
        gpio.setup(self.M11, gpio.OUT)
        gpio.setup(self.M12, gpio.OUT)
        gpio.setup(self.M21, gpio.OUT)
        gpio.setup(self.M22, gpio.OUT)

        self.file = open('data.csv', 'w', newline='')
        self.writer = csv.writer(self.file)

    def right(self):
        gpio.output(self.M11, True)
        gpio.output(self.M12, False)
        gpio.output(self.M21, False)
        gpio.output(self.M22, False)
        print("Right")

        # time.sleep(0.3)
        # gpio.output(self.M11, False)
        # gpio.output(self.M12, False)
        # gpio.output(self.M21, False)
        # gpio.output(self.M22, False)

    def left(self):
        gpio.output(self.M11, False)
        gpio.output(self.M12, False)
        gpio.output(self.M21, False)
        gpio.output(self.M22, True)
        print("Left")

        # time.sleep(0.3)
        # gpio.output(self.M11, False)
        # gpio.output(self.M12, False)
        # gpio.output(self.M21, False)
        # gpio.output(self.M22, False)

    def forward(self):
        gpio.output(self.M11, True)
        gpio.output(self.M12, False)
        gpio.output(self.M21, False)
        gpio.output(self.M22, True)
        print("Forward")

    def reset(self):
        time.sleep(0.1)
        gpio.output(self.M11, False)
        gpio.output(self.M12, False)
        gpio.output(self.M21, False)
        gpio.output(self.M22, False)

    def reverse(self):
        gpio.output(self.M11, False)
        gpio.output(self.M12, True)
        gpio.output(self.M21, True)
        gpio.output(self.M22, False)
        print("Reverse")

        # time.sleep(0.3)
        # gpio.output(self.M11, False)
        # gpio.output(self.M12, False)
        # gpio.output(self.M21, False)
        # gpio.output(self.M22, False)

    # def getch(self):
    #     fd = sys.stdin.fileno()
    #     old_settings = termios.tcgetattr(fd)
    #     try:
    #         tty.setraw(sys.stdin.fileno())
    #         ch = sys.stdin.read(1)
    #     finally:
    #         termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    #     return ch

    def on_press(self, key):

        if key == Key.up:
            print("Forward")
            self.path = '/home/pi/Documents/images/image_' + \
                str(self.i) + '.jpg'
            self.camera.capture(self.path)
            self.i += 1
            self.writer.writerow((self.path, 0))
            self.forward()
        elif key == Key.down:
            print("Reverse")

            self.reset()
        elif key == Key.left:
            print('Left')
            self.path = '/home/pi/Documents/images/image_' + \
                str(self.i) + '.jpg'
            self.camera.capture(self.path)
            self.i += 1
            self.writer.writerow((self.path, 2))
            self.left()
        elif key == Key.right:
            print('Right')
            self.path = '/home/pi/Documents/images/image_' + \
                str(self.i) + '.jpg'
            self.camera.capture(self.path)
            self.i += 1
            self.writer.writerow((self.path, 3))
            self.right()

        elif key == Key.e:
            self.file.close()

    def on_release(self, key):
        pass


if __name__ == '__main__':
    car = Car()

    with Listener(
            on_press=car.on_press,
            on_release=car.on_release) as listener:
        listener.join()

    # with open('data.csv', 'w', newline='') as file:
    #     writer = csv.writer(file)

    #     while True:
    #         char = car.getch()
    #         path = '/home/pi/Documents/images/image_' + str(car.i) + '.jpg'
    #         car.camera.capture(path)
    #         car.i += 1

    #         writer.writerow((path, char))
