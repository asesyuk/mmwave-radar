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

# import the required Python packages
import struct
import math
import binascii
import codecs
import socket
import time
import numpy as np
from datetime import datetime

# definations for parser pass/fail
TC_PASS   =  0
TC_FAIL   =  1

serverAddress = ('192.168.30.150',2222)
#serverAddress = ('localhost',2222) 
#serverAddress = ('MacBook-Pro.local',2222)

UDPClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def getUint32(data):
    """!
       This function coverts 4 bytes to a 32-bit unsigned integer.

        @param data : 1-demension byte array  
        @return     : 32-bit unsigned integer
    """ 
    return (data[0] +
            data[1]*256 +
            data[2]*65536 +
            data[3]*16777216)

def getUint16(data):
    """!
       This function coverts 2 bytes to a 16-bit unsigned integer.

        @param data : 1-demension byte array
        @return     : 16-bit unsigned integer
    """ 
    return (data[0] +
            data[1]*256)

def getHex(data):
    """!
       This function coverts 4 bytes to a 32-bit unsigned integer in hex.

        @param data : 1-demension byte array
        @return     : 32-bit unsigned integer in hex
    """ 
    return (binascii.hexlify(data[::-1]))

def checkMagicPattern(data):
    """!
       This function check if data arrary contains the magic pattern which is the start of one mmw demo output packet.  

        @param data : 1-demension byte array
        @return     : 1 if magic pattern is found
                      0 if magic pattern is not found 
    """ 
    found = 0
    if (data[0] == 2 and data[1] == 1 and data[2] == 4 and data[3] == 3 and data[4] == 6 and data[5] == 5 and data[6] == 8 and data[7] == 7):
        found = 1
    return (found)
          
def parser_helper(data, readNumBytes):
    
    """!
       This function is called by parser_one_mmw_demo_output_packet() function or application to read the input buffer, find the magic number, header location, the length of frame, the number of detected object and the number of TLV contained in this mmw demo output packet.

        @param data                   : 1-demension byte array holds the the data read from mmw demo output. It ignorant of the fact that data is coming from UART directly or file read.  
        @param readNumBytes           : the number of bytes contained in this input byte array  
            
        @return headerStartIndex      : the mmw demo output packet header start location
        @return totalPacketNumBytes   : the mmw demo output packet lenght           
        @return numDetObj             : the number of detected objects contained in this mmw demo output packet          
        @return numTlv                : the number of TLV contained in this mmw demo output packet           
        @return subFrameNumber        : the sbuframe index (0,1,2 or 3) of the frame contained in this mmw demo output packet
    """ 

    headerStartIndex = -1

    for index in range (readNumBytes):
        if checkMagicPattern(data[index:index+8:1]) == 1:
            headerStartIndex = index
            break
  
    if headerStartIndex == -1: # does not find the magic number i.e output packet header 
        totalPacketNumBytes = -1
        numDetObj           = -1
        numTlv              = -1
        subFrameNumber      = -1
        platform            = -1
        frameNumber         = -1
        timeCpuCycles       = -1
    else: # find the magic number i.e output packet header 
        totalPacketNumBytes = getUint32(data[headerStartIndex+12:headerStartIndex+16:1])
        platform            = getHex(data[headerStartIndex+16:headerStartIndex+20:1])
        frameNumber         = getUint32(data[headerStartIndex+20:headerStartIndex+24:1])
        timeCpuCycles       = getUint32(data[headerStartIndex+24:headerStartIndex+28:1])
        numDetObj           = getUint32(data[headerStartIndex+28:headerStartIndex+32:1])
        numTlv              = getUint32(data[headerStartIndex+32:headerStartIndex+36:1])
        subFrameNumber      = getUint32(data[headerStartIndex+36:headerStartIndex+40:1])
    
    #print("headerStartIndex    = %d" % (headerStartIndex))
    #print("totalPacketNumBytes = %d" % (totalPacketNumBytes))
    #print("platform            = %s" % (platform)) 
    #print("frameNumber         = %d" % (frameNumber)) 
    #print("timeCpuCycles       = %d" % (timeCpuCycles))   
    #print("numDetObj           = %d" % (numDetObj)) 
    #print("numTlv              = %d" % (numTlv))
    #print("subFrameNumber      = %d" % (subFrameNumber))   
                              
    return (headerStartIndex, totalPacketNumBytes, numDetObj, numTlv, subFrameNumber)


