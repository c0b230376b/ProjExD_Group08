import os
import sys
import pygame as pg

# ゲームウィンドウのサイズ設定
WIDTH, HEIGHT = 750, 700
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 方向キーに対応する移動量
DIRECTION_DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (5, 0),
}

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内にあるかを判定する関数。
    引数:
        obj_rct (pg.Rect): 位置を判定したいオブジェクトの矩形（こうかとんやアイテムなど）。
    戻り値:
        tuple[bool, bool]: 横方向および縦方向のはみ出しを判定するブール値タプル。
                          横方向: Trueなら画面内、Falseなら画面外。
                          縦方向: Trueなら画面内、Falseなら画面外。
    """
    yoko, tate = True, True
    if obj_rct.left < 50 or WIDTH - 50 < obj_rct.right:
        yoko = False
    if obj_rct.top < 100 or HEIGHT - 50 < obj_rct.bottom:
        tate = False
    for i in range(6):
        num = 100 * i
        if (100 + num) < obj_rct.left < (150 + num) or (100 + num) < obj_rct.right < (150 + num):
            for j in range(5):
                num = 100 * j
                if 150 + num < obj_rct.top < 200 + num or 150 + num < obj_rct.bottom < 200 + num:
                    yoko = False
                    tate = False
    return yoko, tate

class Hero:
    """
    ゲームキャラクター「こうかとん」の動き、画像切り替え、描画を管理するクラス
    """

    def __init__(self, initial_position):
        """
        Heroクラスのインスタンスを初期化し、こうかとんの画像、位置、初期状態を設定する。
        引数:
            initial_position (tuple[int, int]): こうかとんの初期位置（x, y座標のタプル）。
        """
        self.images = {
            "left": [pg.image.load("fig/5.png"), pg.image.load("fig/9.png")],
            "right": [pg.image.load("fig/10.png"), pg.image.load("fig/11.png")],
            "up": [pg.image.load("fig/14.png"), pg.image.load("fig/12.png")],
            "down": [pg.image.load("fig/13.png"), pg.image.load("fig/15.png")],
            "idle": pg.image.load("fig/3.png")  # 静止時の画像
        }
        self.rect = self.images["idle"].get_rect()
        self.rect.center = initial_position
        self.current_image = self.images["idle"]
        self.frame_count = 0
        self.direction = "idle"  # 初期状態は静止

    def move(self, keys):
        """
        キーボード入力に基づいてこうかとんの移動と画像の方向を変更する。
        引数:
            keys (list[bool]): 現在押されているキーの状態（pygame.key.get_pressed()の結果）。
        """
        movement_vector = [0, 0]  # 各方向の移動量を格納するベクトル
        if keys[pg.K_LEFT]:
            movement_vector[0] += DIRECTION_DELTA[pg.K_LEFT][0]
            self.direction = "left"
        elif keys[pg.K_RIGHT]:
            movement_vector[0] += DIRECTION_DELTA[pg.K_RIGHT][0]
            self.direction = "right"
        elif keys[pg.K_UP]:
            movement_vector[1] += DIRECTION_DELTA[pg.K_UP][1]
            self.direction = "up"
        elif keys[pg.K_DOWN]:
            movement_vector[1] += DIRECTION_DELTA[pg.K_DOWN][1]
            self.direction = "down"
        else:
            self.direction = "idle"  # 移動がない場合は静止


        self.rect.move_ip(movement_vector)
        if check_bound(self.rect) != (True, True):
            self.rect.move_ip(-movement_vector[0], -movement_vector[1])  

        self.frame_count += 1  

    def get_current_image(self):
        """
        現在の移動方向に基づいてアニメーション用の画像を取得する。
        戻り値:
            pg.Surface: 現在のアニメーション状態に応じた画像。
        """
        if self.direction == "idle":
            return self.images["idle"]
        images = self.images[self.direction]
        return images[self.frame_count // 10 % len(images)]  

    def update(self, keys, screen):
        """
        こうかとんの位置と画像を更新し、画面に描画する。
        引数:
            keys (list[bool]): 現在押されているキーの状態（pygame.key.get_pressed()の結果）。
            screen (pg.Surface): 描画対象の画面。
        """
        self.move(keys)  
        self.current_image = self.get_current_image() 
        screen.blit(self.current_image, self.rect) 
def main():
    """
    ゲームのメインループを制御し、背景画像とこうかとんを表示する。
    pygameのイベントループを使用して、キー入力、画面更新、フレームレート管理を行う。
    """
    pg.display.set_caption("ボンバーこうかとん") 
    screen = pg.display.set_mode((WIDTH, HEIGHT)) 
    bg_img = pg.image.load("images/bg_ver.1.0.png")  

    hero = Hero((75, 125)) 
    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, [0, 50]) 
        keys = pg.key.get_pressed() 
        hero.update(keys, screen)

        pg.display.update()
        clock.tick(50)  

if __name__ == "__main__":
    pg.init() 
    main() 
    pg.quit()
    sys.exit()
