from manim import *
from manim_slides import Slide
import random

redC = "#ff001d"
greenC = "#00fe2d"
yellowC = "#fefe00"

# CYBER_BLUE = "#00f3ff"
bl = "#0009FF"

# NEON_PURPLE = "#bc13fe"
HOLO_GRADIENT = [bl]
GLOW_OPACITY = 0.3

class BinaryTree(VGroup):
    def __init__(self, label, left=None, right=None, level=0, spacing=3.0, **kwargs):
        super().__init__(**kwargs)
        self.label = label
        
        # Holographic node design
        self.node = RoundedRectangle(
            corner_radius=0.15,
            width=1.0,
            height=0.7,
            fill_opacity=1,
            stroke_width=3,
            stroke_color=bl
        ).set_fill(
            color=random.choice(HOLO_GRADIENT),
            opacity=1
        ).add_updater(lambda m: m.set_sheen(
            random.uniform(-0.3, 0.3), 
            random.choice([UL, UR, DL, DR])
        ))
        
        # Glow effect
        self.glow = VGroup(*[
            Circle(radius=0.5, color=color, fill_opacity=GLOW_OPACITY)
            for color in HOLO_GRADIENT
        ]).arrange_in_grid(rows=1, buff=0).move_to(self.node)
        self.glow.add_updater(lambda m, dt: m.set_fill(
            color=interpolate_color(
                HOLO_GRADIENT[0],
                HOLO_GRADIENT[-1],
                (np.sin(self.renderer.time * 1) + 1) / 2
            ),
            opacity=GLOW_OPACITY + 0.4 * ((np.sin(self.renderer.time * 1.5) + 1) / 2)
        ))
        
        # Cyber text styling
        self.text = Text(str(label), font="Orbitron", 
                        font_size=26, weight=BOLD, color=WHITE)\
            .set_stroke(bl, width=2, background=True)\
            .move_to(self.node.get_center())
            
        self.add(self.glow, self.node, self.text)
        
        # Rest of initialization remains same
        self.left = left
        self.right = right
        self.level = level
        self.spacing = spacing
        self.vertical_buff = 1.0
        self.arrange_subtrees()

    def arrange_subtrees(self):
        current_pos = self.get_center()
        horizontal_offset = self.spacing * (0.6 ** self.level)
        vertical_buff = 1.5

        # Position right-skewed children
        if self.right:
            self.right.level = self.level + 1
            new_pos = current_pos + RIGHT * horizontal_offset * 1.2 + DOWN * vertical_buff
            self.right.move_to(new_pos)
            self.right.arrange_subtrees()

        # Position left children normally
        if self.left:
            self.left.level = self.level + 1
            new_pos = current_pos + LEFT * horizontal_offset + DOWN * vertical_buff
            self.left.move_to(new_pos)
            self.left.arrange_subtrees()

        # Create skewed connections
        self.submobjects = [self.node, self.text]
        if self.right:
            # Connect parent's bottom-right to child's left-side
            start = self.node.get_bottom() + RIGHT * 0.25
            end = self.right.node.get_left() + UP * 0.25
            line = Line(start, end, stroke_width=3, color=GREY_B)
            self.add(line, self.right)

        if self.left:
            # Standard left connection
            start = self.node.get_bottom() + LEFT * 0.25
            end = self.left.node.get_top() + RIGHT * 0.25
            line = Line(start, end, stroke_width=3, color=GREY_B)
            self.add(line, self.left)

# -------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------

class SplayTreePresentation(Slide, Scene):
    def construct(self):
        # === Persistent Background ===
        gradient = Rectangle(
            width=self.camera.frame_width,
            height=self.camera.frame_height,
            fill_color=["#00002b", "#13003d", "#210051"],
            fill_opacity=1,
            stroke_width=0
        )
        self.add(gradient)

