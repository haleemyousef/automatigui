#!/usr/bin/env python3

# General-purpose dependencies
import time
import json
import sys
import argparse
# Record dependencies
from pynput import mouse
from pynput import keyboard
# Play dependencies
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController

# n = len(sys.argv)

# if n < 2:
#     exit("Takes a compulsory argument - name of recording, and optional argument - record-all")

# if n > 3:
#     exit("Only takes two arguments - name of recording and (optional) record-all")

# if n == 2:
#     name_of_recording = str(sys.argv[1])
#     record_all = False
# if n == 3:
#     if str(sys.argv[2]) != "record-all":
#         exit("The second argument given must be 'record-all', otherwise only pass the name of recording as a parameter")
#     name_of_recording = str(sys.argv[1])
#     record_all = True


def main():
    """
    Here goes the configuration variables like
    Exit key
    Pause key

    """
    # if sys.argv != correct_number :
    #       you specified an incorrect number of arguments 
    #       print arg help
    # OR 
    # try:
    #       do all this
    # except:
    #       print help
    parser = argparse.ArgumentParser(
        prog='',
        description=''
    )
    command = parser.add_subparsers(dest='command', required=True)

    record = command.add_parser('record')
    record.add_argument(
        'FILE', 
        type=str,
        help='The path of the file where the recording will be saved. If the file does not exist, it will be automatically created.'
    )

    play = command.add_parser('play')
    play.add_argument(
        'FILE', 
        type=str,
        help='The path of the recording to be played'
    )
    play.add_argument(
        '-s', '--speed',
        type=int,
        default=1,
        help='with play only, speed of by which each iteration will be executed. Default value is 1.'
    )
    play.add_argument(
        '-l', '--loop',
        type=int,
        default=1,
        help='with play only, how many times the recording is executed. Default value is 1.'
    )
    play.add_argument(
        '-t', '--time',
        type=int,
        help='with play only, for how long in seconds the recording will be executed. This option if chosen overrides --loop'
    )
    parser.add_argument(
        '-v', '--verbose',
        help='',
        action='store_true'
    )

    args = parser.parse_args()
    # if argument -r was used:
    # Collect events from keyboard until esc
    # Collect events from mouse until scroll
    keyboard_listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)

    mouse_listener = mouse.Listener(
            on_click=on_click,
            on_scroll=on_scroll,
            on_move=on_move)

    keyboard_listener.start()
    mouse_listener.start()
    keyboard_listener.join()
    mouse_listener.join()
    # elif argument -p was used:
    # else:
    #       print help message

##########################################################
# Start of Recording Class
##########################################################
storage = []
count = 0

def on_press(key):
    try:
        json_object = {'action':'pressed_key', 'key':key.char, '_time': time.time()}
    except AttributeError:
        if key == keyboard.Key.esc:
            return False
        json_object = {'action':'pressed_key', 'key':str(key), '_time': time.time()}
    storage.append(json_object)

def on_release(key):
    try:
        json_object = {'action':'released_key', 'key':key.char, '_time': time.time()}
    except AttributeError:
        json_object = {'action':'released_key', 'key':str(key), '_time': time.time()}
    storage.append(json_object)
        

def on_move(x, y):
    if (record_all) == True:
        if len(storage) >= 1:
            if storage[-1]['action'] != "moved":
                json_object = {'action':'moved', 'x':x, 'y':y, '_time':time.time()}
                storage.append(json_object)
            elif storage[-1]['action'] == "moved" and time.time() - storage[-1]['_time'] > 0.02:
                json_object = {'action':'moved', 'x':x, 'y':y, '_time':time.time()}
                storage.append(json_object)
        else:
            json_object = {'action':'moved', 'x':x, 'y':y, '_time':time.time()}
            storage.append(json_object)
    else:
        if len(storage) >= 1:
            if (storage[-1]['action'] == "pressed" and storage[-1]['button'] == 'Button.left') or (storage[-1]['action'] == "moved" and time.time() - storage[-1]['_time'] > 0.02):
                json_object = {'action':'moved', 'x':x, 'y':y, '_time':time.time()}
                storage.append(json_object)

