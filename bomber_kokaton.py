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

# 初期位置をランダムに決めるための関数
def random_position() -> list:
    """
    盤面領域内の四隅の座標タプルをシャッフルしたリストを返す
    戻り値：タプルのリスト
    """
    pos = [
        (75, 125),
        (75, HEIGHT - 75),
        (WIDTH - 75, 125),
        (WIDTH - 75, HEIGHT - 75),
    ]
    return random.sample(pos, len(pos))

# こうかとん（プレイヤー）のクラス
class Hero:
    """
    ゲームキャラクター（こうかとん）に関するクラス
    """
    delta = {
        pg.K_UP: (0, -50),
        pg.K_DOWN: (0, +50),
        pg.K_LEFT: (-50, 0),
        pg.K_RIGHT: (+50, 0),
    }
    img0 = pg.transform.rotozoom(pg.image.load("images/Kokaton/3.png"), 0, 0.9)
    img = pg.transform.flip(img0, True, False)
    imgs = {
        (+50, 0): img,
        (+50, -50): pg.transform.rotozoom(img, 45, 0.9),
        (0, -50): pg.transform.rotozoom(img, 90, 0.9),
        (-50, -50): pg.transform.rotozoom(img0, -45, 0.9),
        (-50, 0): img0,
        (-50, +50): pg.transform.rotozoom(img0, 45, 0.9),
        (0, +50): pg.transform.rotozoom(img, -90, 0.9),
        (+50, +50): pg.transform.rotozoom(img, -45, 0.9),
    }
    mvct = 0

    def __init__(self, xy: tuple[int, int]) -> None:
        self.img = __class__.imgs[(+50, 0)]
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.center = xy
        self.dire = (+50, 0)
        self.score = 0  # スコアの初期化

    def add_score(self, points: int) -> None:
        """スコアにポイントを追加するメソッド"""
        self.score += points

    # キーの入力で動く処理
    def update(self, key_lst: list[bool], screen: pg.Surface) -> None:
        """
        押下キーに応じてこうかとんを移動させる
        引数1 key_lst：押下キーの真理値リスト
        引数2 screen：画面Surface
        """
        sum_mv = [0, 0]
        if __class__.mvct == 0:
            for k, mv in __class__.delta.items():
                if key_lst[k]:
                    sum_mv[0] += mv[0]
                    sum_mv[1] += mv[1]
            self.rct.move_ip(sum_mv)
            __class__.mvct = 15
        elif 0 < __class__.mvct:
            __class__.mvct -= 1
        if check_bound(self.rct) != (True, True):
            self.rct.move_ip(-sum_mv[0], -sum_mv[1])
        if not (sum_mv[0] == 0 and sum_mv[1] == 0):
            self.img = __class__.imgs[tuple(sum_mv)]
            self.dire = sum_mv
        screen.blit(self.img, self.rct)

# エイリアンのクラス
class Enemy(pg.sprite.Sprite):
    """
    敵に関するクラス
    """
    imgs = [pg.image.load(f"images/ufo/alien{i}.png") for i in range(1, 4)]

    def __init__(self, num: int, vx: tuple[int, int]) -> None:
        """
        敵のSurfaceの作成
        引数1 num: 画像指定用整数
        引数2 vx: Rectのcenter用タプル
        """
        super().__init__()
        self.num = num
        self.img = __class__.imgs[self.num]
        self.image = pg.transform.rotozoom(self.img, 0, 0.5)
        self.rect = self.image.get_rect()
        self.rect.center = vx
        self.vx, self.vy = 0, 0
        self.mvct = 0
        self.state = "move"

    # エイリアンの移動制御
    def control(self) -> None:
        """
        的に関する動作制御を行う
        """
        img_key = {
            (+50, 0): pg.transform.rotozoom(self.img, 0, 0.5),
            (0, -50): pg.transform.rotozoom(self.image, 90, 1.0),
            (-50, 0): pg.transform.flip(self.image, True, False),
            (0, +50): pg.transform.rotozoom(self.image, -90, 1.0),
        }
        move_list = [
            (0, -50),
            (0, +50),
            (-50, 0),
            (+50, 0),
        ]
        if self.mvct == 0:
            while True:
                sum_mv = random.choice(move_list)
                self.rect.move_ip(sum_mv[0], sum_mv[1])
                if check_bound(self.rect) != (True, True):
                    self.rect.move_ip(-sum_mv[0], -sum_mv[1])
                    continue
                break
            self.image = img_key[sum_mv]
            self.mvct = 15
        elif self.mvct > 0:
            self.mvct -= 1

    def update(self) -> None:
        """
        敵の情報を更新する
        """
        __class__.control(self)

# 爆弾（ボンバー）のクラス
class Bomber(pg.sprite.Sprite):
    """
    爆弾に関するクラス
    """
    def __init__(self, vx: tuple[int, int], hero: Hero, enemies: pg.sprite.Group) -> None:
        super().__init__()
        self.bom_img = pg.image.load("images/bom/bom.png")
        self.exp_img = pg.image.load("images/bom/explosion.png")
        self.image = pg.transform.rotozoom(self.bom_img, 0, 0.1)
        self.rect = self.image.get_rect()
        self.rect.center = vx
        self.count = 300
        self.state = "bom"
        self.hero = hero
        self.enemies = enemies

    # 爆弾の制御
    def control(self) -> None:
        """
        爆弾の動作を処理する
        """
        if self.count == 0:
            if self.state == "bom":
                self.image = pg.transform.rotozoom(self.exp_img, 180, 0.05)
                self.count = 30
                self.state = "explosion"
            else:
                # 爆発時に敵と衝突した場合スコアを増加
                collided_enemies = pg.sprite.spritecollide(self, self.enemies, True)
                if collided_enemies:
                    self.hero.add_score(100 * len(collided_enemies))
                self.kill()
        elif self.count > 0:
            self.count -= 1
            if self.state == "explosion":
                self.image = pg.transform.rotate(self.image, 90)

    def update(self) -> None:
        """
        爆弾の情報を更新する
        """
        self.control()

# メイン関数
def main() -> None:
    """
    ゲームのメインループを制御する
    """
    pg.display.set_caption("ボンバーこうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("images/bg_ver.1.0.png")
    position = random_position()
    hero = Hero(position[-1])
    boms = pg.sprite.Group()
    enemys = pg.sprite.Group()
    for i, j in enumerate(position[:-1]):
        enemys.add(Enemy(i, j))
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    boms.add(Bomber(hero.rct.center, hero, enemys))

        screen.blit(bg_img, [0, 50])
        key_lst = pg.key.get_pressed()
        hero.update(key_lst, screen)
        enemys.update()
        enemys.draw(screen)
        boms.update()
        boms.draw(screen)

        # スコアを表示する処理
        font = pg.font.SysFont("Arial", 24, bold=False)
        score_surf = font.render(f"Score: {hero.score}", True, (200, 200, 200))
        screen.blit(score_surf, (5, 5))

        pg.display.update()
        tmr += 1
        clock.tick(60)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
