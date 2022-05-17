# Trame v2

Trame Version 2.0 is on the verge to be released and we wanted to start sharing what it is bringing to the table while also providing a migration guide.

First of all, Trame v2 is not changing the ideas and concepts that made trame what it is. This new version is really focusing on a more powerful and refined suite for creating Python application effortlessly while supporting many deployment type. With trame we aim to support desktop, client/server, cloud services and Jupyter notebook without changing a single line of code change.

![trame](/trame/images/trame-architecture.jpg)

Like shown in the architecture diagram, trame focus on 4 types of services which help the development of interactive visual applications.

- __State__ in trame is shared across the presentation layer and the buisness logic. Also on top of being shared, it is reactive which means that the UI will react to reflect any change done from the buisness logic. Also in the same fashion, when a slider or else modify a given variable, the buisness logic can listen to it and react appropriately. This __state__ make the binding of the **buisness logic** and **UI** a breeze.
- __Events__ are used to trigger actions usually on buisness logic side to react to user interaction such as a mouse click, hover or else. Trame offer an elegent solution for simply binding methods to any available UI event.
- __Widgets__ are key for building and composing a graphical application. Trame already provide an extensive set of widgets that include the common set of form elements but also charts, maps and 3D visualization based on VTK/ParaView. Also on top of the built-in ones, it is easy to contribute or include your own set of widget when developing your own application. Basically you are not limited to what we have. Trame can easily integrate any web based component and interface it so you can use it directly within Python.
- __UI__ are mainly the same thing as widgets except they are more geared toward layouts or pages sections that you may want to update dynamically during the life cycle of your application. Usually applications have a single layout component which represent the UI of the application.


With the release of trame v2, we focused on rationalizing and normalizing how we want users to leverage and contributes to trame. In other words, trame v1 allowed the magic to happen while v2 focus on the best practice by streamlining APIs and code structure while enabling composition and integration into existing web applications.

With trame v2, we are deprecating PyWebVue in favor of our trame suite (trame + trame-*) to better support code evolution and cross compatibility. One issue we had before with PyWebVue was that it was doing too many things and sometime was getting out of sync with trame. Now with our trame suite, each python module contains both its client and its server side which make it almost impossible to have them out of sync or not working.

Also now that we have formalized how new Python modules should interface with trame. The community can more simply extend trame with their new widgets and/or UI elements.

Now you might be wondering if a trame v3 is planed with yet another breaking change in another 6 months? Well to be honest we may have released too early pywebvue and trame but they were so game changer that it was hard to keep them for ourself. To be honest, I don't see a v3 anytime soon as v2 has gave us a chance to review our api, fixed what we didn't like and provide an easy path across our various use-cases.