def on_click(x, y, button, pressed):
    json_object = {'action':'pressed' if pressed else 'released', 'button':str(button), 'x':x, 'y':y, '_time':time.time()}
    storage.append(json_object)
    if len(storage) > 1:
        if storage[-1]['action'] == 'released' and storage[-1]['button'] == 'Button.right' and storage[-1]['_time'] - storage[-2]['_time'] > 2:
            with open('data/{}.txt'.format(name_of_recording), 'w') as outfile:
                json.dump(storage, outfile)
            return False


def on_scroll(x, y, dx, dy):
    json_object = {'action': 'scroll', 'vertical_direction': int(dy), 'horizontal_direction': int(dx), 'x':x, 'y':y, '_time': time.time()}
    storage.append(json_object)

##########################################################
# End of Recording Class
##########################################################



def play(name_of_recording, number_of_plays): # and an optional argument for time

#     name_of_recording = "data/" + str(sys.argv[1]) +'.txt'
#     number_of_plays = int(sys.argv[2])

    with open(name_of_recording) as json_file:
        data = json.load(json_file)

    special_keys = {"Key.shift": Key.shift, "Key.tab": Key.tab, "Key.caps_lock": Key.caps_lock, "Key.ctrl": Key.ctrl, "Key.alt": Key.alt, "Key.cmd": Key.cmd, "Key.cmd_r": Key.cmd_r, "Key.alt_r": Key.alt_r, "Key.ctrl_r": Key.ctrl_r, "Key.shift_r": Key.shift_r, "Key.enter": Key.enter, "Key.backspace": Key.backspace, "Key.f19": Key.f19, "Key.f18": Key.f18, "Key.f17": Key.f17, "Key.f16": Key.f16, "Key.f15": Key.f15, "Key.f14": Key.f14, "Key.f13": Key.f13, "Key.media_volume_up": Key.media_volume_up, "Key.media_volume_down": Key.media_volume_down, "Key.media_volume_mute": Key.media_volume_mute, "Key.media_play_pause": Key.media_play_pause, "Key.f6": Key.f6, "Key.f5": Key.f5, "Key.right": Key.right, "Key.down": Key.down, "Key.left": Key.left, "Key.up": Key.up, "Key.page_up": Key.page_up, "Key.page_down": Key.page_down, "Key.home": Key.home, "Key.end": Key.end, "Key.delete": Key.delete, "Key.space": Key.space}

    mouse = MouseController()
    keyboard = KeyboardController()

    for loop in range(number_of_plays):
        for index, obj in enumerate(data):
            action, _time= obj['action'], obj['_time']
            try:
                next_movement = data[index+1]['_time']
                pause_time = next_movement - _time
            except IndexError as e:
                pause_time = 1
            
            if action == "pressed_key" or action == "released_key":
                key = obj['key'] if 'Key.' not in obj['key'] else special_keys[obj['key']]
                print("action: {0}, time: {1}, key: {2}".format(action, _time, str(key)))
                if action == "pressed_key":
                    keyboard.press(key)
                else:
                    keyboard.release(key)
                time.sleep(pause_time)


            else:
                move_for_scroll = True
                x, y = obj['x'], obj['y']
                if action == "scroll" and index > 0 and (data[index - 1]['action'] == "pressed" or data[index - 1]['action'] == "released"):
                    if x == data[index - 1]['x'] and y == data[index - 1]['y']:
                        move_for_scroll = False
                print("x: {0}, y: {1}, action: {2}, time: {3}".format(x, y, action, _time))
                mouse.position = (x, y)
                if action == "pressed" or action == "released" or action == "scroll" and move_for_scroll == True:
                    time.sleep(0.1)
                if action == "pressed":
                    mouse.press(Button.left if obj['button'] == "Button.left" else Button.right)
                elif action == "released":
                    mouse.release(Button.left if obj['button'] == "Button.left" else Button.right)
                elif action == "scroll":
                    horizontal_direction, vertical_direction = obj['horizontal_direction'], obj['vertical_direction']
                    mouse.scroll(horizontal_direction, vertical_direction)
                time.sleep(pause_time)
    





if __name__ == '__main__':
    main()
