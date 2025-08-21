"""
Main Application Module

This module contains the main execution flow, game window management,
and state handling for the physics simulation application.
"""

import arcade
from simulation import PhysicsSimulation
from constants import WIDTH, HEIGHT, TITLE, MENU_STATE, SIMULATION_STATE, OPTIONS_STATE


class App(arcade.Window):
    """Main application window handling game states and UI."""
    
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE, resizable=True, update_rate=1 / 120)
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)
        
        # Game state management
        self.current_state = MENU_STATE
        self.selected_menu_item = 0  # 0=Start, 1=Options, 2=Exit
        
        # Initialize physics simulation
        self.simulation = PhysicsSimulation(WIDTH, HEIGHT)

    def on_draw(self):
        """Main draw method that delegates to state-specific draw methods."""
        self.clear()
        
        if self.current_state == MENU_STATE:
            self.draw_menu()
        elif self.current_state == SIMULATION_STATE:
            self.simulation.draw()
        elif self.current_state == OPTIONS_STATE:
            self.draw_options()
    
    def draw_menu(self):
        """Draw the main menu screen."""
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
        arcade.draw_text("Select: ENTER / click   Fullscreen: F11", 
                        WIDTH // 2, 50, arcade.color.LIGHT_GRAY, 16, anchor_x="center")
    
    def draw_options(self):
        """Draw the options screen."""
        # Title
        arcade.draw_text("Options", WIDTH // 2, HEIGHT - 100, 
                        arcade.color.WHITE, 36, anchor_x="center")
        
        # Options content
        arcade.draw_text("Gravity: -980 pixels/second²", WIDTH // 2, HEIGHT // 2 + 50, 
                        arcade.color.WHITE, 20, anchor_x="center")
        arcade.draw_text("Move Speed: 500 pixels/second", WIDTH // 2, HEIGHT // 2, 
                        arcade.color.WHITE, 20, anchor_x="center")
        arcade.draw_text("Update Rate: 120 FPS", WIDTH // 2, HEIGHT // 2 - 50, 
                        arcade.color.WHITE, 20, anchor_x="center")
        
        # Instructions
        arcade.draw_text("Press ESC to return to menu", WIDTH // 2, 50, 
                        arcade.color.LIGHT_GRAY, 16, anchor_x="center")

    def on_update(self, delta_time: float):
        """Main update method that delegates to simulation when active."""
        # Only update physics when in simulation state
        if self.current_state == SIMULATION_STATE:
            self.simulation.update(delta_time)

    def on_key_press(self, symbol: int, modifiers: int):
        """Handle key press events based on current state."""
        if self.current_state == MENU_STATE:
            self.handle_menu_keys(symbol)
        elif self.current_state == SIMULATION_STATE:
            self.handle_simulation_keys(symbol)
        elif self.current_state == OPTIONS_STATE:
            self.handle_options_keys(symbol)
    
    def handle_menu_keys(self, symbol: int):
        """Handle key presses in the menu state."""
        if symbol in (arcade.key.UP, arcade.key.W):
            self.selected_menu_item = (self.selected_menu_item - 1) % 3
        elif symbol in (arcade.key.DOWN, arcade.key.S):
            self.selected_menu_item = (self.selected_menu_item + 1) % 3
        elif symbol == arcade.key.ENTER:
            self.select_menu_item()
        elif symbol == arcade.key.F11:
            self.set_fullscreen(not self.fullscreen)
        elif symbol == arcade.key.ESCAPE:
            arcade.exit()
    
    def select_menu_item(self):
        """Execute the currently selected menu item."""
        if self.selected_menu_item == 0:  # Start Simulation
            self.current_state = SIMULATION_STATE
            self.simulation.reset()  # Reset simulation state
        elif self.selected_menu_item == 1:  # Options
            self.current_state = OPTIONS_STATE
        elif self.selected_menu_item == 2:  # Exit
            arcade.exit()
    
    def handle_simulation_keys(self, symbol: int):
        """Handle key presses in the simulation state."""
        if symbol == arcade.key.ESCAPE:
            self.current_state = MENU_STATE
        elif symbol == arcade.key.F11:
            self.set_fullscreen(not self.fullscreen)
        else:
            # Delegate movement keys to simulation
            self.simulation.handle_key_press(symbol)
    
    def handle_options_keys(self, symbol: int):
        """Handle key presses in the options state."""
        if symbol == arcade.key.F11:
            self.set_fullscreen(not self.fullscreen)
        elif symbol == arcade.key.ESCAPE:
            self.current_state = MENU_STATE

    def on_key_release(self, symbol: int, modifiers: int):
        """Handle key release events."""
        # Only handle key releases in simulation state
        if self.current_state == SIMULATION_STATE:
            self.simulation.handle_key_release(symbol)
    
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """Handle mouse click events."""
        if self.current_state == MENU_STATE and button == arcade.MOUSE_BUTTON_LEFT:
            # Calculate which menu item was clicked
            start_y = HEIGHT // 2 + 50
            for i in range(3):  # 3 menu items
                y_pos = start_y - (i * 60)
                # Check if click is within the menu item area (approximate)
                if y_pos - 30 <= y <= y_pos + 30:
                    self.selected_menu_item = i
                    self.select_menu_item()
                    break
    
    def on_resize(self, width: int, height: int):
        """Handle window resize events."""
        super().on_resize(width, height)
        # Update simulation dimensions
        self.simulation.resize(width, height)


if __name__ == "__main__":
    app = App()
    arcade.run()
