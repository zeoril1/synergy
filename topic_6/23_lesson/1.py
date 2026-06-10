#!/usr/bin/env python3
"""
Лесная Пожарная Игра — Вертолёт 🚁

Управление: WASD — движение, E — тушить/вода, H — госпиталь, P — магазин
  SPACE — тик, Q — выход, F1 — сохранить, F2 — загрузить

T-дерево @-пожар #-гарь ~-вода H-госпиталь $-магазин X-вертолёт C/O-облака *-молния
"""

import os, sys, time, json, random
from datetime import datetime

# --- Константы ---
CELL_GRASS, CELL_WATER, CELL_TREE, CELL_BURNING = ' ', '~', 'T', '@'
CELL_BURNED, CELL_HOSPITAL, CELL_SHOP = '#', 'H', '$'
CELL_CLOUD, CELL_DARK_CLOUD, CELL_LIGHTNING, CELL_HELI = 'C', 'O', '*', 'X'

C_RESET = '\033[0m'
COLOR_MAP = {
    CELL_GRASS: '\033[48;5;28m', CELL_WATER: '\033[48;5;27m',
    CELL_TREE: '\033[48;5;22m\033[38;5;46m', CELL_BURNING: '\033[48;5;214m\033[38;5;196m',
    CELL_BURNED: '\033[48;5;52m\033[38;5;130m', CELL_HOSPITAL: '\033[48;5;231m\033[38;5;196m',
    CELL_SHOP: '\033[48;5;220m\033[38;5;16m', CELL_CLOUD: '\033[48;5;250m',
    CELL_DARK_CLOUD: '\033[48;5;240m', CELL_LIGHTNING: '\033[48;5;226m\033[38;5;16m',
    CELL_HELI: '\033[48;5;227m\033[38;5;16m',
}

DEFAULT_WIDTH, DEFAULT_HEIGHT = 30, 18
DEFAULT_LIVES, DEFAULT_TANKS = 5, 3
SCORE_SAVE, SCORE_BURN = 50, -30
HOSPITAL_COST, HOSPITAL_HEAL, SHOP_COST = 100, 2, 150

TREE_GROW_CHANCE = 0.001
FIRE_START_CHANCE = 0.005
FIRE_SPREAD_CHANCE = 0.005
LIGHTNING_CHANCE = 0.03
RAIN_CHANCE = 0.002
BURN_MAX_TICKS = 100


