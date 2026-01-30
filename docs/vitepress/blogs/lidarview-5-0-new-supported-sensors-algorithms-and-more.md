[post](https://www.kitware.com/lidarview-5-0-new-supported-sensors-algorithms-and-more/)

# LidarView 5.0 – new supported sensors, algorithms, and more!

November 5, 2024

[Timothee Couble](https://www.kitware.com/author/timothee-couble/ "Posts by Timothee Couble") and [Gatien Ferret](https://www.kitware.com/author/gatien-ferret/ "Posts by Gatien Ferret")

![](https://www.kitware.com/main/wp-content/uploads/2024/11/thumbnail.png)

## LidarView: One software to read and process them all!

We’ve added to [LidarView](https://lidarview.kitware.com/) several new LiDARs from different manufacturers. They can be used in the same way, regardless of the model, to visualize live streams, replay .pcap records and running algorithms. You can even open two different LiDARs at the same time!

Here is a current exhaustive list of sensors supported by [LidarView](https://lidarview.kitware.com/):

[**Velodyne**](https://www.velodyneacoustics.com/en/): VLP-16, VLP-32, HDL-32, HDL-64, Puck LITE, Puck Hi-Res and Alpha Prime (VLS-128).

[**Hesai**](https://www.hesaitech.com/): Pandar40P, Pandar40M, Pandar64, Pandar20A, Pandar20B, PandarQT, PandarXT-16, PandarXT-32, PandarXTM and Pandar128.

[**Robosense**](https://www.robosense.ai/en): RS16, RS32, BPearl, Helios (16 & 32), Ruby (48, 80 & 128), Ruby Plus (48, 80 & 128), M1, M2 and E1.

[**Livox**](https://www.livoxtech.com/): Mid-360 and HAP.

[**Leishen**](https://www.lslidar.com/): C16, C32 and MS\_C16.

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXcXExPXkD5ZVVuZ9t68lOUyIrMzU3jO0zUWvglZF27Ux7ONxLUDVX55QqeLTJncZ-ZhAEKm5HK-gUuT3Qrk1Ch53cMC80QcTSMFmIxhHg2Jl5glDi2kKZFttcB_jtfj2i8YqvL70e_-uOZZH9xmO8YXf7z3?key=CP0dasOOrcWuC0b8kWKI3Q)

Are you using a sensor that is not supported here and you would like to have it supported?

* Check [here](https://gitlab.kitware.com/LidarView/lidarview/-/blob/master/README.md?ref_type=heads#introduction) if it isn’t already supported on the master branch as this keeps evolving ( Other Livox sensors are coming up very soon !).
* If not, and that there are public drivers / specifications for them [contact us](https://www.kitware.eu/contact/) so that we can add them.
* If you are yourself developing a sensor, or that you have access to specific drivers / specifications, [contact us](https://www.kitware.eu/contact/) to implement a dedicated plugin (which may stay private if the information used for this is not publicly available).

For ROS2 users: you can now also read .mcap files in LidarView. This means that you may have access to the whole UI, visualization capabilities and set of algorithms of the software on your data recorded in ROS2.

## Make LidarView easier to use!

### LidarView now has 3 modes for simpler interactions

**The Lidar Viewer mode :** This is the default mode for the simple usage of having a software to visualize live sensor feed, save recordings ( in the form of pcap files), replay those recordings and have access to simple visualization parameterization and data interaction capabilities.

In previous versions of LidarView (and in VeloView), this was the default mode ( when not switching to “Advanced Mode”).

For a simpler interface, the Pipeline Browser is hidden from this mode.

**The Point Cloud Tool mode :** This mode is intended to give access to the still point cloud processing tools of LidarView. In this mode, the time player is not available anymore and Temporal filters are hidden. This can typically be used whenever you have a collected point cloud to process, either using the ParaView functionalities, or the LidarView point cloud specific filters.

This mode brings LidarView closer to other 3D point cloud processing software

**The Advanced Mode** : This mode contains all of LidarView capabilities, including any algorithm available in the point cloud Tool mode, the LiDAR player, and all of the filters available in LidarView.

Those modes are configured with a configuration file ( [interface\_modes\_config.json](https://gitlab.kitware.com/LidarView/lidarview/-/blob/master/Application/Qt/ApplicationComponents/Resources/interface_modes_config.json) file in the share folder of the installation tree), which you can edit manually if you require to customize it even more without having to recompile LidarView.

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXewyPXNgMqzppLhC0XT9Q2bMCEiyft3EIPzzzpU21glfRALig6iF_aqOF0L46WysHfM-XgjCUJr3nebdwKhvAb662f9ispPM0rGnxPdMlmWkoX6IiTAvPBcZCQFYtUKUqwOAeyVOGZInsOuGu82RYRKQJx8?key=CP0dasOOrcWuC0b8kWKI3Q)

In the future, we plan to create modes for specific usages with specific sets of toolboxes, for examples:

* Point Cloud Statistics toolbox
* Automotive LiDAR setup
* Building Modelling with LiDAR scans
* LiDAR for intersection monitoring
* Big point cloud handling (such as city scale aerial scans)
* …

Let us know which application you would like to tailor Lidarview for!

### Lidar Configuration dialog updates

Some LiDAR require intrinsic calibration files, which contains some correction parameters for each individual sensor estimated at the end of the production line. Though when high precision is not required, default ones are enough, and some are provided within LidarView. Some models embed this calibration within the streamed data and therefore do not require such a file ( see each sensor datasheet for more details).

Now you may directly select the sensor model you want to work with, and if required, default files will be used automatically.

You may still use your own files provided by the manufactures for the relevant sensors.

Those options are now saved for later usage, avoiding having to switch between configs if you are working with various sensors.

### Toolbar for SLAM !

LidarView embeds a state of the art LiDAR SLAM algorithm which is widely configurable to your use case and sensor.

It is based on an external [open source library](https://gitlab.kitware.com/keu-computervision/slam) that we develop at Kitware, which can also be embedded in ROS/ROS2 environment or even your own software. More details about it in our previous [blogpost](https://www.kitware.com/lidar-slam-spotlight-on-kitwares-open-source-library/).

On top of registering frames one after the other, it embeds the following features :

* External sensor fusion : IMU, GNSS,INS, Wheel Odometer, Features from cameras
* Loop closure detection and optimization
* Relocalization in an input map
* Dynamic object removal
* Frame Aggregation for dense maps
* …

As we know that setting it up and fine tuning it may be a bit tedious, we have added a toolbar to help novice users do it in the most common cases.

In particular this include : easy setup of the SLAM, default configuration depending on the LiDAR model and environment, dialog for adding external sensor information and for loop closure management.

This should help you tackle the most common use cases for SLAM algorithms, and feel free to contact us for more challenging ones!

<video src="https://www.kitware.com/main/wp-content/uploads/2024/11/SLAM_toolbar1.mp4" controls width="640">
  SLAM toolbar demo
</video>

<center>*SLAM toolbar demo*</center>

## New filters!

New functionalities have been introduced in LidarView: object tracking based on still point clouds and volume measurement.

### Motion detector

The motion detection algorithm highlights all moving points and can even cluster and track them! It requires only a few frames for initialization and stationary LiDAR data.

It should be tuned according to the LiDAR properties, the range of interest and the sizes of the objects involved

<img decoding="async" src="https://lh7-rt.googleusercontent.com/docsz/AD_4nXcoOZpV7o6-B0TTW3rJFqKCK3QXqAceKQdejlzFM8rgu_WOrcW9M1v8Mit8nxHh5OizAtU9cKOhvbYwVRbQXMpOPJtSB1BNYD2vk8WX3NRZa1IUTRe_Hc8pWY6CQ0EPdZzMxkss5vjrqIcnXFIaRTxmgTXM?key=CP0dasOOrcWuC0b8kWKI3Q" style="width: 960px">

<center>*Motion detection applied to person detection and tracking in an office environment*</center>

### Volume measurement

We have added some functionalities to allow for measuring volumes or real objects in point clouds.

As of now, this calculates the volume contained between a portion of the point cloud (your object of interest) and an underlying plane. It could be extended with other variants depending on the use case.

This may be used for instance in material stock assessment.

Input point clouds may come from direct complete scans or be constructed with SLAM as in the example below.

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXdBTjr2EBOwcwDOCofJE6Y0FGWJicJLQuuA1WZ92k_TbWuBWWTNd6xxWPxCw0Fp_QyzVqmA4hHcwrmInIEUNMnuTqfOkef2YSbEeFaNCU6Woz0fQBtgSEd5B1W8tI0xs-cJxynDNPU0Cb-fPkzw7mKprFx4?key=CP0dasOOrcWuC0b8kWKI3Q)

<center>*Toy example of a box in a SLAM reconstructed point cloud of our office.*</center>

## LidarView Client Server mechanism, connectivity and web applications !

Similar to its big brother ParaView, LidarView now allows the client server connection.

As for Paraview, you can now handle large data hosted on a high performance computer from your desktop client, see [this guide](https://www.kitware.com/paraview-hpc-scalability-guide/) for such usage.

To give an idea of what is now possible, here is an example of such a visualization using WebGPU technology to visualize large scale aerial LiDAR scans (not yet integrated in ParaView / LidarView, more details in that [blogpost](https://www.kitware.com/achieving-interactivity-with-a-point-cloud-of-2-billion-points-in-a-single-workstation/))

Deriving from this: one can now also connect to a distant server for remote visualization, meaning having for instance a mobile robot acquiring data and acting as a server streaming resulting images to your client desktop app (warning: this is a stretch from the ParaView inherited server mechanism and has some limitations).

### Web visualization and interaction

LidarView can now connect to a python [trame](https://www.kitware.com/trame/) application and expose its functionalities there.

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXd-LjnVnFCQDptYPOoi1cpBntTsFfczSM_Ct604Ti25bjp5DjlVTDgjFHVSbvJx9Qms08U19k34kmM8RupKOuaw7IjV_3PsN7o6Iij7bnpWRZE6oalTABbBF67RrLpqs-xl2-7oH_R7OvXJfajFmxcoXWdB?key=CP0dasOOrcWuC0b8kWKI3Q)

<center>*Control the SLAM algorithm through a web page written in trame!*</center>

### Outputting data from LidarView to other programs

We added 2 examples outputting data through UDP:

* A generic [UDP exporter](https://gitlab.kitware.com/LidarView/lidarview-core/-/blob/master/LidarCore/IO/Network/vtkUDPPointSender.cxx?ref_type=heads) for point data (which includes data such as SLAM trajectories).
* A specific [exporter](https://gitlab.kitware.com/LidarView/lidarview-core/-/blob/master/Plugins/MotionDetectorToolbox/IO/vtkDetectedClusterUDPSender.cxx?ref_type=heads) for detected objects in 3D.

## Conclusion

[LidarView 5.0](https://lidarview.kitware.com/) is a big leap towards universal LiDAR viewer and processing tool, Kitware is dedicated to make this tool evolve by:

* Expanding the list of supported devices.
* Adding base algorithms for LiDAR point cloud processing.
* Adding domain specific algorithms and interfaces.

You may download the latest [LidarView](https://lidarview.kitware.com/) version and check the full release notes from the [release](https://gitlab.kitware.com/LidarView/lidarview/-/releases) page.

Contact us to let us know how you would use it, and how it can be adapted to your LiDAR data workflow!

## Support and Services

Looking to take your application to new heights? [Get in touch](https://www.kitware.com/contact/) with Kitware for expert development and support services to fast-track your success with Kitware's open source frameworks.

  <!-- Icon/link tiles -->
<table>
  <tr>
    <td align="center" width="33%">
      <img src="https://www.kitware.com/main/wp-content/uploads/2021/11/icon_collaboration.svg" width="50"><br>
      <strong><a href="https://www.kitware.com/training/">Training</a></strong><br>
      <small>Learn how to confidently use and customize 3D Slicer from the expert developers at Kitware.</small>
    </td>
    <td align="center" width="33%">
      <img src="https://www.kitware.com/main/wp-content/uploads/2021/12/icon_research_develop.svg" width="50"><br>
      <strong><a href="https://www.kitware.com/support/">Support</a></strong><br>
      <small>Our experts can assist your team as you build your application and establish in-house expertise.</small>
    </td>
    <td align="center" width="33%">
      <img src="https://www.kitware.com/main/wp-content/uploads/2021/11/icon_custom_software.svg" width="50"><br>
      <strong><a href="https://www.kitware.com/contact">Custom Development</a></strong><br>
      <small>Leverage Kitware's 25+ years of experience to quickly build your application.</small>
    </td>
  </tr>
</table>

Tags:

[Computer Vision](https://www.kitware.com/tag/computer-vision/) | [ITS](https://www.kitware.com/tag/its/) | [Lidar](https://www.kitware.com/tag/lidar/) | [LidarView](https://www.kitware.com/tag/lidarview/) | [ParaView](https://www.kitware.com/tag/paraview/) | [Point Cloud](https://www.kitware.com/tag/point-cloud/) | [Sensors](https://www.kitware.com/tag/sensors/) | [slam](https://www.kitware.com/tag/slam/) | [Trame](https://www.kitware.com/tag/trame/) | [UDP](https://www.kitware.com/tag/udp/)
