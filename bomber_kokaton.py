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
            "idle": pg.image.load("images/Kokaton/4.png")  # 静止時の画像
        }
        self.rect = self.images["idle"].get_rect()  # 画像の初期位置
        self.rect.center = initial_position
        self.current_image = self.images["idle"]  # 現在表示中の画像
        self.frame_count = 0  # フレーム数カウンタ

    def move(self, keys):
        """キー入力に応じてこうかとんを移動させ、画像を切り替える"""
        movement_vector = [0, 0]  # 各方向の移動量を格納するベクトル
        if keys[pg.K_LEFT]:
            movement_vector[0] += DIRECTION_DELTA[pg.K_LEFT][0]
            self.current_image = self.get_current_image("left")
        elif keys[pg.K_RIGHT]:
            movement_vector[0] += DIRECTION_DELTA[pg.K_RIGHT][0]
            self.current_image = self.get_current_image("right")
        elif keys[pg.K_UP]:
            movement_vector[1] += DIRECTION_DELTA[pg.K_UP][1]
            self.current_image = self.get_current_image("up")
        elif keys[pg.K_DOWN]:
            movement_vector[1] += DIRECTION_DELTA[pg.K_DOWN][1]
            self.current_image = self.get_current_image("down")
        else:
            self.current_image = self.images["idle"]

        self.rect.move_ip(movement_vector)
        self.frame_count += 1

    def get_current_image(self, direction):
        """指定方向ごとのフレーム画像を取得するメソッド"""
        return self.images[direction][self.frame_count // 10 % 2]  # 10フレームごとに切り替え

    def draw(self, surface):
        """画面上に現在の画像を描画する"""
        surface.blit(self.current_image, self.rect)


class Score:
    """ゲームのスコアを管理するクラス"""

    def __init__(self, font_size=30, initial_score=0):
        self.score = initial_score
        self.font = pg.font.Font(None, font_size)
        self.color = (255, 255, 255)  # 白色の文字
        self.position = (10, 10)  # 左上隅に表示

    def increase(self, points=1):
        self.score += points

    def reset(self):
        self.score = 0

    def draw(self, surface):
        score_text = self.font.render(f"Score: {self.score}", True, self.color)
        surface.blit(score_text, self.position)


def main():
    """ゲームのメインループを制御する"""
    pg.display.set_caption("ボンバーこうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("images/bg_ver.1.0.png")

    # 左右、上下移動用の画像を読み込む
    left_images = [pg.image.load("images/Kokaton/5.png"), pg.image.load("images/Kokaton/9.png")]
    right_images = [pg.image.load("images/Kokaton/10.png"), pg.image.load("images/Kokaton/11.png")]
    up_images = [pg.image.load("images/Kokaton/14.png"), pg.image.load("images/Kokaton/12.png")]
    down_images = [pg.image.load("images/Kokaton/13.png"), pg.image.load("images/Kokaton/15.png")]

    # こうかとんとスコアのインスタンスを作成
    kouka_ton = KoukaTon(left_images, right_images, up_images, down_images, (300, 200))
    score = Score()  # スコア機能

    # 爆弾と敵の画像と初期位置を読み込み
    bomb_img = pg.image.load("images/bom/bom.png")
    bomb_rect = bomb_img.get_rect(center=(400, 400))
    enemy_img = pg.image.load("images/bom/explosion.png")
    enemy_rect = enemy_img.get_rect(center=(400, 400))

    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:  # スペースキーでスコアを増やす
                    score.increase(10)

        # 背景画像を描画
        screen.blit(bg_img, [0, 0])

        # 現在のキーの状態を取得
        keys = pg.key.get_pressed()
        kouka_ton.move(keys)  # こうかとんの移動処理
        kouka_ton.draw(screen)  # こうかとんを画面に描画

        # 爆弾と敵の画像を描画
        screen.blit(bomb_img, bomb_rect)
        screen.blit(enemy_img, enemy_rect)

        # 爆弾と敵が重なる場合スコアを加算
        if bomb_rect.colliderect(enemy_rect):
            score.increase(10)

        # スコアを画面に描画
        score.draw(screen)

        pg.display.update()  # 画面を更新
        clock.tick(50)  # フレームレートを制御


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
