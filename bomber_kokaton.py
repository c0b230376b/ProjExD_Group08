import os
import sys
import pygame as pg
from typing import Dict, List, Tuple

# ゲームウィンドウのサイズ設定
WIDTH, HEIGHT = 750, 750
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 方向キーに対応する移動量
DIRECTION_DELTA: Dict[int, Tuple[int, int]] = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (5, 0),
}

def check_bound(obj_rct: pg.Rect) -> Tuple[bool, bool]:
    """
    オブジェクトが画面内にあるかを判定する関数。

    Parameters:
    obj_rct (pg.Rect): チェック対象のオブジェクトの矩形領域 (pygame.Rectオブジェクト)。

    Returns:
    Tuple[bool, bool]: x方向とy方向の境界内かどうかを表す2つのブール値を含むタプル。
                       - (True, True): オブジェクトは画面内にある。
                       - (False, True): オブジェクトは横方向に画面外。
                       - (True, False): オブジェクトは縦方向に画面外。
                       - (False, False): オブジェクトは両方向に画面外。
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
    ゲームキャラクター「こうかとん」の動き、画像切り替え、描画を管理するクラス。
    """

    def __init__(self, initial_position: Tuple[int, int]) -> None:
        """
        Heroクラスのインスタンスを初期化し、こうかとんの画像、位置、初期状態を設定する。

        Parameters:
        initial_position (Tuple[int, int]): こうかとんの初期位置を表すタプル (x座標, y座標)。
        """
        self.images: Dict[str, List[pg.Surface]] = {
            "left": [pg.transform.rotozoom(pg.image.load("fig/5.png"), 0, 0.7), pg.transform.rotozoom(pg.image.load("fig/9.png"), 0, 0.7)],
            "right": [pg.transform.rotozoom(pg.image.load("fig/10.png"), 0, 0.7), pg.transform.rotozoom(pg.image.load("fig/11.png"), 0, 0.7)],
            "up": [pg.transform.rotozoom(pg.image.load("fig/14.png"), 0, 0.7), pg.transform.rotozoom(pg.image.load("fig/12.png"), 0, 0.7)],
            "down": [pg.transform.rotozoom(pg.image.load("fig/13.png"), 0, 0.7), pg.transform.rotozoom(pg.image.load("fig/15.png"), 0, 0.7)],
            "idle": pg.transform.rotozoom(pg.image.load("fig/4.png"), 0, 0.7)
        }
        self.rect: pg.Rect = self.images["idle"].get_rect(center=initial_position)
        self.direction: str = "idle"  # 初期方向
        self.frame_count: int = 0  # アニメーションフレーム用カウンタ

    def update(self, keys: pg.key.ScancodeWrapper, screen: pg.Surface) -> None:
        """
        こうかとんの位置と画像を更新し、画面に描画する。

        Parameters:
        keys (pg.key.ScancodeWrapper): プレイヤーからのキー入力情報。
        screen (pg.Surface): 描画対象のpygameの画面Surface。
        """
        movement_vector = [0, 0]
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

        # 移動
        self.rect.move_ip(movement_vector)
        if check_bound(self.rect) != (True, True):
            self.rect.move_ip(-movement_vector[0], -movement_vector[1])

        # フレームカウントに基づいて画像を切り替え
        self.frame_count += 1
        if self.direction == "idle":
            current_image = self.images["idle"]
        else:
            images = self.images[self.direction]
            current_image = images[self.frame_count // 10 % len(images)]

        screen.blit(current_image, self.rect)

def main() -> None:
    """
    ゲームのメインループを制御し、背景画像とこうかとんを表示する。
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
        clock.tick(25)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
