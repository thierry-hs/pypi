import math
import random
import sys
import pygame

# --- CONFIGURAÇÕES GERAIS ---
pygame.init()
pygame.font.init()

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 650
FPS = 60

# Cores (RGB)
GREEN = (34, 139, 34)
LAWN_GREEN1 = (118, 203, 76)
LAWN_GREEN2 = (142, 222, 93)
BROWN = (139, 69, 19)
YELLOW = (255, 215, 0)
RED = (220, 20, 60)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
ICE_BLUE = (135, 206, 250)
PURPLE = (147, 112, 219)
DARK_RED = (139, 0, 0)
ORANGE = (255, 140, 0)

# Dimensões da Grade
ROWS = 5
COLS = 9
GRID_X = 140
GRID_Y = 120
TILE_W = 95
TILE_H = 95

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Plantas vs Zombies — Modo Duplo 🌻 vs 🧟")
clock = pygame.time.Clock()

font_small = pygame.font.SysFont("Comic Sans MS", 16, bold=True)
font_main = pygame.font.SysFont("Comic Sans MS", 22, bold=True)
font_title = pygame.font.SysFont("Comic Sans MS", 36, bold=True)


# --- RECURSOS (SOL / CÉREBRO) ---
class Resource:

    def __init__(self, x, y, res_type="sun", target_y=None):
        self.x = x
        self.y = y
        self.res_type = res_type
        self.radius = 20
        self.target_y = target_y if target_y is not None else y
        self.alive = True
        self.spawn_time = pygame.time.get_ticks()
        self.rect = pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2,
        )

    def update(self):
        if self.y < self.target_y:
            self.y += 2
            self.rect.y = int(self.y - self.radius)

        if pygame.time.get_ticks() - self.spawn_time > 8000:
            self.alive = False

    def draw(self, surface):
        if self.res_type == "sun":
            pygame.draw.circle(
                surface, YELLOW, (int(self.x), int(self.y)), self.radius
            )
            pygame.draw.circle(
                surface, ORANGE, (int(self.x), int(self.y)), self.radius - 5, 2
            )
        else:  # brain
            pygame.draw.circle(
                surface, PURPLE, (int(self.x), int(self.y)), self.radius
            )
            pygame.draw.circle(
                surface,
                (255, 182, 193),
                (int(self.x), int(self.y)),
                self.radius - 5,
            )


# --- PROJÉTEIS ---
class Pea:

    def __init__(self, x, y, row, is_ice=False):
        self.x = x
        self.y = y
        self.row = row
        self.speed = 7
        self.damage = 20
        self.is_ice = is_ice
        self.radius = 8
        self.rect = pygame.Rect(self.x - 8, self.y - 8, 16, 16)
        self.alive = True

    def update(self):
        self.x += self.speed
        self.rect.x = int(self.x)
        if self.x > SCREEN_WIDTH:
            self.alive = False

    def draw(self, surface):
        color = ICE_BLUE if self.is_ice else (50, 205, 50)
        pygame.draw.circle(
            surface, color, (int(self.x), int(self.y)), self.radius
        )
        pygame.draw.circle(
            surface, (0, 100, 0), (int(self.x), int(self.y)), self.radius, 1
        )


# --- EXPLOSÃO (BOMBA CEREJA) ---
class Explosion:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10
        self.max_radius = 90
        self.alive = True

    def update(self):
        self.radius += 5
        if self.radius >= self.max_radius:
            self.alive = False

    def draw(self, surface):
        pygame.draw.circle(
            surface, RED, (int(self.x), int(self.y)), int(self.radius)
        )
        pygame.draw.circle(
            surface, ORANGE, (int(self.x), int(self.y)), int(self.radius * 0.7)
        )


