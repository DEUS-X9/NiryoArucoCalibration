
from niryo_robot_python_ros_wrapper import *
import os
import rospy
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge
import cv2

# faut faire un singleton
class RosWrapperCalib:
    def __init__(self):
        self.Vision = Vision()
        self.niryo = self.__niryo()
    def forceCalibration(self):
        if(os.system("rosservice call /niryo_robot/joints_interface/request_new_calibration") == 0):
            os.system("rosservice call /niryo_robot/joints_interface/calibrate_motors 1")
            return True
        return self.__autoCalibrate()

    def __autoCalibrate(self):
        try:
            self.niryo.calibrate_auto()
            return True
        except:
            return False


    def __niryo(self):
        rospy.init_node('niryo_auto_calibration')
        return NiryoRosWrapper()

        
    def move(self, joint1, joint2, joint3, joint4, joint5, joint6):
        try:
            self.niryo.calibrate_auto()
            self.niryo.set_learning_mode(False)

        #niryo_robot.move_joints(0.5, 0.5, 1.5, 0, -1.5, 0)
        #niryo_robot.move_joints(1.5, -1.0, 0, 0, -1.75, 0)
        #Move for calibration

        #joint1, joint2, joint3, joint4, joint5, joint6 = joints

            self.niryo.move_joints(joint1, joint2, joint3, joint4, joint5, joint6)
        #Move to home
        #niryo_robot.move_joints(-1.57, 0, 0, -0.08, 0, 0)
        
        #niryo_robot.move_to_sleep_pose()
            joints = self.niryo.get_joints()
            return joints
        except:
            self.forceCalibration()
            self.move(joint1, joint2, joint3, joint4, joint5, joint6)
    def cameraCalibrationDefault(self):
        return self.niryo.get_camera_intrinsics()
    def move_to_sleep_pose(self):
        self.niryo.move_to_sleep_pose()







class Vision:
    def listener(self):
        # Initialize the node

        #rospy.init_node('listener', anonymous=True)

        # Subscribe to the topic

        #NED
        sub = rospy.Subscriber('/niryo_robot_vision/compressed_video_stream', CompressedImage)
        msg = rospy.wait_for_message('/niryo_robot_vision/compressed_video_stream', CompressedImage)

        sub.unregister()

        return msg
    def getImage(self, name=None):
        bridge = CvBridge()

        l =self.listener()
        
        cv_image = bridge.compressed_imgmsg_to_cv2(l, "bgr8")
        if name:
            cv2.imwrite('picture/'+name+'.png',cv_image)
        return cv_image