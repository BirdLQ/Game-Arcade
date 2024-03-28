# TODO: Add error handling to handle potential errors in a user-friendly way.
# TODO: Optimize screen dimension validation using a more efficient and OS-independent method.
# TODO: Add music control functions for pausing, unpausing, and setting the volume of the music.

import locale
import os
import platform
import sys
import threading
from pygame import mixer

import animation
import loading

# Constants for screen dimensions
MIN_SCREEN_WIDTH = 1300
MIN_SCREEN_HEIGHT = 600

class MusicPlayer:
    @staticmethod
    def play_background_music() -> None:
        """Initialize the mixer and play the background music in a loop."""
        mixer.init()
        mixer.music.load('data/music/theme3.mp3')
        mixer.music.set_volume(0.5)
        mixer.music.play(-1)

class SystemValidator:
    @staticmethod
    def validate_operating_system():
        """Check if the operating system is supported."""
        if platform.system() not in ['Windows', 'Linux', 'Darwin']:
            raise Exception("OPERATING SYSTEM NOT SUPPORTED")

    @staticmethod
    def validate_screen_dimensions() -> None:
        """Check if the screen size is large enough."""
        if platform.system() == 'Windows':
            from win32api import GetSystemMetrics
            screen_width = GetSystemMetrics(0)
            screen_height = GetSystemMetrics(1)

            os.system('title ' + 'Game Palace')
        elif platform.system() in ['Linux', 'Darwin']:
            import subprocess
            output = subprocess.check_output("xrandr | grep '*' | awk '{print $1}'", shell=True)
            screen_width, screen_height = map(int, output.decode().split('x'))
            sys.stdout.write("\\\\x1b]2;" + 'Game Palace' + "\\\\x07")
            sys.stdout.flush()
        if screen_width <= MIN_SCREEN_WIDTH or screen_height <= MIN_SCREEN_HEIGHT:
            raise Exception('SCREEN TOO SMALL')

class ScreenMode:
    @staticmethod
    def enable_full_screen_mode() -> None:
        """Enable full screen mode."""
        import keyboard
        keyboard.press_and_release('f11')

class GameAnimation:
    @staticmethod
    def start_loading_screen_animation() -> None:
        """Start the loading screen animation."""
        loading.load()

    @staticmethod
    def start_game_animation(loading_thread) -> None:
        """Start the main game animation.
        
        Args:
            loading_thread (threading.Thread): The thread running the loading screen animation.
        """
        while True:
            if not loading_thread.is_alive():
                animation.main_anim()

if __name__ == "__main__":
    # Set encoding to utf-8
    locale.setlocale(locale.LC_ALL, '')

    # Validate the operating system
    SystemValidator.validate_operating_system()
    # Validate the screen dimensions
    SystemValidator.validate_screen_dimensions()
    
    # Enable full screen mode
    ScreenMode.enable_full_screen_mode()

    # Start the music thread
    music_thread = threading.Thread(target=MusicPlayer.play_background_music)
    music_thread.start()

    # Start the loading screen animation thread
    loading_thread = threading.Thread(target=GameAnimation.start_loading_screen_animation)
    loading_thread.start()

    # Start the main game animation
    GameAnimation.start_game_animation(loading_thread)