# -------------------------------------------------------------------------------------------------------------------------------------------

        # === Title Slide ===
        title = Title("Analysis of Splay Trees").scale(0.80)
        subtitle = Text("By: Dhruv Patel, Ashton Holland, Adam Kulikowski, Aditya Behara").scale(0.5).next_to(title, DOWN)
        title_grp = VGroup(title, subtitle)
        self.play(Write(title_grp))
        self.next_slide()
        self.play(FadeOut(title_grp))

# -------------------------------------------------------------------------------------------------------------------------------------------

        # === Introduction Slide ===
        intro_header = Text("Introduction").scale(0.7).to_edge(UP, buff=0.3)
        intro = BulletedList(
            "BSTs support insertion, deletion, and lookup efficiently.",
            "Traditional BSTs like AVL/red-black enforce balance → complexity.",
            "Sleator and Tarjan introduced splay trees: self-adjusting via access.",
            "Splaying moves accessed node to root, improving locality.",
            "No need for metadata; simple implementation with good performance."
        ).scale(0.5)
        intro.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        intro.set_width(self.camera.frame_width * 0.9)
        intro_grp = VGroup(intro_header, intro)
        self.play(Write(intro_grp))
        self.next_slide()
        self.play(FadeOut(intro_grp))

# -------------------------------------------------------------------------------------------------------------------------------------------

        # === Problem Statement and Motivation Slide ===
        prob_header = Text("Problem Statement and Motivation").scale(0.7).to_edge(UP, buff=0.3)
        problem = BulletedList(
            "Goal: Efficient BSTs for sequences, not just individual ops.",
            "Balanced trees are complex, static optimal trees lack adaptability.",
            "Finger and biased trees use metadata or assumptions.",
            "Need: Simpler, adaptive structure without metadata."
        ).scale(0.5)
        problem.set_width(self.camera.frame_width * 0.9)
        prob_grp = VGroup(prob_header, problem)
        # Fade out previous slide already done; now show problem slide
        self.play(Write(prob_grp))
        self.next_slide()
        self.play(FadeOut(prob_grp))

 # -------------------------------------------------------------------------------------------------------------------------------------------

        # === Technical Background Slide ===
        tech_header = Text("Technical Background").scale(0.7).to_edge(UP, buff=0.3)
        tech = BulletedList(
            "Splaying: Rotations (Zig, Zag, Zig-Zig, Zag-Zag, Zig-Zag, Zag-Zig).",
            "No extra metadata (e.g., height).",
            "Amortized analysis via potential function.",
            "Key theorems: Balance, Static Optimality, Working Set, Static Finger."
        ).scale(0.5)
        tech.set_width(self.camera.frame_width * 0.9)
        tech_grp = VGroup(tech_header, tech)
        self.play(Write(tech_grp))
        self.next_slide()
        self.play(FadeOut(tech_grp))

# -------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------
        # === Tree Rotations Slide - Animations! ===
        rot_header = Text("Splaying Rotations: Zig, Zag, Zig-Zig, Zag-Zag, Zig-Zag, Zag-Zig").scale(0.5).to_edge(UP, buff=0.3)
        self.play(Write(rot_header))
        
        # --- Zig Rotation Slide ---
        zig_tree = BinaryTree(6)
        zig_tree.left = BinaryTree(4)
        zig_tree.right = BinaryTree(7)
        zig_tree.left.left = BinaryTree(3)
        zig_tree.left.right = BinaryTree(5)
        zig_tree.arrange_subtrees()
        zig_tree.move_to(ORIGIN)
        zig_label = Text("Pre-Zig(4) (Single Right Rotation)").scale(0.5).next_to(zig_tree, DOWN)
        zig_label.set_color(redC)
        zig_grp = VGroup(zig_tree, zig_label)
        self.play(Write(zig_grp))
        self.next_slide()
        self.play(FadeOut(zig_grp))
