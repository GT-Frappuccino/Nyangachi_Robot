#!/usr/bin/env python
import time
import math

'''
### check PWM Servo Driver channel number 
'''
fr_forearm_channel_num = 2
fr_thigh_channel_num = 1
fl_forearm_channel_num = 12
fl_thigh_channel_num = 11
br_forearm_channel_num = 4
br_thigh_channel_num = 5
bl_forearm_channel_num = 6
bl_thigh_channel_num = 8


class NyangMove(object):

    def __init__(self, is_real=False):

        ##### custom value #1 start #####

        if is_real:
            self._pwm = PCA9685()
            self._PWM_FREQ = 50
            self._pwm.setPWMFreq(self._PWM_FREQ)

        self.is_real = is_real

        self.step_length = 0.01
        self.velocity = 0.01 # (m/s)
        self.step_num = 5 # step number in 1 step_length

        # to calculate angle of servos (m)
        self.stand_height = 0.085 # calculate: 0.0836
        self.forearm_length = 0.05
        self.thigh_length = 0.055

        ##### custom value  #1 end #####

        self.FR_FOREARM_INIT_ANGLE = 84
        self.FR_THIGH_INIT_ANGLE = 90
        self.FL_FOREARM_INIT_ANGLE = 101
        self.FL_THIGH_INIT_ANGLE = 90
        self.BR_FOREARM_INIT_ANGLE = 0
        self.BR_THIGH_INIT_ANGLE = 0
        self.BL_FOREARM_INIT_ANGLE = 0
        self.BL_THIGH_INIT_ANGLE = 0

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
        # self.move_4forearm_4thigh(fr_forearm=self.FR_FOREARM_INIT_ANGLE, fr_thigh=self.FR_THIGH_INIT_ANGLE, fl_forearm=self.FL_FOREARM_INIT_ANGLE,
        #          fl_thigh=self.FL_THIGH_INIT_ANGLE, br_forearm=self.BR_FOREARM_INIT_ANGLE, br_thigh=self.BR_THIGH_INIT_ANGLE, bl_forearm=self.BL_FOREARM_INIT_ANGLE, bl_thigh=self.BL_THIGH_INIT_ANGLE)
        
        # self.move_4forearm_4thigh(fr_forearm=100, fr_thigh=60, fl_forearm=85,
        #          fl_thigh=120, br_forearm=self.BR_FOREARM_INIT_ANGLE, br_thigh=self.BR_THIGH_INIT_ANGLE, bl_forearm=self.BL_FOREARM_INIT_ANGLE, bl_thigh=self.BL_THIGH_INIT_ANGLE)

    def __del__(self, is_real=False):
        print("\nCleaning NyangMove...")
        if is_real:
            self._pwm.exit_PCA9685()
            GPIO.cleanup()
        print("\nNyangMove END")

    ##### custom method start #####
    
    def inverse_kinematics(self, end_x, end_z, leg_position): # to modify 
        distance_btw_thigh_end = math.sqrt(math.pow(end_x,2)+math.pow(self.stand_height-end_z,2)) # > 0
        angle_btw_parpendicular_end = math.degrees(math.atan2(end_x, self.stand_height-end_z)) # -90 ~ 90
        angle_btw_thigh_end = math.pow(distance_btw_thigh_end, 2) + math.pow(self.thigh_length, 2) - math.pow(self.forearm_length, 2) # a^2 + b^2 - c^2 
        angle_btw_thigh_end = math.degrees(math.acos(angle_btw_thigh_end/(2*distance_btw_thigh_end*self.thigh_length))) # 0 < acos(a^2 + b^2 - c^2)/(2bc) < 180
        angle_btw_thigh_forearm = math.pow(self.forearm_length, 2) + math.pow(self.thigh_length, 2) - math.pow(distance_btw_thigh_end, 2)
        print('angle_btw_thigh_forearm mid ', angle_btw_thigh_forearm/(2*self.forearm_length*self.thigh_length))
        angle_btw_thigh_forearm = math.degrees(math.acos(angle_btw_thigh_forearm/(2*self.forearm_length*self.thigh_length)))
        _goal_thigh_angle = angle_btw_parpendicular_end - angle_btw_thigh_end

        if leg_position == "fr":
            print('inverse_kinematics -- fr and br')
            _thigh_angle = self.fr_thigh_angle  - self.FR_THIGH_INIT_ANGLE 
            self.move_fr_thigh(self.FR_THIGH_INIT_ANGLE + _goal_thigh_angle)
            self.move_fr_forearm(self.FR_FOREARM_INIT_ANGLE + angle_btw_thigh_forearm - 90)
        elif leg_position == "fl":
            print('inverse_kinematics -- fl and bl')
            _thigh_angle = self.FL_THIGH_INIT_ANGLE - self.fl_thigh_angle 
            self.move_fl_thigh(self.FL_THIGH_INIT_ANGLE - _goal_thigh_angle)
            self.move_fl_forearm(self.FL_FOREARM_INIT_ANGLE - angle_btw_thigh_forearm + 90)
        elif leg_position == "br":
            print('inverse_kinematics -- fr and br')
            _thigh_angle = self.br_thigh_angle  - self.BR_THIGH_INIT_ANGLE 
            self.move_br_thigh(self.BR_THIGH_INIT_ANGLE + _goal_thigh_angle)
            self.move_br_forearm(self.BR_FOREARM_INIT_ANGLE + angle_btw_thigh_forearm - 90)
        elif leg_position == "bl":
            print('inverse_kinematics -- fl and bl')
            _thigh_angle = self.BL_THIGH_INIT_ANGLE - self.bl_thigh_angle 
            self.move_bl_thigh(self.BL_THIGH_INIT_ANGLE - _goal_thigh_angle)
            self.move_bl_forearm(self.BL_FOREARM_INIT_ANGLE - angle_btw_thigh_forearm + 90)
        else:
            print("inverse kinematics -- wrong leg position\n")

        print("inverse kinematics -- compare ")
        print('end_x: ' + str(end_x))
        print('end_z: ' + str(end_z))
        self.calculate_forearm_end_xz(leg_position)

    def calculate_forearm_end_xz(self, leg_position): # for debugging inverse_kinematics()
        if leg_position == "fr":
            _thigh_angle = self.fr_thigh_angle - self.FR_THIGH_INIT_ANGLE 
            _forearm_angle = 90 + _thigh_angle - (self.fr_forearm_angle - self.FR_FOREARM_INIT_ANGLE)
        elif leg_position == "fl":
            _thigh_angle = self.FL_THIGH_INIT_ANGLE - self.fl_thigh_angle 
            _forearm_angle = 90 + _thigh_angle - (self.FL_FOREARM_INIT_ANGLE - self.fl_forearm_angle)
        elif leg_position == "br":
            _thigh_angle = self.br_thigh_angle - self.BR_THIGH_INIT_ANGLE 
            _forearm_angle = 90 + _thigh_angle - (self.br_forearm_angle - self.BR_FOREARM_INIT_ANGLE)
        elif leg_position == "bl":
            _thigh_angle = self.BL_THIGH_INIT_ANGLE - self.bl_thigh_angle
            _forearm_angle = 90 + _thigh_angle - (self.BL_FOREARM_INIT_ANGLE - self.bl_forearm_angle)
        else :
            print('calculate_forearm_end_xz  -- wrong leg position\n')
            return   
            
        cal_end_x = self.thigh_length * math.sin(math.radians(_thigh_angle)) + self.forearm_length * math.sin(math.radians(_forearm_angle))
        cal_end_z = self.stand_height - (self.thigh_length * math.cos(math.radians(_thigh_angle)) + self.forearm_length * math.cos(math.radians(_forearm_angle)))
        print('cal_end_x: ' + str(cal_end_x))
        print('cal_end_z: ' + str(cal_end_z))

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
        if self.is_real:
            self._pwm.setRotationAngle(fr_forearm_channel_num, fr_forearm_angle)
        self.fr_forearm_angle = fr_forearm_angle
        print("move_fr_forearm: " + str(fr_forearm_angle))

    def move_fr_thigh(self, fr_thigh_angle):
        if self.is_real:
            self._pwm.setRotationAngle(fr_thigh_channel_num, fr_thigh_angle)
        self.fr_thigh_angle = fr_thigh_angle
        print("move_fr_thigh: " + str(fr_thigh_angle))

    def move_fl_forearm(self, fl_forearm_angle):
        if self.is_real:
            self._pwm.setRotationAngle(fl_forearm_channel_num, fl_forearm_angle)
        self.fl_forearm_angle = fl_forearm_angle
        print("move_fl_forearm: " + str(fl_forearm_angle))

    def move_fl_thigh(self, fl_thigh_angle):
        if self.is_real:
            self._pwm.setRotationAngle(fl_thigh_channel_num, fl_thigh_angle)
        self.fl_thigh_angle = fl_thigh_angle
        print("move_fl_thigh: " + str(fl_thigh_angle))

    def move_br_forearm(self, br_forearm_angle):
        if self.is_real:
            self._pwm.setRotationAngle(br_forearm_channel_num, br_forearm_angle)
        self.br_forearm_angle = br_forearm_angle
        print("move_br_forearm: " + str(br_forearm_angle))

    def move_br_thigh(self, br_thigh_angle):
        if self.is_real:
            self._pwm.setRotationAngle(br_thigh_channel_num, br_thigh_angle)
        self.br_thigh_angle = br_thigh_angle
        print("move_br_thigh: " + str(br_thigh_angle))

    def move_bl_forearm(self, bl_forearm_angle):
        if self.is_real:
            self._pwm.setRotationAngle(bl_forearm_channel_num, bl_forearm_angle)
        self.bl_forearm_angle = bl_forearm_angle
        print("move_bl_forearm: " + str(bl_forearm_angle))

    def move_bl_thigh(self, bl_thigh_angle):
        if self.is_real:
            self._pwm.setRotationAngle(bl_thigh_channel_num, bl_thigh_angle)
        self.bl_thigh_angle = bl_thigh_angle
        print("move_bl_thigh: " + str(bl_thigh_angle))

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
            self.move_fr_forearm(fr_forearm_angle=angle)

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
            self.move_fl_forearm(fl_forearm_angle=angle)

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
            self.move_br_forearm(br_forearm_angle=angle)

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
            self.move_bl_forearm(bl_forearm_angle=angle)

    def input_bl_thigh_test(self):

        while True:
            input_x = raw_input("Type Angle to move to")
            angle = int(input_x)
            print("Moving Bl_Thigh=" + str(angle))
            self.move_bl_thigh(bl_thigh_angle=angle)

    def leg_circle_test(self, position, repetitions=1):

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


