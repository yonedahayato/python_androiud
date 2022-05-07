"""main.py
ClockApp

時間を表示するアプリ
"""

from kivy.app import App

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import (
    get_color_from_hex,
    get_random_color
)

from time import strftime
import random

def get_random_color_hex():
    color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])]
    return color[0]

class ClockApp(App):
    """ClockApp class
    時間を表示するアプリ
    """
    def __init__(self, **args):
        super().__init__(**args)

        self.color = get_random_color(alpha=1.0)
        self.change_rate = 0.2

    def update_color(self):
        for color_id in range(3):
            noise = random.uniform(1, -1)
            color_value = self.color[color_id] + noise * self.change_rate

            if color_value > 1:
                color_value -= noise * self.change_rate * 2
            elif color_value < -1:
                color_value += noise * self.change_rate * 2

            self.color[color_id] = color_value

        return self.color

    def update_time(self, nap):
        """update_time func
        時間を更新するメソッド
        """
        self.root.ids.time.text = strftime("[b]%H[/b]:%M:%S")

        color = self.update_color()
        Window.clearcolor = color

    def on_start(self):
        """on_start func
        schedule_interval で upldate_time を定期実行する
        """
        Clock.schedule_interval(self.update_time, 1)

if __name__ == "__main__":
    Window.size = (400, 700)
    ClockApp().run()