"""
Simulation Module

This module contains the simulation state and visual representation
for the particle physics simulation.
"""

import arcade
import PIL.Image
import PIL.ImageDraw
from typing import Set
from physics import PhysicsEngine, PhysicsObject, PlayerController
from constants import BALL_RADIUS, OBJECT_INITIAL_SPEED_X, BAR_WIDTH, BAR_HEIGHT, BAR_POSITION_Y

# Custom method to override SpriteCircle texture with a multiple color one
def make_multicolor_circle_texture(diameter: int) -> arcade.Texture:
    # Create transparent image
    image = PIL.Image.new("RGBA", (diameter, diameter), (0, 0, 0, 0))
    draw = PIL.ImageDraw.Draw(image)

    # Example: half red, half blue
    draw.pieslice([0, 0, diameter, diameter], start=0, end=180, fill=(255, 0, 0, 255))
    draw.pieslice([0, 0, diameter, diameter], start=180, end=360, fill=(255, 255, 255, 255))

    return arcade.Texture(name="circle", image=image)

class PhysicsSimulation:
    """Handles the physics simulation state and visual representation."""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        
        # Physics-only object sprite
        self.object = arcade.SpriteCircle(BALL_RADIUS, arcade.color.AZURE_MIST, False)  # 16 pixel radius = 32 pixel diameter.
        self.object.texture = make_multicolor_circle_texture(BALL_RADIUS*2)
        self.object.center_x = width // 2
        self.object.center_y = height // 2
        self.object_list = arcade.SpriteList()
        self.object_list.append(self.object)
        
        # Player-controlled bar sprite
        self.bar = arcade.SpriteSolidColor(BAR_WIDTH, BAR_HEIGHT, 0, 0, arcade.color.BABY_BLUE)
        self.bar.center_x = width // 2
        self.bar.center_y = BAR_POSITION_Y  # Near bottom of screen
        self.bar_list = arcade.SpriteList()
        self.bar_list.append(self.bar)
        
        # Initialize physics engine
        self.physics_engine = PhysicsEngine()
        
        # Create physics object for the bouncing object
        self.physics_object = PhysicsObject(self.object)
        self.physics_engine.add_physics_object(self.physics_object)
        
        # Create player controller for the bar
        self.player_controller = PlayerController(self.bar)
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
        self.physics_engine.reset_player_controller(0, self.width // 2, BAR_POSITION_Y)
        
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
        controls = "Tilt Counter-Clockwise: A   Tilt Clockwise: D   Reset: R   Fullscreen: F11   Back to Menu: ESC"
        arcade.draw_text(controls, 10, 500, arcade.color.LIGHT_GRAY, 14)
        
        # Object info
        info = f"Blue Ball: Physics-only (bouncing)   Red Bar: Player-controlled"
        arcade.draw_text(info, 10, 520, arcade.color.LIGHT_GRAY, 14)
    
    def handle_key_press(self, symbol: int):
        """Handle key press events for simulation."""
        if symbol == arcade.key.A:
            self.keys.add("counter-clockwise")
        elif symbol == arcade.key.D:
            self.keys.add("clockwise")
        elif symbol == arcade.key.R:
            self.reset()
    
    def handle_key_release(self, symbol: int):
        """Handle key release events for simulation."""
        if symbol == arcade.key.A:
            self.keys.discard("counter-clockwise")
        elif symbol == arcade.key.D:
            self.keys.discard("clockwise")
    
    def resize(self, width: int, height: int):
        """Handle window resize events."""
        self.width = width
        self.height = height
