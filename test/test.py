from iotronic_lightningrod.modules.plugins import Plugin
# from iotronic_lightningrod.modules.plugins import pluginApis as API

from oslo_log import log as logging
LOG = logging.getLogger(__name__)

# User imports
import time
from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from twisted.internet.defer import inlineCallbacks
from os import environ
import cv2
import numpy as np

url = environ.get("AUTOBAHN_DEMO_ROUTER", "ws://212.189.207.233:8181/ws")
realm = "s4t"

class Component(ApplicationSession):
    @inlineCallbacks
    def onJoin(self, details):
        cap = cv2.VideoCapture(0)
        while(cap.isOpened()):
            ret, imageFrame = cap.read()
            hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV) # Convert the imageFrame in BGR(RGB color space) to HSV(hue-saturation-value) color space
            red_lower = np.array([136, 87, 111], np.uint8)
            red_upper = np.array([180, 255, 255], np.uint8)
            red_mask = cv2.inRange(hsvFrame, red_lower, red_upper) # Set range for red color and define mask
            kernal = np.ones((5, 5), "uint8")
            # For red color
            red_mask = cv2.dilate(red_mask, kernal)
            res_red = cv2.bitwise_and(imageFrame, imageFrame, mask = red_mask)

            # Creating contour to track red color
            contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if(area > 300):
                    x, y, w, h = cv2.boundingRect(contour)
                    #print("backend publishing x:{} y:{} w:{} h:{}".format(x,y,w,h))
                    LOG.info("backend publishing x:{} y:{} w:{} h:{}".format(x,y,w,h))
                    self.publish('com.myapp.topic1', " x: ", x , " y: ", y , " w: ", w , " h: ", h)
                    time.sleep(1)
                    #imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    #cv2.putText(imageFrame, "Red Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255))


class Worker(Plugin.Plugin):
    def __init__(self, name, params=None):
        super(Worker, self).__init__(name,  params)

    def run(self):
        LOG.info("Plugin " + self.name + " starting...")
        runner = ApplicationRunner(url, realm)
        runner.run(Component)
