# Warehouse Location Optimizer

A Python program that uses Particle Swarm Optimization (PSO) to find the best locations for warehouses in a city while avoiding restricted areas and staying safe distance from homes.

## What Does This Program Do?

This program helps to place warehouses in a city by:
- Avoiding army restricted zones
- Keeping minimum distance from residential areas (homes)
- Keeping warehouses separated from each other
- Placing warehouses near city center (not on edges)

## Quick Start

### Clone and Run

1. **Clone this repository:**
```bash
git clone https://github.com/mshirazkamran/swarm-intelligence-example.git
```

2. **Navigate to the project directory:**
```bash
cd swarm-intelligence-example
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the program:**
```bash
python src/main.py
```

5. **Check the output:**
   - View the generated image: `warehouse_solution.png`
   - See warehouse coordinates in the terminal output

6. **(Optional) Generate animation:**
```bash
pip install manim
python generate_animation.py --quality low
```
   - Creates video showing swarm optimization in action
   - Video saved in `media/videos/animate_pso/` folder

### Get Started with Docker

**🚧 Docker support is currently in development and will be available soon!**

Stay tuned for containerized deployment options that will make setup even easier.

## Requirements

You need to install these Python libraries:

```bash
pip install numpy matplotlib
```

Or install from the requirements file:

```bash
pip install -r requirements.txt
```

## How to Run

If you already have the project set up, simply run:

```bash
python src/main.py
```

**Note:** The program takes about 1-2 minutes to complete. Output will be saved as `warehouse_solution.png`.

## 🎬 Animation Feature (NEW!)

Visualize the swarm optimization process in action using Manim!

### Quick Animation

Generate a video showing particles searching for optimal warehouse locations:

```bash
python generate_animation.py
```

This creates a video in the `media/videos/animate_pso/` folder.

### Animation Options

**Different quality levels:**
```bash
# Low quality (fast, good for preview)
python generate_animation.py --quality low

# Medium quality
python generate_animation.py --quality medium

# High quality (recommended for presentations)
python generate_animation.py --quality high

# Production quality (best, but slow)
python generate_animation.py --quality production
```

**Different scenes:**
```bash
# Main swarm animation (default)
python generate_animation.py --scene PSOAnimation

# Fitness convergence graph
python generate_animation.py --scene FitnessConvergence

# Generate both animations
python generate_animation.py --scene both --quality high
```

### Animation Requirements

The animation feature requires additional dependencies:

```bash
pip install manim
```

**Note:** Manim also requires FFmpeg and LaTeX. See [Manim installation guide](https://docs.manim.community/en/stable/installation.html) for system-specific setup.

**For detailed animation instructions, see [ANIMATION_GUIDE.md](ANIMATION_GUIDE.md)**

### What the Animation Shows

The animation visualizes:
- 🔵 **Blue dots**: Individual particles (candidate solutions) searching
- 🟢 **Green circles**: Residential areas with safety zones
- 🔴 **Red rectangles**: Army restricted zones
- ⭐ **Yellow stars**: Best warehouse positions found
- 📊 **Live fitness counter**: Shows solution quality improving over time

**Tip:** Start with low quality (`-ql`) for quick previews. Use high quality (`-qh`) for final videos.

## Basic Settings (Variables You Can Change)

Open `src/main.py` and look at **Section 1: BASIC SETTINGS**. Here are the main variables you can adjust:

### City Settings
```python
CITY_SIZE = 1000  # Size of city (1000 x 1000 km)
```

### Number of Warehouses
```python
N_WAREHOUSES = 3  # How many warehouses to place (default: 3)
```

### Safety Distances
```python
D_MIN_RESIDENTIAL = 50.0   # Minimum distance from homes (km)
D_MIN_WAREHOUSE = 100.0    # Minimum distance between warehouses (km)
```

### PSO Algorithm Settings
```python
N_PARTICLES = 40     # How many possible solutions to test at once
N_ITERATIONS = 200   # How many times to improve the solution
```
- **More particles** = explores more possibilities but runs slower
- **More iterations** = better solution but takes more time

### Importance Weights
```python
ALPHA_WEIGHT = 0.5   # Importance of staying away from homes (0-1)
BETA_WEIGHT = 0.3    # Importance of warehouse separation (0-1)
GAMMA_WEIGHT = 1.0   # Importance of staying near city center (0-1)
```
- Higher weight = more important goal
- Lower weight = less important goal

### Random Locations
```python
N_RESIDENTIAL = 15   # How many residential areas to create
N_ARMY_ZONES = 5     # How many army zones to create
```

## Understanding the Output

### Console Output
The program prints:
1. Progress updates every 20 iterations
2. Final fitness score (lower is better)
3. Coordinates of each warehouse

Example:
```
Iteration 20/200, Best Fitness: 1.2108
...
Final Best Fitness (Cost): 1.1995
Best Warehouse Locations:
  Warehouse 1: (x=669.79, y=597.26)
  Warehouse 2: (x=202.25, y=350.06)
  Warehouse 3: (x=420.57, y=618.10)
