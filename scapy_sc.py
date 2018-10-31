from scapy.all import *
import random
import optparse
import time
import datetime

def makePorts(port_str = None):
    default_ports = [21,22,23,25,69,80,81,82,83,84,110,389,389,443,445,488,512,513,514,873,901,1043,1080,1099,1090,1158,1352,1433,1434,1521,2049,2100,2181,2601,2604,3128,3306,3307,3389,4440,4444,4445,4848,5000,5280,5432,5500,5632,5900,5901,5902,5903,5984,6000,6033,6082,6379,6666,7001,7001,7002,7070,7101,7676,7777,7899,7988,8000,8001,8002,8003,8004,8005,8006,8007,8008,8009,8069,8080,8081,8082,8083,8084,8085,8086,8087,8088,8089,8090,8091,8092,8093,8094,8095,8098,8099,8980,8990,8443,8686,8787,8880,8888,9000,9001,9043,9045,9060,9080,9081,9088,9088,9090,9091,9100,9200,9300,9443,9871,9999,10000,10068,10086,11211,20000,22022,22222,27017,28017,50060,50070]
    try:
        if port_str:
            default_ports = []
            if "," in port_str:
                temp_ports = port_str.split(",")
                for p in temp_ports:
                    default_ports.append(int(p))
            elif "-" in port_str:
                for x in xrange(int(port_str.split("-")[0]),int(port_str.split("-")[1])):
                    default_ports.append(int(x))
            else:
                pass
    except Exception as e:
        pass
    return list(set(default_ports))

if __name__ == "__main__":
    start = time.time()

    parser = optparse.OptionParser('usage: sudo python scapy_sc.py -i 221.216.75.205 -p 1-10000')
    parser.add_option('-i', dest='ip', type='string', help='ip for scanner')
    parser.add_option('-p', dest='port', type='string', help='ports for scanner')
    parser.add_option('-t', dest='timeout', type='string', help='timeout for scanner')

    (options, args) = parser.parse_args()
    port_sub = options.port
    ip = options.ip
    timeout = options.timeout
    print "Starting Scapy Portscan with SYN at %s " % (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    if (ip is not None):
        ports = makePorts(port_str=port_sub)
        if timeout is None:
            timeout = 2
    ans, unans = sr( IP(dst=ip)/TCP(flags="S", dport=ports),timeout=int(timeout))

    ans.filter(lambda (s, r): TCP in r and r[TCP].flags & 2).make_table(lambda (s, r):(s.dst, s.dport, "is open"))
    end = time.time()

    print "[*] scanned in %s s" % str(end - start)
