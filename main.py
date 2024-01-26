#
# ZeroWriter
#
# This code is open-source. Feel free to modify and redistribute as you want.
# Participate on reddit in r/zerowriter if you want.
#
# Using the new4in2part library
#
# a python e-typewriter using eink and a USB keyboard
# this program outputs directly to the SPI eink screen, and is driven by a
# raspberry pi zero (or any pi). technically, it operates headless as the OS has no
# access to the SPI screen. it handles keyboard input directly via keyboard library.
#
# currently ONLY supports waveshare 4in2
#

import time
import keyboard
import keymaps
from PIL import Image, ImageDraw, ImageFont
import textwrap
import subprocess
import signal
from waveshare_epd import new4in2part
from pathlib import Path
from handle_input import init_keyboard_listeners, handle_interrupt
from display_update import init_display, update_display, update_input_area
from cursor import insert_character, delete_character
from file import load_previous_lines,save_previous_lines, init_file_path


epd = init_display() #initialize the display

#Initialize display-related variables)
display_image = Image.new('1', (epd.width,epd.height), 255)
display_draw = ImageDraw.Draw(display_image)

#Display settings like font size, spacing, etc.
display_start_line = 0
font24 = ImageFont.truetype('Courier Prime.ttf', 18) #24
textWidth=16
linespacing = 22
chars_per_line = 32 #28
lines_on_screen = 12
last_display_update = time.time()

#display related
needs_display_update = True
needs_input_update = True
updating_input_area = False
input_catchup = False
display_catchup = False
display_updating = False
shift_active = False
control_active = False
exit_cleanup = False
console_message = ""
scrollindex=1

#init file path
file_path = init_file_path()

# Initialize cursor position
cursor_position = 0

# Initialize text matrix (size of text file)
max_lines = 100  # Maximum number of lines, adjust as needed
max_chars_per_line = chars_per_line  # Maximum characters per line, adjust as needed
text_content=""
temp_content=""
input_content=""
previous_lines = []
typing_last_time = time.time()  # Timestamp of last key press

#Startup Stuff ---
init_keyboard_listeners()
signal.signal(signal.SIGINT, handle_interrupt(signal, frame, epd))

#init_display routine
epd.init()
epd.Clear
previous_lines = load_previous_lines(file_path)#('previous_lines.txt')
epd.init_Partial()
epd.Clear
needs_display_update = True
needs_input_update = False

#mainloop
try:
    while True:
        
        if exit_cleanup:
            break
                
        if needs_display_update and not display_updating:
            update_display()
            needs_diplay_update=False
            typing_last_time = time.time()
            
        elif (time.time()-typing_last_time)<(.5): #if not doing a full refresh, do partials
            #the screen enters a high refresh mode when there has been keyboard input
            if not updating_input_area and scrollindex==1:
                update_input_area()
        #time.sleep(0.05) #the sleep here seems to help the processor handle things, especially on 64-bit installs
        
except KeyboardInterrupt:
    pass

finally:
    keyboard.unhook_all()
    epd.init()
    time.sleep(1)
    epd.Clear()
    epd.sleep()
