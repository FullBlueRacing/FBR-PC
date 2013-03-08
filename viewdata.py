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



volts_x = [x.accel_x for x in log]
volts_x = [x.accel_x for x in log]
volts_xdn = [x.accel_x for x in log]   
plt.axis([0.0, 100000,-3.0,3.0])
plt.plot(volts_x)
plt.show()
#############################################################################################
#Savitzky-Golay Filter
#The numbers below are calculated from a complicated formula, so 
#it's just better to copy them from a table

filter_width=25
convolution_integers=[-253,-138,-33,62,147,222,287,343,387,422,447,462,467,462,447,422,387,343,287,222,147,62,-33,-138,-253]
sum_conv_int=5177
for i in range (1+filter_width/2, len(volts_x)-filter_width/2):
    volts_xdn[i] = 0
    for j in range (-filter_width/2, filter_width/2):
        volts_xdn[i]=volts_xdn[i]+convolution_integers[j+filter_width/2]*volts_x[i+j]
    volts_xdn[i]=volts_xdn[i]/sum_conv_int
plt.plot(volts_xdn)
plt.show()

#############################################################################################

#coolant_temp = [x.coolant_temp for x in log]
#plt.plot(coolant_temp)
#plt.show()
 