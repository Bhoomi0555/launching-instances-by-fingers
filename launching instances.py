import boto3
import cv2
from cvzone.HandTrackingModule import HandDetector
import os
import time

# Create EC2 client
myec2 = boto3.client('ec2', region_name='ap-south-1') 
# Function to launch EC2 instance
def OSlaunch():
    instance = myec2.run_instances(
        ImageId='ami-0f58b397bc5c1f2e8',
        InstanceType='t3.micro',
        MinCount=1,
        MaxCount=1,
        KeyName='my-ec2-key',
        SecurityGroupIds=['sg-025a04500c333fc1a']
    )
    print("Instance Launched:", instance['Instances'][0]['InstanceId'])

# Open webcam
cap = cv2.VideoCapture(0)

# Hand detector
brain_hand_detector = HandDetector(detectionCon=0.8)

status, photo = cap.read()
cv2.imshow("Hi", photo)
cv2.waitKey(10000)
cv2.destroyAllWindows()

# Detect hand and fingers
my_hand = brain_hand_detector.findHands(photo)[0]  # Returns list of hands
if my_hand:
    my_finger_up = brain_hand_detector.fingersUp(my_hand[0])
    print("Finger Status:", my_finger_up)

    if my_finger_up == [1, 1, 1, 1, 1]:
        OSlaunch()

cap.release()
