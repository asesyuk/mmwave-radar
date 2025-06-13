# ****************************************************************************
# * (C) Copyright 2020, Texas Instruments Incorporated. - www.ti.com
# ****************************************************************************
# *
# *  Redistribution and use in source and binary forms, with or without
# *  modification, are permitted provided that the following conditions are
# *  met:
# *
# *    Redistributions of source code must retain the above copyright notice,
# *    this list of conditions and the following disclaimer.
# *
# *    Redistributions in binary form must reproduce the above copyright
# *    notice, this list of conditions and the following disclaimer in the
# *     documentation and/or other materials provided with the distribution.
# *
# *    Neither the name of Texas Instruments Incorporated nor the names of its
# *    contributors may be used to endorse or promote products derived from
# *    this software without specific prior written permission.
# *
# *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# *  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# *  PARTICULAR TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# *  A PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT  OWNER OR
# *  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# *  EXEMPLARY, ORCONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# *  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# *  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# *  LIABILITY, WHETHER IN CONTRACT,  STRICT LIABILITY, OR TORT (INCLUDING
# *  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# *  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# *
# ****************************************************************************


# ****************************************************************************
# Sample mmW demo UART output parser script - should be invoked using python3
#       ex: python3 mmw_demo_example_script.py <recorded_dat_file_from_Visualizer>.dat
#
# Notes:
#   1. The parser_mmw_demo script will output the text version 
#      of the captured files on stdio. User can redirect that output to a log file, if desired
#   2. This example script also outputs the detected point cloud data in mmw_demo_output.csv 
#      to showcase how to use the output of parser_one_mmw_demo_output_packet
# ****************************************************************************

import os
import sys
import serial
import time
import numpy as np
import socket
from datetime import datetime
# import the parser function 
from parcer_XY_test     import parser_one_mmw_demo_output_packet


# GET VALUES FROM SERVER

import socket
import numpy as np

HOST = "192.168.30.152"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

data = []

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            data = data.decode('utf-8')
            split_data = data.split(', ')

           
#             if not data:
#                 tt = str(0).encode('utf-16')
#                 conn.sendall(tt)
#                 break
            message=HOST+" received the data"
            tt = message.encode('utf-8')
            conn.sendall(tt)
            conn.close()
            break
 

IDtemp=split_data[0]
ID=int(IDtemp[1:])
X=float(split_data[1])
Y=float(split_data[2])
Z=float(split_data[3])
sensor_delay=float(split_data[4])
yaw_psi=float(split_data[5])
pitch_theta=float(split_data[6])
roll_phi_temp=split_data[7]
roll_phi=float(roll_phi_temp[:-1])
print(ID, X, Y, Z, sensor_delay, yaw_psi, pitch_theta, roll_phi)

#------------------------------------------------------------

#msgFromClient = "Hello Server"
#bytesToSend = msgFromClient.encode('utf-8')
serverAddress = ('192.168.30.150',2222)
#serverAddress = ('localhost',2222) 
#serverAddress = ('MacBook-Pro.local',2222) 
#ServerIP = '172.16.18.26'
#ServerPort = 2222
bufferSize = 102400  
UDPClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# Change the configuration file name
configFileName = 'xwr18xx_profile_2023_07_26T08_46_17_507.cfg'
CLIport = {}
Dataport = {}
byteBuffer = np.zeros(2**15,dtype = 'uint8')
byteBufferLength = 0;

       
# ------------------------------------------------------------------

# Function to configure the serial ports and send the data from
# the configuration file to the radar

    # Open the serial ports for the configuration and the data ports
    
    # Raspberry pi
CLIport = serial.Serial('/dev/ttyACM0', 115200)
Dataport = serial.Serial('/dev/ttyACM1', 921600)
    
    # Windows
#CLIport = serial.Serial('COM10', 115200)
#Dataport = serial.Serial('COM9', 921600)

    # Read the configuration file and send it to the board
config = [line.rstrip('\r\n') for line in open(configFileName)]
for i in config:
    CLIport.write((i+'\n').encode())
    print(i)
    time.sleep(0.01)
        

# ------------------------------------------------------------------

# Function to parse the data insi de the configuration file

configParameters = {} # Initialize an empty dictionary to store the configuration parameters
    
    # Read the configuration file and send it to the board
config = [line.rstrip('\r\n') for line in open(configFileName)]
for i in config:
        
        # Split the line
    splitWords = i.split(" ")
        
        # Hard code the number of antennas, change if other configuration is used
    numRxAnt = 4
    numTxAnt = 2
        
        # Get the information about the profile configuration
    if "profileCfg" in splitWords[0]:
        startFreq = int(float(splitWords[2]))
        idleTime = int(splitWords[3])
        rampEndTime = float(splitWords[5])
        freqSlopeConst = float(splitWords[8])
        numAdcSamples = int(splitWords[10])
        numAdcSamplesRoundTo2 = 1;
            
        while numAdcSamples > numAdcSamplesRoundTo2:
            numAdcSamplesRoundTo2 = numAdcSamplesRoundTo2 * 2;
                
        digOutSampleRate = int(splitWords[11]);
            
        # Get the information about the frame configuration    
    elif "frameCfg" in splitWords[0]:
            
        chirpStartIdx = int(splitWords[1]);
        chirpEndIdx = int(splitWords[2]);
        numLoops = int(splitWords[3]);
        numFrames = int(splitWords[4]);
        framePeriodicity = int(splitWords[5]);
