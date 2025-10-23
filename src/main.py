import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ============================================
# SECTION 1: BASIC SETTINGS
# ============================================

# City map size (like a grid)
MIN_COORD = 0
MAX_COORD = 1000
CITY_SIZE = 1000

# How many warehouses we need to place
N_WAREHOUSES = 4
N_DIMENSIONS = N_WAREHOUSES * 2  # we need x,y for each warehouse (3 warehouses = 6 numbers)

# Safety rules (minimum distances in kilometers)
D_MIN_RESIDENTIAL = 50.0   # warehouses must be this far from homes
D_MIN_WAREHOUSE = 100.0    # warehouses must be this far from each other

# Punishment values (big numbers to force following rules)
PENALTY_ARMY_ZONE = 1_000_000_000       # very big punishment if warehouse goes in army area
PENALTY_RESIDENTIAL_MIN = 1_000_000 # big punishment if too close to homes
PENALTY_WAREHOUSE_MIN = 1_000_000   # big punishment if warehouses too close together

# PSO algorithm settings (controls how particles search for best solution)
N_PARTICLES = 50     # how many particles (possible solutions) to use
N_ITERATIONS = 200   # how many times to repeat the search
c1 = 1.5  # learning from own best position
c2 = 1.5  # learning from group best position

# Movement speed control (starts fast, ends slow)
W_MAX = 0.9  # start with fast movement to explore
W_MIN = 0.5  # end with slow movement to fine-tune

# Importance weights (how much we care about different goals)
ALPHA_WEIGHT = 0.6   # staying away from homes (medium importance)
BETA_WEIGHT = 0.5    # staying away from other warehouses (low importance)
GAMMA_WEIGHT = 0.9   # staying near city center (high importance)

# ============================================
# SECTION 2: CREATE RANDOM LOCATIONS
# ============================================

# Create random residential (home) areas
N_RESIDENTIAL = 10
RESIDENTIAL_CENTERS = np.random.rand(N_RESIDENTIAL, 2) * CITY_SIZE

# Create random army restricted zones
N_ARMY_ZONES = 5
ARMY_ZONES = []
for _ in range(N_ARMY_ZONES):
    x_min = np.random.rand() * (CITY_SIZE - 20)  # keep away from edges
    y_min = np.random.rand() * (CITY_SIZE - 20)
    width = np.random.uniform(5, 20)   # random width
    height = np.random.uniform(5, 20)  # random height
    ARMY_ZONES.append((x_min, y_min, x_min + width, y_min + height))

# ============================================
# SECTION 3: HELPER FUNCTIONS
# ============================================

def euclidean_distance(p1, p2):
    """Calculate straight line distance between two points."""
    return np.sqrt(np.sum((p1 - p2)**2))

def is_in_army_zone(point, zones):
    """Check if a point is inside any army zone (returns True or False)."""
    x, y = point
    for (x_min, y_min, x_max, y_max) in zones:
        if x_min <= x <= x_max and y_min <= y <= y_max:
            return True
    return False

# ============================================
# SECTION 4: FITNESS FUNCTION
# ============================================
# This function checks how good a solution is
# Lower number = better solution

def calculate_fitness(particle):
    """
    Check quality of warehouse positions.
    Lower value means better position.
    Input: particle = [x1, y1, x2, y2, x3, y3] (coordinates of 3 warehouses)
    """
    # Convert flat array to 2D array of warehouse positions
    warehouses = particle.reshape(N_WAREHOUSES, 2)
    
    total_hard_penalty = 0.0  # punishment for breaking rules
    total_soft_cost = 0.0     # cost for not-ideal placement
    
    # Step 1: Check hard rules (must follow these)
    
    # Rule 1: warehouse cannot be in army zone
    for wh in warehouses:
        if is_in_army_zone(wh, ARMY_ZONES):
            total_hard_penalty += PENALTY_ARMY_ZONE
            
    # Rule 2: warehouse must be far enough from homes
    for wh in warehouses:
        for res in RESIDENTIAL_CENTERS:
            dist = euclidean_distance(wh, res)
            if dist < D_MIN_RESIDENTIAL:
                # punish based on how much we violated the rule
                total_hard_penalty += PENALTY_RESIDENTIAL_MIN * (D_MIN_RESIDENTIAL - dist)
                
    # Rule 3: warehouses must be far enough from each other
    for i in range(N_WAREHOUSES):
        for j in range(i + 1, N_WAREHOUSES):
            dist = euclidean_distance(warehouses[i], warehouses[j])
            if dist < D_MIN_WAREHOUSE:
                total_hard_penalty += PENALTY_WAREHOUSE_MIN * (D_MIN_WAREHOUSE - dist)

    # Step 2: If all rules are followed, calculate soft costs (nice-to-have goals)
    if total_hard_penalty == 0:
        soft_cost_residential = 0.0
        soft_cost_warehouse = 0.0
        soft_cost_centrality = 0.0
        
        # Goal 1: prefer warehouses farther from homes (but not too extreme)
        # Uses exponential decay so benefit reduces after safe distance
        for wh in warehouses:
            for res in RESIDENTIAL_CENTERS:
                dist = euclidean_distance(wh, res)
                safety_margin = dist - D_MIN_RESIDENTIAL
                soft_cost_residential += np.exp(-safety_margin / 100.0)
                
        # Goal 2: prefer warehouses spread apart (but not too extreme)
        for i in range(N_WAREHOUSES):
            for j in range(i + 1, N_WAREHOUSES):
                dist = euclidean_distance(warehouses[i], warehouses[j])
                separation_margin = dist - D_MIN_WAREHOUSE
                soft_cost_warehouse += np.exp(-separation_margin / 100.0)
        
        # Goal 3: prefer warehouses near city center (prevents edge placement)
        city_center = np.array([CITY_SIZE / 2, CITY_SIZE / 2])
        for wh in warehouses:
            dist_from_center = euclidean_distance(wh, city_center)
            # normalize to 0-1 range
            max_center_dist = euclidean_distance(np.array([0, 0]), city_center)
            normalized_dist = dist_from_center / max_center_dist
            # square it to give more penalty for farther distances
            soft_cost_centrality += normalized_dist ** 2
        
        # Combine all soft costs with their importance weights
        total_soft_cost = (ALPHA_WEIGHT * soft_cost_residential) + \
                          (BETA_WEIGHT * soft_cost_warehouse) + \
                          (GAMMA_WEIGHT * soft_cost_centrality)

    # Final fitness = rule penalties + soft costs
    return total_hard_penalty + total_soft_cost