# -------------------------------------------------------------------------------------------------------------------------------------------

        # Show post-Zig state
        zig_rotated = BinaryTree(4)
        zig_rotated.right = BinaryTree(6)
        zig_rotated.right.right = BinaryTree(7)
        zig_rotated.left = BinaryTree(3)
        zig_rotated.right.left = BinaryTree(5)
        zig_rotated.arrange_subtrees()
        zig_rotated.move_to(ORIGIN)
        zig_r_label = Text("Post-Zig(4) (Single Right Rotation)").scale(0.5).next_to(zig_rotated, DOWN)
        zig_r_label.set_color(greenC)
        zig_r_Grp = VGroup(zig_rotated, zig_r_label)
        self.play(ReplacementTransform(zig_tree, zig_rotated))
        self.play(Write(zig_r_label))
        self.next_slide()
        self.play(FadeOut(zig_r_Grp, rot_header))
# -------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------

        # --- Zag Rotation Slide ---
        zag_header = Text("Zag (Single Left Rotation)").scale(0.8).to_edge(UP, buff=0.3)
        self.play(Write(zag_header))
        
        zag_tree = BinaryTree(4)
        zag_tree.left = BinaryTree(3)
        zag_tree.right = BinaryTree(6)
        zag_tree.right.left = BinaryTree(5)
        zag_tree.right.right = BinaryTree(7)
        zag_tree.arrange_subtrees()
        zag_tree.move_to(ORIGIN)
        zag_label = Text("Pre-Zag(6) (Single Left Rotation)").scale(0.5).next_to(zag_tree, DOWN)
        zag_label.set_color(redC)
        zag_grp = VGroup(zag_tree, zag_label)
        self.play(Write(zag_grp))
        self.next_slide()
        self.play(FadeOut(zag_grp))
# -------------------------------------------------------------------------------------------------------------------------------------------

        # Show post-Zag state
        zag_r = BinaryTree(6)
        zag_r.right = BinaryTree(7)
        zag_r.left = BinaryTree(4)
        zag_r.left.left = BinaryTree(3)
        zag_r.left.right = BinaryTree(5)
        zag_r.arrange_subtrees()
        zag_r.move_to(ORIGIN)
        zag_r_label = Text("Post-Zag(6) (Single Left Rotation)").scale(0.5).next_to(zag_tree, DOWN)
        zag_r_label.set_color(greenC)
        zag_r_Grp = VGroup(zag_r, zag_r_label)
        self.play(ReplacementTransform(zag_tree, zag_r))
        self.play(Write(zag_r_label))
        self.next_slide()
        self.play(FadeOut(zag_r_Grp), FadeOut(zag_header))
# -------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------

        # --- Zig-Zig Rotation Slide ---
        zig_zig_Header = Text("Zig-Zig (Double Right Rotation)").scale(0.8).to_edge(UP, buff=0.3)
        self.play(Write(zig_zig_Header))
        
        zig_zig_T = BinaryTree(6, level = 0)
        zig_zig_T.left = BinaryTree(4, level = 1)
        zig_zig_T.right = BinaryTree(7, level = 1)
        zig_zig_T.left.left = BinaryTree(3, level = 2)
        zig_zig_T.left.right = BinaryTree(5, level = 2)
        zig_zig_T.arrange_subtrees()
        zig_zig_T.move_to(ORIGIN)
        zig_zig_L = Text("Pre-Zig-Zig(3) (Double Right Rotation)").scale(0.5).next_to(zig_zig_T, DOWN)
        zig_zig_L.set_color(redC)
        zig_zig_grp = VGroup(zig_zig_T, zig_zig_L)
        self.play(Write(zig_zig_grp))
        self.next_slide()
        self.play(FadeOut(zig_zig_grp))
# -------------------------------------------------------------------------------------------------------------------------------------------

        # Post-Zig-Zig
        zig_zig_R = BinaryTree(3, level = 0)
        zig_zig_R.right = BinaryTree(4, level = 1)
        zig_zig_R.right.right = BinaryTree(6, level = 2)
        zig_zig_R.right.right.left = BinaryTree(5, level = 3)
        zig_zig_R.right.right.right = BinaryTree(7, level = 3)
        zig_zig_R.arrange_subtrees()
        zig_zig_R.move_to(ORIGIN)
        zig_zig_pstL = Text("Post-Zig-Zig(3) (Double Right Rotation)").scale(0.5).next_to(zig_zig_T, DOWN, buff = 1.2)
        zig_zig_pstL.set_color(greenC)
        zig_zig_RGrp = VGroup(zig_zig_R, zig_zig_pstL)
        self.play(ReplacementTransform(zig_zig_T, zig_zig_R))
        self.play(Write(zig_zig_pstL))
        self.next_slide()
        self.play(FadeOut(zig_zig_RGrp), FadeOut(zig_zig_Header))
