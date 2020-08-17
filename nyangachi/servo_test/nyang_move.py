#!/usr/bin/env python
import time
import math
import RPi.GPIO as GPIO
from PCA9685 import PCA9685

'''
### check PWM Servo Driver channel number 
'''
fr_forearm_channel_num = 11
fr_thigh_channel_num = 12
fl_forearm_channel_num = 15
fl_thigh_channel_num = 14
br_forearm_channel_num = 4
br_thigh_channel_num = 5
bl_forearm_channel_num = 6
bl_thigh_channel_num = 8


class NyangMove(object):

    def __init__(self):

        ##### custom value #1 start #####
        
        self.step_length = 0.01
        self.velocity = 0.01 # (m/s)
        self.stand_height = 0.085 # calculate: 0.0836

        # to calculate angle of servos (m)
        self.forearm_length = 0.05
        self.thigh_length = 0.055

        ##### custom value  #1 end #####

        self._pwm = PCA9685()

        self._PWM_FREQ = 50
        self._pwm.setPWMFreq(self._PWM_FREQ)

        self.FR_FOREARM_INIT_ANGLE = 84
        self.FR_THIGH_INIT_ANGLE = 90
        self.FL_FOREARM_INIT_ANGLE = 101
        self.FL_THIGH_INIT_ANGLE = 90
        self.BR_FOREARM_INIT_ANGLE = 0
        self.BR_THIGH_INIT_ANGLE = 0
        self.BL_FOREARM_INIT_ANGLE = 0
        self.BL_THIGH_INIT_ANGLE = 0

        self.move_4forearm_4thigh(fr_forearm=self.FR_FOREARM_INIT_ANGLE, fr_thigh=self.FR_THIGH_INIT_ANGLE, fl_forearm=self.FL_FOREARM_INIT_ANGLE,
                 fl_thigh=self.FL_THIGH_INIT_ANGLE, br_forearm=self.BR_FOREARM_INIT_ANGLE, br_thigh=self.BR_THIGH_INIT_ANGLE, bl_forearm=self.BL_FOREARM_INIT_ANGLE, bl_thigh=self.BL_THIGH_INIT_ANGLE)

        ##### custom value #2 start #####

        self.fr_forearm_angle = self.FR_FOREARM_INIT_ANGLE
        self.fr_thigh_angle = self.FR_THIGH_INIT_ANGLE
        self.fl_forearm_angle = self.FL_FOREARM_INIT_ANGLE
        self.fl_thigh_angle = self.FL_THIGH_INIT_ANGLE
        self.br_forearm_angle = self.BR_FOREARM_INIT_ANGLE
        self.br_thigh_angle = self.BR_THIGH_INIT_ANGLE
        self.bl_forearm_angle = self.BL_FOREARM_INIT_ANGLE
        self.bl_thigh_angle = self.BL_THIGH_INIT_ANGLE       

        ##### custom value #2 end #####

    def __del__(self):
        self._pwm.exit_PCA9685()
        print("\nCleaning NyangMove...")
        GPIO.cleanup()
        print("\nNyangMove END")

    ##### custom method start #####
    
    def inverse_kinematics(self, end_x, end_z, leg_position):
        distance_btw_thigh_end = math.sqrt(math.pow(end_x,2)+math.pow(self.stand_height-end_z,2))
        angle_btw_parpendicular_end = math.degrees(math.atan2(end_x,(self.stand_height-end_z)))
        angle_btw_thigh_end = math.pow(distance_btw_thigh_end, 2) + math.pow(self.thigh_length, 2) - math.pow(self.forearm_length, 2)
        angle_btw_thigh_end = math.degrees(math.acos(angle_btw_thigh_end/(2*distance_btw_thigh_end*self.thigh_length)))
        angle_btw_thigh_forearm = math.pow(self.forearm_length, 2) + math.pow(self.thigh_length, 2) - math.pow(distance_btw_thigh_end, 2)
        angle_btw_thigh_forearm = math.degrees(math.acos(angle_btw_thigh_end/(2*self.forearm_length*self.thigh_length)))

        if leg_position == "fr" or "br":
            return
        elif leg_position == "fl" or "bl":
            if leg_position == "fl":
                _thigh_angle = self.fl_thigh_angle - self.FL_THIGH_INIT_ANGLE
                if _thigh_angle >= angle_btw_parpendicular_end:
                    goal_thigh_angle = angle_btw_parpendicular_end + angle_btw_thigh_end
                else:
                    goal_thigh_angle = angle_btw_parpendicular_end - angle_btw_thigh_end
                self.move_fl_thigh(self.fl_thigh_angle + goal_thigh_angle - _thigh_angle)
                self.move_fl_forearm(self.FL_FOREARM_INIT_ANGLE + angle_btw_thigh_forearm - 90)
            else:
                return
        else:
            print("inverse kinematics -- wrong leg position\n")

    ##### custom method end #####

    def move_4forearm_4thigh(self, fr_forearm, fr_thigh, fl_forearm, fl_thigh, br_forearm, br_thigh, bl_forearm, bl_thigh):
        self.move_fr_forearm(fr_forearm_angle=fr_forearm)
        self.move_fr_thigh(fr_thigh_angle=fr_thigh)
        self.move_fl_forearm(fl_forearm_angle=fl_forearm)
        self.move_fl_thigh(fl_thigh_angle=fl_thigh)
        self.move_br_forearm(br_forearm_angle=br_forearm)
        self.move_br_thigh(br_thigh_angle=br_thigh)
        self.move_bl_forearm(bl_forearm_angle=bl_forearm)
        self.move_bl_thigh(bl_thigh_angle=bl_thigh)

    def move_fr_forearm(self, fr_forearm_angle):
        self._pwm.setRotationAngle(fr_forearm_channel_num, fr_forearm_angle)
        self.fr_forearm_angle = fr_forearm_angle

    def move_fr_thigh(self, fr_thigh_angle):
        self._pwm.setRotationAngle(fr_thigh_channel_num, fr_thigh_angle)
        self.fr_thigh_angle = fr_thigh_angle

    def move_fl_forearm(self, fl_forearm_angle):
        self._pwm.setRotationAngle(fl_forearm_channel_num, fl_forearm_angle)
        self.fl_forearm_angle = fl_forearm_angle

    def move_fl_thigh(self, fl_thigh_angle):
        self._pwm.setRotationAngle(fl_thigh_channel_num, fl_thigh_angle)
        self.fl_thigh_angle = fl_thigh_angle

    def move_br_forearm(self, br_forearm_angle):
        self._pwm.setRotationAngle(br_forearm_channel_num, br_forearm_angle)
        self.br_forearm_angle = br_forearm_angle

    def move_br_thigh(self, br_thigh_angle):
        self._pwm.setRotationAngle(br_thigh_channel_num, br_thigh_angle)
        self.br_thigh_angle = br_thigh_angle

    def move_bl_forearm(self, bl_forearm_angle):
        self._pwm.setRotationAngle(bl_forearm_channel_num, bl_forearm_angle)
        self.bl_forearm_angle = bl_forearm_angle

    def move_bl_thigh(self, bl_thigh_angle):
        self._pwm.setRotationAngle(bl_thigh_channel_num, bl_thigh_angle)
        self.bl_thigh_angle = bl_thigh_angle

    def fr_forearm_range_test(self):
        """
        It tests the range of fr_forearm servo once
        :return:
        """
        for angle in range(10,170,1):
            print("Moving Fr_Forearm="+str(angle))
            self.move_fr_forearm(fr_forearm_angle=angle)
            time.sleep(0.1)

        for angle in range(170,10,-1):
            print("Moving Fr_Forearm="+str(angle))
            self.move_fr_forearm(fr_forearm_angle=angle)
            time.sleep(0.1)


    def fr_thigh_range_test(self):
        """
        It tests the range of fr_thigh servo once
        :return:
        """
        for angle in range(10,170,1):
            print("Moving Fr_Thigh="+str(angle))
            self.move_fr_thigh(fr_thigh_angle=angle)
            time.sleep(0.1)

        for angle in range(170,10,-1):
            print("Moving Fr_Thigh="+str(angle))
            self.move_fr_thigh(fr_thigh_angle=angle)
            time.sleep(0.1)

    def fl_forearm_range_test(self):
        """
        It tests the range of fl_forearm servo once
        :return:
        """
        for angle in range(10,170,1):
            print("Moving Fl_Forearm="+str(angle))
            self.move_fl_forearm(fl_forearm_angle=angle)
            time.sleep(0.1)

        for angle in range(170,10,-1):
            print("Moving Fl_Forearm="+str(angle))
            self.move_fl_forearm(fl_forearm_angle=angle)
            time.sleep(0.1)

    def fl_thigh_range_test(self):
        """
        It tests the range of fl_thigh servo once
        :return:
        """
        for angle in range(10,170,1):
            print("Moving Fl_Thigh="+str(angle))
            self.move_fl_thigh(fl_thigh_angle=angle)
            time.sleep(0.1)

        for angle in range(170,10,-1):
            print("Moving Fl_Thigh="+str(angle))
            self.move_fl_thigh(fl_thigh_angle=angle)
            time.sleep(0.1)

    def br_forearm_range_test(self):
        """
        It tests the range of br_forearm servo once
        :return:
        """
        for angle in range(10,170,1):
            print("Moving br_Forearm="+str(angle))
            self.move_br_forearm(br_forearm_angle=angle)
            time.sleep(0.1)

        for angle in range(170,10,-1):
            print("Moving br_Forearm="+str(angle))
            self.move_br_forearm(br_forearm_angle=angle)
            time.sleep(0.1)

    def br_thigh_range_test(self):
        """
        It tests the range of br_thigh servo once
        :return:
        """
        for angle in range(10,170,1):
            print("Moving br_Thigh="+str(angle))
            self.move_br_thigh(br_thigh_angle=angle)
            time.sleep(0.1)

        for angle in range(170,10,-1):
            print("Moving br_Thigh="+str(angle))
            self.move_br_thigh(br_thigh_angle=angle)
            time.sleep(0.1)

    def bl_forearm_range_test(self):
        """
        It tests the range of bl_forearm servo once
        :return:
        """
        for angle in range(10,170,1):
            print("Moving bl_Forearm="+str(angle))
            self.move_bl_forearm(bl_forearm_angle=angle)
            time.sleep(0.1)

        for angle in range(170,10,-1):
            print("Moving bl_Forearm="+str(angle))
            self.move_bl_forearm(bl_forearm_angle=angle)
            time.sleep(0.1)

    def bl_thigh_range_test(self):
        """
        It tests the range of bl_thigh servo once
        :return:
        """
        for angle in range(10,170,1):
            print("Moving bl_Thigh="+str(angle))
            self.move_bl_thigh(bl_thigh_angle=angle)
            time.sleep(0.1)

        for angle in range(170,10,-1):
            print("Moving bl_Thigh="+str(angle))
            self.move_bl_thigh(bl_thigh_angle=angle)
            time.sleep(0.1)


    def input_fr_forearm_test(self):

        while True:
            input_x = raw_input("Type Angle to move to")
            angle = int(input_x)
            print("Moving Fr_Forearm=" + str(angle))
            self.move_fr_forearm(yaw_angle=angle)

    def input_fr_thigh_test(self):

        while True:
            input_x = raw_input("Type Angle to move to")
            angle = int(input_x)
            print("Moving Fr_Thigh=" + str(angle))
            self.move_fr_thigh(fr_thigh_angle=angle)

    def input_fl_forearm_test(self):

        while True:
            input_x = raw_input("Type Angle to move to")
            angle = int(input_x)
            print("Moving Fl_Forearm=" + str(angle))
            self.move_fl_forearm(yaw_angle=angle)

    def input_fl_thigh_test(self):

        while True:
            input_x = raw_input("Type Angle to move to")
            angle = int(input_x)
            print("Moving Fl_Thigh=" + str(angle))
            self.move_fl_thigh(fl_thigh_angle=angle)

    def input_br_forearm_test(self):

        while True:
            input_x = raw_input("Type Angle to move to")
            angle = int(input_x)
            print("Moving Br_Forearm=" + str(angle))
            self.move_br_forearm(yaw_angle=angle)

    def input_br_thigh_test(self):

        while True:
            input_x = raw_input("Type Angle to move to")
            angle = int(input_x)
            print("Moving Br_Thigh=" + str(angle))
            self.move_br_thigh(br_thigh_angle=angle)

    def input_bl_forearm_test(self):

        while True:
            input_x = raw_input("Type Angle to move to")
            angle = int(input_x)
            print("Moving Bl_Forearm=" + str(angle))
            self.move_bl_forearm(yaw_angle=angle)

    def input_bl_thigh_test(self):

        while True:
            input_x = raw_input("Type Angle to move to")
            angle = int(input_x)
            print("Moving Bl_Thigh=" + str(angle))
            self.move_bl_thigh(bl_thigh_angle=angle)

    def leg_circle_test(self, repetitions=1, position):

        # These values are base on Hardware observations where they are stable.
        max_range = 100
        min_range = 30
        period = 0.1
        increments = 10

        for num in range(repetitions):

            for angle in range(0,359,increments):
                forearm_angle = int((((math.sin(math.radians(angle)) + 1.0) / 2.0) * (max_range - min_range)) + min_range)
                thigh_angle = int((((math.cos(math.radians(angle)) + 1.0) / 2.0) * (max_range - min_range)) + min_range)

                print("Moving Forearm=" + str(forearm_angle))
                print("Moving Thigh="+str(thigh_angle))

                if position == "fr" :
                    self.move_fr_forearm(fr_forearm_angle=forearm_angle)
                    self.move_fr_thigh(fr_thigh_angle=fr_thigh_angle)
                elif position == "fl" :
                    self.move_fl_forearm(fl_forearm_angle=forearm_angle)
                    self.move_fl_thigh(fl_thigh_angle=fl_thigh_angle)                
                elif position == "br" :
                    self.move_br_forearm(br_forearm_angle=forearm_angle)
                    self.move_br_thigh(br_thigh_angle=br_thigh_angle)                
                elif position == "bl" :
                    self.move_bl_forearm(bl_forearm_angle=forearm_angle)
                    self.move_bl_thigh(bl_thigh_angle=bl_thigh_angle)   

                time.sleep(period)

            for angle in range(359,0,-increments):
                forearm_angle = int((((math.sin(math.radians(angle)) + 1.0) / 2.0) * (max_range - min_range)) + min_range)
                thigh_angle = int((((math.cos(math.radians(angle)) + 1.0) / 2.0) * (max_range - min_range)) + min_range)

                print("Moving Forearm=" + str(forearm_angle))
                print("Moving Thigh="+str(thigh_angle))

                if position == "fr" :
                    self.move_fr_forearm(fr_forearm_angle=forearm_angle)
                    self.move_fr_thigh(fr_thigh_angle=fr_thigh_angle)
                elif position == "fl" :
                    self.move_fl_forearm(fl_forearm_angle=forearm_angle)
                    self.move_fl_thigh(fl_thigh_angle=fl_thigh_angle)                
                elif position == "br" :
                    self.move_br_forearm(br_forearm_angle=forearm_angle)
                    self.move_br_thigh(br_thigh_angle=br_thigh_angle)                
                elif position == "bl" :
                    self.move_bl_forearm(bl_forearm_angle=forearm_angle)
                    self.move_bl_thigh(bl_thigh_angle=bl_thigh_angle)   
                    
                time.sleep(period)


