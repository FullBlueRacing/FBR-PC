from protobuf.fbr_pb2 import telemetry_message
from google.protobuf.message import DecodeError
import struct
import pylab as plt
import sys

# Definitions

MAX_G = 		5.0     # MUST BE CHANGED ACCORDING TO CAR SPECIFICATIONS
MIN_G = 		-5.0	
MIN_COOLANT = 	-10															
MAX_COOLANT = 	100		
MIN_MANIFOLD = 	-10															
MAX_MANIFOLD = 	100		
MIN_GEAR = 		-1															
MAX_GEAR = 		6			
MIN_AIRTEMP = 	-10															
MAX_AIRTEMP = 	50		
MIN_SPEED = 	-10														
MAX_SPEED = 	150		
MIN_LAMBDA = 	-10														
MAX_LAMBDA = 	10		
MIN_OILTEMP = 	-10													
MAX_OILTEMP = 	100		
MIN_RPM = 		-10												
MAX_RPM = 		10000	
MIN_VOLTAGE = 	-1												
MAX_VOLTAGE = 	15		
MIN_THROTTLE = 	-10												
MAX_THROTTLE = 	100		

#

data = file(sys.argv[1], "rb")
log = []
count = 0

# Read data from log file and append telemetry object to log

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
	count = count + 1
		
    except DecodeError as e:
        print(e)
        break

# Display data as a function of time (in minutes) instead of number of samples
time = []
labels_locs = []   # locations of labels
labels_vals = []   # values of labels
time_range = (count//100)   # max range in seconds (rough integer division) (100Hz)
for i in range (0, time_range):
	time.append(i)					# fill time list with values
time_range = time_range//60
for i in range (0, time_range):
	labels_vals.append(i)
for i in range (1, time_range):
	labels_locs.append(time[i]*100*60) # find location of the corresponding labels
	
# Set up graph to display raw acceleration
plt.figure(1)
plt.title('FBR 2014')
plt.subplot(321)
plt.xticks(labels_locs, labels_vals)
volts_x = [x.accel_x for x in log]
volts_x = [x.accel_x for x in log]
volts_xdn = [x.accel_x for x in log]
plt.axis([0.0, count,MIN_G,MAX_G])
plt.ylabel('Acceleration (xG)')
plt.title('Raw acceleration data')
plt.xticks(labels_locs, labels_vals)
plt.plot(volts_x)

# Set up filter to make acceleration data smoother
filter_width=25
convolution_integers=[-253,-138,-33,62,147,222,287,343,387,422,447,462,467,462,447,422,387,343,287,222,147,62,-33,-138,-253]
sum_conv_int=5177
for i in range (1+filter_width/2, len(volts_x)-filter_width/2):
    volts_xdn[i] = 0
    for j in range (-filter_width/2, filter_width/2):
        volts_xdn[i]=volts_xdn[i]+convolution_integers[j+filter_width/2]*volts_x[i+j]
    volts_xdn[i]=volts_xdn[i]/sum_conv_int
	
# Set up graph to display filtered acceleration data
plt.subplot(323)
plt.xticks(labels_locs, labels_vals)
plt.axis([0.0, count,MIN_G,MAX_G])
plt.ylabel('Acceleration (xG)')
plt.title('Filtered acceleration data')
plt.plot(volts_xdn)

# Set up graph to display throttle position data
throttle = [x.throttle_pos for x in log]
plt.subplot(325)
plt.xticks(labels_locs, labels_vals)
plt.axis([0.0, count, MIN_THROTTLE, MAX_THROTTLE])
plt.xlabel('Time (min)')
plt.ylabel('Position')
plt.title('Throttle position')
plt.plot(throttle, 'r')

# Set up graph to display speed
speed = [x.speed for x in log]
plt.subplot(322)
plt.xticks(labels_locs, labels_vals)
plt.axis([0.0, count, MIN_SPEED, MAX_SPEED])
plt.ylabel('Speed')
plt.title('Speed')
plt.plot(speed)

# Set up graph to display rpm
rpm = [x.rpm for x in log]
plt.subplot(324)
plt.xticks(labels_locs, labels_vals)
plt.axis([0.0, count, MIN_RPM, MAX_RPM])
plt.ylabel('RPM')
plt.title('RPM')
plt.plot(rpm, 'r')
 
# Set up graph to display gear change data
plt.subplot(326)
gear = [x.gear for x in log]
plt.axis([0.0,count,MIN_GEAR,MAX_GEAR])
plt.xticks(labels_locs, labels_vals)
plt.xlabel('Time (min)')
plt.ylabel('Gear')
plt.title('Gear changes')
plt.plot(gear, 'ks')

#plt.show()

#########################################################################################
plt.figure(2)

# Set up graph to display raw coolant temperature data
plt.subplot(321)
coolant_temp = [x.coolant_temp for x in log]
plt.axis([0.0,count, MIN_COOLANT, MAX_COOLANT])
plt.xticks(labels_locs, labels_vals)
plt.ylabel('Temperature (C)')
plt.title('Coolant Temperature');
plt.plot(coolant_temp, 'r')

# Set up graph to display raw manifold pressure data
plt.subplot(322)
manifold_pressure = [x.manifold_pres for x in log]
plt.axis([0.0,count,MIN_MANIFOLD,MAX_MANIFOLD])
plt.xticks(labels_locs, labels_vals)
plt.ylabel('Pressure reading')
plt.title('Manifold Pressure')
plt.plot(manifold_pressure)

# Set up graph to display air intake temperature
plt.subplot(323)
airtemp = [x.air_temp for x in log]
plt.axis([0.0,count,MIN_AIRTEMP,MAX_AIRTEMP])
plt.xticks(labels_locs, labels_vals)
plt.ylabel('Temperature')
plt.title('Air intake temperature')
plt.plot(airtemp, 'r')

# Set up graph to display oil temperature
plt.subplot(324)
oil = [x.oil_temp for x in log]
plt.axis([0.0,count,MIN_OILTEMP,MAX_OILTEMP])
plt.xticks(labels_locs, labels_vals)
plt.ylabel('Temperature')
plt.title('Oil Temperature')
plt.plot(oil, 'r')

# Set up graph to display battery voltage
plt.subplot(325)
voltage = [x.voltage for x in log]
plt.axis([0.0,count,MIN_VOLTAGE,MAX_VOLTAGE])
plt.xticks(labels_locs, labels_vals)
plt.xlabel('Time (min)')
plt.ylabel('Voltage')
plt.title('Battery voltage')
plt.plot(voltage, 'k')

# Set up graph to display data from lambda sensor
plt.subplot(326)
lambda_sensor = volts_xdn             #############################################
#lambda_sensor = [x.lambda for x in log]                  # PROBLEM WITH DEFINITION FOR LAMBDA SENSOR VARIABLE IN TELEMETRY OBJECT
plt.axis([0.0,count,MIN_LAMBDA,MAX_LAMBDA]) ######################################
plt.xticks(labels_locs, labels_vals)
plt.xlabel('Time (min)')
plt.ylabel('Lambda Value')
plt.title('Lambda Sensor')
plt.plot(lambda_sensor, 'k')

plt.show()