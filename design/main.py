from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from kivy.uix.checkbox import CheckBox
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import ObjectProperty
import kivy.core.text
import cv2
from kivy.base import EventLoop
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.window import Window
import os
import sys
import Builder as builder


class States:
    isFace = False
    isGender = False
    isAge = False
    isRelease = False

class KivyCamera(Image):
    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = None
        self.builder = builder.FaceDetBuilder()
        self.director = builder.Director(self.builder)

    def start(self, capture, fps=60):
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def stop(self):
        Clock.unschedule(self.update)
        self.capture.release()
        self.capture = None
        States.isRelease = False

    def update(self, dt):
        if States.isRelease:
            self.stop()
        else:
            return_value, frame = self.capture.read()
            if return_value:
                w, h = frame.shape[1], frame.shape[0]
                if not self.texture or self.texture.width != w or self.texture.height != h:
                    self.texture = Texture.create(size=(w, h))
                    self.texture.flip_vertical()
                if (States.isFace is False and States.isGender is False and States.isAge is False) or (States.isFace is True and States.isGender is True and States.isAge is True):
                    self.director.buildAllDet(frame)
                elif States.isFace is True and States.isGender is False and States.isAge is False:
                    self.director.buildFaceDet(frame)
                elif States.isFace is True and States.isGender is True and States.isAge is False:
                    self.director.buildFaceGendDet(frame)
                elif States.isFace is True and States.isGender is False and States.isAge is True:
                    self.director.buildFaceAgeDet(frame)
                elif States.isFace is False and States.isGender is False and States.isAge is True:
                    self.director.buildAgeDet(frame)
                elif States.isFace is False and States.isGender is True and States.isAge is False:
                    self.director.buildGendDet(frame)
                elif States.isFace is False and States.isGender is True and States.isAge is False:
                    self.director.buildGendDet(frame)
                elif States.isFace is False and States.isGender is True and States.isAge is True:
                    self.director.buildAgeGendDet(frame)
                self.texture.blit_buffer(frame.tobytes(), colorfmt='bgr')
                self.canvas.ask_update()
capture = None

class MenuScreen(Screen):
    def init_qrtest(self):
        pass

    def dostart(self, *largs):
        global capture
        capture = cv2.VideoCapture(0)
        self.ids.qrcam.start(capture)

    def doexit(self):
        States.isRelease = True


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._request_android_permissions()

    def closeApp(self):
        App.get_running_app().stop()


    @staticmethod
    def is_android():
        return platform == 'android'

    def _request_android_permissions(self):
        if not self.is_android():
            return
        from android.permissions import request_permission, Permission
        request_permission(Permission.CAMERA)


class SettingsScreen(Screen):
    def checkbox_click1(self, instance, value):
        if value is True:
            print("Checkbox1 Checked")
            States.isFace = True
        else:
            print("Checkbox1 Unchecked")
            States.isFace = False
    def checkbox_click2(self, instance, value):
        if value is True:
            print("Checkbox2 Checked")
            States.isGender = True
        else:
            print("Checkbox2 Unchecked")
            States.isGender = False
    def checkbox_click3(self, instance, value):
        if value is True:
            print("Checkbox3 Checked")
            States.isAge = True
        else:
            print("Checkbox3 Unchecked")
            States.isAge = False


class ScreenManager(ScreenManager):
    pass

buildKV = Builder.load_file("Test.kv")
class TestApp(App):
    def build(self):
        return buildKV

if __name__ == '__main__':
    TestApp().run()