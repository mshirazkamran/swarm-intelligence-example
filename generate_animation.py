"""
Helper script to generate PSO animation
This script runs the manim animation with optimal settings
"""

import os

def run_animation(quality='low', scene='PSOAnimation', use_cache=False):
    """
    Run the PSO animation with manim
    
    Parameters:
    -----------
    quality : str
        'low' (-ql), 'medium' (-qm), 'high' (-qh), or 'production' (-qk)
    scene : str
        Scene name: 'PSOAnimation' or 'FitnessConvergence'
    use_cache : bool
        If True, use cached frames instead of recalculating (faster re-renders)
    """
    
    quality_flags = {
        'low': '-ql',
        'medium': '-qm',
        'high': '-qh',
        'production': '-qk'
    }
    
    quality_flag = quality_flags.get(quality, '-ql')
    
    # By default, manim uses caching. Only disable it if NOT using cache
    cache_flag = '--disable_caching' if not use_cache else ''
    
    # Command to run manim
    cmd = f'manim -p {quality_flag} {cache_flag} src/animate_pso.py {scene}'.replace('  ', ' ')
    
    print(f"\n{'='*60}")
    print(f"Generating {scene} animation at {quality} quality...")
    print(f"Command: {cmd}")
    print(f"{'='*60}\n")
    
    os.system(cmd)
    
    print(f"\n{'='*60}")
    print("Animation complete!")
    print("Check the 'media/videos/animate_pso/' folder for output")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate PSO animation using Manim')
    parser.add_argument(
        '--quality', '-q',
        choices=['low', 'medium', 'high', 'production'],
        default='low',
        help='Video quality (default: low for quick preview)'
    )
    parser.add_argument(
        '--scene', '-s',
        choices=['PSOAnimation', 'FitnessConvergence', 'both'],
        default='PSOAnimation',
        help='Which scene to render (default: PSOAnimation)'
    )
    parser.add_argument(
        '--cache', '-c',
        action='store_true',
        help='Use cached frames instead of recalculating (much faster re-renders)'
    )
    
    args = parser.parse_args()
    
    if args.scene == 'both':
        run_animation(args.quality, 'PSOAnimation', args.cache)
        run_animation(args.quality, 'FitnessConvergence', args.cache)
    else:
        run_animation(args.quality, args.scene, args.cache)
