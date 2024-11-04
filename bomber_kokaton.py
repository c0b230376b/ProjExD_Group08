import os
import sys

import pygame as pg


WIDTH, HEIGHT = 750, 700
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し，真理値タプルを返す関数
    引数：こうかとんやその他動的オブジェクトのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True

    #盤面領域判定
    if obj_rct.left < 50 or WIDTH - 50 < obj_rct.right: # ブロックにぶつかったら止まるように
        yoko = False
    if obj_rct.top < 100 or HEIGHT - 50< obj_rct.bottom:
        tate = False

    #盤面領域内障害物判定
    for i in range(6):
        num = 100*i
        if (100 + num) < obj_rct.left < (150 + num) or (100 + num) < obj_rct.right < (150 + num):
            for j in range(5):
                num = 100 * j
                if 150 + num < obj_rct.top < 200 + num or 150 + num < obj_rct.bottom < 200 + num:
                    yoko = False
                    tate = False

    return yoko, tate


class Hero:
    """
    ゲームキャラクター（こうかとん）に関するクラス
    """
    delta = {  # 押下キーと移動量の辞書
        pg.K_UP: (0, -50),
        pg.K_DOWN: (0, +50),
        pg.K_LEFT: (-50, 0),
        pg.K_RIGHT: (+50, 0),
    }
    img0 = pg.transform.rotozoom(pg.image.load("images/Kokaton/3.png"), 0, 0.9)
    img = pg.transform.flip(img0, True, False)  # デフォルトのこうかとん（右向き）
    imgs = {  # 0度から反時計回りに定義
        (+50, 0): img,  # 右
        (+50, -50): pg.transform.rotozoom(img, 45, 0.9),  # 右上
        (0, -50): pg.transform.rotozoom(img, 90, 0.9),  # 上
        (-50, -50): pg.transform.rotozoom(img0, -45, 0.9),  # 左上
        (-50, 0): img0,  # 左
        (-50, +50): pg.transform.rotozoom(img0, 45, 0.9),  # 左下
        (0, +50): pg.transform.rotozoom(img, -90, 0.9),  # 下
        (+50, +50): pg.transform.rotozoom(img, -45, 0.9),  # 右下
    }
    mvct = 0 # 移動時のためのクールタイム

    def __init__(self, xy: tuple[int, int]): # こうかとんの画像、位置、状態を初期化する
        """
        こうかとん画像Surfaceを生成する
        引数 xy：こうかとん画像の初期位置座標タプル
        """
        self.img = __class__.imgs[(+50, 0)]
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.center = xy
        self.dire = (+50, 0)

    def change_img(self, num: int, screen: pg.Surface):
        """
        こうかとん画像を切り替え，画面に転送する
        引数1 num：こうかとん画像ファイル名の番号
        引数2 screen：画面Surface
        """
        self.img = pg.transform.rotozoom(pg.image.load(f"fig/{num}.png"), 0, 0.9)
        screen.blit(self.img, self.rct)

    def update(self, key_lst: list[bool], screen: pg.Surface):
        """
        押下キーに応じてこうかとんを移動させる
        引数1 key_lst：押下キーの真理値リスト
        引数2 screen：画面Surface
        """
        sum_mv = [0, 0]
        if __class__.mvct == 0: # 連続移動防止用カウント
            for k, mv in __class__.delta.items():
                if key_lst[k]:
                    sum_mv[0] += mv[0]
                    sum_mv[1] += mv[1]
            self.rct.move_ip(sum_mv)
            __class__.mvct = 5 # 5カウント分のクールタイム
        elif 0 < __class__.mvct:
            __class__.mvct -= 1

        #盤面領域内判定に応じた移動の可否
        if check_bound(self.rct) != (True, True):
            self.rct.move_ip(-sum_mv[0], -sum_mv[1])
        if not (sum_mv[0] == 0 and sum_mv[1] == 0):
            self.img = __class__.imgs[tuple(sum_mv)]
            self.dire = sum_mv # 更新
        screen.blit(self.img, self.rct)


class Enemy(pg.sprite.Sprite):
    """
    敵に関するクラス
    """
    def __init__(self):
        pass


def main():
    """
    ゲームのメインループを制御する
    """
    pg.display.set_caption("ボンバーこうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("images/bg_ver.1.0.png") # 背景(完成版)
    hero = Hero((75, 125))
    enemys = pg.sprite.Group() # 敵のスプライトグループ
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, [0, 50])

        key_lst = pg.key.get_pressed()
        hero.update(key_lst, screen)

        pg.display.update()
        tmr += 1
        clock.tick(10)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
