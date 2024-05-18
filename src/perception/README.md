## How to read a rosbag

Since rosbag doesnt have a fixed tf frame often you need to reference the camera frame 


Before this however: 

run :
```./play_rosbag.sh ~/Downloads/238r2--.bag```
(otherwise it would be ```rosbag play --.bag```)

this will run the rosbag in a loop so that you dont need to think about restarting it everytime

Next: 

run ```rviz```

finally: 

change 'Fixed Frame' to the sensor frame that has been recorded, for example: 

```camera_colo_optical_frame``` for the color image

Then you should see the sensor messages !!