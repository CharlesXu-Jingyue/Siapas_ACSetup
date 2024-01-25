# from time import sleep
# from picamera import PiCamera

# camera = PiCamera()
# camera.resolution = (1024, 768)

# try:
#     camera.start_preview()
#     # Camera warm-up time
#     sleep(2)
#     camera.capture('my_picture.jpg')
# finally:
#     camera.stop_preview()
#     camera.close()

from picamera2 import Picamera2, Preview
import time
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start_preview(Preview.DRM)
picam2.start()
time.sleep(2)
picam2.capture_file("HelloWorld.jpg")