# ============================================
# SECTION 5: PSO ALGORITHM (MAIN OPTIMIZER)
# ============================================

def run_pso(record_animation=False):
    """Run particle swarm optimization to find best warehouse positions."""
    print("Initializing PSO swarm...")
    
    # Create random starting positions for all particles
    positions = np.random.rand(N_PARTICLES, N_DIMENSIONS) * CITY_SIZE
    
    # Create random starting velocities (speed and direction)
    velocities = (np.random.rand(N_PARTICLES, N_DIMENSIONS) - 0.5) * 0.1
    
    # Track each particle's personal best position
    pbest_positions = positions.copy()
    pbest_fitness = np.array([calculate_fitness(p) for p in positions])
    
    # Track global best position (best among all particles)
    gbest_index = np.argmin(pbest_fitness)
    gbest_position = pbest_positions[gbest_index].copy()
    gbest_fitness = pbest_fitness[gbest_index]
    
    # Keep history to see improvement over time
    gbest_history = [gbest_fitness]
    
    # Animation data storage (if recording)
    animation_data = {
        'positions_history': [],
        'gbest_history_positions': [],
        'pbest_positions_history': [],
        'residential': RESIDENTIAL_CENTERS.copy(),
        'army_zones': ARMY_ZONES.copy(),
        'fitness_history': [gbest_fitness]
    } if record_animation else None
    
    if record_animation and animation_data is not None:
        animation_data['positions_history'].append(positions.copy())
        animation_data['gbest_history_positions'].append(gbest_position.copy())
        animation_data['pbest_positions_history'].append(pbest_positions.copy())

    print(f"Starting optimization for {N_ITERATIONS} iterations...")
    
    # Main loop: repeat search many times
    for it in range(N_ITERATIONS):
        # Calculate inertia weight (starts high, ends low)
        w = W_MAX - (it / N_ITERATIONS) * (W_MAX - W_MIN)
        
        # Update each particle
        for i in range(N_PARTICLES):
            
            # Step 1: Check how good current position is
            current_fitness = calculate_fitness(positions[i])
            
            # Step 2: Update personal best if current is better
            if current_fitness < pbest_fitness[i]:
                pbest_fitness[i] = current_fitness
                pbest_positions[i] = positions[i].copy()
                
                # Step 3: Update global best if this is best overall
                if current_fitness < gbest_fitness:
                    gbest_fitness = current_fitness
                    gbest_position = positions[i].copy()
                    
            # Step 4: Calculate new velocity
            r1 = np.random.rand(N_DIMENSIONS)  # random factor 1
            r2 = np.random.rand(N_DIMENSIONS)  # random factor 2
            
            # Pull toward personal best position
            cognitive_velocity = c1 * r1 * (pbest_positions[i] - positions[i])
            # Pull toward global best position
            social_velocity = c2 * r2 * (gbest_position - positions[i])
            
            # Combine: keep some old speed + personal pull + group pull
            velocities[i] = (w * velocities[i]) + cognitive_velocity + social_velocity
            
            # Step 5: Move particle to new position
            positions[i] = positions[i] + velocities[i]
            
            # Step 6: Keep particle inside city bounds
            positions[i] = np.clip(positions[i], MIN_COORD, MAX_COORD)
            
        # Save best fitness of this iteration
        gbest_history.append(gbest_fitness)
        
        # Save animation data if recording
        if record_animation and animation_data is not None:
            animation_data['positions_history'].append(positions.copy())
            animation_data['gbest_history_positions'].append(gbest_position.copy())
            animation_data['pbest_positions_history'].append(pbest_positions.copy())
            animation_data['fitness_history'].append(gbest_fitness)
        
        # Print progress every 20 iterations
        if (it + 1) % 20 == 0:
            if gbest_fitness < 1e6:
                print(f"Iteration {it+1}/{N_ITERATIONS}, Best Fitness: {gbest_fitness:.4f}")
            else:
                print(f"Iteration {it+1}/{N_ITERATIONS}, Best Fitness: (Still violating constraints)")

    print("\nOptimization Finished.")
    
    if record_animation:
        return gbest_position, gbest_fitness, gbest_history, animation_data
    return gbest_position, gbest_fitness, gbest_history

