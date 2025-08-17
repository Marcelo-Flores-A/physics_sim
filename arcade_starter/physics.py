"""
Physics Module

This module contains the physics calculations and logic
for objects in the simulation.
"""

import arcade
from typing import Tuple

BAR_MASS = 1.0
BAR_SPEED = 400.0
OBJECT_MASS = 1.0
OBJECT_INITIAL_SPEED_X = 100.0
GAVITY = -980.0 # pixels/second²
FRICTION_COEFICIENT = 0.1

class PhysicsObject:
    """A physics-enabled object with position, velocity, and collision detection."""
    
    def __init__(self, sprite: arcade.Sprite, mass: float = OBJECT_MASS, velocity_x: float = OBJECT_INITIAL_SPEED_X, acceleration_x: float = 0.0, velocity_y: float = 0.0, acceleration_y: float = GAVITY):
        self.sprite = sprite
        self.mass = mass
        self.velocity_x = velocity_x
        self.acceleration_x = acceleration_x
        self.velocity_y = velocity_y
        self.acceleration_y = acceleration_y
    
    def update_physics(self, delta_time: float, world_width: int, world_height: int):
        """Update physics for this object."""
        # Get distances from borders of object to its center
        half_w = self.sprite.width / 2
        half_h = self.sprite.height / 2

        # Calculate horizontal movement
        self.velocity_x += self.acceleration_x * delta_time
        dx = self.velocity_x * delta_time
        # Calculate vertical movement
        self.velocity_y += self.acceleration_y * delta_time
        dy = self.velocity_y * delta_time

        # Update position
        new_x = self.sprite.center_x + dx
        new_y = self.sprite.center_y + dy

        # Bounce off floor for y direction
        if new_y <= half_h:
            self.velocity_y = -0.5 * self.velocity_y
            new_y = max(half_h, new_y)
            # Update x movement due to floor's friction
            self.velocity_x -= (1 if self.velocity_x > 0 else -1) * FRICTION_COEFICIENT * abs(GAVITY) * delta_time

        # Bounce off walls for x direction
        if new_x <= half_w or new_x >= world_width - half_w:
            self.velocity_x = -self.velocity_x
            new_x = max(half_w, min(world_width - half_w, new_x))
        
        # Clamp to window bounds
        self.sprite.center_x = new_x
        self.sprite.center_y = max(half_h, min(world_height - half_h, new_y))


class PlayerController:
    """Handles player input and movement for controllable objects."""
    
    def __init__(self, sprite: arcade.Sprite, mass: float = BAR_MASS, rotation_speed: float = BAR_SPEED):
        self.sprite = sprite
        self.mass = mass
        self.rotation_speed = rotation_speed
    
    def update_movement(self, delta_time: float, keys: set, world_width: int):
        """Update player-controlled movement."""
        # Get distances from borders of sprite to its center
        half_w = self.sprite.width / 2
        
        # Player control for sprite's x position
        self.sprite.change_angle = (("clockwise" in keys) - ("counter-clockwise" in keys)) * self.rotation_speed

        # Update bar's new tilt angle
        self.sprite.angle += self.sprite.change_angle * delta_time


class PhysicsEngine:
    """Main physics engine that manages all physics objects and controllers."""
    
    def __init__(self):
        self.physics_objects = []
        self.player_controllers = []
    
    def add_physics_object(self, physics_object: PhysicsObject):
        """Add a physics object to be managed by the engine."""
        self.physics_objects.append(physics_object)
    
    def add_player_controller(self, player_controller: PlayerController):
        """Add a player controller to be managed by the engine."""
        self.player_controllers.append(player_controller)
    
    def check_collision(self, sprite1: arcade.Sprite, sprite2: arcade.Sprite) -> bool:
        """Check if two sprites are colliding using bounding box collision detection."""
        # Get half dimensions for each sprite
        half_w1, half_h1 = sprite1.width / 2, sprite1.height / 2
        half_w2, half_h2 = sprite2.width / 2, sprite2.height / 2
        
        # Calculate distance between centers
        dx = abs(sprite1.center_x - sprite2.center_x)
        dy = abs(sprite1.center_y - sprite2.center_y)
        
        # Check if sprites overlap
        return dx < (half_w1 + half_w2) and dy < (half_h1 + half_h2)
    
    def handle_collision(self, physics_obj: PhysicsObject, controller: PlayerController):
        """Handle collision between a physics object and a player-controlled object."""
        # Calculate collision normal based on relative positions
        dx = physics_obj.sprite.center_x - controller.sprite.center_x
        dy = physics_obj.sprite.center_y - controller.sprite.center_y
        
        # Determine collision side based on which axis has smaller overlap
        sprite1, sprite2 = physics_obj.sprite, controller.sprite
        half_w1, half_h1 = sprite1.width / 2, sprite1.height / 2
        half_w2, half_h2 = sprite2.width / 2, sprite2.height / 2
        
        # Calculate overlap on each axis
        x_overlap = (half_w1 + half_w2) - abs(dx)
        y_overlap = (half_h1 + half_h2) - abs(dy)
        
        # Resolve collision based on smallest overlap
        if x_overlap < y_overlap:
            # Horizontal collision - reverse x velocity
            physics_obj.velocity_x = -physics_obj.velocity_x
            # Separate sprites horizontally
            if dx > 0:
                physics_obj.sprite.center_x = controller.sprite.center_x + half_w2 + half_w1
            else:
                physics_obj.sprite.center_x = controller.sprite.center_x - half_w2 - half_w1
        else:
            # Vertical collision - reverse y velocity with some energy loss
            physics_obj.velocity_y = -physics_obj.velocity_y * 0.8
            # Separate sprites vertically
            if dy > 0:
                physics_obj.sprite.center_y = controller.sprite.center_y + half_h2 + half_h1
            else:
                physics_obj.sprite.center_y = controller.sprite.center_y - half_h2 - half_h1
            
            # Add some horizontal velocity based on where the ball hit the bar
            # This makes the game more interesting by allowing the player to influence ball direction
            bar_center = controller.sprite.center_x
            ball_center = physics_obj.sprite.center_x
            hit_position = (ball_center - bar_center) / (controller.sprite.width / 2)  # -1 to 1
            physics_obj.velocity_x += hit_position * 200  # Add velocity based on hit position
    
    def update(self, delta_time: float, keys: set, world_width: int, world_height: int):
        """Update all physics objects and player controllers."""
        # Update physics objects
        for physics_obj in self.physics_objects:
            physics_obj.update_physics(delta_time, world_width, world_height)
        
        # Update player controllers
        for controller in self.player_controllers:
            controller.update_movement(delta_time, keys, world_width)
        
        # Check for collisions between physics objects and player controllers
        for physics_obj in self.physics_objects:
            for controller in self.player_controllers:
                if self.check_collision(physics_obj.sprite, controller.sprite):
                    self.handle_collision(physics_obj, controller)
    
    def reset_physics_object(self, index: int, x: float, y: float, velocity_x: float = 0.0, velocity_y: float = 0.0):
        """Reset a physics object to initial state."""
        if 0 <= index < len(self.physics_objects):
            physics_obj = self.physics_objects[index]
            physics_obj.sprite.center_x = x
            physics_obj.sprite.center_y = y
            physics_obj.velocity_x = velocity_x
            physics_obj.velocity_y = velocity_y
    
    def reset_player_controller(self, index: int, x: float, y: float):
        """Reset a player controller to initial position."""
        if 0 <= index < len(self.player_controllers):
            controller = self.player_controllers[index]
            controller.sprite.center_x = x
            controller.sprite.center_y = y