# --- PLANTAS ---
class Plant:

    def __init__(self, row, col, plant_type):
        self.row = row
        self.col = col
        self.x = GRID_X + col * TILE_W + TILE_W // 2
        self.y = GRID_Y + row * TILE_H + TILE_H // 2
        self.plant_type = plant_type
        self.rect = pygame.Rect(
            GRID_X + col * TILE_W + 10,
            GRID_Y + row * TILE_H + 10,
            TILE_W - 20,
            TILE_H - 20,
        )
        self.created_at = pygame.time.get_ticks()

        # Atributos por tipo
        stats = {
            "sunflower": {"hp": 100},
            "peashooter": {"hp": 100},
            "wallnut": {"hp": 400},
            "snowpea": {"hp": 100},
            "cherrybomb": {"hp": 300},
            "repeater": {"hp": 100},
        }
        self.hp = stats[plant_type]["hp"]
        self.max_hp = self.hp
        self.last_action_time = pygame.time.get_ticks()

    def update(self, game):
        now = pygame.time.get_ticks()

        # Girassol
        if self.plant_type == "sunflower":
            if now - self.last_action_time > 7000:
                self.last_action_time = now
                game.resources.append(
                    Resource(
                        self.x + random.randint(-15, 15),
                        self.y - 10,
                        res_type="sun",
                    )
                )

        # Ervilharada e Ervilha Gelada
        elif self.plant_type in ["peashooter", "snowpea"]:
            zombies_in_row = [
                z for z in game.zombies if z.row == self.row and z.x > self.x
            ]
            if zombies_in_row and (now - self.last_action_time > 1800):
                self.last_action_time = now
                is_ice = self.plant_type == "snowpea"
                game.peas.append(
                    Pea(self.x + 20, self.y - 10, self.row, is_ice=is_ice)
                )

        # Repetidora (Dispara 2 ervilhas consecutivas)
        elif self.plant_type == "repeater":
            zombies_in_row = [
                z for z in game.zombies if z.row == self.row and z.x > self.x
            ]
            if zombies_in_row and (now - self.last_action_time > 1800):
                self.last_action_time = now
                game.peas.append(Pea(self.x + 20, self.y - 10, self.row))
                game.peas.append(Pea(self.x + 45, self.y - 10, self.row))

        # Bomba Cereja (Explode após 1 segundo)
        elif self.plant_type == "cherrybomb":
            if now - self.created_at >= 1000:
                game.explosions.append(Explosion(self.x, self.y))
                # Causa dano massivo na área 3x3
                for z in game.zombies[:]:
                    if (
                        abs(z.row - self.row) <= 1
                        and abs(z.x - self.x) <= TILE_W * 1.5
                    ):
                        z.hp -= 500
                        if z.hp <= 0 and z in game.zombies:
                            game.zombies.remove(z)
                game.plants.remove(self)

    def draw(self, surface):
        if self.plant_type == "sunflower":
            pygame.draw.circle(surface, YELLOW, (self.x, self.y), 22)
            pygame.draw.circle(surface, BROWN, (self.x, self.y), 12)
            pygame.draw.rect(surface, GREEN, (self.x - 4, self.y + 15, 8, 20))

        elif self.plant_type == "peashooter":
            pygame.draw.circle(surface, GREEN, (self.x - 5, self.y - 5), 20)
            pygame.draw.rect(
                surface, GREEN, (self.x, self.y - 12, 22, 14), border_radius=4
            )
            pygame.draw.rect(surface, GREEN, (self.x - 4, self.y + 10, 8, 25))

        elif self.plant_type == "snowpea":
            pygame.draw.circle(surface, ICE_BLUE, (self.x - 5, self.y - 5), 20)
            pygame.draw.rect(
                surface,
                ICE_BLUE,
                (self.x, self.y - 12, 22, 14),
                border_radius=4,
            )
            pygame.draw.rect(surface, GREEN, (self.x - 4, self.y + 10, 8, 25))

        elif self.plant_type == "repeater":
            pygame.draw.circle(
                surface, (0, 150, 0), (self.x - 5, self.y - 5), 20
            )
            pygame.draw.rect(
                surface,
                (0, 150, 0),
                (self.x - 5, self.y - 12, 30, 14),
                border_radius=4,
            )
            pygame.draw.rect(surface, GREEN, (self.x - 4, self.y + 10, 8, 25))

        elif self.plant_type == "wallnut":
            color = BROWN if self.hp > 200 else (100, 50, 10)
            pygame.draw.ellipse(
                surface, color, (self.x - 22, self.y - 25, 44, 52)
            )
            pygame.draw.circle(surface, WHITE, (self.x - 8, self.y - 8), 5)
            pygame.draw.circle(surface, BLACK, (self.x - 8, self.y - 8), 2)
            pygame.draw.circle(surface, WHITE, (self.x + 8, self.y - 8), 5)
            pygame.draw.circle(surface, BLACK, (self.x + 8, self.y - 8), 2)

        elif self.plant_type == "cherrybomb":
            pygame.draw.circle(surface, DARK_RED, (self.x - 12, self.y), 15)
            pygame.draw.circle(surface, DARK_RED, (self.x + 12, self.y), 15)
            pygame.draw.line(
                surface,
                BROWN,
                (self.x - 12, self.y),
                (self.x, self.y - 20),
                3,
            )
            pygame.draw.line(
                surface, BROWN, (self.x + 12, self.y), (self.x, self.y - 20), 3
            )


