import os 
import random
import sys
import time
import pygame as pg
WIDTH, HEIGHT = 750, 700
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DELTA = {pg.K_UP: (0, -5),
          pg.K_DOWN: (0, 5),
          pg.K_LEFT: (-5, 0),
          pg.K_RIGHT: (5, 0), }
class Score:
    """
    スコア管理クラス
    スコアの追跡と更新を処理する
    """
    def __init__(self) -> None:
        self.score = 0  # 初期スコアは0

    def add_score(self, points: int) -> None:
        self.score += points  # スコアを加算
        print(f"Score: {self.score}")  # 現在のスコアを表示（デバッグ用）

    def get_score(self) -> int:
        return self.score  # 現在のスコアを返す


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


def game_over(scr: pg.Surface) -> None:
    bo = pg.Surface((WIDTH, HEIGHT))
    bo.set_alpha(205)
    pg.draw.rect(bo, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    fonto = pg.font.Font(None, 70)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    kk_cry_img = pg.image.load("fig/8.png")
    scr.blit(bo, [0, 0])
    scr.blit(txt, [(WIDTH / 2) - 140, (HEIGHT / 2) - 40])
    scr.blit(kk_cry_img, [(WIDTH / 2) - 205, (HEIGHT / 2) - 50])
    scr.blit(kk_cry_img, [(WIDTH / 2) + 145, (HEIGHT / 2) - 50])
    pg.display.update()
    time.sleep(5)


def show_title_screen(screen: pg.Surface) -> None:
    fonto = pg.font.SysFont("hg正楷書体pro", 70)
    title_txt = fonto.render("ボンバーこうかとん", True, (255, 255, 255))
    start_txt = fonto.render("START", True, (255, 255, 255))
    picture = pg.image.load("fig/forest_dot1.jpg")  # 画像のパスを修正

    while True:
        screen.blit(picture, (0, 0))  # 背景として画像を描画
        
        screen.blit(title_txt, [(WIDTH / 2) - (title_txt.get_width() / 2), HEIGHT / 3])
        screen.blit(start_txt, [(WIDTH / 2) - (start_txt.get_width() / 2), HEIGHT / 2])
        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                return


def bb_chenger() -> tuple[list, list]:
    accs = [a for a in range(1, 11)]
    img = []

    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r))
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        img.append(bb_img)

    return (accs, img)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
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

def main() -> None:
    """
    ゲームのメインループを制御する
    """
    pg.display.set_caption("ボンバーこうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    # タイトル画面の表示
    show_title_screen(screen)

    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))
    bb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
    vx, vy = 5, -5
    bb_accs, bb_imgs = bb_chenger()
    bg_img = pg.image.load("images/bg_ver.1.0.png")  # 背景(完成版)
    hero = Hero((75, 125))  # 主人公の初期位置
    boms = pg.sprite.Group()  # 爆弾クラスのグループ作成
    position = random_position()
    enemys = pg.sprite.Group()  # 敵のスプライトグループ
    for i, j in enumerate(position[:-1]):
        enemys.add(Enemy(i, j))  # 敵のインスタンス生成
    clock = pg.time.Clock()
    tmr = 0
    score = Score()  # スコアオブジェクトを作成

    # フォントの初期化
    pg.font.init()
    font = pg.font.Font(None, 36)  # フォントを作成

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, [0, 0])

        if kk_rct.colliderect(bb_rct):
            game_over(screen)
            return

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:  # スペースキーで爆弾設置
                    boms.add(Bomber(hero.rct.center, hero, enemys))  # 传递 hero 和 enemies

        screen.blit(bg_img, [0, 50])
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        kk_rct.move_ip(sum_mv)

        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        screen.blit(kk_img, kk_rct)
        bb_img = bb_imgs[min(tmr // 500, 9)]
        bb_img.set_colorkey((0, 0, 0))
        avx = vx * bb_accs[min(tmr // 500, 9)]
        avy = vy * bb_accs[min(tmr // 500, 9)]
        bb_rct.move_ip((avx, avy))
        yoko, tate = check_bound(bb_rct)

        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        screen.blit(bb_img, bb_rct)
        hero.update(key_lst, screen)
        enemys.update()
        enemys.draw(screen)
        boms.update()
        boms.draw(screen)

        # 爆弾と敵の衝突判定
        for bom in boms:
            if bom.state == "explosion":
                for enemy in enemys:
                    if bom.rect.colliderect(enemy.rect):  # 衝突判定
                        score.add_score(100)  # スコアを加算
                        enemy.kill()  # 敵を消去
                        break

        # スコアの表示
        screen.fill((0,0,0),(10,10,150,36))
        score_text = font.render(f"Score: {score.get_score()}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))  # スコアを画面の左上に描画

        pg.display.update()
        clock.tick(60)  # framerateを60に設定



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()