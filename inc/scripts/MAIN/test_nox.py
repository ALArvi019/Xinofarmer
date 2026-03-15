from windowcapture import WindowCapture
import cv2 as cv

# ask to user the src_windows name
src_window = input("Enter the LDPLAYER or NOX windows name: ")

wincap = WindowCapture(src_window)

while True:
    screenshot = wincap.get_screenshot()

    # show image
    cv.imshow(src_window, screenshot)
    if cv.waitKey(1) & 0xFF == ord('q'):
        cv.destroyAllWindows()
        break