# --- ZUMBIS ---
class Zombie:

    def __init__(self, row, z_type="normal"):
        self.row = row
        self.x = SCREEN_WIDTH + 30
        self.y = GRID_Y + row * TILE_H + TILE_H // 2
        self.z_type = z_type
        self.slow_timer = 0

        stats = {
            "normal": {"hp": 100, "speed": 0.5},
            "cone": {"hp": 250, "speed": 0.5},
            "bucket": {"hp": 500, "speed": 0.45},
            "runner": {"hp": 90, "speed": 1.0},
        }
        self.hp = stats[z_type]["hp"]
        self.max_hp = self.hp
        self.base_speed = stats[z_type]["speed"]
        self.damage = 0.5
        self.rect = pygame.Rect(self.x - 20, self.y - 30, 40, 60)

    def update(self, game):
        # Controle de lentidão por gelo
        speed = self.base_speed
        if self.slow_timer > 0:
            speed *= 0.5
            self.slow_timer -= 1

        eating = False
        for plant in game.plants:
            if plant.row == self.row and self.rect.colliderect(plant.rect):
                eating = True
                plant.hp -= self.damage
                if plant.hp <= 0 and plant in game.plants:
                    game.plants.remove(plant)
                break

        if not eating:
            self.x -= speed

        self.rect.x = int(self.x - 20)

    def draw(self, surface):
        # Tinta de gelo
        body_color = ICE_BLUE if self.slow_timer > 0 else (107, 142, 35)

        # Corpo
        pygame.draw.rect(
            surface, GRAY, (self.x - 15, self.y - 10, 30, 35), border_radius=3
        )
        # Cabeça
        pygame.draw.circle(surface, body_color, (int(self.x), self.y - 20), 16)
        # Olho
        pygame.draw.circle(surface, RED, (int(self.x) - 5, self.y - 22), 3)

        # Acessórios
        if self.z_type == "cone":
            pygame.draw.polygon(
                surface,
                ORANGE,
                [
                    (self.x - 12, self.y - 25),
                    (self.x + 12, self.y - 25),
                    (self.x, self.y - 50),
                ],
            )
        elif self.z_type == "bucket":
            pygame.draw.rect(
                surface,
                GRAY,
                (self.x - 12, self.y - 42, 24, 20),
                border_radius=2,
            )

        # Barra de Vida
        if self.hp < self.max_hp:
            bar_w = 30
            curr_w = int((self.hp / self.max_hp) * bar_w)
            pygame.draw.rect(surface, RED, (self.x - 15, self.y - 48, bar_w, 4))
            pygame.draw.rect(
                surface, GREEN, (self.x - 15, self.y - 48, curr_w, 4)
            )


