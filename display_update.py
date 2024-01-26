from waveshare_epd import new4in2part


def init_display():
    # Initialize the e-Paper display
    # clear refreshes whole screen, should be done on slow init()
    epd = new4in2part.EPD()
    epd.init()
    epd.Clear()
    return epd

def update_display():
    global last_display_update
    global needs_display_update
    global cursor_index
    global previous_lines
    global display_updating
    global updating_input_area
    global console_message
    global current_line
    global scrollindex
    
    # Clear the main display area -- also clears input line (270-300)
    display_draw.rectangle((0, 0, 400, 300), fill=255)
    
    # Display the previous lines
    y_position = 270 - linespacing  # leaves room for cursor input

    #Make a temp array from previous_lines. And then reverse it and display as usual.
    current_line=max(0,len(previous_lines)-lines_on_screen*scrollindex)
    temp=previous_lines[current_line:current_line+lines_on_screen]
    #print(temp)# to debug if you change the font parameters (size, chars per line, etc)

    for line in reversed(temp[-lines_on_screen:]):
       display_draw.text((10, y_position), line[:max_chars_per_line], font=font24, fill=0)
       y_position -= linespacing

    #Display Console Message
    if console_message != "":
        display_draw.rectangle((300, 270, 400, 300), fill=255)
        display_draw.text((300, 270), console_message, font=font24, fill=0)
        console_message = ""
    
    #generate display buffer for display
    partial_buffer = epd.getbuffer(display_image)
    epd.display(partial_buffer)

    last_display_update = time.time()
    display_catchup = True
    display_updating= False
    needs_display_update = False

def update_input_area(): #this updates the input area of the typewriter (active line)
    global last_display_update
    global needs_display_update
    global cursor_index
    global needs_input_update
    global updating_input_area

    cursor_index = cursor_position
    display_draw.rectangle((0, 270, 400, 300), fill=255)  # Clear display
    
    #add cursor
    temp_content = input_content[:cursor_index] + "|" + input_content[cursor_index:]
    
    #draw input line text
    display_draw.text((10, 270), str(temp_content), font=font24, fill=0)
    
    #generate display buffer for input line
    updating_input_area = True
    partial_buffer = epd.getbuffer(display_image)
    epd.display(partial_buffer)
    updating_input_area = False