```

### Image Output
File: `warehouse_solution.png`

**Left chart** shows:
- **Green circles** = Residential areas
- **Red rectangles** = Army restricted zones
- **Blue stars** = Optimized warehouse positions
- **Dashed green circles** = Safety zones around homes
- **Dotted blue circles** = Minimum distance between warehouses

**Right chart** shows:
- How the fitness (cost) improved over iterations
- Line goes down = solution getting better

## Troubleshooting

### Problem: "No valid solution found"
**Cause:** Constraints are too strict (impossible to satisfy)

**Solution:**
- Reduce `D_MIN_RESIDENTIAL` (allow closer to homes)
- Reduce `D_MIN_WAREHOUSE` (allow warehouses closer together)
- Reduce `N_WAREHOUSES` (place fewer warehouses)
- Increase `N_ITERATIONS` (give more time to search)

### Problem: "Warehouses at city edges"
**Cause:** GAMMA_WEIGHT is too low

**Solution:**
- Increase `GAMMA_WEIGHT` to 1.5 or 2.0

### Problem: "Program is very slow"
**Cause:** Too many particles or iterations

**Solution:**
- Reduce `N_PARTICLES` to 20-30
- Reduce `N_ITERATIONS` to 100-150

### Problem: "Fitness not improving"
**Cause:** Algorithm stuck at local minimum

**Solution:**
- Increase `W_MAX` to 1.0 (more exploration)
- Increase `c1` and `c2` to 2.0
- Run the program multiple times (results are random)

## Example Modifications

### To place 5 warehouses instead of 3:
```python
N_WAREHOUSES = 5
```

### To make algorithm faster (but less accurate):
```python
N_PARTICLES = 20
N_ITERATIONS = 100
```

### To prioritize safety over center placement:
```python
ALPHA_WEIGHT = 2.0   # very important
GAMMA_WEIGHT = 0.3   # less important
```

### To create denser city with more obstacles:
```python
N_RESIDENTIAL = 30
N_ARMY_ZONES = 10
```


## Project Structure

```
warehouse-lab-mid/
├── src/
│   ├── main.py                  # Main PSO optimization program
│   └── animate_pso.py           # Manim animation scenes
├── generate_animation.py        # Helper script to generate animations
├── requirements.txt             # Core dependencies
├── requirements-animation.txt   # Animation-specific dependencies
├── README.md                    # This file
├── ANIMATION_GUIDE.md          # Detailed animation documentation
├── TECHNICAL_SUMMARY.md        # Technical deep-dive
├── warehouse_solution.png      # Output image (created after running)
└── media/                      # Animation videos (created by manim)
    └── videos/
        └── animate_pso/
            ├── 480p15/         # Low quality videos
            ├── 720p30/         # Medium quality videos
            ├── 1080p60/        # High quality videos
            └── 1440p60/        # Production quality videos
```

## Additional Notes

- Each time you run the program, you get different results (because locations are random)
- The algorithm uses randomness, so running it multiple times may give slightly different warehouse positions
- If you want same results every time, add this line at top of main.py:
  ```python
  np.random.seed(42)  # any number works
  ```

## Need Help?

If something is not working:
1. Check if you installed all requirements (`numpy`, `matplotlib`)
2. Make sure you are in correct folder when running
3. Try with default settings first
4. Check if Python version is 3.6 or higher

---

**Good luck optimizing your warehouse locations!** 
