import FaceDetect as fd
import ImageProcessor as ip
class Director:
    def __init__(self, builder):
        self._ip = ip.ImageProcessor()
        self._builder = builder
        self._models = self._builder.getModels()

    def buildFaceDet(self, img):
        gray = self._ip.grayScale(img)
        faces = self._builder.getDetector(gray)
        coords = self._builder.buildFacePredictor(faces)
        for coord in coords:
            self._ip.drawRect(img, coord)

    def buildAgeDet(self, img):
        gray = self._ip.grayScale(img)
        faces = self._builder.getDetector(gray)
        if len(faces) > 0:
            coords = self._builder.buildFacePredictor(faces)
            age = self._builder.buildAgePredictor(faces, img, self._models[0])
            for i in range(len(coords)):
                text = f"Age:{age[i]}"
                self._ip.putText(img, text, coords[i][0], coords[i][1] + 50)

    def buildGenderDet(self, img):
        gray = self._ip.grayScale(img)
        faces = self._builder.getDetector(gray)
        if len(faces) > 0:
            coords = self._builder.buildFacePredictor(faces)
            gender = self._builder.buildGenderPredictor(faces, img, self._models[1])
            for i in range(len(coords)):
                text = f"{gender[i]}"
                self._ip.putText(img, text, coords[i][0], coords[i][1] + 50)


    def buildFaceGendDet(self, img):
        gray = self._ip.grayScale(img)
        faces = self._builder.getDetector(gray)
        if len(faces) > 0:
            coords = self._builder.buildFacePredictor(faces)
            gender = self._builder.buildGenderPredictor(faces, img, self._models[1])
            for i in range(len(coords)):
                text = f"{gender[i]}"
                self._ip.drawRect(img, coords[i])
                self._ip.putText(img, text, coords[i][0], coords[i][1] + 50)

    def buildAgeGendDet(self, img):
        gray = self._ip.grayScale(img)
        faces = self._builder.getDetector(gray)
        if len(faces) > 0:
            coords = self._builder.buildFacePredictor(faces)
            gender = self._builder.buildGenderPredictor(faces, img, self._models[1])
            age = self._builder.buildAgePredictor(faces, img, self._models[0])
            for i in range(len(coords)):
                text = f"Age:{age[i]}, {gender[i]}"
                self._ip.putText(img, text, coords[i][0], coords[i][1] + 50)

    def buildFaceAgeDet(self, img):
        gray = self._ip.grayScale(img)
        faces = self._builder.getDetector(gray)
        if len(faces) > 0:
            coords = self._builder.buildFacePredictor(faces)
            age = self._builder.buildAgePredictor(faces, img, self._models[0])
            for i in range(len(coords)):
                text = f"Age:{age[i]}"
                self._ip.drawRect(img, coords[i])
                self._ip.putText(img, text, coords[i][0], coords[i][1] + 50)

    def buildAllDet(self, img):
        gray = self._ip.grayScale(img)
        faces = self._builder.getDetector(gray)
        if len(faces)>0:
            coords = self._builder.buildFacePredictor(faces)
            gender = self._builder.buildGenderPredictor(faces, img, self._models[1])
            age = self._builder.buildAgePredictor(faces, img, self._models[0])
            for i in range(len(coords)):
                text = f"Age:{age[i]}, {gender[i]}"
                self._ip.drawRect(img, coords[i])
                self._ip.putText(img, text, coords[i][0], coords[i][1]+50)
        else:
            pass

class FaceDetBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        self._product = fd.FaceDetect()

    @property
    def product(self):
        product = self._product
        self.reset()
        return product

    def getModels(self):
        return self._product.initModels()

    def getDetector(self, img):
        return self._product.detect(img)

    def buildFacePredictor(self, faces):
        return self._product.predictFace(faces)

    def buildAgePredictor(self, faces, img, model):
        blob = self._product.getFace(faces, img)
        return self._product.predictAge(blob, model)

    def buildGenderPredictor(self, faces, img, model):
        blob = self._product.getFace(faces, img)
        return self._product.predictGender(blob, model)
