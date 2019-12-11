#### Dependencies and Installation

- Python3 
- matplotlib
- bounce-viz, another github repo for geometry calculations (included as
submodule)

The necessary libraries are included in requirements.txt. To automatically
install the dependencies, run

```
pip install -r requirements.txt
```

Then, add the submodule and install the dependencies there:

```
git submodule init
git submodule update
cd bounce-viz
pip install -r requirements.txt
```

#### Getting Started

Run `python game.py` to start the interactive visualization. A new window should
open with an environment. Move the sliders to change the robot's start position
and bounce angle, and use the buttons to change bounce rule definitions.