def parser_one_mmw_demo_output_packet(data, readNumBytes, ID, X_translation, Y_translation, Z_translation, yaw_psi, pitch_theta, roll_phi):
    """!
       This function is called by application. Firstly it calls parser_helper() function to find the start location of the mmw demo output packet, then extract the contents from the output packet.
       Each invocation of this function handles only one frame at a time and user needs to manage looping around to parse data for multiple frames.

        @param data                   : 1-demension byte array holds the the data read from mmw demo output. It ignorant of the fact that data is coming from UART directly or file read.  
        @param readNumBytes           : the number of bytes contained in this input byte array  
            
        @return result                : parser result. 0 pass otherwise fail
        @return headerStartIndex      : the mmw demo output packet header start location
        @return totalPacketNumBytes   : the mmw demo output packet lenght           
        @return numDetObj             : the number of detected objects contained in this mmw demo output packet          
        @return numTlv                : the number of TLV contained in this mmw demo output packet           
        @return subFrameNumber        : the sbuframe index (0,1,2 or 3) of the frame contained in this mmw demo output packet
        @return detectedX_array       : 1-demension array holds each detected target's x of the mmw demo output packet
        @return detectedY_array       : 1-demension array holds each detected target's y of the mmw demo output packet
        @return detectedZ_array       : 1-demension array holds each detected target's z of the mmw demo output packet
        @return detectedV_array       : 1-demension array holds each detected target's v of the mmw demo output packet
        @return detectedRange_array   : 1-demension array holds each detected target's range profile of the mmw demo output packet
        @return detectedAzimuth_array : 1-demension array holds each detected target's azimuth of the mmw demo output packet
        @return detectedElevAngle_array : 1-demension array holds each detected target's elevAngle of the mmw demo output packet
        @return detectedSNR_array     : 1-demension array holds each detected target's snr of the mmw demo output packet
        @return detectedNoise_array   : 1-demension array holds each detected target's noise of the mmw demo output packet
    """

    headerNumBytes = 40
    
    

    PI = 3.14159265

    detectedX_array = []
    detectedY_array = []
    detectedZ_array = []
    detectedV_array = []
    detectedRange_array = []
    detectedAzimuth_array = []
    detectedElevAngle_array = []
    detectedSNR_array = []
    detectedNoise_array = []

    result = TC_PASS
    
    #headerStartIndex = int(headerStartIndex).encode('utf-8')
    #totalPacketNumBytes = int(totalPacketNumBytes).encode('utf-8')
    #readNumBytes = int(readNumBytes).encode('utf-8')
    
    # call parser_helper() function to find the output packet header start location and packet size 
    (headerStartIndex, totalPacketNumBytes, numDetObj, numTlv, subFrameNumber) = parser_helper(data, readNumBytes)
                         
    if headerStartIndex == -1:
        result = TC_FAIL
        # This is normal when no complete packet is available, don't spam with errors
        # print("************ Frame Fail, cannot find the magic words *****************")
        #fail_1 = str("************ Frame Fail, cannot find the magic words *****************").encode('utf-8')
        #UDPClient.sendto(fail_1, serverAddress)
    else:
        nextHeaderStartIndex = headerStartIndex + totalPacketNumBytes 

        if int(headerStartIndex) + int(totalPacketNumBytes) > int(readNumBytes):
            result = TC_FAIL
            # This is normal - just means we need more data, don't print error
            # print("********** Frame Fail, readNumBytes may not long enough ***********")
