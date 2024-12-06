import struct
import functools

def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))

class ControlMessage:
    def __init__(self, climb=0, roll=0, pitch=0, yaw=0, pitchTrim=0, rollTrim=0, yawTrim=0, 
                 speed=0, noHead=False, propLock=False, flip=False, takeoff=False, land=False, calibrate=False):
        self.climb = climb
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw
        self.pitchTrim = pitchTrim
        self.rollTrim = rollTrim
        self.yawTrim = yawTrim
        self.speed = speed
        self.noHead = noHead
        self.propLock = propLock
        self.flip = flip
        self.takeoff = takeoff
        self.land = land
        self.calibrate = calibrate

    @staticmethod
    def pack_bigvec(f):
        return int(round((f / 2 + 0.5) * 255))

    @staticmethod
    def unpack_bigvec(b):
        return (b / 255.0 - 0.5) * 2

    @staticmethod
    def pack_smallvec(f):
        return int(round((f / 2 + 0.5) * 127))

    @staticmethod
    def unpack_smallvec(b):
        return (b / 127.0 - 0.5) * 2

    @staticmethod
    def pack_trim(t):
        return t + 16

    @staticmethod
    def unpack_trim(b):
        return b - 16

    def to_protocol(self):
        field = bytearray(11)
        field[0] = 0xFF
        field[1] = 0x08
        field[2] = self.pack_bigvec(self.climb)
        field[3] = self.pack_smallvec(self.yaw)
        field[4] = self.pack_smallvec(self.pitch)
        field[5] = self.pack_smallvec(self.roll)
        field[6] = self.pack_trim(self.yawTrim) | (self.calibrate << 6) | (1 << 7)
        field[7] = self.pack_trim(self.pitchTrim)
        field[8] = self.pack_trim(self.rollTrim)
        field[9] = self.speed | (self.flip << 2) | (self.noHead << 4) | (self.propLock << 5) | (self.takeoff << 6) | (self.land << 7)
        field[10] = 255 - (sum(field[1:10]) % 256)
        return field

    @classmethod
    def from_proto(clazz, field, ignoreChecksum = False):
        assert ignoreChecksum or field[10] == 255 - (sum(field[1:10]) % 256), "checksum fail"
        m = ControlMessage()
        m.climb = m.unpack_bigvec(field[2])
        m.yaw = m.unpack_smallvec(field[3])
        m.pitch = m.unpack_smallvec(field[4])
        m.roll = m.unpack_smallvec(field[5])
        m.yawTrim = m.unpack_trim(field[6] & 0b00011111)
        m.calibrate = (field[6] & 1<<6) != 0
        m.pitchTrim = m.unpack_trim(field[7])
        m.rollTrim = m.unpack_trim(field[8])
        m.speed = field[9] & 0b11
        m.flip = (field[9] & 1<<2) != 0
        m.noHead = (field[9] & 1<<4) != 0
        m.propLock = (field[9] & 1<<5) != 0
        m.takeoff = (field[9] & 1<<6) != 0
        m.land = (field[9] & 1<<7) != 0
        return m


    def __str__(self):
        return "climb: {}\npitch: {}\nroll: {}\nyaw: {}\npitch trim: {}\nroll trim: {}\nyaw trim: {}\nspeed: {}\ncalibrate: {}\nflip: {}\nno head: {}\nprop lock: {}\ntakeoff: {}\nland: {}".format(
        self.climb, self.pitch, self.roll, self.yaw,
        self.pitchTrim, self.rollTrim, self.yawTrim,
        self.speed, self.calibrate, self.flip, self.noHead, self.propLock, self.takeoff, self.land
        )

class Drone:
    def __init__(self):
        self.pitch_trim = 0
        self.roll_trim = 0
        self.yaw_trim = 0
        self.pitch = 0
        self.roll = 0
        self.yaw = 0
        self.climb = 0
        self.speed = 0
        self.action_timers = dict()
        self.action_callbacks = set()

    def register_callback(self, callback):
        self.action_callbacks.add(callback)

    def unregister_callback(self, callback):
        self.action_callbacks.remove(callback)

    def fire_callbacks(self, event, data):
        for cb in self.action_callbacks:
            cb(event, data)

    def set_pitch_roll_vec(self, pitch, roll, invert_pitch=True):
        self.pitch = min(1, max(-1, pitch)) * (-1 if invert_pitch else 1)
        self.roll = min(1, max(-1, roll))

    def set_yaw_climb_vec(self, yaw, climb):
        self.yaw = min(1, max(-1, yaw))
        self.climb = min(1, max(-1, climb))

    def trim_left(self):
        if self.roll_trim > -16:
            self.roll_trim-=1

    def trim_right(self):
        if self.roll_trim < 15:
            self.roll_trim+=1

    def trim_forward(self):
        if self.pitch_trim < 15:
            self.pitch_trim+=1

    def trim_aft(self):
        if self.pitch_trim > -16:
            self.pitch_trim-=1

    def takeoff(self):
        self.action_timers["takeoff"] = 50

    def land(self):
        self.action_timers["land"] = 50

    def stop(self):
        self.action_timers["propLock"] = 50

    def flip(self):
        self.action_timers["flip"] = 50
    
    def calibrate(self):
        self.action_timers["calibrate"] = 50

    def next_speed(self):
        self.speed = (self.speed+1) % 3

    def attitude_hold(self):
        self.pitch = 0
        self.roll = 0
        self.yaw = 0
        self.climb = 0


    def next_message(self):
        action_args = {}
        for key in list(self.action_timers.keys()):
            self.action_timers[key] -= 1
            if self.action_timers[key] == 0:
                self.fire_callbacks("action_end", key)
                del self.action_timers[key]
            else:
                action_args[key] = True

        return ControlMessage(
            pitch=self.pitch,
            roll=self.roll,
            yaw=self.yaw,
            climb=self.climb,
            pitchTrim = self.pitch_trim,
            rollTrim = self.roll_trim,
            yawTrim = self.yaw_trim,
            speed = self.speed,
            **action_args
        )

    # def send_control_message(self, sender, message):
    #     packet = message.to_protocol()
    #     sender.send_command(packet.decode('latin1'))
