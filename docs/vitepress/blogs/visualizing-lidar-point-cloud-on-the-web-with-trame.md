[post](https://www.kitware.com/visualizing-lidar-point-cloud-on-the-web-with-trame/)

# Lidar point cloud on the web with trame

February 27, 2024

[Adrien Stucky](https://www.kitware.com/author/adrien-stucky/ "Posts by Adrien Stucky"), [Jules Bourdais](https://www.kitware.com/author/jules-bourdais/ "Posts by Jules Bourdais"), [Gatien Ferret](https://www.kitware.com/author/gatien-ferret/ "Posts by Gatien Ferret") and [Julien Finet](https://www.kitware.com/author/julien-finet/ "Posts by Julien Finet")

![](https://www.kitware.com/main/wp-content/uploads/2024/02/20240226-Screenshot.png)

[LidarView](https://lidarview.kitware.com/) is an open source application developed by Kitware based on ParaView and enabling live 3D sensor reading, recording and processing from multiple vendors.

[trame](https://kitware.github.io/trame/), is a python based framework developed by Kitware to easily create web applications for visual analytics by leveraging python libraries and with a client-server mechanism.

Combining both opens the door to new types of usage and user experience with LiDAR sensors. You can now share a no-install web interface for your point cloud processing pipelines,  remotely render live visualizations seen by a LiDARs sensor without the need to transmit the whole point cloud from the server to the client ( i.e. web browser).

If you have a robot/drone with a mounted LiDAR sensor, you can visualize in real time what it sees and trigger processes directly from a web page.

![](https://www.kitware.com/main/wp-content/uploads/2024/02/first_minute_x3speed-800px.gif)

A trame-based LidarView web application (video accelerated for best effect)

[A few months ago](https://www.kitware.com/point-cloud-visualization-on-the-web-with-lidarview-and-vtk-js/), we exposed LidarView onto the web with ParaView Web. We recently improved the demo to extend its usage and capabilities. By using trame, we created a web viewer that remotely renders a LiDAR point-cloud while adding more types of visualization (a map with [Leaflet](https://leafletjs.com/) and a chart with [Plotly](https://plotly.com/)). The point-cloud is registered in real-time using [LidarView’s SLAM algorithm](https://www.kitware.com/lidar-slam-spotlight-on-kitwares-open-source-library/).

The web application is 100% Python code and internally calls LidarView and ParaView Python functions.

Reach us out if you want to know how you can bring your point-clouds onto the web.

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

[Lidar](https://www.kitware.com/tag/lidar/) | [LidarView](https://www.kitware.com/tag/lidarview/) | [Point Cloud](https://www.kitware.com/tag/point-cloud/) | [Python](https://www.kitware.com/tag/python/) | [slam](https://www.kitware.com/tag/slam/) | [Trame](https://www.kitware.com/tag/trame/) | [Web Visualization](https://www.kitware.com/tag/web-visualization/)

