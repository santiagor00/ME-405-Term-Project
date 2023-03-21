# ME-405-Term-Project
Nerf Turret

This program controls the motion of a nerf turret to aim at a person. The nerf turret uses a thermal camera to locate the camera.

The turret is constructed outt of wood and a turntable bearing. The Nerf gun that is used is a Rapidstrike CS-18. 

A preliminary finite state machine is shown below.
![image](https://user-images.githubusercontent.com/91160149/222659616-70aec763-9652-46c0-8a5b-9024be7f3c49.png)


# Software Design

The software is written so that the motors run cooperatively. Before that, there is a setup function that runs. The setup function initializes the x axis motor, spins the turret around, and captures the targeting image after the targets stop moving. Once the image is analyzed, the motors cooperate to align the gun with the target, and once there, the relay triggers the firing sequence.
