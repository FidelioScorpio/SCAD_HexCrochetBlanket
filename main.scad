include <blanket.scad>

line_w = 3;
// A double duvet is 200x200cm
duvet_square();
module duvet_square()
{
    duvet = 2000;
    translate([0, 0, 0]) color("black") cube([line_w, duvet, 6]);
    translate([0, duvet, 0]) color("black") cube([duvet, line_w, 6]);
    translate([0, 0, 0]) color("black") cube([duvet, line_w, 6]);
    translate([duvet, 0, 0]) color("black") cube([line_w, duvet, 6]);
}
// Val's knitted blanket is 170x184cm
vals_square();
module vals_square()
{
    x = 1700;
    y = 1840;
    translate([0, 0, 0]) color("blue") cube([line_w, y, 6]);
    translate([0, y, 0]) color("blue") cube([x, line_w, 6]);
    translate([0, 0, 0]) color("blue") cube([x, line_w, 6]);
    translate([x, 0, 0]) color("blue") cube([line_w, y, 6]);
}
//base_plate();
module base_plate()
{
    translate([-200,-200, -5]) color("#ffffff") cube([3000,3000,1]);
}