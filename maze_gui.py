from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.uix.label import Label

from kivy.graphics.texture import Texture
from kivy.graphics import Color
from kivy.graphics import Rectangle

from kivy.core.window import Window
from kivy.config import Config

from kivy.clock import Clock
from kivy.app import App

from PIL import ImageGrab
import os
import cv2
import numpy as np

from src import maze_solver

os.chdir("C:\\Users\\Ahmet\\PycharmProjects\\maze_solving\\mazes_img")


class KivyPIL(Image):
    def __init__(self, fps, **kwargs):
        super(KivyPIL, self).__init__(**kwargs)
        self.maze_solver = maze_solver.MazeSolver()
        self.frame_per_second_value = 25
        self.fps_controller = Clock.schedule_interval(self.update, 1.0 / self.frame_per_second_value)

        self.size_hint_x = 1
        self.size_hint_y = .9

    def update(self, dt):
        frame = self.maze_solver.implement_movement()
        frame = cv2.resize(frame, dsize=(int(Window.size[0] * 1.1), int(Window.size[1] * .7)),
                           interpolation=cv2.INTER_CUBIC)
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        image_texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.texture = image_texture

    def change_fps_value(self, instance, value):
        self.fps_controller.cancel()
        self.fps_controller = Clock.schedule_interval(self.update, 1.0 / value)


class BackgroundLayout(StackLayout):
    def __init__(self):
        super(BackgroundLayout, self).__init__()


class ChildBackground(GridLayout):
    def __init__(self):
        super(ChildBackground, self).__init__()


class AnimationLabel(Label):
    def __init__(self):
        super(AnimationLabel, self).__init__()
        self.text = "MAZE SOLVER"
        self.underline = True
        self.bold = True
        self.font_size = 30
        self.rect = Rectangle(pos=self.pos, size=self.size)
        self.canvas.add(Color(0, 1, 1, 0.5))
        self.canvas.add(self.rect)

        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class MazeSolverApp(App):
    def __init__(self):
        super(MazeSolverApp, self).__init__()

        self.background = BackgroundLayout()
        self.background.rows = 2

        self.animation_part = ChildBackground()
        self.animation_part.size_hint_x = 1
        self.animation_part.size_hint_y = .7
        self.animation_part.cols = 1
        self.animation_part.rows = 2

        self.controller_panel = ChildBackground()
        self.controller_panel.size_hint_x = 1
        self.controller_panel.size_hint_y = .3
        self.controller_panel.cols = 2
        self.controller_panel.rows = 5

        self.speed_control_label = Label(text="Speed", font_size='20sp')
        self.speed_control_slider = Slider(min=1, max=60, value=24)

    def change_label_text(self, instance, value):
        self.speed_control_label.text = str(value)

    def build(self):
        my_camera = KivyPIL(fps=60)

        shape = my_camera.maze_solver.maze.shape
        Window.size = (shape[0]*2, shape[1]*2)

        animation_label = AnimationLabel()
        animation_label.size_hint_x = 1
        animation_label.size_hint_y = .1

        print("Position: ", animation_label.pos)
        print("Size: ", animation_label.size)
        # animation_label.canvas(Color(0, 1, 1, .5), Rectangle(pos=animation_label.pos, size=animation_label.size))

        self.speed_control_slider.bind(value=my_camera.change_fps_value)

        self.animation_part.add_widget(animation_label)
        self.animation_part.add_widget(my_camera)

        self.controller_panel.add_widget(self.speed_control_label)
        self.controller_panel.add_widget(self.speed_control_slider)

        self.background.add_widget(self.animation_part)
        self.background.add_widget(self.controller_panel)

        return self.background

if __name__ == '__main__':
    MazeSolverApp().run()
