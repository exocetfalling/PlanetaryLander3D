# Imports

import math
from typing import cast
import pygame
import pygame.freetype  # Import the freetype module.

# Variables

# Polar coordinates as as commonly used in physics (ISO 80000-2:2019 convention): 
# radial distance r (distance to origin), 
# polar angle theta (angle with respect to polar axis), 
# azimuthal angle phi (angle of rotation from the initial meridian plane).

l_theta_deg = 0
l_theta_rad = 0
l_phi_deg = 0
l_phi_rad = 0
l_radial_velocity = 0

l_accel_x = 0
l_accel_y = 0
l_accel_z = 0

l_x_velocity = 0
l_y_velocity = 0
l_z_velocity = 0

l_total_velocity = 0

l_angular_accel_x = 0
l_angular_accel_y = 0
l_angular_accel_z = 0

l_angular_vel_x = 0
l_angular_vel_y = 0
l_angular_vel_z = 0

l_angular_displacement_x = 0
l_angular_displacement_y = 0
l_angular_displacement_z = 0

l_alt = 0

l_pitch_rad = 0
l_roll_rad = 0
l_yaw_rad = 0

l_thrust_force = 0

# Axes are defined as:
# For lander:
# X: left -ve, right +ve
# Y: aft -ve, forward +ve
# Z: down -ve, up +ve

# For world:
# X: west -ve, east +ve
# Y: south -ve, north +ve
# Z: down -ve, up +ve

w_x_velocity = 0
w_y_velocity = 0
w_z_velocity = 0

w_vec_velocity = [0, 0, 0]

w_x_pos = 0
w_y_pos = 0
w_z_pos = 0

w_vec_pos = [0, 0, 0]

# Masses in kg
c_mass_dry_lander = 1000
c_mass_wet_lander = 2000

# Lengths in m
c_radius_lander = 5

# MOIs in kg m^2
l_moi_x = 0
l_moi_y = 0
l_moi_z = 0

l_accel_x_grav = 0
l_accel_y_grav = 0
l_accel_z_grav = 0

pygame.init()
SIZE = WIDTH, HEIGHT = (1024, 720)
FPS = 60
screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
clock = pygame.time.Clock()

# Functions
def Calc_Velocity_World(axis, total_vel, angle_azimuthal, angle_polar): 
    if axis == 'x':
        return (total_vel * math.sin(angle_azimuthal)) * math.sin(angle_polar)
    if axis == 'y':
        return (total_vel * math.cos(angle_azimuthal)) * math.sin(angle_polar)
    if axis == 'z':
        return (total_vel * math.cos(angle_azimuthal))

def Calc_Velocity_Total_Magnitude(vel_x, vel_y, vel_z):
    return math.sqrt(math.sqrt((pow(vel_x, 2) + pow(vel_y, 2))) + pow(vel_z, 2))

def Calc_Force_Angular_Acc(moi, force_magnitude, distance_from_pivot):
    return force_magnitude * distance_from_pivot / moi

def Calc_Angular_Vel():
    pass

def Calc_MOI(axis, mass, radius):
    if (axis =='x'):
        return 2/5 * mass * math.pow(radius, 2)
    if (axis =='y'):
        return 2/5 * mass * math.pow(radius, 2)
    if (axis =='z'):
        return 2/5 * mass * math.pow(radius, 2)

def Calc_Force_Acc(force_magnitude, mass_kg):
    return force_magnitude / mass_kg

def Calc_Integral(value, time_interval):
    return value * time_interval

def Calc_Acc_Gravity(axis, angle_roll, angle_pitch):
    if (axis == 'x'):
        return -9.8065 * math.sin(angle_roll)
    if (axis == 'y'):
        return -9.8065 * math.sin(angle_pitch)
    if (axis == 'z'):
        return -9.8065 * math.cos(angle_pitch)

def Convert_Angle_Rad_To_Deg(angle_rad):
    return angle_rad * 57.2958

def Convert_Angle_Deg_To_Rad(angle_deg):
    return angle_deg / 57.2958