# --- GERENCIADOR PRINCIPAL DO JOGO ---
class PvZGame:

    def __init__(self):
        self.state = "MENU"  # 'MENU', 'GAME_PLANTS', 'GAME_ZOMBIES', 'GAME_OVER', 'VICTORY'
        self.mode = None  # 'PLANTS' ou 'ZOMBIES'

        self.reset_game()

    def reset_game(self):
        self.sun_score = 150
        self.brain_score = 150
        self.selected_item = None

        self.plants = []
        self.zombies = []
        self.peas = []
        self.resources = []
        self.explosions = []

        self.last_resource_spawn = pygame.time.get_ticks()
        self.last_ai_spawn = pygame.time.get_ticks()
        self.ai_spawn_rate = 7000

        # Cards para Modo Planta
        self.plant_cards = [
            {"type": "sunflower", "cost": 50, "name": "Girassol"},
            {"type": "peashooter", "cost": 100, "name": "Ervilha"},
            {"type": "wallnut", "cost": 50, "name": "Noz"},
            {"type": "snowpea", "cost": 175, "name": "Ervilha Gelo"},
            {"type": "cherrybomb", "cost": 150, "name": "Cereja Bomba"},
            {"type": "repeater", "cost": 200, "name": "Repetidora"},
        ]

        # Cards para Modo Zumbi
        self.zombie_cards = [
            {"type": "normal", "cost": 50, "name": "Normal"},
            {"type": "cone", "cost": 100, "name": "Cone"},
            {"type": "runner", "cost": 125, "name": "Corredor"},
            {"type": "bucket", "cost": 175, "name": "Balde"},
        ]

    def handle_click(self, pos):
        # 1. MENU PRINCIPAL
        if self.state == "MENU":
            btn_plants = pygame.Rect(
                SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 40, 360, 50
            )
            btn_zombies = pygame.Rect(
                SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + 30, 360, 50
            )

            if btn_plants.collidepoint(pos):
                self.mode = "PLANTS"
                self.state = "GAME_PLANTS"
                self.reset_game()
            elif btn_zombies.collidepoint(pos):
                self.mode = "ZOMBIES"
                self.state = "GAME_ZOMBIES"
                self.reset_game()
                # Preencher o campo com algumas plantas para o jogador atacar
                self.setup_zombie_mode_field()
            return

        # 2. TELA FINAL DE JOGO (REINICIAR)
        if self.state in ["GAME_OVER", "VICTORY"]:
            self.state = "MENU"
            return

        # 3. GAMEPLAY
        # Coleta de Recursos
        for res in self.resources[:]:
            if math.hypot(pos[0] - res.x, pos[1] - res.y) <= res.radius:
                if res.res_type == "sun":
                    self.sun_score += 25
                else:
                    self.brain_score += 25
                self.resources.remove(res)
                return

        # Seleção de Cards (MODO PLANTA)
        if self.mode == "PLANTS":
            for i, card in enumerate(self.plant_cards):
                card_rect = pygame.Rect(180 + i * 85, 15, 75, 80)
                if card_rect.collidepoint(pos):
                    if self.sun_score >= card["cost"]:
                        self.selected_item = card["type"]
                    return

            # Plantar na Grade
            if self.selected_item:
                mx, my = pos
                if (
                    GRID_X <= mx < GRID_X + COLS * TILE_W
                    and GRID_Y <= my < GRID_Y + ROWS * TILE_H
                ):
                    col = (mx - GRID_X) // TILE_W
                    row = (my - GRID_Y) // TILE_H

                    occupied = any(
                        p.row == row and p.col == col for p in self.plants
                    )
                    cost = next(
                        c["cost"]
                        for c in self.plant_cards
                        if c["type"] == self.selected_item
                    )

                    if not occupied and self.sun_score >= cost:
                        self.plants.append(
                            Plant(row, col, self.selected_item)
                        )
                        self.sun_score -= cost
                        self.selected_item = None

        # Seleção de Cards (MODO ZUMBI)
        elif self.mode == "ZOMBIES":
            for i, card in enumerate(self.zombie_cards):
                card_rect = pygame.Rect(180 + i * 90, 15, 80, 80)
                if card_rect.collidepoint(pos):
                    if self.brain_score >= card["cost"]:
                        self.selected_item = card["type"]
                    return

            # Invocar Zumbi no Lado Direito
            if self.selected_item:
                mx, my = pos
                if (
                    GRID_X <= mx < SCREEN_WIDTH
                    and GRID_Y <= my < GRID_Y + ROWS * TILE_H
                ):
                    row = (my - GRID_Y) // TILE_H
                    cost = next(
                        c["cost"]
                        for c in self.zombie_cards
                        if c["type"] == self.selected_item
                    )

                    if 0 <= row < ROWS and self.brain_score >= cost:
                        self.zombies.append(Zombie(row, self.selected_item))
                        self.brain_score -= cost
                        self.selected_item = None

    def setup_zombie_mode_field(self):
        """Cria uma defesa inicial de plantas quando o jogador joga de Zumbi"""
        for r in range(ROWS):
            self.plants.append(Plant(r, 0, "sunflower"))
            self.plants.append(Plant(r, 1, "peashooter"))
            if random.random() > 0.4:
                self.plants.append(Plant(r, 2, "wallnut"))

    def update(self):
        if self.state in ["MENU", "GAME_OVER", "VICTORY"]:
            return

        now = pygame.time.get_ticks()

        # Geração Natural de Recursos
        if now - self.last_resource_spawn > 8000:
            self.last_resource_spawn = now
            rx = random.randint(GRID_X + 20, GRID_X + COLS * TILE_W - 20)
            ry = random.randint(GRID_Y + 50, GRID_Y + ROWS * TILE_H - 30)

            if self.mode == "PLANTS":
                self.resources.append(Resource(rx, 0, "sun", ry))
            else:
                self.resources.append(Resource(rx, 0, "brain", ry))

        # IA DO JOGO (Depende do Modo)
        if now - self.last_ai_spawn > self.ai_spawn_rate:
            self.last_ai_spawn = now

            if self.mode == "PLANTS":
                # IA envia Zumbis
                z_type = random.choice(["normal", "cone", "runner", "bucket"])
                self.zombies.append(
                    Zombie(random.randint(0, ROWS - 1), z_type)
                )
                if self.ai_spawn_rate > 2500:
                    self.ai_spawn_rate -= 150

            elif self.mode == "ZOMBIES":
                # IA posiciona novas Plantas defensivas na grade
                empty_spots = [
                    (r, c)
                    for r in range(ROWS)
                    for c in range(COLS - 2)
                    if not any(
                        p.row == r and p.col == c for p in self.plants
                    )
                ]
                if empty_spots:
                    r, c = random.choice(empty_spots)
                    p_type = random.choice(
                        [
                            "peashooter",
                            "snowpea",
                            "wallnut",
                            "repeater",
                            "sunflower",
                        ]
                    )
                    self.plants.append(Plant(r, c, p_type))

        # Atualizar Explosões
        for exp in self.explosions[:]:
            exp.update()
            if not exp.alive:
                self.explosions.remove(exp)

        # Atualizar Recursos
        for res in self.resources[:]:
            res.update()
            if not res.alive:
                self.resources.remove(res)

        # Atualizar Plantas
        for plant in self.plants:
            plant.update(self)

        # Atualizar Ervilhas
        for pea in self.peas[:]:
            pea.update()
            if not pea.alive:
                self.peas.remove(pea)

        # Atualizar Zumbis e Colisões
        for zombie in self.zombies[:]:
            zombie.update(self)

            # CONDIÇÕES DE VITÓRIA / DERROTA
            if zombie.x <= GRID_X:
                if self.mode == "PLANTS":
                    self.state = "GAME_OVER"
                else:
                    self.state = "VICTORY"

            # Colisão Ervilha x Zumbi
            for pea in self.peas[:]:
                if pea.row == zombie.row and pea.rect.colliderect(zombie.rect):
                    zombie.hp -= pea.damage
                    if pea.is_ice:
                        zombie.slow_timer = 180  # 3 segundos desacelerado

                    pea.alive = False
                    if pea in self.peas:
                        self.peas.remove(pea)

                    if zombie.hp <= 0:
                        if zombie in self.zombies:
                            self.zombies.remove(zombie)
                        break

    def draw(self, surface):
        surface.fill((30, 20, 10))

        # TELA DE MENU
        if self.state == "MENU":
            title = font_title.render("PLANTAS vs ZOMBIES", True, LAWN_GREEN1)
            surface.blit(
                title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 120)
            )

            btn_p = pygame.Rect(
                SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 40, 360, 50
            )
            btn_z = pygame.Rect(
                SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + 30, 360, 50
            )

            pygame.draw.rect(surface, GREEN, btn_p, border_radius=10)
            pygame.draw.rect(surface, PURPLE, btn_z, border_radius=10)

            txt_p = font_main.render("🌻 Jogar como PLANTAS", True, WHITE)
            txt_z = font_main.render("🧟 Jogar como ZUMBIS", True, WHITE)

            surface.blit(
                txt_p, (btn_p.centerx - txt_p.get_width() // 2, btn_p.centery - 12)
            )
            surface.blit(
                txt_z, (btn_z.centerx - txt_z.get_width() // 2, btn_z.centery - 12)
            )
            return

        # DESENHO DO GRAMADO
        for r in range(ROWS):
            for c in range(COLS):
                color = LAWN_GREEN1 if (r + c) % 2 == 0 else LAWN_GREEN2
                rect = (GRID_X + c * TILE_W, GRID_Y + r * TILE_H, TILE_W, TILE_H)
                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, (100, 180, 60), rect, 1)

        # PAINEL DE CARTÕES (HUD)
        pygame.draw.rect(surface, (190, 150, 90), (0, 0, SCREEN_WIDTH, 105))
        pygame.draw.line(surface, BLACK, (0, 105), (SCREEN_WIDTH, 105), 3)

        # Pontuação
        if self.mode == "PLANTS":
            pygame.draw.circle(surface, YELLOW, (45, 45), 22)
            score_txt = font_main.render(str(self.sun_score), True, BLACK)
            surface.blit(score_txt, (75, 32))

            cards = self.plant_cards
            currency = self.sun_score
        else:
            pygame.draw.circle(surface, PURPLE, (45, 45), 22)
            score_txt = font_main.render(str(self.brain_score), True, WHITE)
            surface.blit(score_txt, (75, 32))

            cards = self.zombie_cards
            currency = self.brain_score

        # Cards
        for i, card in enumerate(cards):
            cx = 180 + i * (85 if self.mode == "PLANTS" else 90)
            card_rect = pygame.Rect(
                cx, 12, 75 if self.mode == "PLANTS" else 80, 82
            )

            is_sel = self.selected_item == card["type"]
            can_buy = currency >= card["cost"]

            bg = WHITE if can_buy else (170, 170, 170)
            border = RED if is_sel else BLACK

            pygame.draw.rect(surface, bg, card_rect, border_radius=6)
            pygame.draw.rect(
                surface, border, card_rect, 3 if is_sel else 1, border_radius=6
            )

            # Rótulo e Custo
            lbl = font_small.render(card["name"], True, BLACK)
            cst = font_small.render(str(card["cost"]), True, BLACK)

            surface.blit(
                lbl, (card_rect.centerx - lbl.get_width() // 2, card_rect.y + 10)
            )
            surface.blit(
                cst, (card_rect.centerx - cst.get_width() // 2, card_rect.y + 52)
            )

        # DESENHAR ENTIDADES
        for plant in self.plants:
            plant.draw(surface)
        for zombie in self.zombies:
            zombie.draw(surface)
        for pea in self.peas:
            pea.draw(surface)
        for res in self.resources:
            res.draw(surface)
        for exp in self.explosions:
            exp.draw(surface)

        # MENSAGEM FINAL
        if self.state in ["GAME_OVER", "VICTORY"]:
            s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            s.set_alpha(210)
            s.fill(BLACK)
            surface.blit(s, (0, 0))

            if self.state == "GAME_OVER":
                msg = "OS ZUMBIS INVASORES VENCERAM!"
                color = RED
            else:
                msg = "VITÓRIA DA SUA HORDA DE ZUMBIS!"
                color = LAWN_GREEN1

            txt = font_title.render(msg, True, color)
            sub = font_main.render(
                "Clique em qualquer lugar para voltar ao Menu", True, WHITE
            )

            surface.blit(
                txt,
                (
                    SCREEN_WIDTH // 2 - txt.get_width() // 2,
                    SCREEN_HEIGHT // 2 - 40,
                ),
            )
            surface.blit(
                sub,
                (
                    SCREEN_WIDTH // 2 - sub.get_width() // 2,
                    SCREEN_HEIGHT // 2 + 20,
                ),
            )


# --- LOOP PRINCIPAL ---
def main():
    game = PvZGame()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    game.handle_click(event.pos)

        game.update()
        game.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()