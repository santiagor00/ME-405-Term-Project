# ME-405-Term-Project


## Introduction

This program controls a Nerf turret. The Nerf turret uses Ametek-Pittman PG6712A077-R3 DC brushed electric motors for movement, a Melexis MLX90640 infrared (IR) canera for target detection, and a Nerf Rapidstrike CS-18 for launching foam darts. The turret and the software are designed to participate in a duel. According to the rules of the duel, the target must remain stationary after 5 seconds and be approximately 200" from the turret. Only the first hit on the target counts, while missed shots subtract points. The turret must start the duel facing away from the target. The target may move to the side as long as they stay in the field of view of the IR camera. The starting orientation of the turret, camera, and target are shown below. 

![image](https://user-images.githubusercontent.com/91160149/226514788-aae2918d-4371-4c49-b76a-7a5b6c7b3d77.png)

This turret is intended for the use of anyone who intends to battle against other turrets using the same duel rules.

## Hardware Design
### Frame
The frame of the turret is constructed of plywood and 2x4 wood planks, held together by screws.
Pictures of the entire turret assembly are shown below.

![IMG_0978 4306](https://user-images.githubusercontent.com/91160149/226517562-6e7b5019-93d5-45b8-b0d3-6c8df30d8273.jpg)
![IMG_0965 4300](https://user-images.githubusercontent.com/91160149/226517597-f2b2bd48-6b48-4603-8f99-092c77d7a852.jpg)

### Yaw Axis Design
To allow rotation in the yaw axis, the top section of the turret rotates on top of a turntable bearing. Using a timing belt and a pair of pulleys, an electric motor drives the yaw motion of the turret. The large pulley was 3D printed out of PLA, and it features a hole in the center for routing wires.

![image](https://user-images.githubusercontent.com/91160149/226525194-70feef28-60af-4617-b5fe-60fd81dc53e9.png)

### Tensioner System
To maintain an approximately constant tension in the belt, a belt tensioner mechanism was used, in which the motor was held by a rotating arm that was pushed against the belt by a spring.

![image](https://user-images.githubusercontent.com/91160149/226522303-68ab5de8-ac42-4557-be9e-6a7a9c2abb6c.png)

### Pitch Axis Design
The turret also has the capability to rotate in the pitch axis, to aim up and down. Just like in the yaw axis, a motor drives a pair of pulleys with a timing belt. The output pulley is connected to a shaft, which rotates on two bearings. E-clips prevent the shaft from sliding along the bearings. The Nerf gun is attached to the shaft with duct tape. However, for this duel we determined that pitch rotation was not necessary, so we locked the rotation in the pitch axis by using screws to restrict the movement of the pitch pulley.

![IMG_0980 4301](https://user-images.githubusercontent.com/91160149/226521803-4845d1dd-e31d-4bd3-93f4-d58bd758e9f7.jpg)

### Trigger System 
![IMG_4423](https://user-images.githubusercontent.com/122560263/226526274-4ca4ddee-a805-4752-8781-9c44f47f0d84.jpg)
The triggering circuit for the gun utilizes a relay that acts as a switch for the gun. The gun utilizes several microswitches that sense whether or not the magazines is in the gun, if the jam door is open and for the triggers as well. After testing, we noticed that we can control the gun's firing mechanism by tricking it into thinking the magazine is in. By directly taking control of this microswitch's signal, we were able to make the gun enter and exit it's firing state so to speak. The circuit attached connects the microswitch signal only when the relay is activated. Otherwise it acts as an "open circuit", and effectively blocks the gun from firing. The flywheel motors were powered directly by splicing into the power cables for the motors. We added a switch to the cables in order to stop the motors as our emergency stop for the gun.

### Finite State Machine
A preliminary finite state machine is shown below.
![image](https://user-images.githubusercontent.com/91160149/222659616-70aec763-9652-46c0-8a5b-9024be7f3c49.png)

## Software Design

The software is written so that the motors run cooperatively. Before that, there is a setup function that runs. The setup function initializes the x axis motor, spins the turret around, and captures the targeting image after the targets stop moving. Once the image is analyzed, the motors cooperate to align the gun with the target, and once there, the relay triggers the firing sequence.

## Testing & Results
An important test we performed was whether the Ametek-Pittman PG6712A077-R3 electric motors had enough torque to overcome the friction of the system. When we first tested this, we had not yet implemented the belt tensioning mechanism (the motor on the rotating arm with the spring). We found that there was a "rough spot" in each revolution of the larger yaw pulley, where the motor got stuck and was not able to rotate any farther. We determined that this was because the large yaw pulley was not perfectly centered with the axis of rotation of the top section of the turret, therefore the belt tension varied greatly as the pulley spun off-center. This led us to realize that we needed the belt tensioner mechanism. This completely solved the issue as the belt tension remained approximately constant and the motor no longer got stuck.

We also tested our software to improve the aim of the turret when it detected the target. To yaw left or right, the program determines the location of the hottest pixel from the IR image, determines how many pixels left or right it is from the center of the image, and uses that to determine the position it should rotate to. Essentially, it scales the pixel offset to an encoder ticks value. To determine how many encoder ticks correspond to a pixel, we iterated. After numerous iterations we found a scaling factor that accurately linked the pixel offset with the desired encoder tick offset.


Another issue we found via testing was that during the inital 180-degree turn to face the target, the timing belt was slipping because the motor was putting out too much torque. We resolved this by decreasing Kp, and therefore making the turret accelrate slower in the yaw axis. With the slower acceleration, the belt no longer slipped. The extra time the turret took to complete the 180 degree turn was not an issue, because the turn was still complete under 5 seconds and the turret would not take a shot until after 5 seconds.

After solving the slipping issue, we still noticed a problem. There was a noticable steady-state error in the yaw axis. This occurred because the turret overshot its setpoint, and when it compensated by moving back toward the setpoint it was not reaching it. Although implementing integral control would have resolved this, it was approximately 3 AM and our turret used only proportional control. So, we solved this by setting a setpoint slightly offset from our desired setpoint, to compensate for the steady state error.

## Lessons Learned

Before this project, we believed that using pulleys was easier than using gears because we thought pulleys could work with looser dimensions. In this project, we learned that even if a pulley is slighly offset, it will cause problems with the belt tension. During one half of the rotation of the pulley, the belt will be exceedingly tight, while during the other half of the rotation the belt will be loose. As the pulley rotates off center, there is an imbalance of tension, which the motor torque may not be able to overcome, leading to the motor getting stuck. The solution to this, as we found out in this project, is to use a flexible element such as spring to keep the belt tensioned, while allowing one pulley to move realtive to the other one.