##################################################################################
# INPUT CONFIGURATION
##################################################################################
# get the captured file name (obtained from Visualizer via 'Record Start')
#if (len(sys.argv) > 1):
  #  capturedFileName=sys.argv[1]
#capturedFileName = 'xwr16xx_processed_stream_2023_01_25T13_32_00_318.dat'
#else:
 #   print ("Error: provide file name of the saved stream from Visualizer for OOB demo")
  #  exit()
#ser = serial.Serial('COM9', 921600)

#outfile = open('data.dat','a')

while True:

    
    #message = "Hello Server"
    #message = message.encode('utf-8')
    #UDPClient.sendto(message, serverAddress)
    #time.sleep(1)
    #data,address = UDPClient.recvfrom(bufferSize)
    #data = data.decode('utf-8')
#outfile = open('data.dat','w+')
    byteCount = Dataport.inWaiting()
    s = Dataport.read(byteCount)
    #s = str(s).encode('utf-8')
    #UDPClient.sendto(s, serverAddress)
#s = s.decode('utf-8').strip()
    #print(s)
##################################################################################
# USE parser_mmw_demo SCRIPT TO PARSE ABOVE INPUT FILES
##################################################################################
# Read the entire file 
#fp = open(capturedFileName,'rb')
#readNumBytes = os.path.getsize(capturedFileName)
    readNumBytes = byteCount
#print("readNumBytes: ", readNumBytes)
    allBinData = s
    
    #if readNumBytes < 864:

    #if allBinData == "b''":
        #pass
    #else:
#print("allBinData: ", allBinData[0], allBinData[1], allBinData[2], allBinData[3])
                 #fp.close()

# init local variables
    totalBytesParsed = 0;
    numFramesParsed = 0;

    # parser_one_mmw_demo_output_packet extracts only one complete frame at a time
    # so call this in a loop till end of file
    while (totalBytesParsed < readNumBytes):
        
        # parser_one_mmw_demo_output_packet function already prints the
        # parsed data to stdio. So showcasing only saving the data to arrays 
        # here for further custom processing
        parser_result, \
        headerStartIndex,  \
        totalPacketNumBytes, \
        numDetObj,  \
        numTlv,  \
        subFrameNumber,  \
        detectedX_array,  \
        detectedY_array,  \
        detectedZ_array,  \
        detectedV_array,  \
        detectedRange_array,  \
        detectedAzimuth_array,  \
        detectedElevation_array,  \
        detectedSNR_array,  \
        detectedNoise_array = parser_one_mmw_demo_output_packet(allBinData[totalBytesParsed::1], readNumBytes-totalBytesParsed, ID, X, Y, Z, yaw_psi, pitch_theta, roll_phi)

        # Check the parser result
        #print ("Parser result: ", parser_result)
        #parser_result = str(parser_result).encode('utf-8')
        #UDPClient.sendto(parser_result, serverAddress)
        if (parser_result == 0): 
            totalBytesParsed += (headerStartIndex+totalPacketNumBytes)    
            numFramesParsed+=1
            #print("totalBytesParsed: ", totalBytesParsed)
            #totalBytesParsed = str(totalBytesParsed).encode('utf-8')
            #UDPClient.sendto(totalBytesParsed, serverAddress)
            #totalBytesParsed = totalBytesParsed.decode('utf-8')
            #UDPClient.sendto("totalBytesParsed: ", totalBytesParsed, serverAddress)
            ##################################################################################
            #   TODO: use the arrays returned by above parser as needed. 
            # For array dimensions, see help(parser_one_mmw_demo_output_packet)
            # help(parser_one_mmw_demo_output_packet)
            ##################################################################################

            
            # For example, dump all S/W objects to a csv file
#             import csv
#             if (numFramesParsed == 1):
#                 democsvfile = open('mmw_demo_output.csv', 'w', newline='')                
#                 demoOutputWriter = csv.writer(democsvfile, delimiter=',',
#                                         quotechar='', quoting=csv.QUOTE_NONE)                                    
#                 demoOutputWriter.writerow(["frame","DetObj#","x","y","z","v","snr","noise"])            
#                 
#             for obj in range(numDetObj):
#                 demoOutputWriter.writerow([numFramesParsed-1, obj, detectedX_array[obj],\
#                                             detectedY_array[obj],\
#                                             detectedZ_array[obj],\
#                                             detectedV_array[obj],\
#                                             detectedSNR_array[obj],\
#                                             detectedNoise_array[obj]])

            
        else: 
            # error in parsing; exit the loop
            break

#     dt = datetime.now()
#     ts = datetime.timestamp(dt)
    
    
    
    
    time.sleep(sensor_delay)
    # All processing done; Exit
    UDPstring = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    print(UDPstring)
    UDPstring = str(UDPstring).encode('utf-16')
    UDPClient.sendto(UDPstring, serverAddress)
    
    
    
    
    #numFramesParsed = str(numFramesParsed).encode('utf-8')
    #UDPClient.sendto(numFramesParsed, serverAddress)
    #UDPClient.sendto(numFramesParsed.encode(),(ServerIP, ServerPort))

    
          
          