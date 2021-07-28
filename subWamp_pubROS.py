#questo file deve servire a iscriversi al topic della webcam su WAMP
#e deve elaborare e pubblicare sul topic ros 
#in modo tale che possa far muovere il robot


from os import environ
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

import rospy
from geometry_msgs.msg import Twist

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner

def move(x, y, z, ax, ay, az):
    # Starts a new node
    rospy.init_node('robot_cleaner', anonymous=True)
    velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    vel_msg = Twist()

    #Receiveing the user's input
    print("Let's move your robot")
    #speed = input("Input your speed:")
    distance = 5
    isForward = True #input("Foward?: ")#True or False

    #Checking if the movement is forward or backwards
    if(isForward):
        vel_msg.linear.x = abs(x)
    else:
        vel_msg.linear.x = -abs(x)
    #Since we are moving just in x-axis
    vel_msg.linear.y = y
    vel_msg.linear.z = z
    vel_msg.angular.x = ax
    vel_msg.angular.y = ay
    vel_msg.angular.z = az

    while not rospy.is_shutdown():

        #Setting the current time for distance calculus
        t0 = rospy.Time.now().to_sec()
        current_distance = 0

        #Loop to move the turtle in an specified distance
        while(current_distance < distance):
            #Publish the velocity
            velocity_publisher.publish(vel_msg)
            #Takes actual time to velocity calculus
            t1=rospy.Time.now().to_sec()
            #Calculates distancePoseStamped
            current_distance= 0.5*(t1-t0) #speed*(t1-t0)
        #After the loop, stops the robot
        vel_msg.linear.x = 0
        #Force the robot to stop
        velocity_publisher.publish(vel_msg)


class Component(ApplicationSession):
    """
    An application component that subscribes and receives events, and
    stop after having received 5 events.
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")
        self.received = 0
        sub = yield self.subscribe(self.on_event, 'com.myapp.topic1')
        print("Subscribed to com.myapp.topic1 with {}".format(sub.id))

    def on_event(self, xt, x, yt, y, wt, w, ht, h):
        print("Got event: {} {} {} {} {} {} {} {}".format(xt, x, yt, y, wt, w, ht, h))
        self.received += 1
        move(0,5,0,0,0,0)
        # self.config.extra for configuration, etc. (see [A])
        if self.received > self.config.extra['max_events']:
            print("Received enough events; disconnecting.")
            self.leave()

    def onDisconnect(self):
        print("disconnected")
        if reactor.running:
            reactor.stop()


if __name__ == '__main__':
    url = environ.get("AUTOBAHN_DEMO_ROUTER", "ws://212.189.207.233:8181/ws")
    realm = "s4t"
    extra=dict(
        max_events=5,  # [A] pass in additional configuration
    )
    runner = ApplicationRunner(url, realm, extra)
    runner.run(Component)