# -------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------
        # --- Zag-Zag Rotation Slide ---
        zag_zag_Header = Text("Zag-Zag (Double Left Rotation)").scale(0.8).to_edge(UP, buff=0.3)
        self.play(Write(zag_zag_Header))
        
        zag_zag_T = BinaryTree(4, level = 0)
        zag_zag_T.left = BinaryTree(3, level = 1)
        zag_zag_T.right = BinaryTree(6, level = 1)
        zag_zag_T.right.left = BinaryTree(5, level = 2)
        zag_zag_T.right.right = BinaryTree(7, level = 2)
        zag_zag_T.arrange_subtrees()
        zag_zag_T.move_to(ORIGIN)
        zag_zag_L = Text("Pre-Zag-Zag(7) (Double Left Rotation)").scale(0.5).next_to(zag_zag_T, DOWN)
        zag_zag_L.set_color(redC)
        zag_zag_grp = VGroup(zag_zag_T, zag_zag_L)
        self.play(Write(zag_zag_grp))
        self.next_slide()
        self.play(FadeOut(zag_zag_grp))
# -------------------------------------------------------------------------------------------------------------------------------------------

        # Post-Zag-Zag
        zag_zag_R = BinaryTree(7, level = 0)
        zag_zag_R.left = BinaryTree(6, level = 1)
        zag_zag_R.left.left = BinaryTree(4, level = 2)
        zag_zag_R.left.left.left = BinaryTree(3, level = 3)
        zag_zag_R.left.left.right = BinaryTree(5, level = 3)
        zag_zag_R.arrange_subtrees()
        zag_zag_R.move_to(ORIGIN)
        zag_zag_pstL = Text("Post-Zag-Zag(7) (Double left Rotation)").scale(0.5).next_to(zag_zag_R, DOWN, buff = 1.0)
        zag_zag_pstL.set_color(greenC)
        zag_zag_RGrp = VGroup(zag_zag_R, zag_zag_pstL)
        self.play(ReplacementTransform(zag_zag_T, zag_zag_R))
        self.play(Write(zag_zag_pstL))
        self.next_slide()
        self.play(FadeOut(zag_zag_RGrp), FadeOut(zag_zag_Header))

