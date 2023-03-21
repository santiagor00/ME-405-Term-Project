# ME-405-Term-Project
Nerf Turret

This program controls a Nerf turret. The Nerf turret uses Ametek-PittmannPG6712A077-R3 DC brushed electric motors for movement, a Melexis MLX90640 infrared (IR) canera for target detection, and a Nerf Rapidstrike CS-18 for launching foam darts. The turret and the software are designed to participate in a duel. According to the rules of the duel, the target must remain stationary after 5 seconds and be approximately 200" from the turret. Only the first hit on the target counts, while missed shots detract points. The turret must start the duel facing away from the target. The starting orientation of the turret, camera, and target are shown below. The target may move to the side as long as they stay in the field of view of the IR camera.

![image](https://user-images.githubusercontent.com/91160149/226514788-aae2918d-4371-4c49-b76a-7a5b6c7b3d77.png)


The turret is constructed outt of wood and a turntable bearing. The Nerf gun that is used is a Rapidstrike CS-18. 

A preliminary finite state machine is shown below.
![image](https://user-images.githubusercontent.com/91160149/222659616-70aec763-9652-46c0-8a5b-9024be7f3c49.png)


# Software Design

The software is written so that the motors run cooperatively. Before that, there is a setup function that runs. The setup function initializes the x axis motor, spins the turret around, and captures the targeting image after the targets stop moving. Once the image is analyzed, the motors cooperate to align the gun with the target, and once there, the relay triggers the firing sequence.
