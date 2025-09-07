#instascroller.py

import speech_recognition as sr
import pyautogui
import time
import sys
import signal
from typing import Optional


class InstagramVoiceController:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_running = True
        
        # Configure pyautogui
        pyautogui.FAILSAFE = True  # Move mouse to corner to stop
        pyautogui.PAUSE = 0.1  # Small pause between actions
        
        # Command mappings
        self.commands = {
            'scroll': self.scroll_down,
            'down': self.scroll_down,
            'scroll down': self.scroll_down,
            'up': self.scroll_up,
            'scroll up': self.scroll_up,
            'stop': self.stop_session,
            'quit': self.stop_session,
            'exit': self.stop_session
        }
        
        # Setup signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        
    def signal_handler(self, signum, frame):

        print("\n\nShutting down gracefully...")
        self.is_running = False
        sys.exit(0)
        
    def calibrate_microphone(self) -> bool:
        # Calibrate microphone for ambient noise
        try:
            print("Calibrating microphone for ambient noise...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
            print("Microphone calibrated successfully!")
            return True
        except Exception as e:
            print(f"Error calibrating microphone: {e}")
            return False
            
    def listen_for_command(self) -> Optional[str]:
        # Listen for voice command and return recognized text
        try:
            with self.microphone as source:
                # Listen for audio with timeout
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                
            # Recognize speech using Google Web Speech API
            command = self.recognizer.recognize_google(audio).lower()
            print(f"Heard: {command}")
            return command
            
        except sr.WaitTimeoutError:
            # No speech detected within timeout
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error during speech recognition: {e}")
            return None
            
    def scroll_down(self):
        #Scroll down on Instagram
        print("Scrolling down...")
        pyautogui.scroll(-500)  # Scroll down
        
    def scroll_up(self):
        #Scroll up on Instagram
        print("Scrolling up...")
        pyautogui.scroll(500)  # Scroll up
        
    def stop_session(self):
        #Stop the voice control session
        print("Stopping session...")
        self.is_running = False
        
    def process_command(self, command: str) -> bool:
        #Process voice command and execute corresponding action
        command = command.strip().lower()
        
        # Check for exact matches first
        if command in self.commands:
            self.commands[command]()
            return True
            
        # Check for partial matches
        for cmd_key, cmd_func in self.commands.items():
            if cmd_key in command:
                cmd_func()
                return True
                
        return False
        
    def run(self):
        """Main application loop"""
        print("=" * 60)
        print("Voice-Controlled Instagram Autoscroller MVP")
        print("=" * 60)
        print("\nInstructions:")
        print("1. Open Instagram in your desktop browser")
        print("2. Make sure Instagram is the active window")
        print("3. Say commands like 'scroll', 'down', 'up', or 'stop'")
        print("4. Press Ctrl+C to exit anytime")
        print("\nStarting voice recognition...")
        
        # Calibrate microphone
        if not self.calibrate_microphone():
            print("Failed to calibrate microphone. Exiting...")
            return
            
        print("\nListening for commands... (Say 'stop' to quit)")
        print("-" * 40)
        
        while self.is_running:
            try:
                command = self.listen_for_command()
                
                if command:
                    if not self.process_command(command):
                        print(f"Unknown command: '{command}'")
                        print("Available commands: scroll, down, up, stop")
                        
            except KeyboardInterrupt:
                print("\n\nReceived interrupt signal. Shutting down...")
                break
            except Exception as e:
                print(f"Unexpected error: {e}")
                time.sleep(1)  # Brief pause before continuing
                
        print("\nVoice control session ended. Goodbye!")


def main():
    #Main entry point
    try:
        controller = InstagramVoiceController()
        controller.run()
    except Exception as e:
        print(f"Failed to start application: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you have a working microphone")
        print("2. Check your internet connection (required for Google Speech API)")
        print("3. Install required dependencies: pip install -r requirements.txt")
        sys.exit(1)


if __name__ == "__main__":
    main()