# -------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------
        # --- Zig-Zag Rotation Slide ---
        zig_zag_H = Text("Zig-Zag Rotation").scale(0.8).to_edge(UP, buff=0.3)
        self.play(Write(zig_zag_H))

        # Original tree
        zig_zag_T = BinaryTree(4, level=0)
        zig_zag_T.left = BinaryTree(3, level=1)
        zig_zag_T.right = BinaryTree(6, level=1)
        zig_zag_T.right.left = BinaryTree(5, level=2)
        zig_zag_T.right.right = BinaryTree(7, level=2)
        zig_zag_T.arrange_subtrees()
        zig_zag_T.move_to(ORIGIN)

        zig_zag_L = Text("0. Original Splay Tree, Zig-Zag(5)").scale(0.5).next_to(zig_zag_T, DOWN)
        zig_zag_L.set_color(redC)

        zig_zag_grp = VGroup(zig_zag_T, zig_zag_L)
        self.play(Write(zig_zag_grp))
        self.next_slide()

        # --- Replace with first transformation ---
        zig_zag_Z = BinaryTree(4, level=0)
        zig_zag_Z.left = BinaryTree(3, level=1)
        zig_zag_Z.right = BinaryTree(5, level=1)
        zig_zag_Z.right.right = BinaryTree(6, level=2)
        zig_zag_Z.right.right.right = BinaryTree(7, level=3)
        zig_zag_Z.arrange_subtrees()
        zig_zag_Z.move_to(ORIGIN)

        zig_zag_ZLabel = Text("1. Zig Rotation(6)").scale(0.5).next_to(zig_zag_Z, DOWN)
        zig_zag_ZLabel.set_color(yellowC)

        zig_zag_ZGrp = VGroup(zig_zag_Z, zig_zag_ZLabel)
        # Transform the entire original group into the new group
        self.play(ReplacementTransform(zig_zag_grp, zig_zag_ZGrp))
        self.next_slide()
        self.play(FadeOut(zig_zag_ZGrp))

        # --- Replace with second transformation ---
        zig_zag_ZG = BinaryTree(5, level=0)
        zig_zag_ZG.left = BinaryTree(4, level=1)
        zig_zag_ZG.right = BinaryTree(6, level=1)
        zig_zag_ZG.left.left = BinaryTree(3, level=2)
        zig_zag_ZG.right.right = BinaryTree(7, level=2)
        zig_zag_ZG.arrange_subtrees()
        zig_zag_ZG.move_to(ORIGIN)

        zig_zag_ZGLabel = Text("2. Zag Rotation(4)").scale(0.5).next_to(zig_zag_ZG, DOWN)
        zig_zag_ZGLabel.set_color(greenC)

        zig_zag_ZG_Grp = VGroup(zig_zag_ZG, zig_zag_ZGLabel)
        # Transform the previous group into the new one
        self.play(ReplacementTransform(zig_zag_ZGrp, zig_zag_ZG_Grp))
        self.next_slide()
        self.play(FadeOut(zig_zag_ZG_Grp), FadeOut(zig_zag_H))
# -------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------
        # --- Zag-Zig Rotation Slide ---
        zag_zig_H = Text("Zag-Zig Rotation").scale(0.8).to_edge(UP, buff=0.3)
        self.play(Write(zag_zig_H))

        # Original tree
        zag_zig_T = BinaryTree(6, level=0)
        zag_zig_T.left = BinaryTree(4, level=1)
        zag_zig_T.right = BinaryTree(7, level=1)
        zag_zig_T.left.left = BinaryTree(3, level=2)
        zag_zig_T.left.right = BinaryTree(5, level=2)
        zag_zig_T.arrange_subtrees()
        zag_zig_T.move_to(ORIGIN)

        zag_zig_L = Text("0. Original Splay Tree, Zag-Zig(5)").scale(0.5).next_to(zag_zig_T, DOWN)
        zag_zig_L.set_color(redC)

        zag_zig_grp = VGroup(zag_zig_T, zag_zig_L)
        self.play(Write(zag_zig_grp))
        self.next_slide()

        # --- First Transformation: Replace original with Zag Rotation ---
        zag_zig_Z = BinaryTree(6, level=0)
        zag_zig_Z.left = BinaryTree(5, level=1)
        zag_zig_Z.right = BinaryTree(7, level=1)
        zag_zig_Z.left.left = BinaryTree(4, level=2)
        zag_zig_Z.left.left.left = BinaryTree(3, level=3)
        zag_zig_Z.arrange_subtrees()
        zag_zig_Z.move_to(ORIGIN)

        zag_zig_ZLabel = Text("1. Zag Rotation(3)").scale(0.5).next_to(zag_zig_Z, DOWN)
        zag_zig_ZLabel.set_color(yellowC)

        zag_zig_ZGrp = VGroup(zag_zig_Z, zag_zig_ZLabel)
        self.play(ReplacementTransform(zag_zig_grp, zag_zig_ZGrp))
        self.next_slide()
        self.play(FadeOut(zag_zig_ZGrp))

        # --- Second Transformation: Replace Zag with Zig Rotation ---
        zag_zig_ZG = BinaryTree(5, level=0)
        zag_zig_ZG.left = BinaryTree(4, level=1)
        zag_zig_ZG.right = BinaryTree(6, level=1)
        zag_zig_ZG.left.left = BinaryTree(3, level=2)
        zag_zig_ZG.right.right = BinaryTree(7, level=2)
        zag_zig_ZG.arrange_subtrees()
        zag_zig_ZG.move_to(ORIGIN)

        zag_zig_ZGLabel = Text("2. Zig Rotation(6)").scale(0.5).next_to(zag_zig_ZG, DOWN)
        zag_zig_ZGLabel.set_color(greenC)

        zag_zig_ZG_Grp = VGroup(zag_zig_ZG, zag_zig_ZGLabel)
        self.play(ReplacementTransform(zag_zig_ZGrp, zag_zig_ZG_Grp))
        self.next_slide()
        self.play(FadeOut(zag_zig_ZG_Grp), FadeOut(zag_zig_H))

