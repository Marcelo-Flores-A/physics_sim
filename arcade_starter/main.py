#!/usr/bin/env python
from typing import Set
import arcade

WIDTH, HEIGHT = 960, 540
TITLE = "Arcade Starter - Experiments"
MOVE_SPEED = 300.0

# Game states
MENU_STATE = 0
SIMULATION_STATE = 1
OPTIONS_STATE = 2


class App(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE, resizable=True, update_rate=1 / 120)
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)
        
        # Game state management
        self.current_state = MENU_STATE
        self.selected_menu_item = 0  # 0=Start, 1=Options, 2=Exit
        
        # Simple controllable object sprite
        self.object = arcade.SpriteSolidColor(32, 32, arcade.color.AZURE)
        self.object.center_x = WIDTH // 2
        self.object.center_y = HEIGHT // 2
        self.object_list = arcade.SpriteList()
        self.object_list.append(self.object)
        self.object_velocity_y = 0.0
        self.gravity = -980 # pixels/second²

        # Track pressed directions
        self.keys: Set[str] = set()

    def on_draw(self):
        self.clear()
        
        if self.current_state == MENU_STATE:
            self.draw_menu()
        elif self.current_state == SIMULATION_STATE:
            self.draw_simulation()
        elif self.current_state == OPTIONS_STATE:
            self.draw_options()
    
    def draw_menu(self):
        # Title
        arcade.draw_text("Physics Simulation", WIDTH // 2, HEIGHT - 100, 
                        arcade.color.WHITE, 48, anchor_x="center")
        
        # Menu options
        menu_items = ["Start Simulation", "Options", "Exit"]
        start_y = HEIGHT // 2 + 50
        
        for i, item in enumerate(menu_items):
            y_pos = start_y - (i * 60)
            color = arcade.color.YELLOW if i == self.selected_menu_item else arcade.color.WHITE
            arcade.draw_text(item, WIDTH // 2, y_pos, color, 24, anchor_x="center")
            
            # Draw selection indicator
            if i == self.selected_menu_item:
                arcade.draw_text(">", WIDTH // 2 - 120, y_pos, arcade.color.YELLOW, 24)
                arcade.draw_text("<", WIDTH // 2 + 120, y_pos, arcade.color.YELLOW, 24)
        
        # Instructions
        arcade.draw_text("Use UP/DOWN arrows to navigate, ENTER to select", 
                        WIDTH // 2, 50, arcade.color.LIGHT_GRAY, 16, anchor_x="center")
    
    def draw_simulation(self):
        self.object_list.draw()
        
        # HUD
        controls = "Move: WASD / Arrows   Fullscreen: F11   Back to Menu: ESC"
        arcade.draw_text(controls, 10, 10, arcade.color.LIGHT_GRAY, 14)
    
    def draw_options(self):
        # Title
        arcade.draw_text("Options", WIDTH // 2, HEIGHT - 100, 
                        arcade.color.WHITE, 36, anchor_x="center")
        
        # Options content
        arcade.draw_text("Gravity: -980 pixels/second²", WIDTH // 2, HEIGHT // 2 + 50, 
                        arcade.color.WHITE, 20, anchor_x="center")
        arcade.draw_text("Move Speed: 300 pixels/second", WIDTH // 2, HEIGHT // 2, 
                        arcade.color.WHITE, 20, anchor_x="center")
        arcade.draw_text("Update Rate: 120 FPS", WIDTH // 2, HEIGHT // 2 - 50, 
                        arcade.color.WHITE, 20, anchor_x="center")
        
        # Instructions
        arcade.draw_text("Press ESC to return to menu", WIDTH // 2, 50, 
                        arcade.color.LIGHT_GRAY, 16, anchor_x="center")

    def on_update(self, delta_time: float):
        # Only update physics when in simulation state
        if self.current_state == SIMULATION_STATE:
            # Player control for object's x position
            dx = (("right" in self.keys) - ("left" in self.keys)) * MOVE_SPEED * delta_time
            # Gravity physics for y position
            self.object_velocity_y += self.gravity * delta_time  # Update velocity
            dy = delta_time * self.object_velocity_y

            # Clamp to window bounds
            new_x = self.object.center_x + dx
            new_y = self.object.center_y + dy
            half_w = self.object.width / 2
            half_h = self.object.height / 2
            # Check that the object's sprite is still within the bounderies of the window
            self.object.center_x = max(half_w, min(self.width - half_w, new_x))
            self.object.center_y = max(half_h, min(self.height - half_h, new_y))

    def on_key_press(self, symbol: int, modifiers: int):
        if self.current_state == MENU_STATE:
            self.handle_menu_keys(symbol)
        elif self.current_state == SIMULATION_STATE:
            self.handle_simulation_keys(symbol)
        elif self.current_state == OPTIONS_STATE:
            self.handle_options_keys(symbol)
    
    def handle_menu_keys(self, symbol: int):
        if symbol == arcade.key.UP:
            self.selected_menu_item = (self.selected_menu_item - 1) % 3
        elif symbol == arcade.key.DOWN:
            self.selected_menu_item = (self.selected_menu_item + 1) % 3
        elif symbol == arcade.key.ENTER:
            if self.selected_menu_item == 0:  # Start Simulation
                self.current_state = SIMULATION_STATE
                # Reset object position and velocity when starting simulation
                self.object.center_x = WIDTH // 2
                self.object.center_y = HEIGHT // 2
                self.object_velocity_y = 0.0
            elif self.selected_menu_item == 1:  # Options
                self.current_state = OPTIONS_STATE
            elif self.selected_menu_item == 2:  # Exit
                arcade.exit()
        elif symbol == arcade.key.ESCAPE:
            arcade.exit()
    
    def handle_simulation_keys(self, symbol: int):
        if symbol == arcade.key.ESCAPE:
            self.current_state = MENU_STATE
            self.keys.clear()  # Clear any held keys when returning to menu
        elif symbol in (arcade.key.LEFT, arcade.key.A):
            self.keys.add("left")
        elif symbol in (arcade.key.RIGHT, arcade.key.D):
            self.keys.add("right")
        elif symbol in (arcade.key.UP, arcade.key.W):
            self.keys.add("up")
        elif symbol in (arcade.key.DOWN, arcade.key.S):
            self.keys.add("down")
        elif symbol == arcade.key.F11:
            self.set_fullscreen(not self.fullscreen)
    
    def handle_options_keys(self, symbol: int):
        if symbol == arcade.key.ESCAPE:
            self.current_state = MENU_STATE

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol in (arcade.key.LEFT, arcade.key.A):
            self.keys.discard("left")
        elif symbol in (arcade.key.RIGHT, arcade.key.D):
            self.keys.discard("right")
        elif symbol in (arcade.key.UP, arcade.key.W):
            self.keys.discard("up")
        elif symbol in (arcade.key.DOWN, arcade.key.S):
            self.keys.discard("down")


if __name__ == "__main__":
    app = App()
    arcade.run()