#             fail_2 = str("************ Frame Fail, cannot find the magic words *****************").encode('utf-8')
#             UDPClient.sendto(fail_2, serverAddress)
        elif int(nextHeaderStartIndex) + 8 < int(readNumBytes) and checkMagicPattern(data[int(nextHeaderStartIndex):int(nextHeaderStartIndex)+8:1]) == 0:
            result = TC_FAIL
            # This can happen during normal operation, don't print unless debugging
            # print("********** Frame Fail, incomplete packet **********") 
            #fail_3 = str("********** Frame Fail, incomplete packet **********").encode('utf-8')
            #UDPClient.sendto(fail_3, serverAddress) 
        elif int(numDetObj) < 0:
            result = TC_FAIL
            print("************ Frame Fail, invalid numDetObj = %d *****************" % (numDetObj))
            #fail_4 = str("************ Frame Fail, numDetObj = %s *****************").encode('utf-8')
            #numDetObj = str(numDetObj).encode('utf-8')
            #.sendto(fail_4 % (numDetObj), serverAddress)
        elif int(subFrameNumber) > 3:
            result = TC_FAIL
            print("************ Frame Fail, subFrameNumber = %d *****************" % (subFrameNumber))
            #fail_5 = str("************ Frame Fail, subFrameNumber = %s *****************").encode('utf-8')
            #subFrameNumber = str(subFrameNumber).encode('utf-8')
            #UDPClient.sendto(fail_5 % (subFrameNumber), serverAddress)
        else: 
            # process the 1st TLV
            tlvStart = int(headerStartIndex) + int(headerNumBytes)
                                                    
            tlvType    = getUint32(data[tlvStart+0:tlvStart+4:1])
            tlvLen     = getUint32(data[tlvStart+4:tlvStart+8:1])       
            offset = 8
            
            #print("The 1st TLV") 
            #print("    type %d" % (tlvType))
            #print("    len %d bytes" % (tlvLen))
            
            #TLV_1 = str("The 1st TLV").encode('utf-8')
            #UDPClient.sendto(TLV_1, serverAddress)
            #UDPClient.sendto(str("    type %d").encode('utf-8') % (tlvType), serverAddress)
            #UDPClient.sendto(str("    len %d bytes").encode('utf-8') % (tlvLen), serverAddress)
                                                    
            # the 1st TLV must be type 1
            if tlvType == 1 and int(tlvLen) < int(totalPacketNumBytes):#MMWDEMO_UART_MSG_DETECTED_POINTS
                         
                # TLV type 1 contains x, y, z, v values of all detect objects. 
                # each x, y, z, v are 32-bit float in IEEE 754 single-precision binary floating-point format, so every 16 bytes represent x, y, z, v values of one detect objects.    
                
                # for each detect objects, extract/convert float x, y, z, v values and calculate range profile and azimuth                           
                for obj in range(int(numDetObj)):
                    # convert byte0 to byte3 to float x value
                    x = struct.unpack('<f', codecs.decode(binascii.hexlify(data[tlvStart + offset:tlvStart + offset+4:1]),'hex'))[0]

                    # convert byte4 to byte7 to float y value
                    y = struct.unpack('<f', codecs.decode(binascii.hexlify(data[tlvStart + offset+4:tlvStart + offset+8:1]),'hex'))[0]

                    # convert byte8 to byte11 to float z value
                    z = struct.unpack('<f', codecs.decode(binascii.hexlify(data[tlvStart + offset+8:tlvStart + offset+12:1]),'hex'))[0]

                    # convert byte12 to byte15 to float v value
                    v = struct.unpack('<f', codecs.decode(binascii.hexlify(data[tlvStart + offset+12:tlvStart + offset+16:1]),'hex'))[0]

                    # calculate range profile from x, y, z
                    compDetectedRange = math.sqrt((x * x)+(y * y)+(z * z))

                    # calculate azimuth from x, y           
                    if y == 0:
                        if x >= 0:
                            detectedAzimuth = 90
                        else:
                            detectedAzimuth = -90 
                    else:
                        detectedAzimuth = math.atan(x/y) * 180 / PI

                    # calculate elevation angle from x, y, z
                    if x == 0 and y == 0:
                        if z >= 0:
                            detectedElevAngle = 90
                        else: 
                            detectedElevAngle = -90
                    else:
                        detectedElevAngle = math.atan(z/math.sqrt((x * x)+(y * y))) * 180 / PI
                            
                    detectedX_array.append(x)
                    detectedY_array.append(y)
                    detectedZ_array.append(z)
                    detectedV_array.append(v)
                    detectedRange_array.append(compDetectedRange)
                    detectedAzimuth_array.append(detectedAzimuth)
                    detectedElevAngle_array.append(detectedElevAngle)
                                                                
                    offset = offset + 16
                # end of for obj in range(numDetObj) for 1st TLV
                                                            
            # Process the 2nd TLV
            tlvStart = tlvStart + 8 + tlvLen
                                                    
            tlvType    = getUint32(data[tlvStart+0:tlvStart+4:1])
            tlvLen     = getUint32(data[tlvStart+4:tlvStart+8:1])      
            offset = 8
            
            #print("The 2nd TLV") 
            #print("    type %d" % (tlvType))
            #print("    len %d bytes" % (tlvLen))
            
            #UDPClient.sendto(str("The 2nd TLV").encode('utf-8'), serverAddress) 
            #UDPClient.sendto(str("    type %d").encode('utf-8') % (tlvType), serverAddress)
            #UDPClient.sendto(str("    len %d bytes").encode('utf-8') % (tlvLen), serverAddress)
                                                            
            if tlvType == 7: 
                
                # TLV type 7 contains snr and noise of all detect objects.
                # each snr and noise are 16-bit integer represented by 2 bytes, so every 4 bytes represent snr and noise of one detect objects.    
            
                # for each detect objects, extract snr and noise                                            
                for obj in range(int(numDetObj)):
                    # byte0 and byte1 represent snr. convert 2 bytes to 16-bit integer
                    snr   = getUint16(data[tlvStart + offset + 0:tlvStart + offset + 2:1])
                    # byte2 and byte3 represent noise. convert 2 bytes to 16-bit integer 
                    noise = getUint16(data[tlvStart + offset + 2:tlvStart + offset + 4:1])

                    detectedSNR_array.append(snr)
                    detectedNoise_array.append(noise)
                                                                    
                    offset = offset + 4
            else:
                for obj in range(numDetObj):
                    detectedSNR_array.append(0)
                    detectedNoise_array.append(0)
            # end of if tlvType == 7
            
            #obj = str(obj).encode('utf-8')
            ##data1 = "Data from Raspberry 1"
            ##data1 = data1.encode('utf-16')
            ##UDPClient.sendto(data1, serverAddress)
            
            ###print("                  x(m)         y(m)         z(m)        v(m/s)    Com0range(m)  azimuth(deg)  elevAngle(deg)  snr(0.1dB)    noise(0.1dB)")
            #UDPClient.sendto(str("                  x(m)         y(m)         z(m)        v(m/s)    Com0range(m)  azimuth(deg)  elevAngle(deg)  snr(0.1dB)    noise(0.1dB)").encode('utf-8'), serverAddress)
            for obj in range(numDetObj):
                #UDPClient.sendto(str("    obj%3d: %12f %12f %12f %12f %12f %12f %12d %12d %12d").encode('utf-8') % (obj, detectedX_array[obj], detectedY_array[obj], detectedZ_array[obj], detectedV_array[obj], detectedRange_array[obj], detectedAzimuth_array[obj], detectedElevAngle_array[obj], detectedSNR_array[obj], detectedNoise_array[obj]), serverAddress)
                #print(detectedRange_array[obj])
                #detectedRange_array =  detectedRange_array[obj]
                #detectedRange_array = [x.encode('utf-8') for [x] in detectedRange_array]

                #UDPClient.sendto(hello, serverAddress)
                ###print("    obj%3d: %12f %12f %12f %12f %12f %12f %12d %12d %12d" % (obj, detectedX_array[obj], detectedY_array[obj], detectedZ_array[obj], detectedV_array[obj], detectedRange_array[obj], detectedAzimuth_array[obj], detectedElevAngle_array[obj], detectedSNR_array[obj], detectedNoise_array[obj]))
                #detectedRange_array = detectedRange_array[obj]