def ForearmsTest():
    pt_object = NyangMove()
    raw_input("Start Forearms Test...Press Key")
    pt_object.fr_forearm_range_test()
    pt_object.fl_forearm_range_test()
    pt_object.br_forearm_range_test()
    pt_object.bl_forearm_range_test()

def ThighsTest():
    pt_object = NyangMove()
    raw_input("Start Thighs Test...Press Key")
    pt_object.fr_thigh_range_test()
    pt_object.fl_thigh_range_test()
    pt_object.br_thigh_range_test()
    pt_object.bl_thigh_range_test()

def InputForearmsTest():
    pt_object = NyangMove()
    raw_input("Start Input Forearms Test...Press Key")
    pt_object.input_fr_forearm_test()
    pt_object.input_fl_forearm_test()
    pt_object.input_br_forearm_test()
    pt_object.input_bl_forearm_test()

def InputThighsTest():
    pt_object = NyangMove()
    raw_input("Start Input Thighs Test...Press Key")
    pt_object.input_fr_thigh_test()
    pt_object.input_fl_thigh_test()
    pt_object.input_br_thigh_test()
    pt_object.input_bl_thigh_test()

def LegsCircleTest(repetition):
    pt_object = NyangMove()
    raw_input("Start Circle Test...Press Key")
    pt_object.leg_circle_test(repetitions=repetition, position="fr")
    pt_object.leg_circle_test(repetitions=repetition, position="fl")
    pt_object.leg_circle_test(repetitions=repetition, position="br")
    pt_object.leg_circle_test(repetitions=repetition, position="bl") 

# custom 
def stand(): 
    pt_object = NyangMove()

    NyangMove.move_4forearm_4thigh(fr_forearm=100, fr_thigh=60, fl_forearm=85, fl_thigh=120, 
            '''revise br bl''' 
            br_forearm=self.BR_FOREARM_INIT_ANGLE, br_thigh=self.BR_THIGH_INIT_ANGLE, bl_forearm=self.BL_FOREARM_INIT_ANGLE, bl_thigh=self.BL_THIGH_INIT_ANGLE)
    
def run():
    pt_object = NyangMove()
    

if __name__ == "__main__":
    # /YawTest()
    #F/orearmsTest()
    #ThighsTest()
    #InputForearmsTest()
    #InputThighsTest()
    #LegsCircleTest()
    stand()
    pt_object = NyangMove()
    while True:
        input_x = raw_input("Type end_x to move to")
        input_z = raw_input("Type end_z to move to")
        pt_object.inverse_kinematics(input_x, end_z, str("fl"))