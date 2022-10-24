# image_manip.py

# Imports
import media as m
import color

def imagescale(pic, scale=.5):
    ''' This function takes a picture and returns a copy of picture to the
    specified scale.
    
    Arguments:
       pic -> media library picture object
       scale -> floating point number '''

    if pic == None:
        return -1
    if scale == 0 or scale > 10:
        scale = .5

    orig_h = m.get_height(pic)
    orig_w = m.get_width(pic)
    target_h = int(orig_h * scale)
    target_w = int(orig_w * scale)

    return_pic = m.create_picture(target_w, target_h, m.cyan)

    for x in xrange(0, target_w):
        for y in xrange(0, target_h):
            old_x = x / scale
            old_y = y / scale
            old_px_col = m.get_color(m.get_pixel(pic, old_x, old_y))
            new_px = m.get_pixel(return_pic, x, y)
            new_px.set_color(old_px_col)

    return return_pic


def greyscale(pic):
    ''' This function receives a picture and greyscales it.
    
    Arguments:
        pic -> media library picture object'''

    for p in pic:
        red = m.get_red(p)
        blue = m.get_blue(p)
        green = m.get_green(p)
        average = (red + blue + green) // 3

        m.set_red(p,average)
        m.set_blue(p,average)
        m.set_green(p,average)


def crop_picture(pic,x1,y1,x2,y2):
    ''' This function takes a picture, pic and returns a new picture containing
    the desired rectangular crop from the original image. If the crop is not
    successful, this function returns -1.

    Arguments:
        pic -> media library picture object
        x1, y1, x2, y2 -> ints '''
    width = max(x2,x1) - min(x2,x1)
    height = max(y2, y1) - min(y2,y1)
    if (width or height) == 0:
        return -1
        # raise ValueError, "New picture can not have no width or height!"

    new_picture = m.create_picture(width,height,m.white)
    for x in range(width):
        for y in range(height):
            pix = m.get_pixel(new_picture,x,y)
            color = m.get_color(m.get_pixel(pic, x+x1, y+min(y1,y2)))
            m.set_color(pix,color)            
    return new_picture


def average_brightness(pic):
    ''' This fucntion determins the average luminance (brightness) of the
    picture. If the picture's width or height is over 999 pixels, it will be
    scaled down to speed up the process. This function does not destroy the
    original picture, and will return the luminance as a float value.
    
    Arguments:
        pic -> media library picture object '''

    pic = pic.copy()
    w = m.get_width(pic)
    h = m.get_height(pic)
    
    if h > 999 or w > 999:
        pic = imagescale(pic)
        w = w * 0.5
        h = h * 0.5

    total_brightness = 0
    for pixel in pic:
        pixel_brightness = sum(\
            [m.get_red(pixel), m.get_blue(pixel), m.get_green(pixel)]) / 3
        total_brightness += pixel_brightness

    pixels_total = int(w * h)
    average_bright = float(total_brightness / pixels_total)
    
    return average_bright


def normalize_brightness(pic):
    ''' This function normalizes the brightness of the picture.
    
    Arguments:
        pic -> media library picture object '''

    average = average_brightness(pic)
    factor = None
    if average != 128:
        factor = 128/average

    for p in pic:
        red = int(m.get_red(p) * factor)
        green = int(m.get_green(p) * factor)
        blue = int(m.get_blue(p) * factor)

        if red > 255:
            red = 255
        if green > 255:
            green = 255
        if blue > 255:
            blue = 255

        m.set_red(p, red)
        m.set_green(p, green)
        m.set_blue(p, blue)


###############################################################################
### Luminance Functions
###############################################################################
def modify_luminance(pic, mode='l'):
    ''' Wraps the luminance functions. Takes a picture and modifies the 
    luminance of the picture depending on the mode given. Returns -1 if no pic.
    
    Arguments:
        pic -> media library picture object
        mode -> str, one of (l, d, lighten, or darken). Default: l '''

    if pic is None:
        return -1

    mode = mode.lower()
    if mode not in ['l', 'd', 'lighten', 'darken']:
        mode = 'l'

    if mode.startswith('l'):
        lighten_picture(pic)
    else:
        darken_picture(pic)


def darken_picture(pic):
    ''' This function darks the picture, pic, by 35%. '''

    for pix in pic:
        m.set_red(pix, m.get_red(pix) * 1.35)
        m.set_blue(pix, m.get_blue(pix) * 1.35)
        m.set_green(pix, m.get_green(pix) * 1.35)


