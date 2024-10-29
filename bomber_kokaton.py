import os
import random
import sys
import time

import pygame as pg


WIDTH, HEIGHT = 750, 700
os.chdir(os.path.dirname(os.path.abspath(__file__)))


DELTA = {pg.K_UP:(0, -5), 
        pg.K_DOWN:(0, 5), 
        pg.K_LEFT:(-5, 0), 
        pg.K_RIGHT:(5, 0),
        } # 練習問題1


def main():
    pg.display.set_caption("ボンバーこうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("images/bg(test).png") # 一時的な背景(緑スペース背景)   
    # kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    # kk_rct = kk_img.get_rect()
    # kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        screen.blit(bg_img, [0, 100]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0] # 横座標、縦座標

        for key , tpl in DELTA.items(): # 練習問題1
            if key_lst[key]:
                sum_mv[0] += tpl[0] # 縦方向
                sum_mv[1] += tpl[1] # 横方向

        # kk_rct.move_ip(sum_mv)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
