import math
from manim import *

# FORCE VERTICAL LAYOUT
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 16.0
config.frame_width = 9.0


class GeneratedScene(ThreeDScene):
    def construct(self):
        # ── Theme ──
        c1, c2 = GOLD, ORANGE

        # ══════════════════════════════════════
        # TOP ZONE — Title + Subtitle (fixed to camera frame)
        # ══════════════════════════════════════
        title = Text("Möbius Strip", font_size=42)
        title.set_color_by_gradient(c1, c2)
        title.move_to(UP * 6)
        self.add_fixed_in_frame_mobjects(title)
        self.add(title)

        subtitle = Text("A surface with only one side", font_size=24, color=GREY_B)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(subtitle)
        self.add(subtitle)

        # ══════════════════════════════════════
        # BOTTOM ZONE — Equation (two lines, font_size=34)
        # ══════════════════════════════════════
        eq_line1 = MathTex(
            r"x = \left(1 + \tfrac{v}{2}\cos\tfrac{u}{2}\right)\cos u",
            font_size=34,
        )
        eq_line2 = MathTex(
            r"y = \left(1 + \tfrac{v}{2}\cos\tfrac{u}{2}\right)\sin u \quad z = \tfrac{v}{2}\sin\tfrac{u}{2}",
            font_size=34,
        )
        eq_group = VGroup(eq_line1, eq_line2).arrange(DOWN, buff=0.2)
        eq_group.set_color_by_gradient(c1, c2)
        eq_group.move_to(DOWN * 5.5)
        self.add_fixed_in_frame_mobjects(eq_group)

        # ══════════════════════════════════════
        # CENTER ZONE — 3D Möbius Strip (BIG)
        # ══════════════════════════════════════

        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-2, 2, 1],
            x_length=7,
            y_length=7,
            z_length=5,
            axis_config={"color": GREY_D, "stroke_width": 1},
        ).move_to(ORIGIN)
        self.add(axes)

        SCALE = 1.8

        def mobius_func(u, v):
            half_u = u / 2
            r = 1 + (v / 2) * math.cos(half_u)
            x_val = r * math.cos(u) * SCALE
            y_val = r * math.sin(u) * SCALE
            z_val = (v / 2) * math.sin(half_u) * SCALE
            return axes.c2p(x_val, y_val, z_val)

        strip = Surface(
            mobius_func,
            u_range=[0, 2 * PI],
            v_range=[-1, 1],
            resolution=(80, 16),
            fill_opacity=0.85,
            stroke_width=0.3,
            stroke_color=WHITE,
            checkerboard_colors=[ORANGE, GOLD_E],
        )

        # ── Camera setup ──
        self.set_camera_orientation(
            phi=65 * DEGREES, theta=-60 * DEGREES, zoom=1.0
        )

        # ══════════════════════════════════════
        # Animation — spinning from the start
        # ══════════════════════════════════════

        self.begin_ambient_camera_rotation(rate=0.2)

        self.play(
            Create(strip),
            Write(eq_group),
            run_time=5,
            rate_func=smooth,
        )
        self.wait(0.5)

        self.play(
            self.camera.zoom_tracker.animate.set_value(1.2),
            run_time=5,
            rate_func=smooth,
        )

        self.wait(3)

        self.play(
            self.camera.zoom_tracker.animate.set_value(1.0),
            run_time=3,
            rate_func=smooth,
        )

        self.wait(2)
        self.stop_ambient_camera_rotation()
        self.wait(0.5)