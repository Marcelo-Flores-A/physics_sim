"""
Simulation Module

This module contains the simulation state and visual representation
for the particle physics simulation.
"""

import arcade
from typing import Set
from physics import PhysicsEngine, PhysicsObject, PlayerController

BAR_SPEED = 500.0
OBJECT_INITIAL_SPEED_X = 100.0

class PhysicsSimulation:
    """Handles the physics simulation state and visual representation."""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        
        # Physics-only object sprite
        self.object = arcade.SpriteSolidColor(32, 32, arcade.color.AZURE) # TBD: Fix object color
        self.object.center_x = width // 2
        self.object.center_y = height // 2
        self.object_list = arcade.SpriteList()
        self.object_list.append(self.object)
        
        # Player-controlled bar sprite
        self.bar = arcade.SpriteSolidColor(80, 16, arcade.color.RED) # TBD: Fix bar color
        self.bar.center_x = width // 2
        self.bar.center_y = 100  # Near bottom of screen
        self.bar_list = arcade.SpriteList()
        self.bar_list.append(self.bar)
        
        # Initialize physics engine
        self.physics_engine = PhysicsEngine()
        
        # Create physics object for the bouncing object
        self.physics_object = PhysicsObject(self.object, velocity_x = OBJECT_INITIAL_SPEED_X, velocity_y=0.0)
        self.physics_engine.add_physics_object(self.physics_object)
        
        # Create player controller for the bar
        self.player_controller = PlayerController(self.bar, move_speed = BAR_SPEED)
        self.physics_engine.add_player_controller(self.player_controller)
        
        # Track pressed directions for bar control
        self.keys: Set[str] = set()
    
    def reset(self):
        """Reset the simulation to initial state."""
        # Reset physics object using physics engine
        self.physics_engine.reset_physics_object(
            0, 
            self.width // 2, 
            self.height - (self.object.height / 2),
            velocity_x = OBJECT_INITIAL_SPEED_X,
            velocity_y=0.0
        )
        
        # Reset player-controlled bar using physics engine
        self.physics_engine.reset_player_controller(0, self.width // 2, 100)
        
        self.keys.clear()
    
    def update(self, delta_time: float):
        """Update physics simulation using the physics engine."""
        # Update all physics objects and player controllers through the physics engine
        self.physics_engine.update(delta_time, self.keys, self.width, self.height)
    
    def draw(self):
        """Draw the simulation objects."""
        self.object_list.draw()
        self.bar_list.draw()
        
        # HUD
        controls = "Move Left: A   Move Right: D   Fullscreen: F11   Back to Menu: ESC"
        arcade.draw_text(controls, 10, 500, arcade.color.LIGHT_GRAY, 14)
        
        # Object info
        info = f"Blue Object: Physics-only (bouncing)   Red Bar: Player-controlled"
        arcade.draw_text(info, 10, 520, arcade.color.LIGHT_GRAY, 14)
    
    def handle_key_press(self, symbol: int):
        """Handle key press events for simulation."""
        if symbol == arcade.key.A:
            self.keys.add("left")
        elif symbol == arcade.key.D:
            self.keys.add("right")
    
    def handle_key_release(self, symbol: int):
        """Handle key release events for simulation."""
        if symbol == arcade.key.A:
            self.keys.discard("left")
        elif symbol == arcade.key.D:
            self.keys.discard("right")
    
    def resize(self, width: int, height: int):
        """Handle window resize events."""
        self.width = width
        self.height = height
        
        # Keep bar at bottom when resizing
        self.bar.center_y = 100
