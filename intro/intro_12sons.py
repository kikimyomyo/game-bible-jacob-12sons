"""야곱의 12 아들 → 12 지파 인트로 (이미지 포함, 7-9초)
- 흰 바탕 + 두꺼운 명조 (Noto Serif KR Bold).
- 게임 자산 이미지(assets/images/*.png) 활용 — 퀴즈와 시각 매칭.
- 야곱 중앙 → 12 이미지+이름 방사형 → 3x4 그리드 → 결론.
"""
from pathlib import Path
from manim import *

SERIF = "Noto Serif KR"
IMG_DIR = Path(__file__).resolve().parent.parent / "assets" / "images"

# (한글명, 영어 파일명, 색상)
SONS = [
    ("르우벤", "reuben",    "#1A4D8F"),
    ("시므온", "simeon",    "#0F6B6B"),
    ("레위",   "levi",      "#8B6914"),
    ("유다",   "judah",     "#7A1A1A"),
    ("단",     "dan",       "#1F5C2C"),
    ("납달리", "naphtali",  "#5A2A7A"),
    ("갓",     "gad",       "#B25500"),
    ("아셀",   "asher",     "#A0306B"),
    ("잇사갈", "issachar",  "#4A2F1A"),
    ("스불론", "zebulun",   "#1F4A6E"),
    ("요셉",   "joseph",    "#A02828"),
    ("베냐민", "benjamin",  "#2A2A6E"),
]


class Jacob12SonsIntro(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        center = ORIGIN

        jacob = Text("야곱", font=SERIF, weight=BOLD, font_size=78, color=BLACK)
        jacob.move_to(center)
        self.play(Write(jacob), run_time=0.7)
        self.wait(0.3)

        radius = 3.0
        n = len(SONS)
        cards = []  # (Group, target_pos)
        for i, (name, key, color) in enumerate(SONS):
            img_path = IMG_DIR / f"{key}.png"
            img = ImageMobject(str(img_path)).set(height=1.1)
            label = Text(name, font=SERIF, weight=BOLD, font_size=24, color=color)
            card = Group(img, label).arrange(DOWN, buff=0.08)
            card.scale(0.15).move_to(center)
            angle = PI / 2 - i * (2 * PI / n)
            target = center + RIGHT * (radius * np.cos(angle)) + UP * (radius * np.sin(angle))
            cards.append((card, target))

        # 야곱을 상단으로 먼저 이동 (카드 펼침에 가려지지 않도록)
        self.play(jacob.animate.scale(0.55).to_edge(UP, buff=0.45), run_time=0.6)

        for card, _ in cards:
            self.add(card)
        self.play(
            *[card.animate.scale(1 / 0.15).move_to(target) for card, target in cards],
            run_time=1.8,
        )
        self.wait(0.4)

        grid_targets = []
        for r in range(3):
            for c in range(4):
                x = (c - 1.5) * 2.6
                y = 1.4 - r * 1.7
                grid_targets.append(RIGHT * x + UP * y)

        movements = [
            cards[i][0].animate.move_to(grid_targets[i])
            for i in range(n)
        ]
        self.play(*movements, run_time=1.7)
        self.wait(0.4)

        title = Text(
            "→ 이스라엘 12 지파",
            font=SERIF,
            weight=BOLD,
            font_size=46,
            color="#1F5C2C",
        )
        title.to_edge(DOWN, buff=0.4)
        self.play(Write(title), run_time=1.0)
        self.wait(1.5)
