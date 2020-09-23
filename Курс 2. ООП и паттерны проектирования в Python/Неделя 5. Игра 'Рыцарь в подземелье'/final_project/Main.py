import pygame
import os
import Objects
import ScreenEngine as SE
import Logic
import Service
from math import ceil # Округление вверх для движения карты

SCREEN_DIM = (800, 600)

pygame.init()
gameDisplay = pygame.display.set_mode(SCREEN_DIM)
pygame.display.set_caption("MyRPG")
KEYBOARD_CONTROL = True

if not KEYBOARD_CONTROL:
    import numpy as np
    answer = np.zeros(4, dtype=float)

base_stats = {
    "strength": 20,
    "endurance": 20,
    "intelligence": 5,
    "luck": 5
}


def create_game(sprite_size, is_new, map_position=[0,0]):
    global hero, engine, drawer, iteration
    if is_new:
        hero = Objects.Hero(base_stats, Service.create_sprite(
            os.path.join("texture", "Hero.png"), sprite_size))
        engine = Logic.GameEngine()
        engine.surf_wall = Service.service_init(sprite_size)
        Service.reload_game(engine, hero)
        
        drawer = SE.GameSurface((640, 480), pygame.SRCALPHA, (0, 480),
                        SE.ProgressBar((640, 120), (640, 0),
                                       SE.InfoWindow((160, 600), (475, 315),
                                                     SE.MiniMap((165, 165), pygame.SRCALPHA, (50, 50),
                                                                SE.HelpWindow((700, 500), pygame.SRCALPHA,
                                                                              (0, 0),
                                                                              SE.ScreenHandle(
                                                                                  (0, 0))
                                                                              )))))
                                                                              
    else:
        engine.sprite_size = sprite_size
        hero.sprite = Service.create_sprite(
            os.path.join("texture", "Hero.png"), sprite_size)
        Service.service_init(sprite_size, False)
        
    engine.map_position = map_position        
    Logic.GameEngine.sprite_size = sprite_size
    
    drawer.connect_engine(engine)
    engine.map_size = [len(engine.map[0]), len(engine.map)]
    iteration = 0
    engine.subscribe(drawer)

size = 60
create_game(size, True)
while engine.working:

    if KEYBOARD_CONTROL:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                engine.working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    engine.show_help = not engine.show_help
                if event.key == pygame.K_m:
                    engine.show_mini_map = not engine.show_mini_map
                if event.key == pygame.K_KP_PLUS:
                    size = size + 1
                    create_game(size, False, engine.map_position)
                if event.key == pygame.K_KP_MINUS:
                    size = size - 1
                    create_game(size, False, engine.map_position)
                if event.key == pygame.K_r:
                    create_game(size, True)
                    
                # Изменение позиции отрисованной карты
                if event.key == pygame.K_w:
                    if engine.map_position[1] > 0:
                        engine.map_position[1] -= 1
                    create_game(size, False, engine.map_position)
                if event.key == pygame.K_a:
                    if engine.map_position[0] > 0:
                        engine.map_position[0] -= 1
                    create_game(size, False, engine.map_position)
                if event.key == pygame.K_s:
                    if engine.map_position[1] + ceil(480/size) < engine.map_size[1]: 
                        # Если движение карты не выводит экран за пределы карты
                        engine.map_position[1] += 1
                    create_game(size, False, engine.map_position)
                if event.key == pygame.K_d:
                    if engine.map_position[0] + ceil(640/size) < engine.map_size[0]:
                        engine.map_position[0] += 1
                    create_game(size, False, engine.map_position)
                    
                if event.key == pygame.K_ESCAPE:
                    engine.working = False
                if engine.game_process:
                    if event.key == pygame.K_UP:
                        for enemy in [obj for obj in engine.objects if isinstance(obj, Objects.Enemy)]:
                            enemy.move(engine.mini_map, engine.hero.position)
                        engine.move_up()
                        iteration += 1
                    elif event.key == pygame.K_DOWN:
                        for enemy in [obj for obj in engine.objects if isinstance(obj, Objects.Enemy)]:
                            enemy.move(engine.mini_map, engine.hero.position)
                        engine.move_down()
                        iteration += 1
                    elif event.key == pygame.K_LEFT:
                        for enemy in [obj for obj in engine.objects if isinstance(obj, Objects.Enemy)]:
                            enemy.move(engine.mini_map, engine.hero.position)
                        engine.move_left()
                        iteration += 1
                    elif event.key == pygame.K_RIGHT:
                        for enemy in [obj for obj in engine.objects if isinstance(obj, Objects.Enemy)]:
                            enemy.move(engine.mini_map, engine.hero.position)
                        engine.move_right()
                        iteration += 1
                else:
                    if event.key == pygame.K_RETURN:
                        create_game()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                engine.working = False
        if engine.game_process:
            actions = [
                engine.move_right,
                engine.move_left,
                engine.move_up,
                engine.move_down,
            ]
            answer = np.random.randint(0, 100, 4)
            prev_score = engine.score
            move = actions[np.argmax(answer)]()
            state = pygame.surfarray.array3d(gameDisplay)
            reward = engine.score - prev_score
            print(reward)
        else:
            create_game()

    gameDisplay.blit(drawer, (0, 0))
    drawer.draw(gameDisplay)

    pygame.display.update()

pygame.display.quit()
pygame.quit()
exit(0)
