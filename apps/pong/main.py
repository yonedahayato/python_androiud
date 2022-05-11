from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import (
    NumericProperty,
    ObjectProperty,
    ReferenceListProperty
)
from kivy.uix.widget import Widget
from kivy.vector import Vector

from random import randint

class PongPaddle(Widget):
    """PongPaddle class
    アプリに登場するラケット(=プレイヤー)に関する処理

    Attributes:
        score: ポイント
        speedup_rate(float): 加速度
    """

    score = NumericProperty(0)
    speedup_rate = 1.1

    def bounce_ball(self, ball):
        """bounce_ball method
        ラケットとボールが衝突したときの処理

        Attributes:
            ball: ボール

        Note:
            1. ボールの速度を取得 (vx, vy)
            2. offset の計算
            3. 跳ね返った後のボール速度 (bounced) を計算
            4. 加速処理
        """

        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)

            bounced = Vector(-1 * vx, vy)
            vel = bounced * self.speedup_rate

            ball.velocity = vel.x, vel.y + offset

class PongBall(Widget):
    """PongBall
    アプリに登場するボールに関する処理

    Attributes:
        velocity_x(NumericProperty): x方向の速度
        velocity_y(NumericProperty): y方向の速度
        velocity(ReferenceListProperty): 速度
    """

    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        """move method
        ボールの動作に関する処理
        """
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    """PongGame class
    このアプリの装飾を司る

    Attributes:
        ball(ObjectProperty): アプリに登場するボール
        player1(ObjectProperty): player1 (左) のラケット
        player2(ObjectProperty): player2 (右) のラケット
    """
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self, vel=(4, 0)):
        """serve_ball method

        ボールを中央に置き、サーブ (ボールが動く) する

        Atrributes:
            vel(tuple): サーブする速度
        """
        self.ball.center = self.center
        self.ball.velocity = Vector(vel).rotate(randint(0, 360))

    def update(self, dt):
        """update method
        定期実行される画面の更新処理

        Args:
            dt: 時間の情報

        Note:
            1. ボールを動かす (move)
            2. ボールとラケットが衝突したときの処理を実行 (bounce_ball)
            3. ボールと上下の壁に衝突したときの処理を実行
            4. 各プレイヤーが得点したときの処理
        """
        
        self.ball.move()

        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.right > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        """on_touch_move method
        ラケットを動かす処理

        Args:
            touch: カーソルなどからの画面への接触
        """
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y

        if touch.x > self.width * (2 / 3):
            self.player2.center_y = touch.y


class PongApp(App):
    """PongApp class
    このアプリの設定、起動
    """

    def build(self):
        """build method
        このアプリの起動時の処理

        Note:
            1. ボールをサーブして、動かす

            2. PongGame class の update method を
            schedule_interval を利用し、定期実行に登録
        """
        # Window.size = (1020, 480)
        Window.fullscreen = 'auto'
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

if __name__ == "__main__":
    PongApp().run()