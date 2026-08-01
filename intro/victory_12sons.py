"""야곱의 12 아들 축하 영상 (~5초)
- 게임 완료 시 자동 재생: 폭죽 + 12 카드 그리드 + "🎉 모두 알았다!"
- 흰 바탕 + 명조 BOLD + 폭발 점 효과.
"""
import random
from pathlib import Path
from manim import *
import numpy as np

SERIF = "Noto Serif KR"
IMG_DIR = Path(__file__).resolve().parent.parent / "assets" / "images"

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

PARTY_COLORS = ["#E63946", "#F77F00", "#FCBF49", "#06A77D", "#118AB2", "#9D4EDD", "#FF6B9D"]


def burst(scene, center, n=35, dist_range=(2.5, 4.5), duration=1.2):
    """폭죽 효과 — center에서 점들이 사방으로 펼쳐지며 사라짐."""
    particles = VGroup()
    targets = []
    for _ in range(n):
        color = random.choice(PARTY_COLORS)
        dot = Dot(center, color=color, radius=random.uniform(0.06, 0.12))
        particles.add(dot)
        angle = random.random() * 2 * PI
        dist = random.uniform(*dist_range)
        targets.append(center + RIGHT * (dist * np.cos(angle)) + UP * (dist * np.sin(angle)))
    scene.add(particles)
    scene.play(
        *[
            particles[i].animate.move_to(targets[i]).set_opacity(0)
            for i in range(n)
        ],
        run_time=duration,
        rate_func=rush_from,
    )
    scene.remove(particles)


class Jacob12SonsVictory(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        random.seed(42)

        # === 1. 초기 폭죽 + 메인 메시지 ===
        burst(self, ORIGIN, n=40, duration=1.0)

        title = Text(
            "🎉  모두 맞췄어요!",
            font=SERIF,
            weight=BOLD,
            font_size=64,
            color="#1F5C2C",
        )
        title.move_to(UP * 2.6)
        self.play(Write(title), run_time=0.9)

        # === 2. 12 카드 그리드 ===
        grid_cards = []
        for i, (name, key, color) in enumerate(SONS):
            img = ImageMobject(str(IMG_DIR / f"{key}.png")).set(height=1.0)
            label = Text(name, font=SERIF, weight=BOLD, font_size=22, color=color)
            mini = Group(img, label).arrange(DOWN, buff=0.06)
            r, c = divmod(i, 4)
            x = (c - 1.5) * 2.6
            y = 0.5 - r * 1.6
            mini.move_to(RIGHT * x + UP * y)
            grid_cards.append(mini)

        self.play(*[FadeIn(card, shift=UP * 0.3) for card in grid_cards], run_time=1.0)
        self.wait(0.4)

        # === 3. 두 번째 폭죽 양옆 + 결론 ===
        burst(self, LEFT * 5 + UP * 1, n=20, dist_range=(1.5, 2.8), duration=0.8)
        burst(self, RIGHT * 5 + UP * 1, n=20, dist_range=(1.5, 2.8), duration=0.8)

        bottom = Text(
            "이스라엘 12 지파를 다 익혔어요",
            font=SERIF,
            weight=BOLD,
            font_size=34,
            color="#444444",
        )
        bottom.to_edge(DOWN, buff=0.4)
        self.play(Write(bottom), run_time=0.9)
        self.wait(1.5)
