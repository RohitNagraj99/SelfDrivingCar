from picamera import PiCamera
from time import sleep

camera  = PiCamera()
camera.rotation = 0

# Preview
#camera.start_preview(alpha = 200) # 0<= alpha(transperancy) <= 255
#sleep(5)
#camera.stop_preview()

# Capturing image
camera.start_preview()
sleep(5)
camera.capture('/home/pi/Documents/image.jpg')
camera.stop_preview()

# Brightness
camera.start_preview()
for i in range(100):
    camera.annotate_text = "Constrast: %s" % i
    camera.contrast = i
    sleep(0.2)
camera.stop_preview()