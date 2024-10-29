import os
import sys
import pygame as pg

WIDTH, HEIGHT = 800, 800
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DIRECTION_DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (5, 0),
}


class KoukaTon:
    """こうかとんキャラクターの動きと描画を管理するクラス"""

    def __init__(self, left_images, right_images, up_images, down_images, initial_position):
        """こうかとんの画像、位置、状態を初期化する"""
        self.images = {
            "left": left_images,      # 左向きの画像リスト
            "right": right_images,    # 右向きの画像リスト
            "up": up_images,          # 上方向の画像リスト
            "down": down_images,      # 下方向の画像リスト
            "idle": pg.image.load("fig/4.png")  # 静止時の画像
        }
        self.rect = self.images["idle"].get_rect()  # 画像の初期位置
        self.rect.center = initial_position
        self.current_image = self.images["idle"]  # 現在表示中の画像
        self.frame_count = 0  # フレーム数カウンタ

    def move(self, keys):
        """キー入力に応じてこうかとんを移動させ、画像を切り替える"""
        movement_vector = [0, 0]  # 各方向の移動量を格納するベクトル
        # 左右の移動
        if keys[pg.K_LEFT]:
            movement_vector[0] += DIRECTION_DELTA[pg.K_LEFT][0]
            self.current_image = self.get_current_image("left")
        elif keys[pg.K_RIGHT]:
            movement_vector[0] += DIRECTION_DELTA[pg.K_RIGHT][0]
            self.current_image = self.get_current_image("right")
        # 上下の移動
        elif keys[pg.K_UP]:
            movement_vector[1] += DIRECTION_DELTA[pg.K_UP][1]
            self.current_image = self.get_current_image("up")
        elif keys[pg.K_DOWN]:
            movement_vector[1] += DIRECTION_DELTA[pg.K_DOWN][1]
            self.current_image = self.get_current_image("down")
        else:
            # 移動していないときは静止状態に戻す
            self.current_image = self.images["idle"]

        # 移動量に基づいて位置を更新
        self.rect.move_ip(movement_vector)
        self.frame_count += 1  # 常にフレーム数を更新

    def get_current_image(self, direction):
        """指定方向ごとのフレーム画像を取得するメソッド"""
        return self.images[direction][self.frame_count // 10 % 2]  # 10フレームごとに切り替え

    def draw(self, surface):
        """画面上に現在の画像を描画する"""
        surface.blit(self.current_image, self.rect)


def main():
    """ゲームのメインループを制御する"""
    pg.display.set_caption("ボンバーこうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")

    # 左右、上下移動用の画像を読み込む
    left_images = [pg.image.load("fig/5.png"), pg.image.load("fig/9.png")]
    right_images = [pg.image.load("fig/10.png"), pg.image.load("fig/11.png")]
    up_images = [pg.image.load("fig/14.png"), pg.image.load("fig/12.png")]
    down_images = [pg.image.load("fig/13.png"), pg.image.load("fig/15.png")]

    # こうかとんのインスタンスを作成
    kouka_ton = KoukaTon(left_images, right_images, up_images, down_images, (300, 200))
    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, [0, 0])  # 背景画像を描画
        keys = pg.key.get_pressed()  # 現在のキーの状態を取得

        kouka_ton.move(keys)  # こうかとんの移動処理
        kouka_ton.draw(screen)  # こうかとんを画面に描画

        pg.display.update()  # 画面を更新
        clock.tick(50)  # フレームレートを制御


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()