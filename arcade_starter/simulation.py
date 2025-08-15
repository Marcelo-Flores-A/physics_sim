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
        
        # Physics-only object sprite
        self.object = arcade.SpriteSolidColor(32, 32, arcade.color.AZURE)
        self.object.center_x = width // 2
        self.object.center_y = height // 2
        self.object_list = arcade.SpriteList()
        self.object_list.append(self.object)
        
        # Physics properties
        self.object_velocity_x = 100.0  # Give it some initial horizontal velocity
        self.object_velocity_y = 0.0
        self.gravity = -980  # pixels/second²
        
        # Player-controlled bar sprite
        self.bar = arcade.SpriteSolidColor(80, 16, arcade.color.RED)
        self.bar.center_x = width // 2
        self.bar.center_y = 50  # Near bottom of screen
        self.bar_list = arcade.SpriteList()
        self.bar_list.append(self.bar)
        
        # Track pressed directions for bar control
        self.keys: Set[str] = set()
    
    def reset(self):
        """Reset the simulation to initial state."""
        # Reset physics object
        self.object.center_x = self.width // 2
        self.object.center_y = self.height - (self.object.height / 2)
        self.object_velocity_x = 100.0  # Reset horizontal velocity
        self.object_velocity_y = 0.0
        
        # Reset player-controlled bar
        self.bar.center_x = self.width // 2
        self.bar.center_y = 50
        
        self.keys.clear()
    
    def update(self, delta_time: float):
        """Update physics simulation."""
        # Update physics-only object
        self.update_physics_object(delta_time)
        
        # Update player-controlled bar
        self.update_player_bar(delta_time)
    
    def update_physics_object(self, delta_time: float):
        """Update the physics-only object."""
        # Get distances from borders of object to its center
        half_w = self.object.width / 2
        half_h = self.object.height / 2

        # Calculate horizontal movement
        dx = self.object_velocity_x * delta_time
        # Calculate vertical movement
        self.object_velocity_y += self.gravity * delta_time
        dy = self.object_velocity_y * delta_time

        # Update position
        new_x = self.object.center_x + dx
        new_y = self.object.center_y + dy
        
        # Bounce off walls for x direction
        if new_x <= half_w or new_x >= self.width - half_w:
            self.object_velocity_x = -self.object_velocity_x
            new_x = max(half_w, min(self.width - half_w, new_x))

        # Bounce off floor for y direction
        if new_y <= half_h:
            self.object_velocity_y = -0.5 * self.object_velocity_y
            new_y = max(half_h, new_y)
        
        # Clamp to window bounds
        self.object.center_x = new_x
        self.object.center_y = max(half_h, min(self.height - half_h, new_y))
    
    def update_player_bar(self, delta_time: float):
        """Update the player-controlled bar."""
        # Get distances from borders of bar to its center
        half_w = self.bar.width / 2
        
        # Player control for bar's x position
        dx = (("right" in self.keys) - ("left" in self.keys)) * MOVE_SPEED * delta_time
        
        # Update position and clamp to window bounds
        new_x = self.bar.center_x + dx
        self.bar.center_x = max(half_w, min(self.width - half_w, new_x))
    
    def draw(self):
        """Draw the simulation objects."""
        self.object_list.draw()
        self.bar_list.draw()
        
        # HUD
        controls = "Move Bar: WASD / Arrows   Fullscreen: F11   Back to Menu: ESC"
        arcade.draw_text(controls, 10, 10, arcade.color.LIGHT_GRAY, 14)
        
        # Object info
        info = f"Blue Object: Physics-only (bouncing)   Red Bar: Player-controlled"
        arcade.draw_text(info, 10, 30, arcade.color.LIGHT_GRAY, 14)
    
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
        
        # Keep bar at bottom when resizing
        self.bar.center_y = 50