def ForearmsTest(is_real):
    nyang_object = NyangMove(is_real)
    raw_input("Start Forearms Test...Press Key")
    nyang_object.fr_forearm_range_test()
    nyang_object.fl_forearm_range_test()
    nyang_object.br_forearm_range_test()
    nyang_object.bl_forearm_range_test()

def ThighsTest(is_real):
    nyang_object = NyangMove(is_real)
    raw_input("Start Thighs Test...Press Key")
    nyang_object.fr_thigh_range_test()
    nyang_object.fl_thigh_range_test()
    nyang_object.br_thigh_range_test()
    nyang_object.bl_thigh_range_test()

def InputForearmsTest(is_real):
    nyang_object = NyangMove(is_real)
    raw_input("Start Input Forearms Test...Press Key")
    nyang_object.input_fr_forearm_test()
    nyang_object.input_fl_forearm_test()
    nyang_object.input_br_forearm_test()
    nyang_object.input_bl_forearm_test()

def InputThighsTest(is_real):
    nyang_object = NyangMove(is_real)
    raw_input("Start Input Thighs Test...Press Key")
    nyang_object.input_fr_thigh_test()
    nyang_object.input_fl_thigh_test()
    nyang_object.input_br_thigh_test()
    nyang_object.input_bl_thigh_test()

