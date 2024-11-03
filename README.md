# AI-Virtual-Marker
This project is to offer an innovative, hands-free drawing application that uses a webcam to recognize hand gestures, providing users with a seamless and intuitive way to create digital art and interact with a virtual canvas.


## Tech Stacks :
- OpenCV (Image Processing and Drawing)
- Mediapipe (Hand Tracking)


## How to Use :
### 1. Writing Mode
- **Gesture:** Raise only your index finger.
- **Action:** Move your index finger across the screen to draw.
- **Details:** The line follows the movement of your finger on the screen.
  
![Writing](https://github.com/user-attachments/assets/ce467eff-14bb-42b9-be83-68e2c0d4f6d1)

### 2. Selection Mode
- **Gesture:** Use your index and middle fingers.
- **Action:** Activate Selection Mode to choose from various colors or the eraser at the top of the screen.
- **Options:**
  
Color | Description
------- | ---------
Pink | Select for pink-colored drawing
Yellow | Select for yellow-colored drawing
Green | Select for green-colored drawing
Eraser | Choose the black section to erase parts of your drawing

![Selection](https://github.com/user-attachments/assets/3f43f996-1b1e-489d-be0f-72dd182155c4)

### 3. Adjusting Thickness
- **Gesture:** Adjust the distance between your thumb and index finger.
- **Action:** Adjust the thickness of the draw based on this distance.
- **Select Thickness:** When the pinky finger is up, the selected thickness is applied.

![Thickness](https://github.com/user-attachments/assets/87cc1eb9-9b32-445a-992f-cdfc7247160e)

### 4. Locking and Unlocking the Screen
#### Lock Screen
- **Gesture:** Raise your index, middle, and ring fingers.
- **Action:** The screen locks, freezing any further drawing. The current content on the screen is preserved, and a “Screen Locked” message appears.
#### Unlock Screen
- **Gesture:** Raise your index, middle, ring, and pinky fingers (thumb down).
- **Action:** Unlock the screen, allowing drawing to continue.

![Screen Lock](https://github.com/user-attachments/assets/3c831ead-4e0f-4aea-b250-18650567e41b)

### 5. Clearing the Screen
- **Condition:** Make sure the screen is unlocked.
- **Gesture:** Close your hand into a fist (all fingers down).
- **Action:** This clears the canvas and removes all drawings.

## Points To Remember : 
> [!NOTE]
> For optimal performance, keep your hand within the camera’s field of view and avoid rapid movements. The system works best when gestures are made steadily and within the visible frame.

> [!TIP]
>To improve gesture recognition, ensure there’s good contrast between your hand and the background. Light or neutral backgrounds work best, and ensure your hand is well-lit.

> [!IMPORTANT]
>  Before starting, confirm that the webcam is positioned correctly, and all necessary libraries (OpenCV, MediaPipe, and NumPy) are installed. This ensures the program runs smoothly without interruptions.

> [!WARNING]
>Avoid blocking the webcam with other objects during use, as this may cause unexpected behaviors or interfere with gesture recognition accuracy.

> [!CAUTION]
> The screen lock feature preserves the current drawing on the canvas. Be cautious when unlocking the screen, as any gestures may immediately affect the canvas if they are in drawing mode.