#                 print(detectedRange_array[obj])
                #print(numDetObj)
                detectedRange = detectedRange_array[obj]
                detectedRange = str(detectedRange).encode('utf-16')
                #numDetObj1 = numDetObj
                #numDetObj1 = str(numDetObj1).encode('utf-16')
#                 UDPClient.sendto(detectedRange, serverAddress)
                #UDPClient.sendto(numDetObj1, serverAddress)
                dt = datetime.now()
                ts = datetime.timestamp(dt)
                #print(dt)
                #print(ts)
                
                #string = ('@', 2, ts, numDetObj, obj, detectedX_array[obj], detectedY_array[obj], detectedZ_array[obj], detectedV_array[obj], detectedRange_array[obj], detectedAzimuth_array[obj], detectedElevAngle_array[obj], detectedSNR_array[obj], detectedNoise_array[obj])
                
                X_Anchor = X_translation
                Y_Anchor = Y_translation
                Z_Anchor = Z_translation
                
                X = detectedX_array[obj]
                Y = detectedY_array[obj]
                Z = detectedZ_array[obj]
                
                #P_ = np.array([X_Anchor, Y_Anchor, Z_Anchor]).reshape(-1,1)
                P_ = np.array([Y, -X, Z]).reshape(-1,1)
                
                
                #phi=roll;theta=pitch;psi=yaw;
                phi = roll_phi/180*math.pi
                theta = pitch_theta/180*math.pi
                psi = yaw_psi/180*math.pi

                Rx = np.array([[1, 0, 0],
                               [0, np.cos(phi), -np.sin(phi)],
                               [0, np.sin(phi), np.cos(phi)]])

                Ry = np.array([[np.cos(theta), 0, np.sin(theta)],
                               [0, 1, 0],
                               [-np.sin(theta), 0, np.cos(theta)]])
                Rz = np.array([[np.cos(psi), -np.sin(psi), 0],
                               [np.sin(psi), np.cos(psi), 0],
                               [0, 0, 1]])

                RotationMatrix = np.dot(np.matmul(Rz, Ry), Rx)

                P = np.matmul(RotationMatrix, P_)

                P = P.flatten().tolist()
                
                X_New = P[0]+X_Anchor
                Y_New = P[1]+Y_Anchor
                Z_New = P[2]+Z_Anchor
                
                #X = -0.72
                #Y = 3.12