# -------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------

        # === Solution Slide ===
        sol_header = Text("Solution").scale(0.8).to_edge(UP, buff=0.3)
        solution = BulletedList(
            "Search: Find node, splay to root.",
            "Insert: Split, insert node, splay new root.",
            "Delete: Splay node, join left/right subtrees.",
            "Join or Split defined using splaying.",
            "Elegance: Frequently accessed nodes move toward root."
        ).scale(0.5)
        solution.set_width(self.camera.frame_width * 0.9)
        sol_grp = VGroup(sol_header, solution)
        self.play(Write(sol_grp))
        self.next_slide()
        self.play(FadeOut(sol_grp))


# -------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------
        # --- Search Slide ---
        search_H = Text("Splay Trees Method: Search()").scale(0.8).to_edge(UP, buff=0.3)
        self.play(Write(search_H))

        # Original tree
        search_1 = BinaryTree(1, level=0)
        search_1.left = BinaryTree(2, level=1)
        search_1.right = BinaryTree(4, level=1)
        search_1.right.left = BinaryTree(3, level=2)
        search_1.right.right = BinaryTree(8, level=2)
        search_1.arrange_subtrees()
        search_1.move_to(ORIGIN)

        search_1Label = Text("0. Original Splay Tree").scale(0.5).next_to(search_1, DOWN)
        search_1Label.set_color(redC)

        search_1grp = VGroup(search_1, search_1Label)
        self.play(Write(search_1grp))
        self.next_slide()

        # --- Replace Original with "Zig" ---
        search_2 = BinaryTree(1, level=0)
        search_2.left = BinaryTree(2, level=1)
        search_2.right = BinaryTree(3, level=1)
        search_2.right.right = BinaryTree(4, level=2)
        search_2.right.right.right = BinaryTree(8, level=3)
        search_2.arrange_subtrees()
        search_2.move_to(ORIGIN)

        search_2Label = Text("1. Zig for Search(3)").scale(0.5).next_to(search_2, DOWN)
        search_2Label.set_color(yellowC)

        search_2grp = VGroup(search_2, search_2Label)
        self.play(ReplacementTransform(search_1grp, search_2grp))
        self.next_slide()

        # --- Replace "Zig" with "Zag" ---
        search_3 = BinaryTree(3, level=0)
        search_3.left = BinaryTree(1, level=1)
        search_3.right = BinaryTree(4, level=1)
        search_3.left.left = BinaryTree(2, level=2)
        search_3.right.right = BinaryTree(8, level=2)
        search_3.arrange_subtrees()
        search_3.move_to(ORIGIN)

        search_3Label = Text("2. Zag for Search(3)").scale(0.5).next_to(search_3, DOWN)
        search_3Label.set_color(greenC)

        search_3grp = VGroup(search_3, search_3Label)
        self.play(ReplacementTransform(search_2grp, search_3grp))
        self.next_slide()

        self.play(FadeOut(search_3grp), FadeOut(search_H))

