import os
import ast

def extract_functions_and_classes(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        tree = ast.parse(file.read(), filename=filepath)
    functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    return {"functions": functions, "classes": classes}

def analyze_project_structure(root_dir):
    results = {}
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                results[filepath] = extract_functions_and_classes(filepath)
    return results

if __name__ == "__main__":
    root_directory = "./src"  # 修改为你的代码目录
    structure = analyze_project_structure(root_directory)
    for filepath, content in structure.items():
        print(f"{filepath}:")
        print(f"  Classes: {content['classes']}")
        print(f"  Functions: {content['functions']}")