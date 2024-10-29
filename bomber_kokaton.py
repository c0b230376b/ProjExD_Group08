import os 
import random
import sys
import time
import pygame as pg

WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DELTA = {pg.K_UP: (0, -5),
          pg.K_DOWN: (0, 5),
          pg.K_LEFT: (-5, 0),
          pg.K_RIGHT: (5, 0), }


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    yoko, tate = True, True

    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or obj_rct.bottom > HEIGHT:
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
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, [0, 0])

        if kk_rct.colliderect(bb_rct):
            game_over(screen)
            return

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
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