def lighten_picture(pic):
    ''' This function lightens the picture, pic, by 35%. '''

    for pix in pic:
        m.set_red(pix, m.get_red(pix) * .65)
        m.set_blue(pix, m.get_blue(pix) * .65)
        m.set_green(pix, m.get_green(pix) * .65)


################################################################################
### Mirror Functions
################################################################################
def mirror(pic, orient='v'):
    ''' Wrapper function for mirror functions. This function takes a picture and
    works by placing a mirror on the horizontal or vertical center of the given
    picture. Modifies the original picture.
    
    *** This function relies on code derived from w5's lecture series. ***
    
    Arguments:
        pic -> media lib picture object
        orient -> string one of (v, vert, vertical, h, hori, horizontal)
                      Default: v '''
    
    orient = orient.lower()
    if orient not in ['v', 'vert', 'vertical', 'h', 'hori', 'horizontal']:
        orient = 'v'
        
    if orient == ('v' or 'vert' or 'vertical'):
        mirror_vertical(pic)
    else:
        mirror_horizontal(pic)


def mirror_pixels(pic, x1, y1, x2, y2):
    ''' Set the colour of the pixel (x2, y2) to the colour of pixel (x1, y1)
    in picture pic.
    
    This function was derived from week 5's lecture on image manipulation. '''
    
    col = m.get_color(m.get_pixel(pic, x1, y1))
    m.set_color(m.get_pixel(pic, x2, y2), col)


def mirror_vertical(pic):
    '''Modify picture pic so that it looks like a mirror was placed 
    vertically down the middle. 
    
    This function was derived from week 5's lecture on image manipulation. '''
    
    width = m.get_width(pic)
    height = m.get_height(pic)
    middle = width / 2
    
    for x in xrange(middle):
        for y in xrange(height):
            mirror_pixels(pic, x, y, width - 1 - x, y)


def mirror_horizontal(pic):
    ''' Modify picture pic so that it looks like a mirror was placed 
    horizontally down the middle.
    
    This function was derived from week 5's lecture on image manipulation. '''
    
    width = m.get_width(pic)
    height = m.get_height(pic)
    middle = height / 2
    
    for x in xrange(width):
        for y in xrange(middle):
            mirror_pixels(pic, x, y, x, height - 1 - y)


################################################################################
### Rotate Functions
################################################################################
def rotate90(pic, direction='r'):
    ''' This function rotates the given picture left or right by 90 degrees.
    Returns a new picture 
    
    Arguments:
        pic -> media lib picture object
        direction -> str, one of (r, right, l, left) Default: r '''
    
    direction = direction.lower()
    if direction not in ['r', 'right', 'l', 'left']:
        direction = 'r'

    width = m.get_width(pic)
    height = m.get_height(pic)
    new_pic = m.create_picture(height,width)

    for x in xrange(width):
        for y in xrange(height):
            pix_colour = m.get_color(m.get_pixel(pic, x, y))
            if direction.startswith('l'):
                pixel = m.get_pixel(new_pic, y, (width - x) - 1)
            else:
                pixel = m.get_pixel(new_pic, (height - y) - 1, x)
            m.set_color(pixel, pix_colour)

    return new_pic


def rotate(pic, direction, degree=90):
    ''' This function rotates a picture by the specified degrees. This
    function only rotates by 90 degree angles. This will return a new
    picture that is rotated. If there is no picture passed, returns -1.
    
    Arguments:
        pic -> media lib picture object
        direction -> str, one of (r, right, l, left) Default: r
        degree -> integer Default: 90 '''
    
    # Rounds down to the closest interval of 90
    if degree % 90 != 0:
        degree = (degree // 90) * 90
    
    # Checks if there is a picture to work with.
    if pic is None:
        return -1

    # Direction checking.
    direction = direction.lower()
    if direction not in ['r', 'l', 'right', 'left']:
        direction = 'r'
    elif direction.startswith('r'):
        direction = 'r'
    elif direction.startswith('l'):
        direction = 'l'

    for i in xrange(degree // 90):
        pic = rotate90(pic, direction)

    return pic


def invert(pic):
    ''' This function accepts a picture and inverts the colours in the image. 
       For example, if the background was white, and the image was black, this
       function would turn the background black and the image white. '''

    for p in pic:
        red = m.get_red(p)
        green = m.get_green(p)
        blue = m.get_blue(p)
        # subtracts RGB from 255(max value) and creates a new picture.
        colour = color.Color(255 - red, 255 - green, 255 - blue)
        # sets new colour
        m.set_color(p, colour)

if __name__ == '__main__':
    test = m.load_picture('/home/simmon/Projects/CSC108/Project/header.jpg')
    m.show(test)
    normalize_brightness(test)
    m.show(test)