#                 X1 = X*math.cos(orientation/180*math.pi)+Y*math.sin(orientation/180*math.pi)
#                 Y1 = -X*math.sin(orientation/180*math.pi)+Y*math.cos(orientation/180*math.pi)
#                 #X2 = math.degrees(X1)
#                 #Y2 = math.degrees(Y1)
#                 X2 = X1 + X_translation
#                 Y2 = Y1 + Y_translation

                #print(str(XY))
                #XY = str(XY).encode('utf-16')
                #UDPClient.sendto(XY, serverAddress)
                
                #string = ['@', 2, ts, numDetObj, obj, X2, Y2, detectedZ_array[obj], detectedV_array[obj], detectedRange_array[obj], detectedAzimuth_array[obj], detectedElevAngle_array[obj], detectedSNR_array[obj], detectedNoise_array[obj]]
                
                string = [ID, ts, numDetObj, obj, X_New, Y_New, Z_New, detectedV_array[obj], detectedRange_array[obj], detectedAzimuth_array[obj], detectedElevAngle_array[obj], detectedSNR_array[obj], detectedNoise_array[obj]]
                print(string)
                string = str(string).encode('utf-16')
                UDPClient.sendto(string, serverAddress)
                #time.sleep(0.1)
                
    return (result, headerStartIndex, totalPacketNumBytes, numDetObj, numTlv, subFrameNumber, detectedX_array, detectedY_array, detectedZ_array, detectedV_array, detectedRange_array, detectedAzimuth_array, detectedElevAngle_array, detectedSNR_array, detectedNoise_array)




    



