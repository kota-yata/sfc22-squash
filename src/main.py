import pyxel
from enum import Enum, auto

DISPLAY_WIDTH = 160
DISPLAY_HEIGHT = 120

BALL_RADIUS = 5

RACKET_LENGTH = 30
RACKET_DURATION = 3

class STATE (Enum):
  ON = auto()
  OVER = auto()

def edge_collision_detection(base_x, base_y, target_x, target_y):
  # 三平方の定理
  distance = pyxel.sqrt((target_x - base_x) * (target_x - base_x) + (target_y - base_y) + (target_y - base_y))
  if (distance <= BALL_RADIUS):
    return True
  else:
    return False

class Racket:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.length = RACKET_LENGTH
    self.duration = RACKET_DURATION
    # pyxel.image(0).load(0, 0, "racket.jpeg")

  def update(self):
    if (pyxel.btnp(pyxel.KEY_LEFT, 1, 1) and self.x > 0):
      self.x -= self.duration
    if (pyxel.btnp(pyxel.KEY_RIGHT, 1, 1) and self.x + self.length < DISPLAY_WIDTH):
      self.x += self.duration

  def draw(self):
    # pyxel.blt(self.x, self.y, 0, 0, 0, self.length, 30)
    pyxel.rect(self.x, self.y, self.length, 2, 1)

class Ball:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.radius = BALL_RADIUS
    self.duration = 2
    self.direction_x = -1
    self.direction_y = -1

  def update_position(self):
    self.x += self.direction_x * self.duration
    self.y += self.direction_y * self.duration

  def update(self, racket):
    # 下部境界
    if (self.y > (DISPLAY_HEIGHT - self.radius)):
      return STATE.OVER
    # ボールの位置がラケットより低い場合は方向転換を行わずゲームオーバーを待つ
    if self.y > racket.y:
      self.update_position()
      return STATE.ON
    # ラケットの表面に触れている場合は縦の方向転換と加速を行う
    if ((self.y + self.radius > racket.y) and (self.x + self.radius > racket.x) and (self.x + self.radius < racket.x + RACKET_LENGTH)):
      self.direction_y = -1
      self.duration += 0.2
    # 両サイドの境界
    if ((self.x > (DISPLAY_WIDTH - self.radius)) or (self.x < self.radius)):
      self.direction_x = -self.direction_x
    # 上部境界
    if (self.y < self.radius):
      self.direction_y = -self.direction_y
    # ボールとラケットの両端の衝突判定
    if (edge_collision_detection(self.x, self.y, racket.x, racket.y) or edge_collision_detection(self.x, self.y, racket.x + RACKET_LENGTH, racket.y)):
      self.direction_y = -1
    self.update_position()
    return STATE.ON

  def draw(self):
    pyxel.cls(0)
    pyxel.circ(self.x, self.y, self.radius, 1)

class App:
  def __init__(self, width, height):
    pyxel.init(width, height, title="squash")
    self.ball = Ball(50, 50)
    self.racket = Racket(60, 100)
    self.state = STATE.ON
    pyxel.run(self.update, self.draw)

  def update_on(self):
    self.state = self.ball.update(self.racket)

  def update_over(self):
    if pyxel.btnp(pyxel.KEY_SPACE):
      self.ball = Ball(50, 50)
      self.racket = Racket(60, 100)
      self.state = STATE.ON

  def update(self):
    if pyxel.btnp(pyxel.KEY_Q):
      pyxel.quit()
    if self.state == STATE.ON:
      # まだゲームオーバーでない場合はボールを動かす
      self.update_on()
    elif self.state == STATE.OVER:
      # ゲームオーバーになったら文字を表示してキー入力を待つ
      self.update_over()
    self.racket.update()

  def draw(self):
    pyxel.cls(0)
    if self.state == STATE.ON:
      self.ball.draw()
      self.racket.draw()
    if self.state == STATE.OVER:
      pyxel.text(60, 50, "GAME OVER...", 3)
      pyxel.text(30, 60, "PRESS SPACE TO TRY AGAIN", 5)

App(DISPLAY_WIDTH, DISPLAY_HEIGHT)
