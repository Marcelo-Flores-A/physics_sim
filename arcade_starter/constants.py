"""
Constants Module

This module contains all shared constants used across the physics simulation.
Centralizing constants here ensures consistency and makes configuration easier.
"""

# Physics Constants
BALL_RADIUS = 16 # pixels
OBJECT_INITIAL_SPEED_X = 100.0
OBJECT_INITIAL_ANGULAR_SPEED = 500.0
GRAVITY = -980.0  # pixels/second²
OBJECT_MASS = 1.0
OBJECT_ELASTICITY = 0.5
FRICTION_COEFFICIENT = 0.1

# Player/Bar Constants 
BAR_WIDTH = 700
BAR_HEIGHT = 16
BAR_MASS = 1.0
BAR_SPEED = 400.0
BAR_POSITION_Y = 200

# Display Constants
WIDTH = 960
HEIGHT = 540
TITLE = "Arcade Starter - Experiments"

# Game States
MENU_STATE = 0
SIMULATION_STATE = 1
OPTIONS_STATE = 2
