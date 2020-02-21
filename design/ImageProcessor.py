import cv2 as cv

class ImageProcessor:
    def drawRect(self, img, coords):
        cv.rectangle(img, (coords[0], coords[1]), (coords[0] + coords[2], coords[1] + coords[3]), (255, 255, 0), 2)

    def grayScale(self, img):
        return cv.cvtColor(img, cv.COLOR_BGR2GRAY)


    def putText(self, img, text, x, y):
        font = cv.FONT_HERSHEY_SIMPLEX
        cv.putText(img, text, (x, y), font, 1, (255, 0, 0), 2, cv.LINE_AA)



