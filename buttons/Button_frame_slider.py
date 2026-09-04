from PyQt5.QtCore import QObject


class Button_frame_slider(QObject):

    def __init__(self, slider, slider_input):
        super().__init__()

        self.slider = slider
        self.slider_input = slider_input


        self.start_frame = slider.minimum()

    # t.4
    def start_value(self):
        self.set_value(self.start_frame)

    # t.5
    def down_10(self):
        self.set_value(self.slider.value() - 10)

    # t.6
    def down_1(self):
        self.set_value(self.slider.value() - 1)

    # t.8
    def up_1(self):
        self.set_value(self.slider.value() + 1)

    # t.9
    def up_10(self):
        self.set_value(self.slider.value() + 10)

    # t.10
    def max_value(self):
        self.set_value(self.slider.maximum())


    def set_value(self, value):

        value = max(self.slider.minimum(), value)
        value = min(self.slider.maximum(), value)

        self.slider.setValue(value)

        self.slider_input.setText(str(value))
