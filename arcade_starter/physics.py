"""
Physics Module

This module contains the physics calculations and logic
for objects in the simulation.
"""

import arcade
from typing import Tuple
import math

BAR_MASS = 1.0
BAR_SPEED = 400.0
OBJECT_MASS = 1.0
OBJECT_INITIAL_SPEED_X = 100.0
GAVITY = -980.0 # pixels/second²
FRICTION_COEFICIENT = 0.1
OBJECT_ELASTICITY = 0.5

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
            self.velocity_y = -OBJECT_ELASTICITY * self.velocity_y
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

    def handle_collision(self, delta_time: float, physics_obj: PhysicsObject, controller: PlayerController):
        """Handle collision between a physics object (circle) and a player-controlled object (rectangle)."""
        
        # Get the bar's angle in radians
        bar_angle_rad = math.radians(controller.sprite.angle)
        cos_angle = math.cos(bar_angle_rad)
        sin_angle = math.sin(bar_angle_rad)

        # Vector from bar's center to circle's center
        dx = physics_obj.sprite.center_x - controller.sprite.center_x
        dy = physics_obj.sprite.center_y - controller.sprite.center_y
        
        # Transform circle position to bar's local coordinates
        #
        # Given a vector d = dxi + dyj that is rotated by an 
        # angle α, it's represented by d' such that: d' = d * Tr
        #  
        #         where d' is the rotated vector
        #               d is the original vector
        #               Tr is the matrix of rotation
        #
        # Tr would then be
        #                     _             _
        #                    | Cos(α) -Sin(α)|
        #               Tr = | Sin(α)  Cos(α)|
        #                    |_             _|
        
        local_x = dx * cos_angle - dy * sin_angle  # Along bar's length
        local_y = dx * sin_angle + dy * cos_angle  # Perpendicular to bar

        # Distance from center to borders of sprites
        bar_half_width = controller.sprite.width / 2
        bar_half_height = controller.sprite.height / 2
        circle_radius = physics_obj.sprite.width / 2

        # Find the closest point on the rectangle to the circle's center
        closest_x = max(-bar_half_width, min(bar_half_width, local_x))
        closest_y = max(-bar_half_height, min(bar_half_height, local_y))

        # Calculate the collision normal in local space
        normal_x = local_x - closest_x
        normal_y = local_y - closest_y
        
        # Normalize the collision normal
        normal_length = math.sqrt(normal_x * normal_x + normal_y * normal_y)
        if normal_length > 0:
            normal_x /= normal_length
            normal_y /= normal_length
        else:
            # Circle center is inside rectangle, use perpendicular distance to edges
            if abs(local_x) / bar_half_width > abs(local_y) / bar_half_height:
                # Closer to left/right edge
                normal_x = 1.0 if local_x > 0 else -1.0
                normal_y = 0.0
            else:
                # Closer to top/bottom edge
                normal_x = 0.0
                normal_y = 1.0 if local_y > 0 else -1.0

        # Transform normal back to world coordinates
        #
        # Given a vector d' = dx'i + dy'j that has been rotated by an 
        # angle α, it's represented by d such that: d = d' * inv(Tr)
        #  
        #         where d is the original vector
        #               d' is the rotated vector
        #               inv(Tr) is the inverse of the matrix of rotation Tr
        #
        # Given that Tr is ortogonal, inv(Tr) would then be its transpose matrix
        #                          _             _
        #                         | Cos(α)  Sin(α)|
        #               inv(Tr) = |-Sin(α)  Cos(α)|
        #                         |_             _|

        world_normal_x = normal_x * cos_angle + normal_y * sin_angle
        world_normal_y = -normal_x * sin_angle + normal_y * cos_angle

        # Calculate relative velocity
        vel_x = physics_obj.velocity_x
        vel_y = physics_obj.velocity_y

        # Calculate velocity component along the normal (dot product)
        vel_normal = vel_x * world_normal_x + vel_y * world_normal_y

        # Only resolve collision if objects are moving towards each other
        if vel_normal < 0:
            # Apply reflection: v_new = v_old - 2 * (v_old · n) * n
            physics_obj.velocity_x -= 2 * vel_normal * world_normal_x
            physics_obj.velocity_y -= 2 * vel_normal * world_normal_y
            
            # Apply elasticity # TBD: Currently the energy loss is way more of what should be...
            physics_obj.velocity_x *= 0.99
            physics_obj.velocity_y *= OBJECT_ELASTICITY

            # Add some horizontal velocity based on where the ball hit the bar (for gameplay)
            #if abs(normal_y) > 0.7:  # Hit top or bottom of bar
            #    hit_position = local_x / bar_half_width  # -1 to 1
            #    physics_obj.velocity_x += hit_position * 150  # Add spin effect

        # Separate the objects to prevent overlap
        penetration_depth = circle_radius - normal_length
        if penetration_depth > 0:
            # Move circle out of rectangle
            physics_obj.sprite.center_x += world_normal_x * penetration_depth
            physics_obj.sprite.center_y += world_normal_y * penetration_depth

    def update(self, delta_time: float, keys: set, world_width: int, world_height: int):
        """Update all physics objects and player controllers."""
        # Update physics objects
        for physics_obj in self.physics_objects:
            physics_obj.update_physics(delta_time, world_width, world_height)
        
        # Update player controllers
        for controller in self.player_controllers:
            controller.update_movement(delta_time, keys, world_width)
        
        # Check for collisions between physics objects and player controllers using arcade's built-in collision detection
        for physics_obj in self.physics_objects:
            for controller in self.player_controllers:
                if physics_obj.sprite.collides_with_sprite(controller.sprite):
                    self.handle_collision(delta_time, physics_obj, controller)
    
    def reset_physics_object(self, index: int, x: float, y: float, velocity_x: float = 0.0, velocity_y: float = 0.0):
        """Reset a physics object to initial state."""
        if 0 <= index < len(self.physics_objects):
            physics_obj = self.physics_objects[index]
            physics_obj.sprite.center_x = x
            physics_obj.sprite.center_y = y
            physics_obj.velocity_x = velocity_x
            physics_obj.velocity_y = velocity_y
    
    def reset_player_controller(self, index: int, x: float, y: float, angle: float = 0.0):
        """Reset a player controller to initial position."""
        if 0 <= index < len(self.player_controllers):
            controller = self.player_controllers[index]
            controller.sprite.center_x = x
            controller.sprite.center_y = y
            controller.sprite.angle = angle
