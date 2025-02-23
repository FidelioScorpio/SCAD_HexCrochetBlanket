

// DK hex
hex_length = 175;

// Aran hex is 185
//hex_length = 185;


x_dist_between_hexes = 2*(sqrt(pow(hex_length/2, 2) - pow(hex_length/4, 2)));
y_dist_between_hexes = 3*hex_length/4;

module hex_crochet(col)
{
    color(col) rotate(360/12) cylinder(d=hex_length, h=5, $fn=6);
    
    // difference()
    // {
    //     color("black") rotate(360/12) cylinder(d=hex_length+8, h=0.1, $fn=6);
    //     rotate(360/12) translate([0,0,-1]) cylinder(d=hex_length, h=8, $fn=6);
    // }
}
