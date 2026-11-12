from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
from PyQt5.QtWidgets import QWidget, QStyle, QStyleOptionSlider
from matplotlib.pyplot import tick_params


class Slider_ruler(QWidget):

    #c0392b
    #style of line
    ruler_color = QColor("#ffffff")
    major_tick_length = 7
    minor_tick_length = 3
    label_size = 7
    label_width = 60
    label_height = 12

    #height of ruler
    height_of_ruler = 22

    margin = 14

    #shandle width
    default_width_of_handler = 10

    def __init__(self, slider_ruler, parent=None):
        super().__init__(parent)

        #slider
        self.slider_ruler = slider_ruler

        #set height ruler
        self.setFixedHeight(self.height_of_ruler)

        #change frame rate
        self.slider_ruler.rangeChanged.connect(lambda minimum_value, maximum_value: self.update())

    #get positions of the groove and the slider handle
    def get_groove_and_handle_of_slider(self):

        #create Qstyle option slider
        slider_ruler_option = QStyleOptionSlider()
        #set font
        slider_ruler_option.initFrom(self.slider_ruler)
        #set orientation
        slider_ruler_option.orientation = Qt.Horizontal
        #set max
        slider_ruler_option.minimum = self.slider_ruler.minimum()
        #set min
        slider_ruler_option.maximum = self.slider_ruler.maximum()
        #change value
        slider_ruler_option.sliderPosition = self.slider_ruler.sliderPosition()
        slider_ruler_option.sliderValue = self.slider_ruler.value()
        #scale of ruler
        slider_ruler_option.singleStep = self.slider_ruler.singleStep()
        slider_ruler_option.pageStep = self.slider_ruler.pageStep()
        #left to right
        slider_ruler_option.upsideDown = self.slider_ruler.invertedAppearance()
        #slader
        slider_ruler_option.subControls = QStyle.SC_SliderGroove | QStyle.SC_SliderHandle

        #set style
        slider_ruler_style = self.slider_ruler.style()
        #first and last groove rect
        groove_rect = slider_ruler_style.subControlRect(QStyle.CC_Slider, slider_ruler_option, QStyle.SC_SliderGroove, self.slider_ruler)
        # first and last handle rect
        handle_rect = slider_ruler_style.subControlRect(QStyle.CC_Slider, slider_ruler_option, QStyle.SC_SliderHandle, self.slider_ruler)

        return groove_rect, handle_rect, slider_ruler_option

    #draw markings and numbers below the slider.
    def paintEvent(self, event):

        #get groove handle and slider_option
        groove_rect, handle_rect, slider_ruler_option = self.get_groove_and_handle_of_slider()

        #center of the handle moves along the width of the groove.
        handle_width = handle_rect.width() if handle_rect.width() > 0 else self.default_width_of_handler
        span_pixels = groove_rect.width() - handle_width
        #if sider is too small them dont't draw
        if span_pixels <= 0:
            return
        #get a list of tallies
        ruler_ticks = compute_ruler_ticks(self.slider_ruler.minimum(), self.slider_ruler.maximum(), span_pixels)

        #provided that the slider is positioned to the right of the ruler
        slider_ruler_left = self.slider_ruler.mapToGlobal(QPoint(0, 0)).x() - self.mapToGlobal(QPoint(0, 0)).x()

        #create painter
        slider_painter = QPainter(self)
        #set pen
        slider_painter.setPen(QPen(self.ruler_color, 1))

        #set style
        slider_label_font = QFont(self.font())
        slider_label_font.setPointSize(self.label_size)
        slider_painter.setFont(slider_label_font)

        #tick begin 1 px from the top edge of the ruler.
        tick_top = 1

        #loop for all tick
        for tick_value, is_major in ruler_ticks:

            #postion of tick in px
            tick_x = slider_ruler_left + groove_rect.x() + handle_width // 2 + QStyle.sliderPositionFromValue(
                self.slider_ruler.minimum(), self.slider_ruler.maximum(), tick_value, span_pixels, slider_ruler_option.upsideDown)

            #set long tick in px
            tick_length = self.major_tick_length if is_major else self.minor_tick_length
            slider_painter.drawLine(tick_x, tick_top, tick_x, tick_top + tick_length)

            #number is right below the large tick
            if is_major:
                label_left = tick_x - self.label_width // 2
                label_rect = QRect(label_left, tick_top + tick_length + 1, self.label_width, self.label_height)
                slider_painter.drawText(label_rect, Qt.AlignHCenter | Qt.AlignTop, str(tick_value))
        #end of painter and stop drawing
        slider_painter.end()



#retrun counting ticks
def compute_ruler_ticks(ticks_minimum, ticks_maximum, ticks_span_pixels, min_label_distance=55, min_tick_distance=5):

    #set intervals btw min and max
    value_count = ticks_maximum - ticks_minimum

    #if is one frame then return  one ticks
    if value_count <= 0 or ticks_span_pixels <= 0:
        return [(ticks_minimum, True)]

    #how many values fit within min_label_distance pixels
    raw_step = value_count * min_label_distance / ticks_span_pixels

    #smallest good step
    label_step = None
    decade = 1
    #select good step
    while label_step is None:
        for factor in (1, 2, 5):
            if factor * decade >= raw_step:
                label_step = factor * decade
                break
        decade *= 10

    #into how many parts do we divide the step using small tick
    first_digit = int(str(label_step)[0])
    divisions = {1: 5, 2: 4, 5: 5}[first_digit]
    minor_step = label_step // divisions

    #small tick marks
    if label_step % divisions != 0 or minor_step < 1 or minor_step * ticks_span_pixels / value_count < min_tick_distance:
        minor_step = label_step

    #large tick
    #min distance
    min_value_distance = min_label_distance * 0.8 * value_count / ticks_span_pixels
    #first and last have number
    tick_major_values = {ticks_minimum, ticks_maximum}
    #first multiple
    tick_first_multiple = (ticks_minimum + label_step - 1) // label_step * label_step
    for value in range(tick_first_multiple, ticks_maximum + 1, label_step):

        #chek if is btw min and max
        if value - ticks_minimum < min_value_distance or ticks_maximum - value < min_value_distance:
            continue
        #add value
        tick_major_values.add(value)

    #small tick between large ones
    ticks = {value: True for value in tick_major_values}
    if minor_step < label_step:
        first_minor = (ticks_minimum + minor_step - 1) // minor_step * minor_step
        for value in range(first_minor, ticks_maximum + 1, minor_step):
            if value not in ticks:
                ticks[value] = False
    #retrun all tick
    return sorted(ticks.items())

