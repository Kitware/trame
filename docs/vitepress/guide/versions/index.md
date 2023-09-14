# Trame

Trame through major version change is not changing the ideas or concepts that made trame what it is. Each version is all about refining its suite for creating Python applications while supporting many deployment types. Trame supports desktop, client/server, cloud services, and Jupyter notebook without changing any code.

![trame](/assets/images/guide/architecture.png)

As shown in the architecture diagram, trame focus on four types of services supporting the development of interactive visual applications.

- __State__ in trame the state is shared across the presentation layer and the business logic. Furthermore, it is reactive which means that the UI responds to any changes made to the business logic. Similarly, when a slider or else modify a given variable, the business logic can listen to it and react appropriately. This __state__ make the binding of the **business logic** and **UI** a breeze.
- __Events__ are used to trigger actions usually on business logic side to react to user interaction such as a mouse click or hover event. Trame offer an elegent solution for simply binding methods to any available UI event.
- __Widgets__ are key to building and composing a graphical application. Trame provides an extensive set of widgets that include the common set of form elements but also charts, maps and 3D visualization based on VTK/ParaView. On top of these built-in widgets, it is easy to contribute or include other widget sets when developing an application. Basically applications are not limited to what trame provides by default. Trame can easily integrate any web based component and provide interfaces to them so they can be used directly from within Python.
- __UI__ are similar to widgets except they are geared toward layouts or pages sections that may need dynamic updates during the life cycle of an application. Usually applications have a single layout component which represent the UI of the application.


With the release of trame v2, we focused on rationalizing and normalizing how we want users to leverage and contributes to trame. In other words, trame v1 allowed the magic to happen while v2 focus on best practices by streamlining APIs and code structures, enabling composition and integration into existing web applications.

With trame v2, we are deprecating PyWebVue in favor of our trame suite (trame + trame-*) to better support code evolution and cross compatibility. One issue we had before with PyWebVue was that it was doing too many things and sometime was getting out of sync with trame. Now in the current trame suite, each Python module contains both its client and its server side which prevents them from becoming out of sync or not working.

In addition, since v2 formalizes how Python modules should interface with trame, the community can more easily extend trame with new widgets and/or UI elements.

With trame v3, we are focusing on enabling vue3 client while making the default bundle as small as possible.