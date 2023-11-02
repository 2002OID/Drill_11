# 이것은 각 상태들을 객체로 구현한 것임.
import random

from pico2d import get_time, load_image, load_font, clamp
import game_world
import game_framework

# state event check
# ( state event type, event value )

# time_out = lambda e : e[0] == 'TIME_OUT'

# Bird Run Speed
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 65.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Bird Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 24

sheet_x = 183.6
sheet_y = 506.0 / 3

class Run:

    @staticmethod
    def enter(bird, e):
        pass

    @staticmethod
    def exit(bird, e):
        pass

    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 14
        bird.x += bird.dir * RUN_SPEED_PPS * game_framework.frame_time
        bird.x = clamp(25, bird.x, 1600 - 25)
        if bird.dir == 1 and bird.x > 1550:
            bird.dir = -1
        elif bird.dir == -1 and bird.x < 50:
            bird.dir = 1

    @staticmethod
    def draw(bird):
        match bird.frame // 5:
            case 0:
                sheet_h = 2
            case 1:
                sheet_h = 1
            case 2:
                sheet_h = 0
        if bird.dir == 1:
            bird.image.clip_composite_draw(int(sheet_x * (int(bird.frame) % 5)), int(sheet_y * sheet_h), int(sheet_x), int(sheet_y), 0, '', bird.x, bird.y, 50, 50)
        elif bird.dir == -1:
            bird.image.clip_composite_draw(int(sheet_x * (int(bird.frame) % 5)), int(sheet_y * sheet_h), int(sheet_x), int(sheet_y), 0, 'h',  bird.x, bird.y, 50, 50)


class StateMachine:
    def __init__(self, bird):
        self.bird = bird
        self.cur_state = Run

    def start(self):
        self.cur_state.enter(self.bird, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.bird)

    def handle_event(self, e):
        pass

    def draw(self):
        self.cur_state.draw(self.bird)


class Bird:
    def __init__(self):
        self.x, self.y = random.randint(100, 1500), 500
        self.frame = random.randint(0, 13)
        self.action = 3
        self.face_dir = 1
        self.dir = 1
        self.image = load_image('bird_animation.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.font = load_font('ENCR10B.TTF', 16)

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x - 60, self.y + 50, f'({get_time():.2f})', (255, 255, 0))
