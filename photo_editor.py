################################################################################
###
### Authors: David Tran, Simmon Li
###     With code from University of Toronto CSC108 and CSC148 Lectures.
###
### Remarks:
###     * Testing suite not implimented
###     * Added picture history using stack (rudimentary implimentation)
###     * Have not implimented Lighten/Darken to Interface (not needed)
###
################################################################################

################################################################################
###
### This template was provided on the course website November 11th, 2008
###
################################################################################

# Imports
import Tkinter as Tk
import media as m
import image_manipulation as image_manip
import tkMessageBox
from stack import Stack       # Implimented with material from 148, see file
from PIL import ImageTk

################################################################################
### Manipulation Function Wrappers
################################################################################
def wrap_resize(label, scale):
    ''' Wrapper for resize functions. '''

    if wrap_checkimage(label):
        label.picture = image_manip.imagescale(label.picture, scale)
        update_label(label)

def wrap_mirror(label, orientation):
    ''' Wrapper for mirror functions. '''

    if wrap_checkimage(label):
        image_manip.mirror(label.picture, orientation)
        update_label(label)

def wrap_greyscale(label):
    ''' Wrapper for greyscale function. '''

    if wrap_checkimage(label):
        image_manip.greyscale(label.picture)
        update_label(label)

def wrap_normalize(label):
    ''' Wrapper for brightness normalization. '''

    if wrap_checkimage(label):
        image_manip.normalize_brightness(label.picture)
        update_label(label)

def wrap_crop(label,x1,y1,x2,y2):
    ''' Wrapper for crop. '''
    
    if wrap_checkimage(label):    
        label.picture = image_manip.crop_picture(label.picture,x1,y1,x2,y2)
        update_label(label)

def wrap_rotate(label, direction, degrees):
    ''' Wrapper for rotate functions. '''

    if wrap_checkimage(label):
        label.picture = image_manip.rotate(label.picture, direction, degrees)
        update_label(label)

def wrap_invert(label):
    ''' Wrapper for invert function. '''

    if wrap_checkimage(label):
        image_manip.invert(label.picture)
        update_label(label)

def picture_undo(label):
    ''' Undoes the last image manipulation that was done. There are some
    limitations that are not addressed with this implimentation. Stack is reset
    when the picture is saved or closed and only contains the previous step to
    the one being saved. This is to avoid some weird stack reversing that's 
    happening. '''

    # Set the label picture to the oldest history copy
    label.picture = PictureHistory.pop()
    update_label(label)

    # Update Status Bar
    Stacksize.set('Undo: ' + str(PictureHistory.size()))

################################################################################
### Update Label Utility Function, provided by course website.
################################################################################
def update_label(label):
    '''Update Label label to re-display its picture. This needs to be called
    any time label's image is changed.'''

    photo = ImageTk.PhotoImage(label.picture.get_image())
    label.config(image=photo)
    label.config(width=photo.width())
    label.config(height=photo.height())

    # Keep a reference to the PhotoImage to avoid garbage collection.
    label.image = photo

def wrap_checkimage(label):
    ''' Wrapper check to see if an image is open in Label label.'''

    global PictureHistory
    global Stacksize

    if label.image is None:
        Stattext.set("No image open!")
        return False
    else:
        # Get a copy of the picture before we modify it
        pic = label.picture.copy()
        # Add to stack
        PictureHistory.push(pic)
        # Update bar
        Stacksize.set('Undo: ' + str(PictureHistory.size()))
        return True

################################################################################
### Mouse event helpers / Crop command
################################################################################
def handle_mouse_click(event, mystery):
    ''' This function recieves an event and an unknown function.  The purpose 
    of this function is to return coordinates using the unknown (mystery) 
    function. '''
    
    # assigns coordinates to the event(click)
    coordinates = event.x, event.y
    # return value from mystery function
    return mystery(coordinates[0],coordinates[1])
    
def return_coordinates(x,y):
    ''' This function accepts a x and y value and returns them as a tuple. '''
    
    return (x,y)

def get_coordinates(event):
    ''' This function obtains an event and uses the event to return coordinates
    and to bind the picture with a mouse click again. '''

    global coords1
    
    # use callback function
    coords1 = handle_mouse_click(event, return_coordinates)
    
    # binds the picture with the left-click on a mouse
    pic_label.bind("<Button-1>", get_coordinates2)
    
