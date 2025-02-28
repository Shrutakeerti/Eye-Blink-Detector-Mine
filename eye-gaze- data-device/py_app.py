import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
import cv2
import numpy as np
import tensorflow as tf



class childApp(GridLayout):
    def __init__(self, **kwargs):
        super(childApp, self).__init__(**kwargs)
        self.cols = 2

        self.add_widget(Label(text="Student Name"))
        self.s_name = TextInput()
        self.add_widget(self.s_name)

        self.add_widget(Label(text="Student Marks"))
        self.s_marks = TextInput()
        self.add_widget(self.s_marks)

        self.add_widget(Label(text="Student Gender"))
        self.s_gender = TextInput()
        self.add_widget(self.s_gender)

        self.press = Button(text="Click Me")
        self.press.bind(on_press=self.click_me)
        self.add_widget(self.press)

        self.gaze_label = Label(text="Gaze Coordinates: (0, 0)")
        self.add_widget(self.gaze_label)

      
        self.webcam_feed = Image()
        self.add_widget(self.webcam_feed)

        
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update_gaze, 1.0 / 30.0)  # 30 FPS

    def click_me(self, instance):
        print("Name of the student is " + self.s_name.text)
        print("Marks of the student is " + self.s_marks.text)
        print("Gender of the student is " + self.s_gender.text)
        print("")

    def update_gaze(self, dt):
        ret, frame = self.capture.read()
        if ret:
           
            buf = cv2.flip(frame, 0).tobytes()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.webcam_feed.texture = image_texture

           
            gaze_coords = self.process_frame(frame)
            self.gaze_label.text = f'Gaze Coordinates: {gaze_coords}'

    def process_frame(self, frame):
        
        gaze_x, gaze_y = 100, 200  # Dummy values
        return gaze_x, gaze_y

    def on_stop(self):
        self.capture.release()

class parentApp(App):
    def build(self):
        return childApp()

if __name__ == "__main__":
    parentApp().run()
