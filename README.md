# NiryoArucoCalibration

NiryoArucoCalibration is a Python Program made to calibrate and check if the Niryo Ned 1 is correctly calibrated.

The program work by comparing with already check Aruco tag position with current position with the camera.

Axis will be draw on the picture in the /picture folder and will look like this :

![alt text](https://github.com/DEUS-X9/NiryoArucoCalibration/blob/main/picture/testAxis0.png)

If the robot is calibrate, it will go into sleep pose and if it's not calibrated ; it will recalibrated.

You can restart a calibration by calling :
```python NiryoArucoCalibration calibrate.py ```
