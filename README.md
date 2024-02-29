# Simple Ray Tracer

Using Python with Numpy, an implementation of a basic backward (eye to light sources) ray tracing algorithm. 

Some examples of ray-traced scene outputs.


![ray_tracer_1](https://user-images.githubusercontent.com/48743548/206934063-838027b4-e46b-44be-aafb-0e5393447bf6.PNG)

*example_1.txt*

![ray_tracer_2](https://user-images.githubusercontent.com/48743548/206934064-caf3726c-f1e8-4a78-a485-b9d6e569adf1.PNG)

*example_2.txt*

![ray_tracer_3](https://user-images.githubusercontent.com/48743548/206934065-c0c567a4-34e4-4124-8d8f-c6f643526900.PNG)

*example_3.txt*

## How to use

The program takes in a txt file with the following syntax:

NEAR \<n>

LEFT \<l>

RIGHT \<r>

BOTTOM \<b>

TOP \<t>

RES \<x> \<y>

SPHERE \<name> \<pos x> \<pos y> \<pos z> \<scl x> \<scl y> \<scl z> \<r> \<g> \<b> \<Ka> \<Kd> \<Ks> \<Kr> \<n>\
… // up to 14 additional sphere specifications

LIGHT \<name> \<pos x> \<pos y> \<pos z> \<lr> \<lg> \<lb>\
… // up to 9 additional light specifications

BACK \<r> \<g > \<b>

AMBIENT \<Ir> \<Ig> \<Ib>

OUTPUT \<name>

### To run the program
````
python ray_tracer.py <path_to_input_file>
````