def get_coordinates2(event):
    ''' This function receives an event and sets another pair of coordinates
    from the second click to be used in the crop function in 
    image_manipulation. '''

    global coords1
    global coords2
    
    # uses callback function for obtaining second pair of coordinates
    coords_second_set = handle_mouse_click(event, return_coordinates)

    # Do some error checking
    if coords_second_set < coords1:
        coords2 = coords1
        coords1 = coords_second_set
    else:
        coords2 = coords_second_set
    
    # Calls crop
    wrap_crop(pic_label,coords1[0],coords1[1],coords2[0],coords2[1])
    
    # Releases the bind on pic_label
    pic_label.unbind("<Button-1>")

def crop_cmd():
    ''' This function binds the picture with a left-click of the mouse. '''

    # <Button-1> = left-click
    pic_label.bind("<Button-1>", get_coordinates)

################################################################################
### Menu Options
################################################################################
def open_pic(label, PictureSaved):
    ''' Prompt for a Picture file, load that picture, and display it in Label
    label. This function was provided by the course website with this
    template.'''

    PictureSaved.set(False)
    # Keep a reference to the picture so it can be modified.
    filename = m.choose_file()
    label.picture = m.load_picture(filename)

    # Update Status bar
    Stattext.set("Loaded: %s" % (filename, ))

    # Update Label
    update_label(label)

    # Update History Stack
    PictureHistory.push(label.picture)
    Stacksize.set('Undo: ' + str(PictureHistory.size()))

def close_pic(label, PictureSaved):
    ''' Prompts the user to ask if they really want to close the picture.
    If yes, closes the currently open picture in the label. '''

    global PictureHistory

    if label.image is None:
        return -1

    msg = "Are you sure you want to close this picture?"
    if not PictureSaved.get():
        msg = "This image is not currently saved!\n" + msg
    if tkMessageBox.askyesno(title="Close Picture", message=msg):
        # Reset stack
        PictureHistory.clear()
        Stacksize.set('Undo: ' + str(PictureHistory.size()))

        # Reset label
        label.image = None
        label.picture = None

def save_pic(label, PictureSaved):
    ''' Saves the current picture. '''

    if label.image is None:
        return -1

    g = m.save_as(label.picture)
    if g == 0:
        PictureSaved.set(True)

        # Reset stack
        last_pic = PictureHistory.pop()
        PictureHistory.clear()
        PictureHistory.push(last_pic)
        Stacksize.set('Undo: ' + str(PictureHistory.size()))

def quit_app(label, PictureSaved):
    ''' Prompts the user to ask if they really want to exit the program. If yes,
    destroys the app window, media's root and quits the TK Interface. '''

    msg = "Are you sure you want to exit?"
    if (label.image is not None) and (not PictureSaved.get()):
        msg = "Picture not saved!\n" + msg

    if tkMessageBox.askyesno(title="Quit?", \
                            message=msg):
        global window
        window.destroy()
        m.root.destroy()
        m.root.quit()

