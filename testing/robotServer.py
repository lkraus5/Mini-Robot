from Robot4WD.Robot4WD import Robot4WD
from SimpleUDP.SimpleUDPServer import SimpleUDPServer
#import threading
import time
import board
import busio
import adafruit_pca9685
i2c = busio.I2C(board.SCL, board.SDA)
hat = adafruit_pca9685.PCA9685(i2c)
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
from numpy import interp

UDP_IP = "" ## Accept all IPs
UDP_PORT = 5005

server = SimpleUDPServer(UDP_IP, UDP_PORT)

LEFT_TRIM   = 0
RIGHT_TRIM  = 0

robot = Robot4WD(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM,left_id1=1,right_id1=2,left_id2=3,right_id2=4)

speedmode = 'low'
speed = 150
opmode = 'skidsteer'




while True:
    
    #inputs = server.listen()

    #print(inputs)

    
    """
    # To many polls to change motor speed. It has to run his own thread with suitable refresh. 
    # So it doens't try to change speed more than X times per second

    if inputs['buttons'][6]:
        axis=inputs['axis'][4]
        #speed=int(interp(axis,[-1,1],[0,255]))
        speed=int(interp(axis,[-1,1],[0,100]))
        robot.forward(1, None)
        robot._left_speed(speed)
        robot._right_speed(speed)

    elif inputs['buttons'][7]:
        robot.backward(50, None)
    else:
        robot.stop()

    """
    #axis=inputs['axis'][4]
    #axis2=inputs['axis'][1]
    #speed1=int(interp(abs(axis),[0,1],[0,250]))
    #speed2=int(interp(abs(axis2),[0,1],[0,250]))
    #speedavg = int(interp(abs((axis + axis2)/2),[0,1],[0,255]))
    

    if opmode == 'skidsteer':
        while opmode == 'skidsteer':
            inputs = server.listen()
            axis=inputs['axis'][4]
            axis2=inputs['axis'][1]
            if ((axis < -0.5) and (axis2 < -0.5)):
                robot.forward(speed,None)
            elif ((axis>0.5) and (axis2>0.5)):
                robot.backward(speed,None)
            elif ((axis<-0.5) and (axis2>0.5)):
                robot.righttwist(speed, speed, None)
            elif ((axis>0.5) and (axis2<-0.5)):
                robot.lefttwist(speed, speed, None)
            elif (axis2 > 0.5):
                robot.rightbackward(speed, None)
            elif (axis2 < -0.5):
                robot.rightforward(speed, None)
            elif (axis > 0.5):
                robot.leftbackward(speed, None)
            elif (axis < -0.5):
                robot.leftforward(speed, None)
            # elif inputs['buttons'][7]:
            #     robot.armup()
            #     # armup = threading.Thread(target=robot.armup(), args=())
            #     # armup.daemon = True # Daemonize thread
            #     # armup.start()
            # elif inputs['buttons'][6]:
            #     robot.armdown()
            #     # armdown = threading.Thread(target=robot.armdown(), args=())
            #     # armdown.daemon = True # Daemonize thread
            #     # armdown.start()
            # elif inputs['buttons'][1]:
            #     opmode = 'simple'
            #     time.sleep(0.001)
            # elif inputs['buttons'][3]:
            #     if speedmode == 'low':
            #         speedmode = 'medium'
            #         speed = 200
            #         time.sleep(0.001)
            #     elif speedmode == 'medium':
            #         speedmode = 'high'
            #         speed = 250
            #         time.sleep(0.001)
            #     elif speedmode == 'high':
            #         speedmode = 'low'
            #         speed = 150
            #         time.sleep(0.001)
            else:
                robot.stop()
            
            if inputs['buttons'][0]:
                #print("STOP")
                robot.stop()

            if inputs['buttons'][3]:
                robot.armup()
            if inputs['buttons'][1]:
                robot.armdown()
            if inputs['buttons'][8]:
                opmode = 'simple'
                time.sleep(0.001)
            if inputs['buttons'][9]:
                if speedmode == 'low':
                    speedmode = 'medium'
                    speed = 200
                    time.sleep(0.001)
                elif speedmode == 'medium':
                    speedmode = 'high'
                    speed = 250
                    time.sleep(0.001)
                elif speedmode == 'high':
                    speedmode = 'low'
                    speed = 150
                    time.sleep(0.001)

            time.sleep(0.0003)
    elif opmode == 'simple':
        while opmode == 'simple':
            inputs = server.listen()
            if inputs['axis'][4]<-0.5:
                robot.forward(speed,None)
            elif inputs['axis'][4]>0.5:
                robot.backward(speed,None)
            elif inputs['buttons'][7]:
                robot.lefttwist(speed, speed, None)
            elif inputs['buttons'][6]:
                robot.righttwist(speed, speed, None)
            elif inputs['buttons'][8]:
                opmode = 'skidsteer'
                time.sleep(0.001)
            elif inputs['buttons'][9]:
                if speedmode == 'low':
                    speedmode = 'medium'
                    speed = 200
                    time.sleep(0.001)
                elif speedmode == 'medium':
                    speedmode = 'high'
                    speed = 250
                    time.sleep(0.001)
                elif speedmode == 'high':
                    speedmode = 'low'
                    speed = 150
                    time.sleep(0.001)
            else:
                robot.stop()

            if inputs['buttons'][0]:
                #print("STOP")
                robot.stop()

            if inputs['buttons'][3]:
                robot.armup()
            if inputs['buttons'][1]:
                robot.armdown()
            time.sleep(0.0003)
    else:
        robot.stop()
        print('unknown mode')
        print('setting to skidsteer')
        opmode = 'skidsteer'
        time.sleep(10)

