# ME-405-Term-Project


## Introduction

This program controls a Nerf turret. The Nerf turret uses Ametek-PittmannPG6712A077-R3 DC brushed electric motors for movement, a Melexis MLX90640 infrared (IR) canera for target detection, and a Nerf Rapidstrike CS-18 for launching foam darts. The turret and the software are designed to participate in a duel. According to the rules of the duel, the target must remain stationary after 5 seconds and be approximately 200" from the turret. Only the first hit on the target counts, while missed shots subtract points. The turret must start the duel facing away from the target. The starting orientation of the turret, camera, and target are shown below. The target may move to the side as long as they stay in the field of view of the IR camera.

![image](https://user-images.githubusercontent.com/91160149/226514788-aae2918d-4371-4c49-b76a-7a5b6c7b3d77.png)

This turret is intended for the use of anyone who intends to battle against other turrets using the same duel rules.

## Hardware Design

The frame of the turret is constructed of plywood and 2x4 wood planks, held together by screws.
Pictures of the entire turret assembly are shown below.

![IMG_0978 4306](https://user-images.githubusercontent.com/91160149/226517562-6e7b5019-93d5-45b8-b0d3-6c8df30d8273.jpg)
![IMG_0965 4300](https://user-images.githubusercontent.com/91160149/226517597-f2b2bd48-6b48-4603-8f99-092c77d7a852.jpg)

To allow rotation in the yaw axis, the top section of the turret rotates on top of a turntable bearing. 


The turret also has the capability to rotate in the pitch axis, to aim up and down. 

A preliminary finite state machine is shown below.
![image](https://user-images.githubusercontent.com/91160149/222659616-70aec763-9652-46c0-8a5b-9024be7f3c49.png)


# Software Design

The software is written so that the motors run cooperatively. Before that, there is a setup function that runs. The setup function initializes the x axis motor, spins the turret around, and captures the targeting image after the targets stop moving. Once the image is analyzed, the motors cooperate to align the gun with the target, and once there, the relay triggers the firing sequence.
