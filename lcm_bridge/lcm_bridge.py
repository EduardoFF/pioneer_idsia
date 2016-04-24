import lcm
from pos_gps_t import pos_gps_t
from plan_waypoint_t import plan_waypoint_t

""" create lcm """
lc = lcm.LCM("udpm://239.255.76.67:7667?ttl=1")



""" to send pose, just call this one """
""" robotid (uint8_t) is a parameter of the node """
def send_pose(robotid, longitude, latitude, altitude):
    msg = pos_gps_t()
    channel = "POSGPS"
    msg.robotid = robotid
    msg.longitude = longitude
    msg.latitude = latitude
    msg.altitude = altitude
    lc.publish(channel, msg.encode())


""" handles incoming WAYPOINTS """
def my_handler(channel, data):
    msg = plan_waypoint_t.decode(data)
    """ the waypoint is: """
    print "the waypoint is ", msg.latitude, msg.longitude, msg.altitude
    
subscription = lc.subscribe("RNPPOS", my_handler)

"""
lcm.handle should be called periodically to handle the incoming
messages

"""
try:
    while True:
        lc.handle()
except KeyboardInterrupt:
    pass

lc.unsubscribe(subscription)


