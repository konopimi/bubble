import math
import random
import sys
from dataclasses import dataclass
from typing import Callable

import const
import esper
import pygame


@dataclass
class Transform:
    position: tuple
    speed: int


@dataclass
class Pooled:
    pass


@dataclass
class Attacker:
    pass


@dataclass
class Goal:
    pass


@dataclass
class Attacking:
    pass


@dataclass
class Goaling:
    pass


@dataclass
class Button:
    rect:pygame.Rect
    onclickFunction: Callable[[], None]
    onePress: bool
    alreadyPressed: bool = False
    #
    # fillColors = {
    #     "normal": "#ffffff",
    #     "hover": "#666666",
    #     "pressed": "#333333",
    # }


FINGER_ATTACK_EVENT = pygame.USEREVENT + 1


screen = pygame.display.set_mode((const.WIDTH, const.HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)

splash_bg = pygame.transform.scale(pygame.image.load("assets/splash_bg.jpeg"), (const.WIDTH * 1.3, const.HEIGHT * 1.3))
splash_txt = pygame.transform.scale(pygame.image.load("assets/splash_txt.png").convert_alpha(), (const.WIDTH, const.HEIGHT))
splash_txt.set_alpha(220)
splash_fg = pygame.transform.scale(pygame.image.load("assets/splash_fg.png").convert_alpha(), (const.WIDTH * 1.3, const.HEIGHT * 1.3))
splash_fg.set_alpha(200)
splash_surface = pygame.Surface((const.WIDTH, const.HEIGHT), pygame.SRCALPHA)

grass = pygame.transform.scale(pygame.image.load("assets/grass.png").convert_alpha(), (const.WIDTH*1.6, 200))
head_size=(200,200)
kid_size=(280,320)
kid_surface = pygame.Surface(kid_size, pygame.SRCALPHA)
# KID HEAD
kid_head_surface = pygame.Surface(head_size, pygame.SRCALPHA)
kid_head = pygame.transform.scale(pygame.image.load("assets/kid_head.png"), head_size)
tears= pygame.transform.scale(pygame.image.load("assets/tears.png"), (300,100))
#KID LIPS
lip_size=(30, 30)
lip_oppened = pygame.transform.scale(pygame.image.load("assets/lip_oppened.png"),lip_size)
lip_clossed = pygame.transform.scale(pygame.image.load("assets/lip_closed.png"), lip_size)
# KID BODY
body_size=(kid_size[0]*0.62, 160)
kid_body = pygame.transform.scale(pygame.image.load("assets/kid_body.png"),body_size )
# kid = pygame.transform.scale(pygame.image.load("assets/kidblow_clean.png"), (300, 300))
cat = pygame.transform.scale(pygame.image.load("assets/cat.png"), (100, 100))

finger_size = (160, 80)
pointing = pygame.transform.scale(pygame.image.load("assets/pointing.png"), finger_size)

background_imagination_surface = pygame.transform.scale(pygame.image.load("assets/background.jpeg"), (const.WIDTH * 1.6, const.HEIGHT * 1.6))

game_over_imagination_surface = pygame.transform.scale(pygame.image.load("assets/game_over.jpeg"), (const.WIDTH, const.HEIGHT))
# Create a transparent surface once


transparent_surface = pygame.Surface((const.WIDTH, const.HEIGHT), pygame.SRCALPHA)
imagination_surface = pygame.Surface((const.WIDTH, const.HEIGHT), pygame.SRCALPHA)

ui_surface = pygame.Surface((const.WIDTH, const.HEIGHT), pygame.SRCALPHA)


debug = False




pygame.font.init()  # you have to call this at the start,

# if you want to use this module.
my_font = pygame.font.SysFont("Comic Sans MS", 30)


mouse_pos=(0,0)

lip=lip_clossed

def bubble_pop():
    sound = pygame.mixer.Sound("assets/bubble-254777.mp3")
    # sound.set_volume(0.9)   # Now plays at 90% of full volume.
    channel = sound.play()      # Sound plays at full volume by default
    # sound.set_volume(0.6)   # Now plays at 60% (previous value replaced).
    # channel.set_volume(0.5) # Now plays at 30% (0.6 * 0.5).
def blow_air():
    blow= f"assets/blow{(int)(random.random()*3)}.wav"
    sound = pygame.mixer.Sound(blow)
    sound.set_volume(0.3+random.random()*0.3)   # Now plays at 90% of full volume.
    channel = sound.play()      # Sound plays at full volume by default
    # sound.set_volume(0.9)   # Now plays at 90% of full volume.
    # sound.set_volume(0.6)   # Now plays at 60% (previous value replaced).
    # channel.set_volume(0.5) # Now plays at 30% (0.6 * 0.5).
def guau_guau():
    guau= f"assets/guau{(int)(random.random()*4)}.wav"
    sound = pygame.mixer.Sound(guau)
    sound.set_volume(0.8+random.random()*0.2)   # Now plays at 90% of full volume.
    channel = sound.play()      # Sound plays at full volume by default
def create_attacker() -> None:
    id = esper.create_entity(Attacker(), Pooled())


def create_goal() -> None:
    id = esper.create_entity(Goal(), Pooled())

def restart_game():
        global game_started,game_over,bubble_points,enemies_points,radius,actual_radius,bubble_decrease_speed,bubble_clicks
        bubble_points = 0
        enemies_points = 0
        game_over= False
        game_started= False
        radius=0
        actual_radius=0
        bubble_decrease_speed = 10
        bubble_clicks = 0
def test():
    global game_started,game_over
    print("test")
    if not game_started:
        game_started= True
        pygame.time.set_timer(FINGER_ATTACK_EVENT, 1000)
    elif game_over:
        # RESTART GAME
        restart_game()
        
        
def create_button() -> None:
    id = esper.create_entity( Button(

    rect=pygame.Rect(const.WIDTH/2-100,const.HEIGHT-100,200,20),
    onclickFunction= test,
    onePress=True,
    alreadyPressed=False,

    # fillColors = {
    #     "normal": "#ffffff",
    #     "hover": "#666666",
    #     "pressed": "#333333",
    # }

    ))

def finger_attack(pos: tuple[int, int]):
    pooled_fingers = esper.get_components(Attacker, Pooled)
    ent, _ = pooled_fingers[0]
    esper.remove_component(ent, Pooled)
    esper.add_component(ent, Transform(position=pos, speed=0.1))
    esper.add_component(ent, Attacking())


def goal_reached():
    pooled_goals = esper.get_components(Goal, Pooled)
    ent, _ = pooled_goals[0]
    esper.remove_component(ent, Pooled)
    esper.add_component(ent, Transform(position=(const.WIDTH / 2 + 10, const.HEIGHT / 2 - 10), speed=1))
    esper.add_component(ent, Goaling())


def calculate_angle(opposite, adjacent):
    # Calculate the tangent of the angle
    tan_value = opposite / adjacent

    # Calculate the arctangent (inverse tangent)
    angle_radians = math.atan(tan_value)

    # Convert radians to degrees
    angle_degrees = math.degrees(angle_radians)
    if adjacent > 0:
        angle_degrees += 180
    return angle_degrees


def blitRotate(surf, image, pos, originPos, angle):

    # offset from pivot to center
    image_rect = image.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd image center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

    # rotate and blit the image
    surf.blit(rotated_image, rotated_image_rect)

def poolGoal(ent):
    esper.remove_component(ent, Transform)
    esper.remove_component(ent, Goaling)
    esper.add_component(ent, Pooled())
    pass
def poolAttacker(ent):
        # if esper.has_component(hexagon["id"], Fow):
    esper.remove_component(ent, Transform)
    esper.remove_component(ent, Attacking)
    esper.add_component(ent, Pooled())
    pass
def poolGoals():
    print("poolingG")
    for ent, _ in esper.get_component(Goaling):
        print("poolingGoal")
        poolGoal(ent)
def poolAttackers():
    print("poolingA")
    for ent, _ in esper.get_component(Attacking):
        print("poolingAttacker")
        poolAttacker(ent)

class ButtonsManager(esper.Processor):
    def process(self, clock, dt):
        global game_over
        for ent, button in esper.get_component(Button):
            # print("drawing button")
            pygame.draw.rect(ui_surface, (55, 55, 255,128), button.rect)
            pygame.draw.rect(ui_surface, (55, 55, 255,255), button.rect,2)

class AttackersManager(esper.Processor):
    def process(self, clock, dt):
        global radius, game_over
        for ent, (transform, _) in esper.get_components(Transform, Attacking):
            # print("doing")
            # print(transform.position)
            transform.position = (transform.position[0] - (transform.position[0] - (const.WIDTH / 2)) * dt * transform.speed, transform.position[1] - (transform.position[1] - (const.HEIGHT / 2)) * dt * transform.speed)
            blitRotate(transparent_surface, pointing, 
                       transform.position, 
                       (finger_size[0] / 2, finger_size[1] / 2), 
                       calculate_angle(transform.position[0] - (const.WIDTH / 2), transform.position[1] - (const.HEIGHT / 2)) + 110)
            # print("drawing finger")
            if debug:
                pygame.draw.circle(transparent_surface, (255, 100, 100, 128), transform.position, 20, 0)
            distance = ((transform.position[0] - (const.WIDTH / 2)) ** 2 + (transform.position[1] - (const.HEIGHT / 2)) ** 2) ** 0.5

            # print("agent distance")
            # print(distance)
            if distance < 60 or distance - 60 < radius:
                # print("game_over!!!!!!!!!")
                pygame.time.set_timer(FINGER_ATTACK_EVENT, 0)
                poolGoals()
                poolAttackers()
                game_over = True


class GoalsManager(esper.Processor):
    def process(self, clock, dt):
        global radius, game_over
        for ent, (transform, _) in esper.get_components(Transform, Goaling):
            # print(transform.position)
            transform.position = (transform.position[0] + (transform.position[0] - (const.WIDTH / 2)) * dt * transform.speed, transform.position[1] + (transform.position[1] - (const.HEIGHT / 2)) * dt * transform.speed)

            distance = ((transform.position[0] - (const.WIDTH / 2)) ** 2 + (transform.position[1] - (const.HEIGHT / 2)) ** 2) ** 0.5
            spice =(math.sin(pygame.time.get_ticks()/100)*0.1+math.sin(pygame.time.get_ticks()/61.8)*0.06)*radius*10
            pygame.draw.circle(transparent_surface, (100, 100, 200), (transform.position[0]+spice,transform.position[1]), 60, 2)  # (r, g, b) is color, (x, y) is center, R is radius and w is the thickness of the circle border.
            pygame.draw.circle(transparent_surface, (100, 60, 250, 128), (transform.position[0]+spice,transform.position[1]), 60, 0)
            # print("agent distance")
            # print(distance)
            if distance > 200:
                poolGoal(ent)


def generate_random_point_in_circle(center_x, center_y, r):
    # Generate random radius and angle
    theta = 2 * math.pi * random.random()
    # print(theta)

    # Convert polar coordinates to Cartesian
    x = center_x + r * math.cos(theta)
    y = center_y + r * math.sin(theta)
    print(f"random {x},{y}")

    return (x, y)


def tutorial():
    global bubble_clicks

    tutorial_text = ""
    if bubble_clicks == 0:
        tutorial_text = "CLICK AQUI"
    elif bubble_clicks == 1:
        tutorial_text = "OTRA VEZ"
    elif bubble_clicks < 5:
        tutorial_text = "SIGUE HACIENDO CLICK"
    elif bubble_clicks < 8:
        tutorial_text = "CLICK!! MAS RAPIDO"
    elif bubble_clicks < 15:
        tutorial_text = "MUCHO MAS RAPIDO"
    elif bubble_clicks < 30 and enemies_points < 3:
        tutorial_text = "ESPANTA LOS DEDOS"
    elif bubble_clicks > 35 and enemies_points > 5:

        tutorial_text = ""
    else:
        tutorial_text = "YA SABES JUGAR"

    pygame.draw.rect(transparent_surface, (255, 255, 255, 200), (const.WIDTH / 2 - len(tutorial_text) * 5, const.HEIGHT / 2 - 5, len(tutorial_text) * 12, 20))
    transparent_surface.blit(my_font.render(tutorial_text, False, (0, 0, 0)), (const.WIDTH / 2 - len(tutorial_text) * 5, const.HEIGHT / 2 - 5))


def main():
    global actual_radius, radius, game_over,game_started, bubble_points, enemies_points, bubble_decrease_speed, bubble_clicks,mouse_pos,lip
    restart_game()
    pygame.init()
    # init()
    clock = pygame.time.Clock()
    esper.add_processor(AttackersManager())
    esper.add_processor(GoalsManager())
    esper.add_processor(ButtonsManager())
    # spawn_finger((100,100))
    for i in range(100):
        create_attacker()
    for i in range(5):
        create_goal()
    create_button()
    lip_time=-1
    blow_multiply=1
    head_rotation=0
    actual_head_rotation=0

    # spawn_finger(generate_random_point_in_circle(const.WIDTH,const.HEIGHT,100))
    while True:
        pooled_goals = esper.get_components(Goal, Pooled)

        # print(f"{len(pooled_goals)}")u
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return
            elif event.type == FINGER_ATTACK_EVENT:

                print("FINGER_ATTACK_EVENT")
                pygame.time.set_timer(FINGER_ATTACK_EVENT, 0)
                finger_attack(generate_random_point_in_circle(const.WIDTH / 2, const.HEIGHT / 2, 300))
                pygame.time.set_timer(FINGER_ATTACK_EVENT, (int)((3000 / (bubble_points + 1)) + random.random() * 2000))
                pass
            elif event.type==pygame.MOUSEMOTION:
                mouse_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for ent, button in esper.get_component(Button):
                    if button.rect.collidepoint(event.pos):
                        button.onclickFunction()
                if not game_over and game_started:
                    distance = ((mouse_x - (const.WIDTH / 2)) ** 2 + (mouse_y - (const.HEIGHT / 2)) ** 2) ** 0.5
                    if distance < 20 or distance < radius:
                        # print(distance)
                        blow_air()
                        bubble_clicks += 1
                        radius += 5
                        bubble_decrease_speed = 10
                        lip=lip_oppened
                        head_rotation=-15
                        blow_multiply=1
                        lip_time =pygame.time.get_ticks()
                        if radius > 100:
                            bubble_points += 1
                            print("GOAL!!!!")
                            bubble_pop()
                            radius = 0
                            bubble_decrease_speed = 60
                            goal_reached()
                    for ent, (transform, _) in esper.get_components(Transform, Attacking):

                        finger_distance = ((mouse_x - transform.position[0]) ** 2 + (mouse_y - transform.position[1]) ** 2) ** 0.5
                        if finger_distance < 70:
                            guau_guau()
                            enemies_points += 1
                            poolAttacker(ent)
                            print("finger cicked YAYYY :)")

        dt = clock.tick(60) / 1000
        # imagination_surface.fill((0, 0, 100))
        transparent_surface.fill((0, 0, 0, 0))
        esper.process(clock, dt)
        if (not game_over) and game_started:


    # IMAGINATION IMAGINATION IMAGINATION
    # IMAGINATION IMAGINATION IMAGINATION
    # IMAGINATION IMAGINATION IMAGINATION
    # IMAGINATION IMAGINATION IMAGINATION

            if lip_time>0 and (pygame.time.get_ticks()-lip_time)>1000:
                head_rotation=15
                lip=lip_clossed
                lip_multiply=0.1
            actual_radius = pygame.math.lerp(actual_radius, radius, dt * 0.6)
            imagination_surface.blit(background_imagination_surface, (-actual_radius * 0.32, 0))
            mod_radius=actual_radius+(math.sin(pygame.time.get_ticks()/100)*0.1+math.sin(pygame.time.get_ticks()/61.8)*0.06)*radius*blow_multiply
# here grass
            imagination_surface.blit(grass, (-mod_radius,const.HEIGHT-150))
            # pygame.draw.rect(imagination_surface, (55, 155, 55), (0, 345, const.WIDTH, const.HEIGHT - 300))
            # KID RIG # KID RIG # KID RIG 
            # KID RIG # KID RIG # KID RIG
            # KID RIG # KID RIG # KID RIG
            # KID RIG # KID RIG # KID RIG
            body_x_offset=(kid_size[0]*0.6)-body_size[0]/2
            kid_surface.fill((0,0,0,0))
            if debug:
                kid_surface.fill((255,0,0,255))
            kid_head_surface.fill((0,0,0,0))
            kid_head_surface.blit(kid_head, (0,0))
            kid_head_surface.blit(lip, (head_size[0]*0.8,head_size[1]*0.75))
            kid_surface.blit(kid_body, (body_x_offset,kid_size[1]-body_size[1]))
            head_pivot=(head_size[0]*0.65,head_size[1]*0.98)
            body_pivot=(body_x_offset+body_size[0]*0.45,kid_size[1]*0.64)
            if debug:
                pygame.draw.circle(kid_head_surface, (100, 100, 200,128),head_pivot , 10, 0)  # (r, g, b) is color, (x, y) is center, R is radius and w is the thickness of the circle border.
                pygame.draw.circle(kid_surface, (000, 200, 00,128),body_pivot , 10, 0)  # (r, g, b) is color, (x, y) is center, R is radius and w is the thickness of the circle border.
            
            actual_head_rotation= pygame.math.lerp(actual_head_rotation, head_rotation, dt * 6)
            blitRotate(kid_surface, kid_head_surface, body_pivot, 
                       # (head_size[0]*0.5,head_size[1])
                       head_pivot
                       ,actual_head_rotation)
            # kid_surface.blit(kid_head_surface, (kid_size[0]*0,0))
            # kid_surface.blit(lip_clossed, ((const.WIDTH / 2) - 265 - actual_radius, (const.HEIGHT / 2) - 160))
            imagination_surface.blit(kid_surface, ((const.WIDTH / 2) - 230 - mod_radius, (const.HEIGHT / 2) - 180))
            imagination_surface.blit(cat, ((const.WIDTH) - 290 - mod_radius, (const.HEIGHT) - 160))

            imagination_surface.blit(pygame.transform.flip(grass,True,False), (-mod_radius,const.HEIGHT-115))
            pygame.draw.circle(imagination_surface, (100, 100, 200), ((const.WIDTH / 2), (const.HEIGHT / 2)), mod_radius, 2)  # (r, g, b) is color, (x, y) is center, R is radius and w is the thickness of the circle border.
            pygame.draw.circle(transparent_surface, (100, 100, 250, 128), ((const.WIDTH / 2), (const.HEIGHT / 2)), mod_radius, 0)

            if radius >= 0:
                radius -= bubble_decrease_speed * dt
                hurry_time=-1
            else:
                radius = 0
                hurry_time=pygame.time.get_ticks()
                print("HURRYYYYYYYYYY!")
            tutorial()
            imagination_surface.blit(transparent_surface, (0, 0))
        elif game_over:
            # pass
            # imagination_surface.fill((255, 0, 0))
            imagination_surface.blit(game_over_imagination_surface, (0, 0))
            # print("the game is over!")
        imagination_surface.blit(my_font.render(f"🫧 {bubble_points} 👇 {enemies_points}", False, (0, 0, 0)), (0, 0))
        if not game_started:

    # SPLASH SPLASH SPLASH
    # SPLASH SPLASH SPLASH
    # SPLASH SPLASH SPLASH
    # SPLASH SPLASH SPLASH

                mouse_diff=(mouse_pos[0]-const.WIDTH/2,mouse_pos[1]-const.HEIGHT/2)
                # print(f"mouse_diff: {mouse_diff}")
                splash_surface.blit(splash_bg, -pygame.math.Vector2(const.WIDTH*0.15,const.HEIGHT*0.15)+pygame.math.Vector2(mouse_diff)*-0.1)
                splash_surface.blit(splash_txt,(0,0))
                # splash_surface.blit(splash_txt,-pygame.math.Vector2(const.WIDTH,const.HEIGHT)+pygame.math.Vector2(mouse_diff)*-0.05)
                splash_surface.blit(splash_fg, -pygame.math.Vector2(const.WIDTH*0.15,const.HEIGHT*0.15)+pygame.math.Vector2(mouse_diff)*0.1)
                screen.blit(splash_surface, (0, 0))
        # if (not game_started) or game_over:

        screen.blit(imagination_surface, (0, 0))
        if (not game_started) or game_over:
            screen.blit(ui_surface, (0, 0))

        pygame.display.update()


if __name__ == "__main__":
    main()
    # asyncio.run(main())
