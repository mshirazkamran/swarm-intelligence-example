# Warehouse Location Optimizer

A Python program that uses Particle Swarm Optimization (PSO) to find the best locations for warehouses in a city while avoiding restricted areas and staying safe distance from homes.

## What Does This Program Do?

This program helps to place warehouses in a city by:
- Avoiding army restricted zones
- Keeping minimum distance from residential areas (homes)
- Keeping warehouses separated from each other
- Placing warehouses near city center (not on edges)

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

1. Open terminal/command prompt
2. Go to the project folder
3. Run the command:

```bash
python src/main.py
```

4. Wait for the program to finish (takes about 1-2 minutes)
5. Check the output image file: `warehouse_solution.png`

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
│   └── main.py              # Main program file
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── warehouse_solution.png   # Output image (created after running)
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
