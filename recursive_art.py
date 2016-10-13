""" Softdes Mini Project II - Anderson Ang Wei Jian
    Changelog:
    First build - v0.1a (fixed evaluate_random_function and remap_interval)
    Second build - v0.1b (added building blocks around evaluate_random_function)
    v1.0a - First stable patch - with build_random_function working around depths 7 to 9
    v1.0b - Added difference and division functions to the mix
    v1.0c - doc_strings added to test difference and division functionality
"""

import random
import math
from PIL import Image
from math import sin, pi, cos # import math functions sin, pi and cos


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list

        Part II:
        Uses a random block number above the base case to return a nested list
        of function calls, comprising of the building blocks defined below:

            Block-types available:
            --- TWO PARAMETERS ---
            prod(a,b) = a*b
            div(a,b) = a/b
            diff(a,b) = a-b
            avg(a,b) = (a+b)/2.0
            --- SINGLE PARAMETER --
            cos_pi(a) = cos(pi*a)
            sin_pi(a) = sin(pi*a)
    """
    # define the block functions as a list to select from randomly
    blocks = ["sin_pi","cos_pi","prod","avg","div","diff"]

    # chooses a value from the depth interval between max and min (this should only be performed once)
    current_depth = random.randint(min_depth, max_depth)

    # base case has two possibilities of occurring - when the initial depth has a possibility of 1, and due to recursion
    if (current_depth == 1 or max_depth == 1):
        # chooses a value of definition between 0 and 1
        base = random.choice([0, 1])
        if (base == 0): # returns x for 0
            return ["x"]
        else:
            # returns y for 1
            return ["y"]
    # intercepts condition when min_depth reaches base case
    elif (min_depth <= 1):
        # prevents a negative value from coming about
        prevent = random.randint(1, max_depth)
        if (prevent == 1):
            base2 = random.choice([0,1])
            if (base2 == 0): # returns x for 0
                return ["x"]
            else:
                # returns y for 1
                return ["y"]
    else: # part 2
        # if current_depth lies above 1, choose between the block options
        block_number = random.randrange(0,5,1)
        if (block_number < 2):
            # single parameter function
            return [blocks[block_number], build_random_function(min_depth-1,max_depth-1)]
        else:
            # dual parameter functions
            return [blocks[block_number], build_random_function(min_depth-1,max_depth-1), build_random_function(min_depth-1,max_depth-1)]

def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02

        testing new functions out
        >>> evaluate_random_function(["div",["x"],["y"]],5.0,2)
        2.5
        >>> evaluate_random_function(["diff",["x"],["y"]],5.0,2)
        3.0
    """
    # checks the first indexed value against a known character (i.e. x or y)
    # x and y serves as the base case for the recursive loop

    if (f[0] == "x"):
        return x
    elif (f[0] == "y"):
        return y
    elif (f[0] == "sin_pi"): # takes sin (pi*value)
        # goes deeper into the nested list with each call
        return math.sin(math.pi * evaluate_random_function(f[1],x,y))
    elif (f[0] == "cos_pi"): # takes cos (pi*value)
        # behaves similarly to sin_pi
        return math.cos(math.pi * evaluate_random_function(f[1],x,y))
    elif (f[0] == "prod"):
        # takes the subsequent two listed values/parameters and multiplies them together
        return evaluate_random_function(f[1],x,y) * evaluate_random_function(f[2],x,y)
    elif (f[0] == "avg"):
        # takes the average of the subsequent two parameters in the list
        return (evaluate_random_function(f[1],x,y) + evaluate_random_function(f[2],x,y))/2.0
    elif (f[0] == "div"): # takes the divisible of the first with the second value/parameter
    # additional functions
        return (evaluate_random_function(f[1],x,y)/ evaluate_random_function(f[2],x,y))
    elif (f[0] == "diff"): # difference between the two parameters
        return (evaluate_random_function(f[1],x,y)- evaluate_random_function(f[2],x,y))


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):

    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    # creates input and output range (note: difference is expected to be positive)
    input_range = float(input_interval_end - input_interval_start)
    output_range = float(output_interval_end - output_interval_start)
    # returns an equivalent floating value in the new range's context
    return ((float(val - input_interval_start) * output_range) / input_range) + float(output_interval_start)

def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel
    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    # Archive : Red = X , Green = Y, Blue = X
    # Stage II - giving a value based on randomization instead of binary choices
    red_function = build_random_function(7,9)
    green_function = build_random_function(7,9)
    blue_function = build_random_function(7,9)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            # maps interval (0,350) to (-1,1), with i and j respectively
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    # calls a handler function to convert the color intensity values from 0 - 255
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )
    # saves file as newart.png
    im.save(filename)

# main executional block
if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    generate_art("newart.png")
    print "Map complete!"
