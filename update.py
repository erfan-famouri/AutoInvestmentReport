import subprocess

scripts = [
    'update_assets.py',
    "refactored_get_html.py",
    "extract_prices.py",
    "assets_summary.py",
    "portfo.py"
]

for script in scripts:
    print(f"\nRunning {script}...")
    if script == 'update_assets.py':
        # Execute without taking output (for user input)
        result = subprocess.run(["python3.11", script])
    else:
        # Routine execution with output and error capture
        result = subprocess.run(["python3.11", script], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Error:", result.stderr)
