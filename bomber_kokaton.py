import os
import random
import sys
import time

import pygame as pg


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DELTA = {pg.K_UP:(0, -5), 
        pg.K_DOWN:(0, 5), 
        pg.K_LEFT:(-5, 0), 
        pg.K_RIGHT:(5, 0),
        } # 練習問題1


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]: # 練習問題3
    """
    引数：こうかとん　または　爆弾のRect,
    戻り地：真理値タプル(横判定結果、縦判定結果)
    """

    yoko, tate = True, True

    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or obj_rct.bottom > HEIGHT:
        tate = False

    return yoko, tate


def game_over(scr: pg.Surface) -> None:
    """
    引数：スクリーンのSurface
    戻り値：None
    """

    # ゲームオーバー画面
    bo = pg.Surface((WIDTH, HEIGHT)) # ブラックアウト
    bo.set_alpha(205)
    pg.draw.rect(bo, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    fonto = pg.font.Font(None, 70) # 文字
    txt = fonto.render("Game Over", True, (255, 255, 255))
    kk_cry_img = pg.image.load("fig/8.png")
    # 反映
    scr.blit(bo, [0, 0])
    scr.blit(txt, [(WIDTH / 2) - 140, (HEIGHT / 2) - 40])
    scr.blit(kk_cry_img, [(WIDTH / 2) - 205, (HEIGHT / 2) - 50])
    scr.blit(kk_cry_img, [(WIDTH / 2) + 145, (HEIGHT / 2) - 50])
    pg.display.update()
    time.sleep(5)


def bb_chenger() -> tuple[list, list]:
    """
    引数：None
    戻り値：listのtuple
    """

    accs = [a for a in range(1, 11)] # 爆弾の加速度
    img = []

    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r))
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        img.append(bb_img)

    return (accs, img)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20)) # 練習問題2
    bb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
    vx, vy = 5, -5 # 爆弾の移動
    bb_accs, bb_imgs = bb_chenger()
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct): # 練習問題4
            # こうかとんと爆弾が重なっていたら
            game_over(screen)
            return 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0] # 横座標、縦座標

        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5

        for key , tpl in DELTA.items(): # 練習問題1
            if key_lst[key]:
                sum_mv[0] += tpl[0] # 縦方向
                sum_mv[1] += tpl[1] # 横方向

        kk_rct.move_ip(sum_mv)

        if check_bound(kk_rct) != (True, True): # 練習問題3
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        screen.blit(kk_img, kk_rct)
        bb_img = bb_imgs[min(tmr // 500, 9)]
        bb_img.set_colorkey((0, 0, 0))
        avx = vx * bb_accs[min(tmr // 500, 9)] # 演習課題2
        avy = vy * bb_accs[min(tmr // 500, 9)]
        bb_rct.move_ip((avx, avy)) # 練習問題2
        yoko, tate = check_bound(bb_rct) # 練習問題3

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