def LegsCircleTest(repetition, is_real):
    nyang_object = NyangMove(is_real)
    raw_input("Start Circle Test...Press Key")
    nyang_object.leg_circle_test(repetitions=repetition, position="fr")
    nyang_object.leg_circle_test(repetitions=repetition, position="fl")
    nyang_object.leg_circle_test(repetitions=repetition, position="br")
    nyang_object.leg_circle_test(repetitions=repetition, position="bl") 

##### custom function start #####
def start_pose(is_real):
    nyang_object = NyangMove(is_real)
    nyang_object.move_4forearm_4thigh(fr_forearm=nyang_object.FR_FOREARM_INIT_ANGLE, fr_thigh=nyang_object.FR_THIGH_INIT_ANGLE, fl_forearm=nyang_object.FL_FOREARM_INIT_ANGLE,
                fl_thigh=nyang_object.FL_THIGH_INIT_ANGLE, br_forearm=nyang_object.BR_FOREARM_INIT_ANGLE, br_thigh=nyang_object.BR_THIGH_INIT_ANGLE, bl_forearm=nyang_object.BL_FOREARM_INIT_ANGLE, bl_thigh=nyang_object.BL_THIGH_INIT_ANGLE)
        
def stand(is_real): 
    nyang_object = NyangMove(is_real)
    raw_input("Start stand Test...Press Key")
    # nyang_object.move_fr_forearm(fr_forearm_angle=100)
    # print(nyang_object.fr_forearm_angle)
    # nyang_object.move_fr_thigh(fr_thigh_angle=60)
    # print(nyang_object.fr_thigh_angle)
    # nyang_object.move_fl_forearm(fl_forearm_angle=85)
    # nyang_object.move_fl_thigh(fl_thigh_angle=120)
    nyang_object.move_4forearm_4thigh(fr_forearm=100, fr_thigh=60, fl_forearm=85,
                fl_thigh=120, br_forearm=nyang_object.BR_FOREARM_INIT_ANGLE, br_thigh=nyang_object.BR_THIGH_INIT_ANGLE, bl_forearm=nyang_object.BL_FOREARM_INIT_ANGLE, bl_thigh=nyang_object.BL_THIGH_INIT_ANGLE)

    print("stand\n")