def blit_text(surface, text, pos, font, color=pygame.Color('green')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.



font = pygame.font.SysFont('Courier', 16)

while True:

    dt = clock.tick(FPS) / 1000
    debug_text = \
        '\nX Vel: ' + str(round(l_x_velocity, 2)) + \
        '\nY Vel: ' + str(round(l_y_velocity, 2)) + \
        '\nZ Vel: ' + str(round(l_z_velocity, 2)) + \
        '\nTotal: ' + str(round(l_total_velocity, 2)) + \
        '\nTHETA: ' + str(round(l_thetl_deg, 2)) + \
        '\nPHI: ' + str(round(l_phi_deg, 2)) + \
        '\nPITCH: ' + str(round(Convert_Angle_Rad_To_Deg(l_pitch_rad), 2)) + \
        '\nROLL: ' + str(round(Convert_Angle_Rad_To_Deg(l_roll_rad), 2))
    l_phi_deg = (l_phi_deg + 360) % 360
    l_thetl_deg = (l_thetl_deg + 360) % 360

    l_phi_rad = Convert_Angle_Deg_To_Rad(l_phi_deg)
    l_thetl_rad = Convert_Angle_Deg_To_Rad(l_thetl_deg)

    l_pitch_rad = l_angular_displacement_x
    l_roll_rad = l_angular_displacement_y

    l_accel_x = \
        Calc_Acc_Gravity('x', l_roll_rad, l_pitch_rad)
    l_accel_y = \
        Calc_Acc_Gravity('y', l_roll_rad, l_pitch_rad)
    l_accel_z = \
        Calc_Acc_Gravity('z', l_roll_rad, l_pitch_rad)

    l_x_velocity = l_x_velocity + Calc_Integral(l_accel_x, dt)
    l_y_velocity = l_y_velocity + Calc_Integral(l_accel_y, dt)
    l_z_velocity = l_z_velocity + Calc_Integral(l_accel_z, dt)

    # l_total_velocity = Calc_Velocity_Total_Magnitude(l_x_velocity, l_y_velocity, l_z_velocity)
    l_total_velocity = math.hypot(l_x_velocity, l_y_velocity, l_z_velocity)

    l_angular_accel_x = \
        Calc_Force_Angular_Acc('x', 0, 0)
    l_angular_accel_y = \
        Calc_Force_Angular_Acc('y', 0, 0)
    l_angular_accel_z = \
        Calc_Force_Angular_Acc('z', 0, 0)

    l_angular_vel_x = l_angular_vel_x + Calc_Integral(l_angular_accel_x, dt)
    l_angular_vel_y = l_angular_vel_y + Calc_Integral(l_angular_accel_y, dt)
    l_angular_vel_z = l_angular_vel_z + Calc_Integral(l_angular_accel_z, dt)

    l_angular_displacement_x = l_angular_displacement_x + Calc_Integral(l_angular_vel_x, dt)
    l_angular_displacement_y = l_angular_displacement_y + Calc_Integral(l_angular_vel_y, dt)
    l_angular_displacement_z = l_angular_displacement_z + Calc_Integral(l_angular_vel_z, dt)

    # l_angular_displacement_x = ((l_angular_displacement_x + (2 * math.pi)) % (2 * math.pi)) - (math.pi)

    w_x_velocity = Calc_Velocity_World('x', l_total_velocity, l_phi_rad, l_thetl_rad)
    w_y_velocity = Calc_Velocity_World('y', l_total_velocity, l_phi_rad, l_thetl_rad)
    w_z_velocity = Calc_Velocity_World('z', l_total_velocity, l_roll_rad, l_thetl_rad)

    w_vec_velocity = [w_x_velocity, w_y_velocity, w_z_velocity]

    w_x_pos = w_x_pos + w_x_velocity * dt
    w_y_pos = w_y_pos + w_y_velocity * dt
    w_z_pos = w_z_pos + w_z_velocity * dt

    keys=pygame.key.get_pressed()

    if keys[pygame.K_w]:
        l_angular_vel_x = -math.pi/30

    if keys[pygame.K_s]:
        l_angular_vel_x =  math.pi/30

    if keys[pygame.K_a]:
        l_angular_vel_y = -math.pi/30

    if keys[pygame.K_d]:
        l_angular_vel_y =  math.pi/30

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    screen.fill(pygame.Color('black'))
    blit_text(screen, debug_text, (20, 20), font)
    pygame.display.update()
