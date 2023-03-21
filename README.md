# ME-405-Term-Project


## Introduction

This program controls a Nerf turret. The Nerf turret uses Ametek-Pittman PG6712A077-R3 DC brushed electric motors for movement, a Melexis MLX90640 infrared (IR) canera for target detection, and a Nerf Rapidstrike CS-18 for launching foam darts. The turret and the software are designed to participate in a duel. According to the rules of the duel, the target must remain stationary after 5 seconds and be approximately 200" from the turret. Only the first hit on the target counts, while missed shots subtract points. The turret must start the duel facing away from the target. The target may move to the side as long as they stay in the field of view of the IR camera. The starting orientation of the turret, camera, and target are shown below. 

![image](https://user-images.githubusercontent.com/91160149/226514788-aae2918d-4371-4c49-b76a-7a5b6c7b3d77.png)

This turret is intended for the use of anyone who intends to battle against other turrets using the same duel rules.

## Hardware Design

The frame of the turret is constructed of plywood and 2x4 wood planks, held together by screws.
Pictures of the entire turret assembly are shown below.

![IMG_0978 4306](https://user-images.githubusercontent.com/91160149/226517562-6e7b5019-93d5-45b8-b0d3-6c8df30d8273.jpg)
![IMG_0965 4300](https://user-images.githubusercontent.com/91160149/226517597-f2b2bd48-6b48-4603-8f99-092c77d7a852.jpg)

To allow rotation in the yaw axis, the top section of the turret rotates on top of a turntable bearing. Using a timing belt and a pair of pulleys, an electric motor drives the yaw motion of the turret. The large pulley was 3D printed out of PLA, and it featueres a hole in the center for routing wires.

![image](https://user-images.githubusercontent.com/91160149/226525194-70feef28-60af-4617-b5fe-60fd81dc53e9.png)


To maintain an approximately constant tension in the belt, a belt tensioner mechanism was used, in which the motor was held by a rotating arm that was pushed against the belt by a spring.

![image](https://user-images.githubusercontent.com/91160149/226522303-68ab5de8-ac42-4557-be9e-6a7a9c2abb6c.png)

The turret also has the capability to rotate in the pitch axis, to aim up and down. Just like in the yaw axis, a motor drives a pair of pulleys with a timing belt. The output pulley is connected to a shaft, which rotates on two bearings. E-clips prevent the shaft from sliding along the bearings. The Nerf gun is attached to the shaft with duct tape. However, for this duel we determined that pitch rotation was not necessary, so we locked the rotation in the pitch axis by using screws to restrict the movement of the pitch pulley.

![IMG_0980 4301](https://user-images.githubusercontent.com/91160149/226521803-4845d1dd-e31d-4bd3-93f4-d58bd758e9f7.jpg)


A preliminary finite state machine is shown below.
![image](https://user-images.githubusercontent.com/91160149/222659616-70aec763-9652-46c0-8a5b-9024be7f3c49.png)


## Software Design

The software is written so that the motors run cooperatively. Before that, there is a setup function that runs. The setup function initializes the x axis motor, spins the turret around, and captures the targeting image after the targets stop moving. Once the image is analyzed, the motors cooperate to align the gun with the target, and once there, the relay triggers the firing sequence.

## Testing
An important test we performed was whether the Ametek-Pittman PG6712A077-R3 electric motors had enough torque to overcome the friction of the system. When we first tested this, we had not yet implemented the belt tensioning mechanism (the motor on the rotating arm with the spring). We found that there was a "rough spot" in each revolution of the larger yaw pulley, where the motor got stuck and was not able to rotate any farther. We determined that this was because the large yaw pulley was not perfectly centered with the axis of rotation of the top section of the turret, therefore the belt tension varied greatly as the pulley spun off-center. This led us to realize that we needed the belt tensioner mechanism. This completely solved the issue as the belt tension remained approximately constant and the motor no longer got stuck.

We also tested our software to improve the aim of the turret when it detected the target. The turret used only proportional control (not derivative or integral).
