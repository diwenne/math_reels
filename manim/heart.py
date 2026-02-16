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
        c1, c2 = RED, PINK

        # ══════════════════════════════════════
        # TOP ZONE — Title (fixed to camera frame)
        # ══════════════════════════════════════
        title = Text("Heart Surface", font_size=42)
        title.set_color_by_gradient(c1, c2)
        title.move_to(UP * 5)
        self.add_fixed_in_frame_mobjects(title)
        self.add(title)

        # ══════════════════════════════════════
        # BOTTOM ZONE — Equation (fixed to camera frame, BIGGER)
        # ══════════════════════════════════════
        eq = MathTex(
            r"(x^2 + \tfrac{9}{4}y^2 + z^2 - 1)^3"
            r"= x^2 z^3 + \tfrac{9}{80}y^2 z^3",
            font_size=34,
        )
        eq.set_color_by_gradient(c1, c2)
        eq.move_to(DOWN * 5)
        self.add_fixed_in_frame_mobjects(eq)

        # ══════════════════════════════════════
        # CENTER ZONE — 3D Heart Surface
        # ══════════════════════════════════════

        # Axes — present from the start, no draw animation
        axes = ThreeDAxes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            z_range=[-3, 2.5, 1],
            x_length=5,
            y_length=5,
            z_length=5.5,
            axis_config={"color": GREY_D, "stroke_width": 1},
        ).move_to(ORIGIN)
        self.add(axes)

        # Parametric heart surface
        SCALE = 0.12

        def heart_func(u, v):
            sv = math.sin(v)
            cv = math.cos(v)

            x_val = sv * (15 * math.sin(u) - 4 * math.sin(3 * u))
            y_val = 8 * cv
            z_val = sv * (
                15 * math.cos(u)
                - 5 * math.cos(2 * u)
                - 2 * math.cos(3 * u)
                - math.cos(4 * u)
            )

            return axes.c2p(x_val * SCALE, y_val * SCALE, z_val * SCALE)

        heart = Surface(
            heart_func,
            u_range=[0, 2 * PI],
            v_range=[0, PI],
            resolution=(64, 64),
            fill_opacity=0.92,
            stroke_width=0.2,
            stroke_color=WHITE,
            checkerboard_colors=[RED_E, MAROON],
        )

        # ── Camera setup ──
        self.set_camera_orientation(
            phi=75 * DEGREES, theta=-90 * DEGREES, zoom=0.85
        )

        # ══════════════════════════════════════
        # Animation — spinning from the very start
        # ══════════════════════════════════════

        # Begin rotation BEFORE drawing the heart
        self.begin_ambient_camera_rotation(rate=0.2)

        # Draw heart + write equation while already spinning
        self.play(
            Create(heart),
            Write(eq),
            run_time=5,
            rate_func=smooth,
        )
        self.wait(0.5)

        # Continue spinning, gentle zoom-in
        self.play(
            self.camera.zoom_tracker.animate.set_value(1.05),
            run_time=5,
            rate_func=smooth,
        )

        self.wait(3)

        # Slight pull-back
        self.play(
            self.camera.zoom_tracker.animate.set_value(0.9),
            run_time=3,
            rate_func=smooth,
        )

        self.wait(2)
        self.stop_ambient_camera_rotation()
        self.wait(0.5)