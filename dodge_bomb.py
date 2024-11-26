import os
import random
import sys
import time

import pygame as pg


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DELTA = {
    pg.K_UP : (0, -5),
    pg.K_DOWN : (0, +5),
    pg.K_LEFT : (-5, 0),
    pg.K_RIGHT : (+5, 0),
    }

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectが画面の中か外かを判定する
    引数:こうかとんRect or 爆弾Rect
    戻り値：真理値タプル（横,縦）/画面内:True, 画面概:False
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None:
    print("ゲームオーバー")  # 動作確認用
    blackout = pg.Surface((WIDTH, HEIGHT))  # 黒のSurface
    pg.draw.rect(blackout, (0, 0, 0), (0, 0, WIDTH, HEIGHT))  # 画面を黒で塗りつぶす
    blackout.set_alpha(128)  # 透明度の設定
    screen.blit(blackout, (0, 0))  
    font = pg.font.Font(None, 80)  # フォントの設定
    text = font.render("Game Over", True, (255, 255, 255))  # 文字の設定
    screen.blit(text, (WIDTH//2 - 150, HEIGHT//2 - 40))  # 文字を表示
    kk_cry_img = pg.image.load("fig/8.png") # こうかとんの画像
    #kk_cry_img = pg.transform.rotozoom(kk_cry_img, 0, 0.9)  # こうかとんの拡大
    screen.blit(kk_cry_img, (WIDTH//2 + 200, HEIGHT//2 - 40))  # こうかとん右に表示
    screen.blit(kk_cry_img, (WIDTH//2 - 240, HEIGHT//2 - 40))  # こうかとん左に表示
    pg.display.update()
    time.sleep(5)
    return
    



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20,20))  # 爆弾用の空Surfac
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 爆弾の円を描く
    bb_img.set_colorkey(0, 0)  # 爆弾の周りの黒を透過
    bb_rct = bb_img.get_rect()  # 爆弾rectの抽出
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    # bb_rct.centerx = random.randint(0, WIDTH)
    # bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            gameover(screen)  # 終了画面の表示
            return  # ゲームオーバー
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key , tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)
        # こうかとんが画面外なら,元の場所戻す
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)  # 爆弾を動かす
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 画面外横
            vx *= -1
        if not tate:  # 画面外縦
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
