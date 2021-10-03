# Hex Crochet Blanket
This is not meant to be printed. This is a 3D design to assist in the creation and colour choices of a crocheted blanket.

The python file when run will create/replace the blanket.scad file.
It can also be used to provide suggestions for next colours from those available.
It uses weightings to determine the best colour choice now to minimise adjacent duplicate colours and colour chains (e.g. red blue red blue).
(The batch just enables the python to be run quickly from windows cmd.)

tile.scad defines the shape and size of one hexagon and is used by the generated blanket file.
main.scad views the full blanket.