if __name__ == "__main__":
    ############################################################################
    ### Set up interface
    ############################################################################

    # Main Window
    window = Tk.Toplevel(padx=10, pady=10, width=30, height=30)
    window.title("CSC108 Image Editor")

    # Program level variables.
    PictureSaved = Tk.BooleanVar()
    Stattext = Tk.StringVar()
    Stattext.set("Hello World.")
    PictureHistory = Stack()
    Stacksize = Tk.StringVar()
    Stacksize.set('Undo: ' + str(PictureHistory.size()))
    coords1 = ()
    coords2 = ()

    # Frame for tools
    tools_frame = Tk.Frame(window, padx=10, pady=10, borderwidth=1,
                                relief=Tk.RAISED)
    tools_frame.pack(side=Tk.LEFT, anchor=Tk.NW)

    # Frame for image
    image_frame = Tk.Frame(window, padx=10)
    image_frame.pack(after=tools_frame, expand=1, anchor=Tk.NW)

    # Make menu
    app_menu = Tk.Menu(window)
    window.config(menu=app_menu)

    # Add Open Picture Option
    invoke_change_pic = lambda : open_pic(pic_label, PictureSaved)
    app_menu.add_command(label="Open...", command=invoke_change_pic)

    # Add Close Picture Option
    invoke_close_pic = lambda : close_pic(pic_label, PictureSaved)
    app_menu.add_command(label="Close...", command=invoke_close_pic)

    # Add Save Picture Option
    invoke_save_pic = lambda : save_pic(pic_label, PictureSaved)
    app_menu.add_command(label="Save As...", command=invoke_save_pic)

    # Add Quit Application Button
    invoke_quit = lambda : quit_app(pic_label, PictureSaved)
    app_menu.add_command(label="Quit...", command=invoke_quit)

    # Add Headers
    pic_header = Tk.Label(image_frame, text="Image")
    pic_header.pack(anchor=Tk.NW)

    tools_header = Tk.Label(tools_frame, text='Tools')
    tools_header.pack()

    # Add a label to display the picture
    pic_label = Tk.Label(image_frame, width=20, height=10)
    pic_label.pack(after=pic_header)

    # Initalize the attributes we'll be using.
    pic_label.image = None
    pic_label.picture = None

    ############################################################################
    ### Add manipulation functions
    ############################################################################

    # Undo
    undo_cmd = lambda : picture_undo(pic_label)
    undo_button = Tk.Button(tools_frame, text='Undo Last Action',
                                    command=undo_cmd)
    undo_button.pack()
    
    # Greyscale
    greyscale_cmd = lambda : wrap_greyscale(pic_label)
    greyscale_button = Tk.Button(tools_frame, text='Greyscale',
                                      command=greyscale_cmd)
    greyscale_button.pack()

    # Normalize Brightness
    normalize_cmd = lambda : wrap_normalize(pic_label)
    normalize_button = Tk.Button(tools_frame, text='Normalize Brightness',
                                      command=normalize_cmd)
    normalize_button.pack()

    # Resize
    resize_scale = Tk.Scale(tools_frame, label="Scale %", from_=50, to=150,
                                 resolution=5, orient=Tk.HORIZONTAL)
    resize_scale.set(100)
    resize_scale.pack()

    resize_cmd = lambda : wrap_resize(pic_label, (resize_scale.get()/100.0))
    resize_button = Tk.Button(tools_frame, text='Scale Image',
                                   command=resize_cmd)
    resize_button.pack()

    # Mirror functions
    mirror_hori_cmd = lambda : wrap_mirror(pic_label, 'h')
    mirror_hori_button = Tk.Button(tools_frame, text='Mirror Horizontally',
                                   command=mirror_hori_cmd)
    mirror_hori_button.pack()

    mirror_vert_cmd = lambda : wrap_mirror(pic_label, 'v')
    mirror_vert_button = Tk.Button(tools_frame, text='Mirror Vertically',
                                   command=mirror_vert_cmd)
    mirror_vert_button.pack()
    
    # Crop
    crop_button = Tk.Button(tools_frame, text = 'Crop', command = crop_cmd)
    crop_button.pack()

    # Rotate
    rotate_scale = Tk.Scale(tools_frame, label="Rotate Degrees", from_=90,
                            to=270, resolution=90, orient=Tk.HORIZONTAL)
    rotate_scale.set(180)
    rotate_scale.pack()

    rotate_right_cmd = lambda : wrap_rotate(pic_label, 'r', rotate_scale.get())
    rotate_button_R = Tk.Button(tools_frame, text='Rotate Clockwise',
                                   command=rotate_right_cmd)
    rotate_button_R.pack()

    rotate_left_cmd = lambda : wrap_rotate(pic_label, 'l', rotate_scale.get())
    rotate_button_L = Tk.Button(tools_frame, text='Rotate Counter-Clockwise',
                                   command=rotate_left_cmd)
    rotate_button_L.pack()
    
    # Invert
    invert_cmd = lambda : wrap_invert(pic_label)
    invert_button = Tk.Button(tools_frame, text='Negative Colors',
                                      command=invert_cmd)
    invert_button.pack()

    ############################################################################
    ### Status Frame, displays variables, mouse location, etc. Must be last.
    ############################################################################

    status_frame = Tk.Frame(window, padx=10)
    status_frame.pack(anchor=Tk.SW, after=image_frame)

    image_saved_label = Tk.Label(status_frame, textvar=str(PictureSaved))
    image_saved_label.grid(row=0, column=0)

    message_label = Tk.Label(status_frame, textvar=Stattext)
    message_label.grid(row=0, column=1)
    
    sep_label = Tk.Label(status_frame, text=' | ')
    sep_label.grid(row=0, column=2)
    
    stack_size_label = Tk.Label(status_frame, textvar=Stacksize)
    stack_size_label.grid(row=0, column=3)

    # Run the event loop
    window.mainloop()