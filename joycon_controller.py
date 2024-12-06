import time
from pyjoycon import JoyCon, get_L_id, get_R_id
from drone_control import Drone
import socket
import threading



left_joycon_id = get_L_id()
right_joycon_id = get_R_id()
left_joycon = JoyCon(*left_joycon_id)
right_joycon = JoyCon(*right_joycon_id)

status_left = left_joycon.get_status()
status_right = right_joycon.get_status()

def run_dynamic_control(drone, left_joycon, right_joycon, sock, drone_ip, drone_port):
    DEADZONE = 256
    last_states = {
        "roll": 0,
        "pitch": 0,
        "yaw": 0,
        "climb": 0,
        "buttons": set(),  # Tracks the last state of buttons
    }
    calibrate_takeoff = False

    try:
        while True:
            # Reading stick inputs and applying deadzone
            roll = right_joycon.get_stick_right_horizontal() / 32767.0  # Right stick X-axis for roll
            pitch = right_joycon.get_stick_right_vertical() / 32767.0  # Right stick Y-axis for pitch
            yaw = left_joycon.get_stick_left_horizontal() / 32767.0    # Left stick X-axis for yaw
            climb = left_joycon.get_stick_left_vertical() / 32767.0    # Left stick Y-axis for climb
            if abs(roll) < DEADZONE / 32767.0:
                roll = 0
            if abs(pitch) < DEADZONE / 32767.0:
                pitch = 0
            if abs(yaw) < DEADZONE / 32767.0:
                yaw = 0
            if abs(climb) < DEADZONE / 32767.0:
                climb = 0

            # Detect joystick movements
            if (roll, pitch, yaw, climb) != (last_states["roll"], last_states["pitch"], last_states["yaw"], last_states["climb"]):
                print(f"Joystick Movement - Roll: {roll:.2f}, Pitch: {pitch:.2f}, Yaw: {yaw:.2f}, Climb: {climb:.2f}")
                last_states.update({"roll": roll, "pitch": pitch, "yaw": yaw, "climb": climb})

            # Update the drone's control vectors
            drone.set_pitch_roll_vec(pitch, roll)
            drone.set_yaw_climb_vec(yaw, climb)

            # Track currently pressed buttons
            pressed_buttons = set()

            # Left Joy-Con button actions
            if left_joycon.get_button_up():
                drone.trim_forward()
                pressed_buttons.add("Trim Forward")
            if left_joycon.get_button_down():
                drone.trim_aft()
                pressed_buttons.add("Trim Aft")
            if left_joycon.get_button_left():
                drone.trim_left()
                pressed_buttons.add("Trim Left")
            if left_joycon.get_button_right():
                drone.trim_right()
                pressed_buttons.add("Trim Right")

            # Speed adjustment on left Joy-Con
            if left_joycon.get_button_l():
                drone.next_speed()
                pressed_buttons.add("Next Speed")

            # Right Joy-Con button actions
            if right_joycon.get_button_r():
                drone.flip()
                pressed_buttons.add("Flip")

            # Emergency stop on right Joy-Con
            if right_joycon.get_button_plus():
                drone.stop()
                pressed_buttons.add("Emergency Stop")


           

            if right_joycon.get_button_home():  # Example: Home button for takeoff
                drone.takeoff()
                pressed_buttons.add("Takeoff")

            if left_joycon.get_button_zl():  # Example: Home button on left Joy-Con for landing
                drone.land()
                pressed_buttons.add("Landing")


            # Print button actions only if new buttons are pressed
            new_buttons = pressed_buttons - last_states["buttons"]
            if new_buttons:
                print(f"Button Pressed: {', '.join(new_buttons)}")
            last_states["buttons"] = pressed_buttons

            # Send the control message to the drone
            m = drone.next_message()
            sock.sendto(m.to_protocol(), (drone_ip, drone_port))
            time.sleep(0.02)

    except KeyboardInterrupt:
        pass