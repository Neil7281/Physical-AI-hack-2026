import ikpy.chain
import numpy as np
import time
import serial

# 1. Load the robot model from your URDF
# We define the active links mask (6 motors + base)
# Adjust the 'False/True' list based on how many joints are in your specific URDF
my_chain = ikpy.chain.Chain.from_urdf_file("so101_new_calib.urdf")

def calculate_ik_trajectory(start_xyz, goal_xyz, steps=20):
    """
    Generates a list of joint angles to move from start to goal position.
    """
    trajectory = []
    
    # Linear interpolation between start and goal in 3D space
    for i in range(steps + 1):
        alpha = i / steps
        # Calculate intermediate (x, y, z) waypoint
        current_target = (1 - alpha) * np.array(start_xyz) + alpha * np.array(goal_xyz)
        
        # Calculate joint angles for this point
        # 'initial_position' helps the solver find the smoothest movement
        joint_angles = my_chain.inverse_kinematics(current_target)
        trajectory.append(joint_angles)
        
    return trajectory

"""def send_to_waveshare(joint_angles, ser):
    
    Converts radians to servo units (0-4095) and sends serial packets.
    
    # Offset and mapping depend on your physical calibration
    for i, angle in enumerate(joint_angles[1:7]): # Skip base link
        servo_id = i + 1
        # Example conversion: center (0 rad) is 2048, range is ~0.088 deg per unit
        position = int(2048 + (angle * (4096 / (2 * np.pi))))
        position = max(0, min(4095, position)) # Safety clamp
        
        # Basic Waveshare/Feetech WRITE packet structure
        # [0xFF, 0xFF, ID, Length, Instruction, Address, LowByte, HighByte, Checksum]
        # (Using a simple direct-write for testing)
        packet = bytearray([0xFF, 0xFF, servo_id, 0x07, 0x03, 0x2A, 
                           position & 0xFF, (position >> 8) & 0xFF, 0, 0])
        # Note: You must calculate the proper checksum here for the motor to move!
        ser.write(packet) """


def send_to_waveshare(joint_angles, ser):
    for i, angle in enumerate(joint_angles[1:7]):
        servo_id = i + 1
        position = int(2048 + (angle * (4096 / (2 * np.pi))))
        position = max(0, min(4095, position))
        
        # Structure: [Header, Header, ID, Length, Instruction, Address, Params..., Checksum]
        # Length = 7 (Instruction(1) + Address(1) + Params(4) + Checksum(1))
        p = [servo_id, 0x07, 0x03, 0x2A, position & 0xFF, (position >> 8) & 0xFF, 0, 0]
        checksum = ~(sum(p) & 0xFF) & 0xFF
        
        packet = bytearray([0xFF, 0xFF] + p[:-1] + [checksum])
        ser.write(packet)

# Main Execution Flow
if __name__ == "__main__":
    # Initialize Serial Port (COM on Windows, /dev/ttyUSB0 on Linux)
    # The Waveshare board usually defaults to 1,000,000 baud
    with serial.Serial('/dev/ttyUSB0', 1000000, timeout=1) as ser:
        start_pos = [0.1, 0.0, 0.1] # [X, Y, Z] in meters
        goal_pos = [0.2, 0.1, 0.15]
        
        traj = calculate_ik_trajectory(start_pos, goal_pos)
        for waypoint in traj:
            send_to_waveshare(waypoint, ser)
            time.sleep(0.05) # 50ms delay for smooth motion