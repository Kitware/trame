# Local rendering with WASM

The example below showcase how the line source for the streamline seeds can be controlled from either a 3D widgets and 2D widget.

To learn more about VTK.wasm and what you can do with it, [the VTK.wasm documentation website](https://kitware.github.io/vtk-wasm/) is the reference to follow.

<video control loop autoplay muted>
    <source src="/assets/videos/cfd-bike-480.mp4" alt="Bike CFD example">
</video>


::: code-group
<<< @/../../examples/06_vtk/04_wasm/app.py{py:line-numbers} [Full code]
<<< @/../../examples/06_vtk/04_wasm/requirements.txt
:::

You can download it and run it as is if you have `uv` available.

```
curl -O https://raw.githubusercontent.com/Kitware/trame/refs/heads/master/examples/06_vtk/04_wasm/app.py
chmod +x app.py
./app.py

# or use uv run
uv run ./app.py
```
