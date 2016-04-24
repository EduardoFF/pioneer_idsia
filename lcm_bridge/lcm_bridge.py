import lcm
from pose_t import pose_t


""" create lcm """
lc = lcm.LCM("udpm://239.255.76.67:7667?ttl=1")



""" to send pose, just call this one """
def send_pose(robotid, longitude, latitude, altitude):
    msg = pose_t()
    channel = "POSE"
    msg.robotid = robotid
    msg.position =  [longitude,latitude,altitude]
    msg.orientation = [0,0,0,0]
    lc.publish(channel, msg.encode())


""" handles incoming WAYPOINTS """
def my_handler(channel, data):
    msg = flow_list_t.decode(data)
    print("Received message on channel \"%s\"" % channel)
    print("   timestamp   = %d" % msg.timestamp)
    print("   addr    = %s" % str(msg.addr))
    print("   n    = %d" % msg.n)
    for i in range(msg.n):
        print "flow_%d: "%(i),
        print "addr: %s -> %s "%(msg.flows[i].src_addr, msg.flows[i].dst_addr),
        print "pkt_cnt %d "%(msg.flows[i].pkt_count),
        print "byte_cnt %d "%(msg.flows[i].byte_count),
        print "rate %f "%(msg.flows[i].data_rate),
        print "last_act %d "%(msg.flows[i].last_activity),
    print("")

    
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


