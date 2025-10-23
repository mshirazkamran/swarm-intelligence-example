"""
Manim Animation for Particle Swarm Optimization
Visualizes the swarm behavior as particles search for optimal warehouse locations
"""

from manim import *
import numpy as np
import sys
import os

# Add parent directory to path to import main module
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import settings and functions from main
try:
    from src.main import (
        CITY_SIZE, MIN_COORD, MAX_COORD, N_WAREHOUSES, N_PARTICLES,
        D_MIN_RESIDENTIAL, D_MIN_WAREHOUSE, run_pso, RESIDENTIAL_CENTERS, ARMY_ZONES
    )
except ImportError:
    # If that doesn't work, try direct import (when run from src folder)
    from main import (
        CITY_SIZE, MIN_COORD, MAX_COORD, N_WAREHOUSES, N_PARTICLES,
        D_MIN_RESIDENTIAL, D_MIN_WAREHOUSE, run_pso, RESIDENTIAL_CENTERS, ARMY_ZONES
    )


class PSOAnimation(Scene):
    """Main animation scene for PSO warehouse optimization"""
    
    def construct(self):
        # Configuration
        self.scale_factor = 6 / CITY_SIZE  # Scale city to fit in manim coordinate system
        self.particle_size = 0.08
        self.warehouse_size = 0.15
        self.frame_duration = 0.1  # Duration per iteration frame
        
        # Run PSO and get animation data
        self.show_title()
        animation_data = self.run_optimization()
        
        # Create the animation
        self.animate_swarm(animation_data)
        
        # Show final result
        self.show_final_result(animation_data)
    
    def show_title(self):
        """Display title screen"""
        title = Text("Particle Swarm Optimization", font_size=48)
        subtitle = Text("Warehouse Location Problem", font_size=32)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))
    
    def run_optimization(self):
        """Run PSO with animation recording"""
        status_text = Text("Running optimization...", font_size=36)
        self.play(Write(status_text))
        
        # Run PSO with animation recording
        print("\n" + "="*50)
        print("Running PSO for animation...")
        print("="*50 + "\n")
        
        result = run_pso(record_animation=True)
        if len(result) == 4:
            gbest_position, gbest_fitness, gbest_history, animation_data = result
        else:
            # Fallback if not recording
            gbest_position, gbest_fitness, gbest_history = result
            animation_data = None
        
        self.play(FadeOut(status_text))
        return animation_data
    
    def scale_coords(self, coords):
        """Convert city coordinates to manim coordinates"""
        # Center around origin and scale
        x = (coords[0] - CITY_SIZE/2) * self.scale_factor
        y = (coords[1] - CITY_SIZE/2) * self.scale_factor
        return np.array([x, y, 0])
    
    def animate_swarm(self, animation_data):
        """Create the main swarm animation"""
        if animation_data is None:
            return
        
        # Setup: Draw city boundaries
        city_border = Rectangle(
            width=CITY_SIZE * self.scale_factor,
            height=CITY_SIZE * self.scale_factor,
            stroke_color=WHITE,
            stroke_width=2
        )
        
        # Draw residential areas
        residential_dots = VGroup()
        residential_circles = VGroup()
        for res in animation_data['residential']:
            pos = self.scale_coords(res)
            dot = Dot(pos, color=GREEN, radius=0.06)
            circle = Circle(
                radius=D_MIN_RESIDENTIAL * self.scale_factor,
                color=GREEN,
                stroke_width=1,
                fill_opacity=0
            ).move_to(pos)
            circle.set_stroke(opacity=0.3)
            residential_dots.add(dot)
            residential_circles.add(circle)
        
        # Draw army zones
        army_rectangles = VGroup()
        for (x_min, y_min, x_max, y_max) in animation_data['army_zones']:
            width = (x_max - x_min) * self.scale_factor
            height = (y_max - y_min) * self.scale_factor
            center_x = (x_min + x_max) / 2
            center_y = (y_min + y_max) / 2
            center_pos = self.scale_coords([center_x, center_y])
            
            rect = Rectangle(
                width=width,
                height=height,
                color=RED,
                fill_opacity=0.3,
                stroke_width=2
            ).move_to(center_pos)
            army_rectangles.add(rect)
        
        # Draw legend
        legend = self.create_legend()
        
        # Display static elements
        self.play(Create(city_border))
        self.play(
            FadeIn(residential_dots),
            FadeIn(residential_circles, lag_ratio=0.1),
            FadeIn(army_rectangles, lag_ratio=0.1)
        )
        self.play(FadeIn(legend))
        
        # Initialize particles
        particle_groups = []
        for particle_pos in animation_data['positions_history'][0]:
            warehouses = particle_pos.reshape(N_WAREHOUSES, 2)
            warehouse_dots = VGroup()
            for wh in warehouses:
                dot = Dot(
                    self.scale_coords(wh),
                    color=BLUE,
                    radius=self.particle_size
                )
                dot.set_opacity(0.5)
                warehouse_dots.add(dot)
            particle_groups.append(warehouse_dots)
        
        all_particles = VGroup(*particle_groups)
        self.play(FadeIn(all_particles, lag_ratio=0.05))
        
        # Create fitness counter
        fitness_text = Text(
            f"Fitness: {animation_data['fitness_history'][0]:.2f}",
            font_size=24
        ).to_corner(UL)
        iteration_text = Text("Iteration: 0", font_size=24).next_to(fitness_text, DOWN, aligned_edge=LEFT)
        
        self.play(Write(fitness_text), Write(iteration_text))
        
        # Animate iterations (sample every few iterations for performance)
        sample_rate = max(1, len(animation_data['positions_history']) // 100)
        
        for iteration in range(1, len(animation_data['positions_history']), sample_rate):
            # Update particle positions
            new_positions = animation_data['positions_history'][iteration]
            animations = []
            
            for i, particle_pos in enumerate(new_positions):
                warehouses = particle_pos.reshape(N_WAREHOUSES, 2)
                for j, wh in enumerate(warehouses):
                    new_pos = self.scale_coords(wh)
                    animations.append(
                        particle_groups[i][j].animate.move_to(new_pos)
                    )
            
            # Update fitness and iteration display
            new_fitness_text = Text(
                f"Fitness: {animation_data['fitness_history'][iteration]:.2f}",
                font_size=24
            ).to_corner(UL)
            new_iteration_text = Text(
                f"Iteration: {iteration}",
                font_size=24
            ).next_to(new_fitness_text, DOWN, aligned_edge=LEFT)
            
            # Play all updates simultaneously
            self.play(
                *animations,
                Transform(fitness_text, new_fitness_text),
                Transform(iteration_text, new_iteration_text),
                run_time=self.frame_duration
            )
        
        self.wait(1)
        
        # Highlight global best solution
        gbest_pos = animation_data['gbest_history_positions'][-1]
        gbest_warehouses = gbest_pos.reshape(N_WAREHOUSES, 2)
        
        best_warehouse_dots = VGroup()
        best_warehouse_circles = VGroup()
        for wh in gbest_warehouses:
            pos = self.scale_coords(wh)
            dot = Star(
                n=5,
                outer_radius=self.warehouse_size,
                color=YELLOW,
                fill_opacity=1
            ).move_to(pos)
            circle = DashedVMobject(
                Circle(
                    radius=D_MIN_WAREHOUSE * self.scale_factor,
                    color=BLUE,
                    stroke_width=2,
                    fill_opacity=0
                ),
                num_dashes=20
            ).move_to(pos)
            circle.set_stroke(opacity=0.5)
            best_warehouse_dots.add(dot)
            best_warehouse_circles.add(circle)
        
        # Fade out particles, highlight best solution
        self.play(
            FadeOut(all_particles),
            FadeIn(best_warehouse_circles),
            FadeIn(best_warehouse_dots, lag_ratio=0.2, scale=1.5)
        )
        
        self.wait(2)
    
    def create_legend(self):
        """Create legend for the animation"""
        legend_items = VGroup()
        
        # Residential
        res_dot = Dot(color=GREEN, radius=0.04)
        res_text = Text("Residential", font_size=18).next_to(res_dot, RIGHT, buff=0.1)
        res_item = VGroup(res_dot, res_text)
        
        # Army Zone
        army_rect = Rectangle(width=0.15, height=0.15, color=RED, fill_opacity=0.3)
        army_text = Text("Army Zone", font_size=18).next_to(army_rect, RIGHT, buff=0.1)
        army_item = VGroup(army_rect, army_text)
        
        # Particles
        particle_dot = Dot(color=BLUE, radius=0.04)
        particle_text = Text("Particles", font_size=18).next_to(particle_dot, RIGHT, buff=0.1)
        particle_item = VGroup(particle_dot, particle_text)
        
        # Best Solution
        best_star = Star(n=5, outer_radius=0.08, color=YELLOW, fill_opacity=1)
        best_text = Text("Best Solution", font_size=18).next_to(best_star, RIGHT, buff=0.1)
        best_item = VGroup(best_star, best_text)
        
        legend_items.add(res_item, army_item, particle_item, best_item)
        legend_items.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        # Add background
        bg = Rectangle(
            width=legend_items.width + 0.3,
            height=legend_items.height + 0.3,
            color=WHITE,
            fill_opacity=0.1,
            stroke_width=1
        )
        
        legend = VGroup(bg, legend_items)
        legend.to_corner(UR, buff=0.3)
        
        return legend
    
    def show_final_result(self, animation_data):
        """Show final statistics"""
        if animation_data is None:
            return
        
        final_fitness = animation_data['fitness_history'][-1]
        
        result_text = VGroup(
            Text("Optimization Complete!", font_size=40, color=GREEN),
            Text(f"Final Fitness: {final_fitness:.4f}", font_size=32),
            Text(f"Total Iterations: {len(animation_data['positions_history'])}", font_size=28),
            Text(f"Particles Used: {N_PARTICLES}", font_size=28)
        ).arrange(DOWN, buff=0.3)
        
        self.play(FadeIn(result_text, shift=UP))
        self.wait(3)


# Additional scene: Fitness convergence graph
class FitnessConvergence(Scene):
    """Separate scene showing fitness improvement over iterations"""
    
    def construct(self):
        # Run PSO to get data
        result = run_pso(record_animation=True)
        if len(result) == 4:
            _, _, _, animation_data = result
        else:
            return
        
        # Create axes
        axes = Axes(
            x_range=[0, len(animation_data['fitness_history']), 20],
            y_range=[0, max(animation_data['fitness_history'][:10]) + 1, 0.5],
            x_length=10,
            y_length=6,
            axis_config={"include_tip": True},
            x_axis_config={"numbers_to_include": np.arange(0, len(animation_data['fitness_history']), 40)},
            y_axis_config={"numbers_to_include": np.arange(0, max(animation_data['fitness_history'][:10]) + 1, 1)}
        )
        
        # Labels
        x_label = axes.get_x_axis_label("Iteration")
        y_label = axes.get_y_axis_label("Fitness", edge=LEFT, direction=LEFT)
        
        # Title
        title = Text("Fitness Convergence", font_size=40).to_edge(UP)
        
        # Plot fitness history
        fitness_history = animation_data['fitness_history']
        graph = axes.plot_line_graph(
            x_values=list(range(len(fitness_history))),
            y_values=fitness_history,
            line_color=BLUE,
            add_vertex_dots=False
        )
        
        # Animate
        self.play(Write(title))
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(Create(graph), run_time=3)
        self.wait(2)


if __name__ == "__main__":
    print("\n" + "="*60)
    print("PSO Animation - Manim Scene File")
    print("="*60)
    print("\nThis file contains Manim scenes for animating PSO.")
    print("\nTo generate animations, use one of these methods:\n")
    print("Method 1 (Recommended) - Use helper script:")
    print("  python generate_animation.py")
    print("  python generate_animation.py --quality high")
    print("\nMethod 2 - Direct manim command:")
    print("  manim -pql src/animate_pso.py PSOAnimation")
    print("  manim -pqh src/animate_pso.py PSOAnimation")
    print("\nMethod 3 - Render both scenes:")
    print("  python generate_animation.py --scene both")
    print("\n" + "="*60 + "\n")
