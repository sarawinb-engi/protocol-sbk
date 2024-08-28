import numpy as np
import matplotlib.pyplot as plt

class PIDController:
    def __init__(self, Kp, Ki, Kd, setpoint, sample_time):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.sample_time = sample_time
        self.clear()

    def clear(self):
        self.current_time = None
        self.last_time = None
        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0
        self.int_error = 0.0
        self.output = 0.0

    def update(self, feedback_value, current_time):
        error = self.setpoint - feedback_value
        delta_time = current_time - self.last_time if self.last_time is not None else self.sample_time
        delta_error = error - self.last_error if self.last_error is not None else 0.0

        self.PTerm = self.Kp * error
        self.ITerm += error * delta_time

        if delta_time > 0:
            self.DTerm = delta_error / delta_time

        self.last_time = current_time
        self.last_error = error

        self.output = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)

        return self.output

def vsd_control(pid_output):
    max_frequency = 50  # Max frequency of VSD in Hz
    frequency = np.clip(pid_output, 0, max_frequency)
    return frequency

def calculate_velocity(frequency):
    velocity = frequency * 0.1  # Simulated effect of frequency on velocity
    return velocity

def calculate_position(velocity, position, dt):
    new_position = position + velocity * dt
    return new_position

# Simulation parameters
setpoint = 10  # Desired position in meters
initial_position = 0  # Initial position in meters
initial_velocity = 0  # Initial velocity in meters/second
time_steps = np.linspace(0, 100, 1000)
sample_time = time_steps[1] - time_steps[0]

# PID controller initialization
pid = PIDController(Kp=2.0, Ki=0.1, Kd=0.05, setpoint=setpoint, sample_time=sample_time)

# Data storage for plotting
positions = []
velocities = []
frequencies = []

# Initial conditions
position = initial_position
velocity = initial_velocity

# Simulation loop
for t in time_steps:
    # Update PID controller with current position
    pid_output = pid.update(position, t)
    
    # VSD control to get frequency
    frequency = vsd_control(pid_output)
    
    # Calculate new velocity based on VSD frequency
    velocity = calculate_velocity(frequency)
    
    # Calculate new position based on velocity
    position = calculate_position(velocity, position, sample_time)
    
    # Store data for plotting
    positions.append(position)
    velocities.append(velocity)
    frequencies.append(frequency)

# Plotting the results
plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.plot(time_steps, positions, label='Position (m)')
plt.axhline(setpoint, color='r', linestyle='--', label='Setpoint')
plt.title('Position Control with PID and VSD')
plt.xlabel('Time')
plt.ylabel('Position (m)')
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(time_steps, velocities, label='Velocity (m/s)', color='g')
plt.title('Velocity Response')
plt.xlabel('Time')
plt.ylabel('Velocity (m/s)')
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(time_steps, frequencies, label='VSD Frequency (Hz)', color='b')
plt.title('VSD Frequency Response')
plt.xlabel('Time')
plt.ylabel('Frequency (Hz)')
plt.legend()

plt.tight_layout()
plt.show()
