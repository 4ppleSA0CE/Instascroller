#!/usr/bin/env python3
"""
Video Player Detection Demo
Demonstrates different methods to detect video player areas in screenshots
"""

import cv2
import numpy as np
import mss
import time
from typing import List, Tuple, Optional

class VideoPlayerDetector:
    def __init__(self):
        self.sct = mss.mss()
        
    def capture_screen(self, region: Optional[Tuple[int, int, int, int]] = None) -> np.ndarray:
        """Capture screen or specific region"""
        if region:
            monitor = {"top": region[1], "left": region[0], 
                      "width": region[2], "height": region[3]}
        else:
            monitor = self.sct.monitors[1]  # Primary monitor
            
        screenshot = self.sct.grab(monitor)
        img = np.array(screenshot)
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    
    
    def detect_video_players(self, img: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Color-based Segmentation to find video player regions
        Find non-black rectangular regions and filter out screen borders
        """
        # Convert to HSV for better color segmentation
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Define range for "non-black" colors
        # Black in HSV: V (value) is low
        lower_non_black = np.array([0, 0, 30])  # V > 30 (not too dark)
        upper_non_black = np.array([180, 255, 255])
        
        # Create mask for non-black regions
        mask = cv2.inRange(hsv, lower_non_black, upper_non_black)
        
        # Clean up the mask
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        rectangles = []
        img_height, img_width = img.shape[:2]
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filter by size and aspect ratio
            if w > 200 and h > 150:
                aspect_ratio = w / h
                # Video players typically have aspect ratios between 0.5 and 2.0
                if 0.5 <= aspect_ratio <= 2.0:
                    # Check if this rectangle is NOT a screen border
                    if not self._is_screen_border(x, y, w, h, img_width, img_height):
                        rectangles.append((x, y, w, h))
        
        return rectangles
    
    def _is_screen_border(self, x: int, y: int, w: int, h: int, img_width: int, img_height: int) -> bool:
        """
        Check if a rectangle is likely a screen border that should be ignored
        """
        # Define border threshold (pixels from edge to consider as border)
        border_threshold = 50
        
        # Check if rectangle touches or is very close to screen edges
        touches_left = x <= border_threshold
        touches_right = (x + w) >= (img_width - border_threshold)
        touches_top = y <= border_threshold
        touches_bottom = (y + h) >= (img_height - border_threshold)
        
        # If it touches multiple edges, it's likely a screen border
        edge_count = sum([touches_left, touches_right, touches_top, touches_bottom])
        
        # Also check if it's too large (covers most of the screen)
        area_ratio = (w * h) / (img_width * img_height)
        
        # Consider it a border if:
        # 1. It touches 2 or more edges, OR
        # 2. It covers more than 80% of the screen area
        return edge_count >= 2 or area_ratio > 0.8
    
    
    def draw_rectangles(self, img: np.ndarray, rectangles: List[Tuple[int, int, int, int]], 
                       color: Tuple[int, int, int] = (0, 255, 0), thickness: int = 2) -> np.ndarray:
        """Draw rectangles on image"""
        result = img.copy()
        for x, y, w, h in rectangles:
            cv2.rectangle(result, (x, y), (x + w, y + h), color, thickness)
        return result
    

def main():
    """Demo function"""
    detector = VideoPlayerDetector()
    
    print("Video Player Detection Demo")
    print("=" * 40)
    print("Press 'q' to quit, 's' to save screenshot")
    print("Using color-based detection with screen border filtering")
    
    while True:
        # Capture screen
        img = detector.capture_screen()
        
        # Detect video players using color-based method
        rectangles = detector.detect_video_players(img)
        # print(f"midpoint: {rectangles[0][0] + rectangles[0][2] / 2, rectangles[0][1] + rectangles[0][3] / 2}")
        
        # Draw results
        result_img = detector.draw_rectangles(img, rectangles)
        
        # Add detection info
        cv2.putText(result_img, f"Video Players Detected: {len(rectangles)}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Add instructions
        cv2.putText(result_img, "Press 'q' to quit, 's' to save", 
                   (10, result_img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Display
        cv2.imshow("Video Player Detection", result_img)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            filename = f"video_detection_{int(time.time())}.png"
            cv2.imwrite(filename, result_img)
            print(f"Saved result: {filename}")
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
