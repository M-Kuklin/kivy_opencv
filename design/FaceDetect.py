import cv2 as cv

class FaceDetect:
    def __init__(self):
        self.age_list = ['0-2', '4-6', '8-12', '15-20', '25-32', '38-43', '48-53', '60-100']
        self.gender_list = ['Male', 'Female']
        self.MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)

    def initModels(self):
        age_net = cv.dnn.readNetFromCaffe('deploy_age.prototxt', 'age_net.caffemodel')
        gender_net = cv.dnn.readNetFromCaffe('deploy_gender.prototxt', 'gender_net.caffemodel')
        return age_net, gender_net

    def getFace(self, faces, img):
        blobList = []
        for x, y, w, h in faces:
            faceImg = img[y:y+h, h:h+w].copy()
            blob = cv.dnn.blobFromImage(faceImg, 1, (227, 227), self.MODEL_MEAN_VALUES, swapRB=False)
            blobList.append(blob)
        return blobList

    def detect(self, img):
        face_cascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(img, 1.1, 5)
        return faces

    def predictAge(self, blobList, age_net):
        ages = []
        for blob in blobList:
            age_net.setInput(blob)
            age_preds = age_net.forward()
            age = self.age_list[age_preds[0].argmax()]
            ages.append(age)
        return ages

    def predictFace(self, faces):
        coords = []
        for x, y, w, h in faces:
            coords.append((x, y, w, h))
        return coords

    def predictGender(self, blobList, gender_net):
        genders = []
        for blob in blobList:
            gender_net.setInput(blob)
            gender_preds = gender_net.forward()
            gender = self.gender_list[gender_preds[0].argmax()]
            genders.append(gender)
        return genders
