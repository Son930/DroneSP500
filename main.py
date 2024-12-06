import threading
# from connection_manager import ConnectionManager
from command_sender import CommandSender
from data_receiver import DataReceiver
from drone_control import Drone, ControlMessage
from pyjoycon import JoyCon, get_L_id, get_R_id
import socket
from joycon_controller import run_dynamic_control
import time

def receive_data_handler(data_receiver):
    data_receiver.receive_data()  # Assuming `receive_data` processes incoming data.

def send_drone_commands(drone, sender):
    while True:
        command = input("Enter a command (type 'exit' to quit): ")

        if command == "exit":
            break

        if command == "takeoff":
            drone.takeoff()
        elif command == "land":
            drone.land()
        elif command == "stop":
            drone.stop()
        elif command == "flip":
            drone.flip()
        elif command == "calibrate":
            drone.calibrate()
        elif command == "speed":
            drone.next_speed()
        elif command == "attitudeHold":
            drone.attitude_hold()
        else:
            print(f"Unknown command: {command}")
            continue

        message = drone.next_message()
        drone.send_control_message(sender, message)



def predefined_test(sock):
    pt = -2
    rt = 3
    messages = \
        [ControlMessage()] * 200 \
        + [ControlMessage(calibrate=True)] * 50 \
        + [ControlMessage()] * 100 \
        + [ControlMessage(takeoff=True)] * 50 \
        + [ControlMessage(pitchTrim=pt, rollTrim=rt)] * 200 \
        + [ControlMessage(pitchTrim=pt, rollTrim=rt, roll=-0.5)] * 20 \
        + [ControlMessage(pitchTrim=pt, rollTrim=rt)] * 25 \
        + [ControlMessage(pitchTrim=pt, rollTrim=rt, roll=0.3)] * 20 \
        + [ControlMessage(pitchTrim=pt, rollTrim=rt)] * 100 \
        + [ControlMessage(pitchTrim=pt, rollTrim=rt, roll=0.5)] * 20 \
        + [ControlMessage(pitchTrim=pt, rollTrim=rt)] * 25 \
        + [ControlMessage(pitchTrim=pt, rollTrim=rt, roll=-0.3)] * 20 \
        + [ControlMessage(pitchTrim=pt, rollTrim=rt)] * 100 \
        + [ControlMessage(pitchTrim=pt, rollTrim=rt, pitch=-0.5)] * 20 \
        + [ControlMessage(pitchTrim=pt, rollTrim=rt)] * 25 \
        + [ControlMessage(pitchTrim=pt, rollTrim=rt, pitch=0.3)] * 20 \
        + [ControlMessage(pitchTrim=pt, rollTrim=rt)] * 100 \
        + [ControlMessage(pitchTrim=pt, rollTrim=rt, pitch=0.5)] * 20 \
        + [ControlMessage(pitchTrim=pt, rollTrim=rt)] * 25 \
        + [ControlMessage(pitchTrim=pt, rollTrim=rt, pitch=-0.3)] * 20 \
        + [ControlMessage(pitchTrim=pt, rollTrim=rt)] * 100 \
        + [ControlMessage(pitchTrim=pt, rollTrim=rt, climb=0.7)] * 15 \
        + [ControlMessage(pitchTrim=pt, rollTrim=rt)] * 200 \
        + [ControlMessage(pitchTrim=pt, rollTrim=rt, climb=-1)] * 15 \
        + [ControlMessage(pitchTrim=pt, rollTrim=rt)] * 200 \
        + [ControlMessage(pitchTrim=pt, rollTrim=rt, yaw=1)] * 100 \
        + [ControlMessage(pitchTrim=pt, rollTrim=rt)] * 200 \
        + [ControlMessage(pitchTrim=pt, rollTrim=rt, land=True)] * 50 \
        + [ControlMessage(pitchTrim=pt, rollTrim=rt)] * 500

    for m in messages:
        sock.sendto(m.to_protocol(), ("172.16.10.1", 8080))
        time.sleep(.02)





    
if __name__ == "__main__":
    drone_ip = "172.16.10.1"  
    drone_port = 8888         

    # udp
    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # tcp
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    left_joycon_id = get_L_id()
    right_joycon_id = get_R_id()
    left_joycon = JoyCon(*left_joycon_id)
    right_joycon = JoyCon(*right_joycon_id)

    
    print(f"Connected Joy-Cons: Left {left_joycon_id}, Right {right_joycon_id}")

   
    drone = Drone()
    m = drone.next_message()
    print(m)
    # sock.sendto(m.to_protocol(), (drone_ip, drone_port))

    sock.connect((drone_ip, drone_port))
    sock.send(m.to_protocol())

   

    run_dynamic_control(drone, left_joycon, right_joycon, sock, drone_ip, drone_port)
    # run_dynamic_control(drone, left_joycon, right_joycon )



    
    time.sleep(.02)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting program.")

    
    sock.close()
    print("Disconnected from drone. Exiting.")
