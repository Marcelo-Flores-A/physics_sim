"""
Physics Simulation Module

This module contains the simulation state and physics calculations
for the particle physics simulation.
"""

import arcade
from typing import Set

MOVE_SPEED = 300.0


class PhysicsSimulation:
    """Handles the physics simulation state and calculations."""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        
        # Simple controllable object sprite
        self.object = arcade.SpriteSolidColor(32, 32, arcade.color.AZURE)
        self.object.center_x = width // 2
        self.object.center_y = height // 2
        self.object_list = arcade.SpriteList()
        self.object_list.append(self.object)
        
        # Physics properties
        self.object_velocity_y = 0.0
        self.gravity = -980  # pixels/second²
        
        # Track pressed directions
        self.keys: Set[str] = set()
    
    def reset(self):
        """Reset the simulation to initial state."""
        self.object.center_x = self.width // 2
        self.object.center_y = self.height - (self.object.height / 2)
        self.object_velocity_y = 0.0
        self.keys.clear()
    
    def update(self, delta_time: float):
        """Update physics simulation."""
        # Get distances from boarders of object to its center
        half_w = self.object.width / 2
        half_h = self.object.height / 2

        # Player control for object's x position
        dx = (("right" in self.keys) - ("left" in self.keys)) * MOVE_SPEED * delta_time
        
        # Gravity physics for y position
        if self.object.center_y > half_h:
            # Update velocity and height during free fall
            self.object_velocity_y += self.gravity * delta_time
            dy = delta_time * self.object_velocity_y
        else:
            # Update velocity during floor collision
            self.object_velocity_y -= 1.6 * self.object_velocity_y
            dy = delta_time * self.object_velocity_y

        # Clamp to window bounds
        new_x = self.object.center_x + dx
        new_y = self.object.center_y + dy
        # Check that the object's sprite is still within the boundaries of the window
        self.object.center_x = max(half_w, min(self.width - half_w, new_x))
        self.object.center_y = max(half_h, min(self.height - half_h, new_y))
    
    def draw(self):
        """Draw the simulation objects."""
        self.object_list.draw()
        
        # HUD
        controls = "Move: WASD / Arrows   Fullscreen: F11   Back to Menu: ESC"
        arcade.draw_text(controls, 10, 10, arcade.color.LIGHT_GRAY, 14)
    
    def handle_key_press(self, symbol: int):
        """Handle key press events for simulation."""
        if symbol in (arcade.key.LEFT, arcade.key.A):
            self.keys.add("left")
        elif symbol in (arcade.key.RIGHT, arcade.key.D):
            self.keys.add("right")
        elif symbol in (arcade.key.UP, arcade.key.W):
            self.keys.add("up")
        elif symbol in (arcade.key.DOWN, arcade.key.S):
            self.keys.add("down")
    
    def handle_key_release(self, symbol: int):
        """Handle key release events for simulation."""
        if symbol in (arcade.key.LEFT, arcade.key.A):
            self.keys.discard("left")
        elif symbol in (arcade.key.RIGHT, arcade.key.D):
            self.keys.discard("right")
        elif symbol in (arcade.key.UP, arcade.key.W):
            self.keys.discard("up")
        elif symbol in (arcade.key.DOWN, arcade.key.S):
            self.keys.discard("down")
    
    def resize(self, width: int, height: int):
        """Handle window resize events."""
        self.width = width
        self.height = height
