#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import sys
import moveit_commander
import tf
import threading
from moveit_msgs.msg import RobotTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint
from geometry_msgs.msg import PoseStamped, Pose
from ar_track_alvar_msgs.msg import AlvarMarkers, AlvarMarker

x = 0
y = 0
z = 0
ox = 0
oy = 0
oz = 0
zw = 0

# 初始化move_group的API
moveit_commander.roscpp_initialize(sys.argv)
# 初始化需要使用move group控制的机械臂中的arm group
arm = moveit_commander.MoveGroupCommander('arm')
# 初始化需要使用move group控制的机械臂中的gripper group
# gripper = moveit_commander.MoveGroupCommander('gripper')
# 获取终端link的名称
end_effector_link = arm.get_end_effector_link()
# 设置目标位置所使用的参考坐标系
reference_frame = 'base_link'
arm.set_pose_reference_frame(reference_frame)
# 当运动规划失败后，允许重新规划
arm.allow_replanning(True)
# 设置位置(单位：米)和姿态（单位：弧度）的允许误差
arm.set_goal_position_tolerance(0.01)
arm.set_goal_orientation_tolerance(0.01)
# gripper.set_goal_joint_tolerance(0.001)

# 控制机械臂先回到初始化位置
# arm.set_named_target('home')
# arm.go()
# 设置机器臂当前的状态作为运动初始状态
arm.set_start_state_to_current_state()
target_pose = PoseStamped()
a = 1


def Listener():
    rospy.init_node('listener', anonymous=True)
    # rospy.Subscriber("/arm_ar_pose_marker",AlvarMarkers,ar_pose,queue_size=1)
    rospy.Subscriber("/ar_pose_marker", AlvarMarkers, ar_pose, queue_size=1)
    rospy.spin()


def ar_pose(data):
	if data.markers[0].pose.pose.position.x >= 0.3:
		x = 0.25
		if data.markers[0].pose.pose.position.y < 0.2 and data.markers[0].pose.pose.position.y > -0.2:
			y = data.markers[0].pose.pose.position.y
			z = data.markers[0].pose.pose.position.z
		elif data.markers[0].pose.pose.position.y > 0.2:
			y = 0.2
			z = data.markers[0].pose.pose.position.z
		else:
			y = -0.2
			z = data.markers[0].pose.pose.position.z
	else:
		if data.markers[0].pose.pose.position.x < 0.3:
			x = data.markers[0].pose.pose.position.x - 0.05
			if data.markers[0].pose.pose.position.y < 0.20 and data.markers[0].pose.pose.position.y > -0.20:
				y = data.markers[0].pose.pose.position.y
				# if data.markers[0].pose.pose.position.z <= -0.05 and data.markers[0].pose.pose.position.z >= -0.3:
				z = data.markers[0].pose.pose.position.z
			# else:
				#z = 0.2
			elif data.markers[0].pose.pose.position.y > 0.2:
				y = 0.2
				z = data.markers[0].pose.pose.position.z
			else:
				y = 0.2
				z = data.markers[0].pose.pose.position.z

    # if data.markers[0].pose.pose.position.x == 0.3:
          # x = 0.25
       # if data.markers[0].pose.pose.position.x < 0.3:
         #  x = data.markers[0].pose.pose.position.x-0.1

    # if data.markers[0].pose.pose.position.y < 0.26:
          # y = data.markers[0].pose.pose.position.y
    # if data.markers[0].pose.pose.position.y > -0.26:
         #  y = data.markers[0].pose.pose.position.y
    # if data.markers[0].pose.pose.position.y > 0.26:
           #y = 0.26
    # if data.markers[0].pose.pose.position.y < -0.26:
           #y = -0.26

    # if data.markers[0].pose.pose.position.z < 0.03:
           #z = data.markers[0].pose.pose.position.z
    # if data.markers[0].pose.pose.position.z > -0.36:
           #z = data.markers[0].pose.pose.position.z
    # if data.markers[0].pose.pose.position.z > 0.03:
           #z = -0.2
    # if data.markers[0].pose.pose.position.z < -0.36:
          # z = -0.2
	
	quaternion = (
        data.markers[0].pose.pose.orientation.x,
        data.markers[0].pose.pose.orientation.y,
        data.markers[0].pose.pose.orientation.z,
        data.markers[0].pose.pose.orientation.w)

    #euler = tf.transformations.euler_from_quaternion(quaternion)
    #print("org rpy:",euler)
    #quaternion2 = tf.transformations.quaternion_from_euler(euler[0]-1.57,euler[1],euler[2]+1.57)
    # print(quaternion2)
	target_pose.header.frame_id = reference_frame
	target_pose.header.stamp = rospy.Time.now()
	target_pose.pose.position.x = x
	target_pose.pose.position.y = y
	target_pose.pose.position.z = z
	target_pose.pose.orientation.x = -0.00719
	target_pose.pose.orientation.y = 0.0599
	target_pose.pose.orientation.z = 0.00123
	target_pose.pose.orientation.w = 0.99818
	print("target_pose:", target_pose)
	# 设置机械臂终端运动的目标位姿
	arm.set_pose_target(target_pose, end_effector_link)
	arm.go()
	global a
	a += 1
	print(" count ", a)
    # 关闭并退出moveit
    # moveit_commander.roscpp_shutdown()
    # moveit_commander.os._exit(0)
	arm.clear_pose_targets()
	print("清除")


if __name__ == "__main__":
    Listener()
