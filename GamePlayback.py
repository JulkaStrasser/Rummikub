
import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
import sys
import matplotlib.pyplot as plt 

class PlayBack():
    def __init__(self):
       self.output_file = "history.avi"
        
    def save_game(self):
        window_name = "python3"
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self.fps = 12.0 # frames per second
        # self.record_seconds = 100 # to bede chciala zamienic na ponowne klikniecie przycisku PlayBack
        self.w = gw.getWindowsWithTitle(window_name)[0]
        self.w.activate()
        self.out = cv2.VideoWriter(self.output_file, fourcc, self.fps, tuple(self.w.size))
        print('Zapisywanie historii')
        while True:
            
            img = pyautogui.screenshot(region=(self.w.left, self.w.top, self.w.width, self.w.height))
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.out.write(frame)
            # if the user clicks q, it exits
            if cv2.waitKey(1) == ord("q"):
                print('Przerwano zapisywanie historii')
                break

    def display_history(self):

        cap = cv2.VideoCapture(self.output_file)

        # Check if camera opened successfully
        if (cap.isOpened()== False):
            print("Error opening video file")

        # Read until video is completed
        while(cap.isOpened()):
            
            ret, frame = cap.read()
            if ret == True:
                cv2.imshow('Frame', frame)
                
            # Press Q on keyboard to exit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break

        # Break the loop
            else:
                break
        
        cap.release()
        cv2.destroyAllWindows()

    def stop(self):
        cv2.destroyAllWindows()
        self.out.release()



if __name__ == '__main__':
    playback = PlayBack()
    playback.save_game()
    playback.stop()
    playback.display_history()