# -------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------
        # --- Insert Implementation ---
        insert_H = Text("Splay Trees Method: Insert()").scale(0.8).to_edge(UP, buff=0.3)
        self.play(Write(insert_H))

        # Original tree
        insert_0 = BinaryTree(1, level=0)
        insert_0.left = BinaryTree(2, level=1)
        insert_0.right = BinaryTree(4, level=1)
        insert_0.right.left = BinaryTree(3, level=2)
        insert_0.right.right = BinaryTree(8, level=2)
        insert_0.arrange_subtrees()
        insert_0.move_to(ORIGIN)

        insert_0Label = Text("0. Original Splay Tree").scale(0.5).next_to(insert_0, DOWN)
        insert_0Label.set_color(WHITE)

        insert_0grp = VGroup(insert_0, insert_0Label)
        self.play(Write(insert_0grp))
        self.next_slide()

        # Replace Original with Insert(0)
        insert_1 = BinaryTree(1, level=0)
        insert_1.left = BinaryTree(2, level=1)
        insert_1.right = BinaryTree(4, level=1)
        insert_1.left.left = BinaryTree(0, level=2)
        insert_1.right.left = BinaryTree(3, level=2)
        insert_1.right.right = BinaryTree(8, level=2)
        insert_1.arrange_subtrees()
        insert_1.move_to(ORIGIN)

        insert_1Label = Text("1. Insert(0)").scale(0.5).next_to(insert_1, DOWN)
        insert_1Label.set_color(redC)

        insert_1grp = VGroup(insert_1, insert_1Label)
        self.play(ReplacementTransform(insert_0grp, insert_1grp))
        self.next_slide()

        # Replace with Zig 1 state
        insert_2 = BinaryTree(2, level=0)
        insert_2.left = BinaryTree(0, level=1)
        insert_2.right = BinaryTree(1, level=1)
        insert_2.right.left = BinaryTree(3, level=2)
        insert_2.right.right = BinaryTree(4, level=2)
        insert_2.right.right.right = BinaryTree(8, level=2)
        insert_2.arrange_subtrees()
        insert_2.move_to(ORIGIN)

        insert_2Label = Text("2. Zig, Insert(0)").scale(0.5).next_to(insert_2, DOWN)
        insert_2Label.set_color(yellowC)

        insert_2grp = VGroup(insert_2, insert_2Label)
        self.play(ReplacementTransform(insert_1grp, insert_2grp))
        self.next_slide()

        # Replace with Zig 2 state (final tree)
        insert_3 = BinaryTree(0, level=0)
        insert_3.right = BinaryTree(2, level=1)
        insert_3.right.right = BinaryTree(1, level=2)
        insert_3.right.right.left = BinaryTree(3, level=3)
        insert_3.right.right.right = BinaryTree(4, level=3)
        insert_3.right.right.right.right = BinaryTree(8, level=4)
        insert_3.arrange_subtrees()
        insert_3.move_to(ORIGIN)

        insert_3Label = Text("3. Zig, Insert(0)").scale(0.5).next_to(insert_3, DOWN)
        insert_3Label.set_color(greenC)

        insert_3grp = VGroup(insert_3, insert_3Label)
        self.play(ReplacementTransform(insert_2grp, insert_3grp))
        self.next_slide()

        self.play(FadeOut(insert_3grp), FadeOut(insert_H))