def step(is_real):
    nyang_object = NyangMove(is_real)
    step_up_length = 0.03
    leg_position = "fl"
    for x in range(nyang_object.step_num):
        nyang_object.inverse_kinematics(0, x*step_up_length/nyang_object.step_num, leg_position)
    for x in range(nyang_object.step_num):
        nyang_object.inverse_kinematics(0, step_up_length - x*step_up_length/nyang_object.step_num, leg_position)

def run(is_real):
    nyang_object = NyangMove(is_real)
    leg_position = "fl"
    run_up_length = 0.02

    # forward to backward
    for x in range(nyang_object.step_num):
        nyang_object.inverse_kinematics(nyang_object.step_length - x*nyang_object.step_length/nyang_object.step_num, 0, leg_position)
    for x in range(nyang_object.step_num):
        nyang_object.inverse_kinematics(-x*nyang_object.step_length/nyang_object.step_num, 0, leg_position)
    
    # backward to forward
    for x in range(nyang_object.step_num):
        nyang_object.inverse_kinematics(-nyang_object.step_length + x*nyang_object.step_length/nyang_object.step_num, x*run_up_length/nyang_object.step_num, leg_position)
    for x in range(nyang_object.step_num):
        nyang_object.inverse_kinematics(x*nyang_object.step_length/nyang_object.step_num, run_up_length - x*run_up_length/nyang_object.step_num, leg_position)
    
##### custom function end #####

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "real":
        import RPi.GPIO as GPIO 
        from PCA9685 import PCA9685   
        is_real = True    
    else:
        is_real = False

    # /YawTest()
    #F/orearmsTest()
    #ThighsTest()
    #InputForearmsTest()
    #InputThighsTest()
    #LegsCircleTest()

    '''
    start_pose(is_real)
    stand(is_real)
    '''
    nyang_object = NyangMove(is_real)
    #nyang_object.input_fl_thigh_test()
    while True:
        input_leg_position = raw_input("Type leg_positon: fr or fl??")
        input_x = float(raw_input("Type end_x to move to"))
        input_z = float(raw_input("Type end_z to move to"))
        nyang_object.inverse_kinematics(input_x, input_z, input_leg_position)

'''        input_thigh_angle = int(raw_input("Type thigh_angle to move to"))
        input_forearm_angle = int(raw_input("Type forearm_angle to move to"))
        if input_leg_position == "fr":
            nyang_object.move_fr_thigh(input_thigh_angle)
            nyang_object.move_fr_forearm(input_forearm_angle)
        elif input_leg_position == "fl":
            nyang_object.move_fl_thigh(input_thigh_angle)
            nyang_object.move_fl_forearm(input_forearm_angle)
        nyang_object.calculate_forearm_end_xz(input_leg_position)'''