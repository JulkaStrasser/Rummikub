
import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
import sys
import matplotlib.pyplot as plt 

class PlayBack():
    def __init__(self):
       pass
        

    def save_game(self):
        window_name = "python3"
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        
        self.fps = 12.0 # frames per second
        # the time you want to record in seconds
        self.record_seconds = 100 # to bede chciala zamienic na ponowne klikniecie przycisku PlayBack
        self.w = gw.getWindowsWithTitle(window_name)[0]
        # activate the window
        self.w.activate()
        # create the video write object
        self.out = cv2.VideoWriter("history.avi", fourcc, self.fps, tuple(self.w.size))
        # for i in range(int(self.record_seconds * self.fps)):
        print('Zapisywanie historii')
        while True:
            
            # make a screenshot
            img = pyautogui.screenshot(region=(self.w.left, self.w.top, self.w.width, self.w.height))
            # convert these pixels to a proper numpy array to work with OpenCV
            frame = np.array(img)
            # convert colors from BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # write the frame
            self.out.write(frame)
            # show the frame
            #cv2.imshow("screenshot", frame)
            # if the user clicks q, it exits
            if cv2.waitKey(1) == ord("q"):
                print('Przerwano zapisywanie historii')
                break

    def display_history(self):

        # Create a VideoCapture object and read from input file
        cap = cv2.VideoCapture('history.avi')

        # Check if camera opened successfully
        if (cap.isOpened()== False):
            print("Error opening video file")

        # Read until video is completed
        while(cap.isOpened()):
            
        # Capture frame-by-frame
            ret, frame = cap.read()
            if ret == True:
            # Display the resulting frame
                cv2.imshow('Frame', frame)
                
            # Press Q on keyboard to exit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break

        # Break the loop
            else:
                break
        # When everything done, release
        # the video capture object
        cap.release()
        # Closes all the frames
        cv2.destroyAllWindows()

    def stop(self):
        # make sure everything is closed when exited
        cv2.destroyAllWindows()
        self.out.release()



if __name__ == '__main__':
    playback = PlayBack()
    playback.save_game()
    playback.stop()
    playback.display_history()