class Field:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.grid = {}
        self.burn_ticks = {}
        self.clouds = []
        self.lightning = None
        self.raining = False
        self.rain_ttl = 0
        self.lightning_spread = []
        for y in range(h):
            for x in range(w):
                self.grid[(x, y)] = CELL_GRASS

    def inside(self, x, y):
        return 0 <= x < self.w and 0 <= y < self.h

    def get(self, x, y):
        return self.grid.get((x, y), CELL_GRASS) if self.inside(x, y) else None

    def set(self, x, y, ch):
        if self.inside(x, y):
            self.grid[(x, y)] = ch
            if ch != CELL_BURNING and (x, y) in self.burn_ticks:
                del self.burn_ticks[(x, y)]

    def neighbors(self, x, y):
        res = []
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            nx, ny = x + dx, y + dy
            if self.inside(nx, ny):
                res.append((nx, ny))
        return res

    def gen_rivers(self, count=2):
        for _ in range(count):
            if random.random() < 0.5:
                x, y, dx, dy = 0, random.randint(0, self.h - 1), 1, 0
            else:
                x, y, dx, dy = random.randint(0, self.w - 1), 0, 0, 1
            for _ in range(random.randint(self.w // 2, self.w + self.h)):
                if not self.inside(x, y):
                    break
                cur = self.grid.get((x, y))
                if cur in (CELL_GRASS, CELL_TREE, CELL_BURNED):
                    self.grid[(x, y)] = CELL_WATER
                if random.random() < 0.25:
                    dx, dy = random.choice(((0, -1), (0, 1), (1, 0), (-1, 0)))
                x, y = x + dx, y + dy

    def gen_trees(self):
        empty = [(x, y) for (x, y), c in self.grid.items() if c == CELL_GRASS]
        random.shuffle(empty)
        for x, y in empty[:int(len(empty) * 0.25)]:
            self.grid[(x, y)] = CELL_TREE

    def place(self, ch, count=1):
        empty = [(x, y) for (x, y), c in self.grid.items() if c == CELL_GRASS]
        if not empty:
            return
        random.shuffle(empty)
        for x, y in empty[:min(count, len(empty))]:
            self.grid[(x, y)] = ch

    def ignite_random(self):
        trees = [(x, y) for (x, y), c in self.grid.items() if c == CELL_TREE]
        if not trees:
            return False
        x, y = random.choice(trees)
        self.grid[(x, y)] = CELL_BURNING
        self.burn_ticks[(x, y)] = 0
        return True

    def tick_burn(self):
        done = []
        for (x, y) in list(self.burn_ticks.keys()):
            if self.grid.get((x, y)) != CELL_BURNING:
                self.burn_ticks.pop((x, y), None)
                continue
            self.burn_ticks[(x, y)] += 1
            if self.burn_ticks[(x, y)] >= BURN_MAX_TICKS:
                done.append((x, y))
        for x, y in done:
            self.grid[(x, y)] = CELL_BURNED
            self.burn_ticks.pop((x, y), None)
        return done

    def spread_fire(self):
        burning = set()
        for (x, y), c in self.grid.items():
            if c == CELL_BURNING:
                burning.add((x, y))
        for (x, y) in list(self.burn_ticks.keys()):
            if self.grid.get((x, y)) != CELL_BURNING:
                self.burn_ticks.pop((x, y), None)
                continue
            burning.add((x, y))
        for x, y in burning:
            for nx, ny in self.neighbors(x, y):
                if self.grid.get((nx, ny)) == CELL_TREE and random.random() < FIRE_SPREAD_CHANCE:
                    self.grid[(nx, ny)] = CELL_BURNING
                    self.burn_ticks[(nx, ny)] = 0
        if self.lightning_spread:
            spread = self.lightning_spread
            self.lightning_spread = []
            for sx, sy in spread:
                for nx, ny in self.neighbors(sx, sy):
                    if self.grid.get((nx, ny)) == CELL_TREE:
                        self.grid[(nx, ny)] = CELL_BURNING
                        self.burn_ticks[(nx, ny)] = 0

    def grow_tree(self):
        empty = [(x, y) for (x, y), c in self.grid.items() if c == CELL_GRASS]
        for x, y in empty:
            if random.random() < TREE_GROW_CHANCE:
                self.grid[(x, y)] = CELL_TREE
                return

    def gen_clouds(self, count=2):
        self.clouds = []
        for i in range(count):
            x = random.randint(0, self.w - 1)
            y = random.randint(2, self.h - 3)
            dark = True if i == 0 else (random.random() < 0.3)
            self.clouds.append([x, y, dark])

    def lightning_strike(self):
        if random.random() >= LIGHTNING_CHANCE:
            return False
        dark = [c for c in self.clouds if c[2]]
        if not dark:
            return False
        c = random.choice(dark)
        x, y = c[0] + random.randint(-2, 2), c[1] + random.randint(-1, 1)
        if not self.inside(x, y):
            return False
        self.lightning = (x, y, 3)
        for nx, ny in self.neighbors(x, y) + [(x, y)]:
            if self.grid.get((nx, ny)) == CELL_TREE:
                self.grid[(nx, ny)] = CELL_BURNING
                self.burn_ticks[(nx, ny)] = 0
        return True

    def tick_lightning(self):
        if self.lightning is None:
            return
        x, y, ttl = self.lightning
        ttl -= 1
        if ttl <= 0:
            self.lightning = None
            if self.inside(x, y) and self.grid.get((x, y)) == CELL_LIGHTNING:
                self.grid[(x, y)] = CELL_GRASS
            return
        self.lightning = (x, y, ttl)
        if self.inside(x, y):
            cur = self.grid.get((x, y))
            if cur not in (CELL_HELI, CELL_HOSPITAL, CELL_SHOP, CELL_BURNING):
                self.grid[(x, y)] = CELL_LIGHTNING

    def start_rain(self):
        if random.random() < RAIN_CHANCE and not self.raining:
            self.raining = True
            self.rain_ttl = random.randint(4, 10)

    def tick_rain(self):
        if not self.raining:
            return
        self.rain_ttl -= 1
        for (x, y), c in list(self.grid.items()):
            if c == CELL_BURNING and random.random() < 0.25:
                self.grid[(x, y)] = CELL_GRASS
                self.burn_ticks.pop((x, y), None)
        if self.rain_ttl <= 0:
            self.raining = False

    def update_weather(self):
        has_dark = any(c[2] for c in self.clouds)
        for c in self.clouds:
            c[0] += 1
            if c[0] >= self.w + 2:
                c[0] = -2
                c[1] = random.randint(2, self.h - 3)
                if not has_dark:
                    c[2], has_dark = True, True
                else:
                    c[2] = random.random() < 0.3
            elif c[2]:
                has_dark = True
        self.lightning_strike()
        self.tick_lightning()
        self.start_rain()
        self.tick_rain()


class Helicopter:
    def __init__(self, field):
        self.x = field.w // 2
        self.y = field.h // 2
        self.water = 0
        self.max_water = DEFAULT_TANKS
        self.lives = DEFAULT_LIVES
        self.score = 0
        self._saved_cell = field.grid.get((self.x, self.y), CELL_GRASS)

    def move(self, dx, dy, field):
        nx, ny = self.x + dx, self.y + dy
        if not field.inside(nx, ny):
            return False
        target = field.grid.get((nx, ny), CELL_GRASS)
        if target == CELL_BURNING:
            self.lives -= 1
            field.grid[(self.x, self.y)] = self._saved_cell
            self._saved_cell = field.grid.get((self.x, self.y), CELL_GRASS)
            return True
        field.grid[(self.x, self.y)] = self._saved_cell
        self.x, self.y = nx, ny
        self._saved_cell = target
        return True

    def take_water(self, field):
        if self.water >= self.max_water:
            return False
        if self._saved_cell == CELL_WATER:
            self.water += 1
            return True
        for nx, ny in field.neighbors(self.x, self.y):
            if field.grid.get((nx, ny)) == CELL_WATER:
                self.water += 1
                return True
        return False

    def extinguish(self, field):
        if self.water <= 0:
            return False
        for nx, ny in field.neighbors(self.x, self.y):
            if field.grid.get((nx, ny)) == CELL_BURNING:
                self.water -= 1
                field.grid[(nx, ny)] = CELL_GRASS
                field.burn_ticks.pop((nx, ny), None)
                self.score += SCORE_SAVE
                return True
        return False

    def visit_hospital(self, field):
        if self._saved_cell != CELL_HOSPITAL:
            return False, "Вы не в госпитале!"
        if self.score < HOSPITAL_COST:
            return False, f"Нужно {HOSPITAL_COST} очков!"
        self.score -= HOSPITAL_COST
        self.lives += HOSPITAL_HEAL
        return True, f"Госпиталь: -{HOSPITAL_COST} очков, +{HOSPITAL_HEAL} жизней!"

    def visit_shop(self, field):
        if self._saved_cell != CELL_SHOP:
            return False, "Вы не в магазине!"
        if self.score < SHOP_COST:
            return False, f"Нужно {SHOP_COST} очков!"
        self.score -= SHOP_COST
        self.max_water += 1
        return True, f"Магазин: -{SHOP_COST} очков, +1 резервуар!"

    def damage(self, field):
        self.lives -= 1
        return self.lives <= 0

    def draw(self, field):
        field.grid[(self.x, self.y)] = CELL_HELI


SAVE_FILE = 'savegame.json'


def save_game(field, heli, tick):
    data = {
        'w': field.w, 'h': field.h,
        'cells': {f'{x},{y}': c for (x, y), c in field.grid.items()},
        'burn': {f'{x},{y}': t for (x, y), t in field.burn_ticks.items()},
        'clouds': field.clouds, 'raining': field.raining, 'rain_ttl': field.rain_ttl,
        'heli': {'x': heli.x, 'y': heli.y, 'water': heli.water, 'max_water': heli.max_water,
                 'lives': heli.lives, 'score': heli.score},
        'tick': tick, 'time': datetime.now().isoformat(),
    }
    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def load_game():
    with open(SAVE_FILE, 'r') as f:
        data = json.load(f)
    field = Field(data['w'], data['h'])
    field.grid = {}
    for k, v in data['cells'].items():
        x, y = map(int, k.split(','))
        field.grid[(x, y)] = v
    field.burn_ticks = {}
    for k, v in data['burn'].items():
        x, y = map(int, k.split(','))
        field.burn_ticks[(x, y)] = v
    field.clouds = data['clouds']
    field.raining = data['raining']
    field.rain_ttl = data['rain_ttl']
    hd = data['heli']
    heli = Helicopter(field)
    heli.x, heli.y = hd['x'], hd['y']
    heli.water, heli.max_water = hd['water'], hd['max_water']
    heli.lives, heli.score = hd['lives'], hd['score']
    return field, heli, data['tick']


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def draw(field, heli, tick, msg=""):
    clear()
    cloud_cells = set()
    for cx, cy, dark in field.clouds:
        for dx in range(-2, 3):
            for dy in range(-1, 2):
                nx, ny = cx + dx, cy + dy
                if field.inside(nx, ny):
                    cloud_cells.add((nx, ny, dark))

    important = {CELL_HELI, CELL_HOSPITAL, CELL_SHOP, CELL_BURNING, CELL_LIGHTNING, CELL_BURNED}
    print('┌' + '─' * field.w + '┐')
    for y in range(field.h):
        line = '│'
        for x in range(field.w):
            ch = field.grid.get((x, y), CELL_GRASS)
            if (x, y, True) in cloud_cells and ch not in important:
                ch = CELL_DARK_CLOUD
            elif (x, y, False) in cloud_cells and ch not in important:
                ch = CELL_CLOUD
            line += COLOR_MAP.get(ch, COLOR_MAP[CELL_GRASS]) + ch + C_RESET
        line += '│'
        print(line)
    print('└' + '─' * field.w + 'И')

    print(f" Тик: {tick}  |  Очки: {heli.score}  |  Жизни: {heli.lives}  |  Вода: {heli.water}/{heli.max_water}")
    print('─' * 60)
    weather = []
    if field.raining:
        weather.append("ДОЖДЬ")
    if field.lightning:
        weather.append("ГРОЗА")
    if weather:
        print(" Погода:", ", ".join(weather))
        print('─' * 60)
    print(" WASD:движение | E:тушить/вода | H:госпиталь | P:магазин")
    print(" SPACE:тик | Q:выход | F1:сохранить | F2:загрузить")
    if msg:
        print('─' * 60)
        print(" >>", msg)


def get_key():
    import termios, tty
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            ch2 = sys.stdin.read(1)
            if ch2 == '[':
                ch3 = sys.stdin.read(1)
                if ch3 in ('1', '2'):
                    ch4 = sys.stdin.read(1)
                    return {'1': '\x1b[11~', '2': '\x1b[12~'}.get(ch3, ch + ch2 + ch3 + ch4)
                return ch + ch2 + ch3
            return ch + ch2
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def game_tick(field, heli, tick, msg):
    tick += 1
    field.grow_tree()
    burned = field.tick_burn()
    for bx, by in burned:
        heli.score += SCORE_BURN
        msg = f"Дерево сгорело! {SCORE_BURN} очков"
    field.spread_fire()
    if random.random() < FIRE_START_CHANCE:
        if field.ignite_random():
            msg = "Новый пожар!"
    burning_now = any(c == CELL_BURNING for (x, y), c in field.grid.items())
    if not burning_now and field.ignite_random():
        msg = "Случайный пожар!"
    field.update_weather()
    return tick, msg


def init_new_game(choice=''):
    sizes = {'1': (18, 10), '3': (40, 22)}
    w, h = sizes.get(choice, (DEFAULT_WIDTH, DEFAULT_HEIGHT))
    field = Field(w, h)
    heli = Helicopter(field)
    print("Генерация мира...")
    field.gen_rivers(random.randint(1, 3))
    field.gen_trees()
    field.place(CELL_HOSPITAL, 1)
    field.place(CELL_SHOP, 1)
    field.gen_clouds(random.randint(1, 2))
    field.ignite_random()
    return field, heli, 0


def main():
    clear()
    print("=" * 60)
    print("           ЛЕСНАЯ ПОЖАРНАЯ ИГРА")
    print("=" * 60)
    print()
    print("Выберите размер поля:")
    print("  1 - Маленькое (18x10)")
    print("  2 - Среднее  (30x18) [по умолчанию]")
    print("  3 - Большое  (40x22)")
    print("  L - Загрузить сохранённую игру")
    print()
    choice = input("Ваш выбор: ").strip().lower()

    if choice == 'l':
        try:
            field, heli, tick = load_game()
            msg = "Игра загружена!"
        except Exception:
            print("Нет сохранения! Начинаем новую игру.")
            time.sleep(1.5)
            field, heli, tick = init_new_game()
            msg = "Добро пожаловать!"
    else:
        field, heli, tick = init_new_game(choice)
        msg = "Добро пожаловать!"

    running = True
    while running:
        heli.draw(field)
        draw(field, heli, tick, msg)
        msg = ""

        key = get_key()
        if key == 'q':
            running = False
            continue

        do_tick = True

        if key in ('w', 's', 'a', 'd'):
            dx = {'w': (0, -1), 's': (0, 1), 'a': (-1, 0), 'd': (1, 0)}[key]
            heli.move(dx[0], dx[1], field)
        elif key == 'e':
            if heli.extinguish(field):
                msg = "Пожар потушен! +50 очков"
                if not any(c == CELL_BURNING for c in field.grid.values()) and field.ignite_random():
                    msg += " Но появился новый пожар!"
            elif heli.take_water(field):
                msg = "Вода взята!"
            else:
                msg = "Здесь нет огня или воды!"
        elif key == 'h':
            _, msg = heli.visit_hospital(field)
        elif key == 'p':
            _, msg = heli.visit_shop(field)
        elif key == '\x1b[11~':
            try:
                save_game(field, heli, tick)
                msg = "Игра сохранена!"
            except Exception as e:
                msg = f"Ошибка сохранения: {e}"
            do_tick = False
        elif key == '\x1b[12~':
            try:
                field, heli, tick = load_game()
                msg = "Игра загружена!"
            except Exception as e:
                msg = f"Ошибка загрузки: {e}"
            do_tick = False

        if do_tick:
            tick, msg = game_tick(field, heli, tick, msg)

        if heli.lives <= 0:
            draw(field, heli, tick, "Жизни закончились!")
            time.sleep(2)
            running = False

    clear()
    print("=" * 60)
    print("              ИГРА ОКОНЧЕНА")
    print("=" * 60)
    print(f"  Пройдено тиков:    {tick}")
    print(f"  Итоговый счёт:     {heli.score}")
    print(f"  Осталось жизней:   {heli.lives}")
    print(f"  Вместимость воды:  {heli.max_water}")
    print()
    input("  Нажмите Enter для выхода...")
    clear()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print("\nИгра прервана пользователем.")
    except Exception as e:
        clear()
        print(f"\nОШИБКА: {e}")
        import traceback
        traceback.print_exc()