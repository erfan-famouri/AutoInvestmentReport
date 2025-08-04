import os
import subprocess
import shutil
import sys
from typing import List

NOTEBOOKS: List[str] = [
    "Display profit and loss_toman.ipynb",
    "Display profit and loss_dollar.ipynb",
    "cash.ipynb",
    "generate_pdf_report.py"  # just listed for tracking, not executed here
]

BASE_OUTPUT_DIR = "executed_notebooks"
FILE_EXTENSIONS_TO_MOVE = [".png", ".jpg"]  # Adjustable

def get_category_dir(notebook_name: str) -> str:
    name_lower = notebook_name.lower()
    if "toman" in name_lower:
        return "toman"
    elif "dollar" in name_lower:
        return "dollar"
    elif "cash" in name_lower:
        return "cash"
    else:
        return "others"

def execute_notebook(notebook_path: str) -> bool:
    filename = os.path.basename(notebook_path)
    notebook_dir = os.path.dirname(notebook_path) or "."

    print(f"🔄 Running notebook: {filename}")

    result = subprocess.run([
        "jupyter", "nbconvert",
        "--to", "notebook",
        "--execute",
        "--inplace",
        filename
    ], cwd=notebook_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print(f"❌ Failed: {filename}")
        print(result.stderr)
        return False

    print(f"✅ Executed: {filename}")
    return True

def move_generated_files(notebook_path: str, category: str):
    notebook_dir = os.path.dirname(notebook_path) or "."
    dest_dir = os.path.join(BASE_OUTPUT_DIR, category)
    os.makedirs(dest_dir, exist_ok=True)

    # Delete previous files in the destination
    for f in os.listdir(dest_dir):
        f_path = os.path.join(dest_dir, f)
        if os.path.isfile(f_path):
            os.remove(f_path)

    # Transfer new files
    for file_name in os.listdir(notebook_dir):
        file_path = os.path.join(notebook_dir, file_name)
        if not os.path.isfile(file_path):
            continue
        if any(file_name.endswith(ext) for ext in FILE_EXTENSIONS_TO_MOVE):
            dest_path = os.path.join(dest_dir, file_name)
            print(f"📦 Moving: {file_name} ➡️ {dest_dir}")
            shutil.move(file_path, dest_path)

def run_report_script():
    print("📝 Running generate_pdf_report.py...")

    result = subprocess.run(
        [sys.executable, "generate_pdf_report.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        print("❌ Failed to run generate_pdf_report.py")
        print(result.stderr)
    else:
        print("✅ PDF report generated.")

def main():
    print("🚀 Starting notebook execution...")

    for notebook in NOTEBOOKS[:-1]:  # Exclude the PDF generator
        if not os.path.exists(notebook):
            print(f"⚠️ Not found: {notebook}")
            continue

        category = get_category_dir(notebook)

        success = execute_notebook(notebook)
        if success:
            move_generated_files(notebook, category)
        else:
            print("⛔ Execution failed. Stopping.")
            break

    run_report_script()
    print("✅ All done.")

if __name__ == "__main__":
    main()