# ============================================
# SECTION 6: VISUALIZATION
# ============================================

def plot_solution(best_solution, residential, army, history, gbest_fitness):
    """Create and save visual chart showing warehouse positions and fitness progress."""
    warehouses = best_solution.reshape(N_WAREHOUSES, 2)
    
    # Create figure with 2 charts side by side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    
    # Chart 1: Draw city map
    # Draw residential centers (green dots)
    ax1.scatter(residential[:, 0], residential[:, 1], c='green', marker='o', s=100, label='Residential Centers')
    
    # Draw army zones (red rectangles)
    for (x_min, y_min, x_max, y_max) in army:
        width = x_max - x_min
        height = y_max - y_min
        ax1.add_patch(patches.Rectangle((x_min, y_min), width, height, facecolor='red', alpha=0.5, label='Army Zone (Restricted)'))
        
    # Draw warehouses (blue stars)
    ax1.scatter(warehouses[:, 0], warehouses[:, 1], c='blue', marker='*', s=200, label='Optimized Warehouses', edgecolor='black')
    
    # Draw safety circles around homes
    for res in residential:
        ax1.add_patch(patches.Circle(res, D_MIN_RESIDENTIAL, color='green', fill=False, linestyle='--', alpha=0.6, label='_nolegend_'))
        
    # Draw minimum distance circles around warehouses
    for wh in warehouses:
        ax1.add_patch(patches.Circle(wh, D_MIN_WAREHOUSE, color='blue', fill=False, linestyle=':', alpha=0.7, label='_nolegend_'))

    # Set chart limits and labels
    ax1.set_xlim(MIN_COORD, MAX_COORD)
    ax1.set_ylim(MIN_COORD, MAX_COORD)
    
    # Add title based on result
    if gbest_fitness < 1e6:
        ax1.set_title(f"Optimized Warehouse Locations (Fitness: {gbest_fitness:.4f})")
    else:
        ax1.set_title("Could not find a valid solution (Constraints Violated)")
        
    ax1.set_xlabel("X Coordinate (km)")
    ax1.set_ylabel("Y Coordinate (km)")
    ax1.grid(True, linestyle=':', alpha=0.5)
    
    # Create legend (remove duplicate labels)
    handles, labels = ax1.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax1.legend(by_label.values(), by_label.keys(), loc='upper right')

    # Chart 2: Draw fitness improvement over time
    ax2.plot(history)
    ax2.set_title("Fitness Improvement Over Iterations")
    ax2.set_xlabel("Iteration")
    ax2.set_ylabel("Global Best Fitness (Cost)")
    ax2.grid(True)
    
    plt.tight_layout()
    
    # Save image to file
    output_filename = "warehouse_solution.png"
    plt.savefig(output_filename)
    plt.close(fig)
    print(f"\nSolution plot saved as '{output_filename}'")

# ============================================
# SECTION 7: MAIN PROGRAM
# ============================================

if __name__ == "__main__":
    # Run the PSO algorithm (without animation recording)
    result = run_pso()
    gbest_position, gbest_fitness, gbest_history = result[0], result[1], result[2]
    
    # Show results
    print("\n--- OPTIMAL SOLUTION ---")
    if gbest_fitness < 1e6:
        print(f"Final Best Fitness (Cost): {gbest_fitness:.4f}")
    else:
        print(f"Final Solution is INVALID (Fitness: {gbest_fitness:.2e})")
        print("This means the algorithm could not satisfy all hard constraints.")
        print("Try increasing iterations/particles or check if constraints are impossible.")
        
    print("Best Warehouse Locations:")
    
    # Convert result to warehouse coordinates and print
    final_warehouses = gbest_position.reshape(N_WAREHOUSES, 2)
    for i, (x, y) in enumerate(final_warehouses):
        print(f"  Warehouse {i+1}: (x={x:.2f}, y={y:.2f})")
    
    # Create and save visualization
    plot_solution(gbest_position, RESIDENTIAL_CENTERS, ARMY_ZONES, gbest_history, gbest_fitness)