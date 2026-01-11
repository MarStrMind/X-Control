import pygame
import keyboard
import json
import sys
from time import sleep

# Key combos that define which key should be emitted at which button
activators = []

# Press and release a key with or without modifier
def press_key(key, mod):
    if mod != "":
        keyboard.press(mod+"+"+key)
        sleep(.25)
        keyboard.release(mod+"+"+key)
    else:
        keyboard.press(key)
        sleep(.25)
        keyboard.release(key)


# Find all activators we want to monitor
def find_activators(json_data):
    for a in json_data["triggers"]:
        activators.append([a["activator"], a["buttons"], a["keys"], a["mods"], 0]) # Key combo, joystick button, keys, modifiers, active 0/1


# Enable a certain key combo to be emitted at a joystick button
def switch_active_key(kb):
    # Disable all activators, except the one that was pressed
    for a in range(0, len(activators)):
        activators[a][4] = 0
        if activators[a][0] == kb:
            activators[a][4] = 1


def handle_control():
    # Load the JSON with the profile we want to use
    json_profile = sys.argv[1]
    json_f = open(json_profile, "r")
    json_data = json.loads(json_f.read())

    # Find activators
    find_activators(json_data)

    # Add all activators
    for a in activators:
        keyboard.add_hotkey(a[0], switch_active_key, args=[a[0]])

    # Initialize Pygame and Joystick module
    pygame.init()
    pygame.joystick.init()

    # Check for connected joysticks
    if pygame.joystick.get_count() == 0:
        print("Error: No joystick connected.")
        return

    # Initialize the first available joystick
    # In Pygame 2.6.0+, it's best to use the device_index or instance_id
    joystick = pygame.joystick.Joystick(json_data["joy_id"])
    joystick.init()
    print(f"Intercepting input from: {joystick.get_name()}")

    keyhold = False
    btnpos = -1
    btnprs = -1
    loopsleep = True

    # Main Event Loop
    # You must pump the event queue (pygame.event.get) to receive updates
    try:
        while True:
            for event in pygame.event.get():

                # Find active button
                if hasattr(event, "button"):
                    for a in range(0, len(activators)):
                        if activators[a][4] == 1:
                            btns = activators[a][1].split(",")
                            btns = map(int, btns)
                            if event.button in btns:
                                btnpos = a
                                break

                # Only do something if one if the defined buttons was pressed, and the
                # corresponding activator was enabled
                if btnpos != -1:

                    # Detect button presses
                    
                    if keyhold == False and event.type == pygame.JOYBUTTONDOWN:
                        if hasattr(event, "button"):
                            keyhold = True
                            btnprs = event.button

                    elif event.type == pygame.JOYBUTTONUP:
                        keyhold = False
                        btnpos = -1
                        btnprs = -1

            if btnpos != -1 and btnprs != -1:
                btns = activators[btnpos][1].split(",")
                keys = activators[btnpos][2].split(",")
                mods = activators[btnpos][3].split(",")
                btns[0] = int(btns[0])
                btns[1] = int(btns[1])
                
                if keyhold == True and btnpos != -1 and btnprs != -1:
                    loopsleep = False
                    if btnprs in btns:
                        if len(mods) < 2:
                            if btnprs == btns[0]:
                                press_key(keys[0], "")
                            if btnprs == btns[1]:
                                press_key(keys[1], "")
                        if len(mods) == 2:
                            if btnprs == btns[0]:
                                press_key(keys[0], mods[0])
                            if btnprs == btns[1]:
                                press_key(keys[1], mods[1])

            if loopsleep == True:
                sleep(.016)
            continue

                

    except KeyboardInterrupt:
        print("\nStopping interceptor...")
    finally:
        pygame.quit()


def list_joysticks():
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

    print("")
    print(" Use the number in brackets in your JSON file to access the correct hardware:")
    print("")
    for j in joysticks:
        print(" [" + str(j.get_id()) + "] - " + j.get_name())
    print("")

def test_joystick(joyid):
    # 1. Initialize Pygame and Joystick module
    pygame.init()
    pygame.joystick.init()

    # 2. Check for connected joysticks
    if pygame.joystick.get_count() == 0:
        print("Error: No joystick connected.")
        return

    # 3. Initialize the first available joystick
    # In Pygame 2.6.0+, it's best to use the device_index or instance_id
    joystick = pygame.joystick.Joystick(joyid)
    joystick.init()
    print(f"Intercepting input from: {joystick.get_name()}")

    # 4. Main Event Loop
    # You must pump the event queue (pygame.event.get) to receive updates
    try:
        while True:
            for event in pygame.event.get():
                # Detect button presses
                if event.type == pygame.JOYBUTTONDOWN:
                    print(f"Button {event.button} pressed.")
                
                # Detect button releases
                elif event.type == pygame.JOYBUTTONUP:
                    print(f"Button {event.button} released.")

                # Detect Axis motion (Joysticks/Triggers)
                # Value ranges from -1.0 to 1.0
                elif event.type == pygame.JOYAXISMOTION:
                    if abs(event.value) > 0.1:  # Small deadzone filter
                        print(f"Axis {event.axis} moved to {event.value:.2f}")

                # Detect D-Pad (Hat) motion
                # Returns a tuple (x, y) like (0, 1) for UP or (-1, 0) for LEFT
                elif event.type == pygame.JOYHATMOTION:
                    print(f"Hat {event.hat} moved to {event.value}")

                # Close script if the window is closed (if a window exists)
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    except KeyboardInterrupt:
        print("\nStopping interceptor...")
    finally:
        pygame.quit()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == "--list":
            list_joysticks()
            exit()

    if len(sys.argv) == 3:
        if sys.argv[1] == "--test":
            test_joystick(int(sys.argv[2]))
            exit()

    handle_control()
