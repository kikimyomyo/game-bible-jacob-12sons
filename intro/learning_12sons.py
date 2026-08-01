"""야곱의 12 아들 학습 영상 + TTS 음성 (~40초)
- 야곱 등장 → 12명 1명씩 큰 카드 (이미지+이름+의미) + 한국어 TTS 음성 → 그리드 → 결론
- 각 카드 충분히 길게 (TTS 길이 + 0.8초 여유) → 어린이가 이미지·이름·의미 모두 흡수
- TTS: macOS say "Jian (Premium)" 한국어 → audio_tts/*.mp3
- 흰 바탕 + 명조 BOLD
"""
from pathlib import Path
from manim import *

SERIF = "Noto Serif KR"
THIS_DIR = Path(__file__).resolve().parent
IMG_DIR = THIS_DIR.parent / "assets" / "images"
TTS_DIR = THIS_DIR / "audio_tts"

# (한글명, 파일명, 색상, 이름의 의미, TTS 음성 길이[초])
SONS = [
    ("르우벤", "reuben",    "#1A4D8F", "보아라, 아들",    2.31),
    ("시므온", "simeon",    "#0F6B6B", "들으심",         2.35),
    ("레위",   "levi",      "#8B6914", "연합",           1.85),
    ("유다",   "judah",     "#7A1A1A", "찬송",           2.26),
    ("단",     "dan",       "#1F5C2C", "심판",           2.24),
    ("납달리", "naphtali",  "#5A2A7A", "씨름",           2.35),
    ("갓",     "gad",       "#B25500", "복",             1.86),
    ("아셀",   "asher",     "#A0306B", "기쁨",           2.49),
    ("잇사갈", "issachar",  "#4A2F1A", "값",             2.00),
    ("스불론", "zebulun",   "#1F4A6E", "거주",           2.17),
    ("요셉",   "joseph",    "#A02828", "더하심",         2.17),
    ("베냐민", "benjamin",  "#2A2A6E", "오른손의 아들",   2.81),
]

TTS_INTRO_DUR = 2.34
TTS_FINAL_DUR = 2.70
PADDING = 0.8  # TTS 끝난 뒤 다음 카드 전에 잠시 멈춤


class Jacob12SonsLearning(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # === 1. 야곱 등장 + 도입 TTS ===
        jacob = Text("야곱", font=SERIF, weight=BOLD, font_size=96, color=BLACK)
        self.play(Write(jacob), run_time=0.9)
        self.wait(0.3)

        intro_line = Text(
            "12 아들을 낳았어요",
            font=SERIF,
            weight=BOLD,
            font_size=42,
            color="#444444",
        )
        intro_line.next_to(jacob, DOWN, buff=0.4)
        self.add_sound(str(TTS_DIR / "intro.mp3"))
        self.play(FadeIn(intro_line, shift=UP * 0.2), run_time=0.6)
        self.wait(TTS_INTRO_DUR + 0.3 - 0.6)
        self.play(FadeOut(jacob), FadeOut(intro_line), run_time=0.5)

        # === 2. 12명 한 명씩 큰 카드 + TTS ===
        prev_card = None
        prev_num = None
        for i, (name, key, color, meaning, tts_dur) in enumerate(SONS):
            num = Text(
                f"{i+1} / 12",
                font=SERIF,
                weight=BOLD,
                font_size=32,
                color="#888888",
            )
            img = ImageMobject(str(IMG_DIR / f"{key}.png")).set(height=3.6)
            name_text = Text(name, font=SERIF, weight=BOLD, font_size=64, color=color)
            meaning_text = Text(
                f"뜻: {meaning}",
                font=SERIF,
                weight=BOLD,
                font_size=34,
                color="#555555",
            )

            num.to_corner(UL, buff=0.5)
            text_group = VGroup(name_text, meaning_text).arrange(DOWN, buff=0.2)
            card = Group(img, text_group).arrange(DOWN, buff=0.3).move_to(ORIGIN)

            # TTS 음성 시작 (카드 등장과 동시)
            self.add_sound(str(TTS_DIR / f"son_{i+1:02d}.mp3"))

            if prev_card is None:
                self.play(FadeIn(card), FadeIn(num), run_time=0.5)
            else:
                self.play(
                    FadeOut(prev_card),
                    FadeOut(prev_num),
                    FadeIn(card),
                    FadeIn(num),
                    run_time=0.45,
                )
            # TTS 길이 + 여유 만큼 보여주기
            self.wait(tts_dur + PADDING - 0.45)
            prev_card = card
            prev_num = num

        self.play(FadeOut(prev_card), FadeOut(prev_num), run_time=0.5)

        # === 3. 그리드 마무리 + 결론 TTS ===
        grid_cards = []
        for i, (name, key, color, _, _) in enumerate(SONS):
            img = ImageMobject(str(IMG_DIR / f"{key}.png")).set(height=1.0)
            label = Text(name, font=SERIF, weight=BOLD, font_size=22, color=color)
            mini = Group(img, label).arrange(DOWN, buff=0.06)
            r, c = divmod(i, 4)
            x = (c - 1.5) * 2.6
            y = 1.6 - r * 1.7
            mini.move_to(RIGHT * x + UP * y)
            grid_cards.append(mini)

        self.add_sound(str(TTS_DIR / "final.mp3"))
        self.play(*[FadeIn(card) for card in grid_cards], run_time=1.0)

        title = Text(
            "→ 이스라엘 12 지파",
            font=SERIF,
            weight=BOLD,
            font_size=46,
            color="#1F5C2C",
        )
        title.to_edge(DOWN, buff=0.4)
        self.play(Write(title), run_time=1.0)
        self.wait(TTS_FINAL_DUR + 0.5 - 1.0)
