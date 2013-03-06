from protobuf.fbr_pb2 import telemetry_message
from google.protobuf.message import DecodeError
import struct
import pylab as plt
import sys

data = file(sys.argv[1], "rb")

log = []

while True:
    len_str = data.read(4)
    
    if len(len_str) <> 4:
        break
    
    len_int, = struct.unpack("<I", len_str)
    message = data.read(len_int)
    #print("{} {}".format(len_int, len(message)))
    try:
        telemetry = telemetry_message()
        telemetry.ParseFromString(message)
        log.append(telemetry)
    except DecodeError as e:
        print(e)
        break

volts = [x.accel_x for x in log]    
plt.plot(volts)
plt.show()

coolant_temp = [x.coolant_temp for x in log]
plt.plot(coolant_temp)
plt.show()
 