# -------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------
        # --- Delete Implementation ---
        delete_H = Text("Splay Trees Method: Delete()").scale(0.8).to_edge(UP, buff=0.3)
        self.play(Write(delete_H))

        # Original tree
        delete_1 = BinaryTree(1, level=0)
        delete_1.left = BinaryTree(2, level=1)
        delete_1.right = BinaryTree(4, level=1)
        delete_1.right.left = BinaryTree(3, level=2)
        delete_1.right.right = BinaryTree(8, level=2)
        delete_1.arrange_subtrees()
        delete_1.move_to(ORIGIN)

        delete_1Label = Text("0. Original Splay Tree").scale(0.5).next_to(delete_1, DOWN)
        delete_1Label.set_color(redC)

        delete_1grp = VGroup(delete_1, delete_1Label)
        self.play(Write(delete_1grp))
        self.next_slide()

        # --- Replace Original with Delete(3) state ---
        delete_2 = BinaryTree(1, level=0)
        delete_2.left = BinaryTree(2, level=1)
        delete_2.right = BinaryTree(4, level=1)
        delete_2.right.right = BinaryTree(8, level=2)
        delete_2.arrange_subtrees()
        delete_2.move_to(ORIGIN)

        delete_2Label = Text("1. Delete(3)").scale(0.5).next_to(delete_2, DOWN)
        delete_2Label.set_color(yellowC)

        delete_2grp = VGroup(delete_2, delete_2Label)
        self.play(ReplacementTransform(delete_1grp, delete_2grp))
        self.next_slide()

        # --- Replace Delete(3) state with final Zag state ---
        delete_3 = BinaryTree(4, level=0)
        delete_3.left = BinaryTree(1, level=1)
        delete_3.right = BinaryTree(8, level=1)
        delete_3.left.left = BinaryTree(2, level=2)
        delete_3.arrange_subtrees()
        delete_3.move_to(ORIGIN)

        delete_3Label = Text("2. Zag").scale(0.5).next_to(delete_3, DOWN)
        delete_3Label.set_color(greenC)

        delete_3grp = VGroup(delete_3, delete_3Label)
        self.play(ReplacementTransform(delete_2grp, delete_3grp))
        self.next_slide()

        self.play(FadeOut(delete_3grp), FadeOut(delete_H))

# -------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------

        # === Variants and Optimizations Slide ===
        var_header = Text("Variants and Optimizations").scale(0.8).to_edge(UP, buff=0.3)
        variants = BulletedList(
            "Top-Down Splaying: One-pass traversal and restructure.",
            "Semi-Splaying: Less restructuring, simpler logic.",
            "Conditional Splaying: Triggered by path length/frequency.",
            "Snapshot Optimization: Temporarily stop splaying."
        ).scale(0.5)
        variants.set_width(self.camera.frame_width * 0.9)
        var_grp = VGroup(var_header, variants)
        self.play(Write(var_grp))
        self.next_slide()
        self.play(FadeOut(var_grp))

        # === Extensions Slide ===
        ext_header = Text("Extensions to Other Data Structures").scale(0.8).to_edge(UP, buff=0.3)
        extensions = BulletedList(
            "Lexicographic Trees: For efficient string search.",
            "Link/Cut Trees: Dynamic trees for network problems.",
            "Splaying helps maintain efficient access."
        ).scale(0.5)
        extensions.set_width(self.camera.frame_width * 0.9)
        ext_grp = VGroup(ext_header, extensions)
        self.play(Write(ext_grp))
        self.next_slide()
        self.play(FadeOut(ext_grp))

        # === Amortized Analysis Slide ===
        am_header = Text("Amortized Complexity").scale(0.8).to_edge(UP, buff=0.3)
        analysis = BulletedList(
            "Potential function: log-based ranks of nodes.",
            "Amortized cost = Actual Cost + change in Potential.",
            "Splaying cost less than or equal to 3(log W - log w) + 1.",
            "Sequence average is O(log n) per operation."
        ).scale(0.5)
        analysis.set_width(self.camera.frame_width * 0.9)
        am_grp = VGroup(am_header, analysis)
        self.play(Write(am_grp))
        self.next_slide()
        self.play(FadeOut(am_grp))

        # === Conclusion Slide ===
        con_header = Text("Conclusion").scale(0.8).to_edge(UP, buff=0.3)
        conclusion = BulletedList(
            "Splay trees: Simplicity + adaptability.",
            "Avoid balance factors and metadata.",
            "Match optimal performance over sequences.",
            "Generalizable technique for other structures.",
            "Valuable lesson in amortized analysis."
        ).scale(0.5)
        conclusion.set_width(self.camera.frame_width * 0.9)
        con_grp = VGroup(con_header, conclusion)
        self.play(Write(con_grp))
        self.next_slide()
        self.play(FadeOut(con_grp))

        # === End Slide ===
        thanks = Text("We appreciate your support CS 3511 TA team. We couldn't have done it without you all!", font_size=32).scale(0.5)
        self.play(Write(thanks))
        self.next_slide()
