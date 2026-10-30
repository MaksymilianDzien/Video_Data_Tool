from PyQt5.QtCore import QObject, QTimer
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut


class Button_frame_slider(QObject):

    #paly time (space)
    play_interval_ms = 80

    def __init__(self, slider, slider_input):
        super().__init__()

        self.slider = slider
        self.slider_input = slider_input


        self.start_frame = slider.minimum()

        #time is start in first frame
        self.play_timer = QTimer(self)
        self.play_timer.setInterval(self.play_interval_ms)
        self.play_timer.timeout.connect(self.play_next_frame)

        #last time frame
        self.play_last_value = None

        #all shortcut for slider buttons
        self.buttons_slider_all_shortcut()

    # t.4
    def start_value(self):
        self.set_value(self.start_frame)

    # t.5
    def down_10(self):
        self.set_value(self.slider.value() - 10)

    # t.6
    def down_1(self):
        self.set_value(self.slider.value() - 1)

    # t.7
    #star and stop
    def play_frames(self):

        #second pres stop timer
        if self.play_timer.isActive():
            self.stop_play()
            return

        #end play in is last frame
        if self.slider.value() >= self.slider.maximum():
            return

        self.play_last_value = self.slider.value()
        self.play_timer.start()

    # t.8
    def up_1(self):
        self.set_value(self.slider.value() + 1)

    # t.9
    def up_10(self):
        self.set_value(self.slider.value() + 10)

    # t.10
    def max_value(self):
        self.set_value(self.slider.maximum())

    #set value to slider
    def set_value(self, value):

        value = max(self.slider.minimum(), value)
        value = min(self.slider.maximum(), value)

        self.slider.setValue(value)

        self.slider_input.setText(str(value))

    #one next frame play
    def play_next_frame(self):

        #if frame is move by hand then stop play
        if self.slider.value() != self.play_last_value:
            self.stop_play()
            return

       #last frame end play
        if self.slider.value() >= self.slider.maximum():
            self.stop_play()
            return

        self.set_value(self.slider.value() + 1)
        self.play_last_value = self.slider.value()

        #last frame
        if self.slider.value() >= self.slider.maximum():
            self.stop_play()

    #stop playing frames
    def stop_play(self):
        self.play_timer.stop()
        self.play_last_value = None


    #all shortcut function
    def buttons_slider_all_shortcut(self):

        #Shift + left
        self.start_shortcut = QShortcut(QKeySequence("Shift+Left"), self.slider)
        self.start_shortcut.activated.connect(self.start_value)

        #Ctrl + left
        self.down_10_shortcut = QShortcut(QKeySequence("Ctrl+Left"), self.slider)
        self.down_10_shortcut.activated.connect(self.down_10)

        #left
        self.down_1_shortcut = QShortcut(QKeySequence("Left"), self.slider)
        self.down_1_shortcut.activated.connect(self.down_1)

        #space
        self.play_shortcut = QShortcut(QKeySequence("Space"), self.slider)
        self.play_shortcut.activated.connect(self.play_frames)

        #right
        self.up_1_shortcut = QShortcut(QKeySequence("Right"), self.slider)
        self.up_1_shortcut.activated.connect(self.up_1)

        #Ctrl + right
        self.up_10_shortcut = QShortcut(QKeySequence("Ctrl+Right"), self.slider)
        self.up_10_shortcut.activated.connect(self.up_10)

        #Shift + right
        self.max_shortcut = QShortcut(QKeySequence("Shift+Right"), self.slider)
        self.max_shortcut.activated.connect(self.max_value)