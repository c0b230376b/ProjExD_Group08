import os
import random
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


def random_position() -> list:
    """
    盤面領域内の四隅の座標タプルをシャッフルしたリストを返す
    戻り値：タプルのリスト
    """
    pos = [
        (75, 125), # 右上
        (75, HEIGHT - 75), # 右下
        (WIDTH - 75, 125), # 左上
        (WIDTH - 75, HEIGHT - 75), # 左下
    ]

    return random.sample(pos, len(pos))


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
            __class__.mvct = 15 # 0.25秒のクールタイム
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
    imgs = [pg.image.load(f"images/ufo/alien{i}.png") for i in range(1, 4)] # 敵画像三枚(3体分)

    def __init__(self, num: int, vx: tuple[int, int]):
        """
        敵のSurfaceの作成
        引数1 num: 画像指定用整数
        引数2 vx: Rectのcenter用タプル
        """
        super().__init__()
        self.num = num
        self.img = __class__.imgs[self.num]
        self.image = pg.transform.rotozoom(self.img, 0, 0.5) # サイズ微調整(仮画像用)
        self.rect = self.image.get_rect()
        self.rect.center = vx
        self.vx, self.vy = 0, 0
        self.mvct = 0 # 連続行動防止用クールタイム
        self.state = "move"  # move、bom(未実装)による行動

    def control(self):
        """
        的に関する動作制御を行う
        """
        img_key = { # 0度から反時計回りに定義
        (+50, 0): pg.transform.rotozoom(self.img, 0, 0.5), # 右
        (0, -50): pg.transform.rotozoom(self.image, 90, 1.0), # 上
        (-50, 0): pg.transform.flip(self.image, True, False), # 左
        (0, +50): pg.transform.rotozoom(self.image, -90, 1.0), # 下
        }
        move_list = [ # 移動方向
            (0, -50), # 上
            (0, +50), # 下
            (-50, 0), # 左
            (+50, 0), # 右
        ]

        # クールタイムの有無を確認する
        if self.mvct == 0:
            while True: # 移動成功までループ
                sum_mv = random.choice(move_list)
                self.rect.move_ip(sum_mv[0], sum_mv[1])
                # 盤面領域内判定による移動の可否
                if check_bound(self.rect) != (True, True):
                    self.rect.move_ip(-sum_mv[0], -sum_mv[1])
                    continue # 移動失敗
                break # 移動成功
            self.image = img_key[sum_mv]
            self.mvct = 15 # 0.25秒のクールタイム
        elif self.mvct > 0: # クールタイムカウント
            self.mvct -= 1

    def update(self):
        """
        敵の情報を更新する
        """
        __class__.control(self)


def main():
    """
    ゲームのメインループを制御する
    """
    pg.display.set_caption("ボンバーこうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("images/bg_ver.1.0.png") # 背景(完成版)
    position = random_position()
    hero = Hero(position[-1]) # 主人公(操作キャラ)
    enemys = pg.sprite.Group() # 敵のスプライトグループ
    for i, j in enumerate(position[:-1]): # Enemyクラスのインスタンス生成
        enemys.add(Enemy(i, j))
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, [0, 50])

        key_lst = pg.key.get_pressed()
        hero.update(key_lst, screen)
        enemys.update()
        enemys.draw(screen)

        pg.display.update()
        tmr += 1
        clock.tick(60) # framerateを60に設定


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
