import os
import ast
from typing import List, Tuple, Set


def separate_functions(file_path: str, target_directory: str) -> None:
    print(f"Processing file: {file_path}")

    with open(file_path, "r") as file:
        code = file.read()

    functions, all_function_names = extract_functions(code)
    num_functions = len(functions)
    print(f"Found {num_functions} functions in the file.")

    # Ensure the target directory exists
    os.makedirs(target_directory, exist_ok=True)

    for i, func in enumerate(functions, start=1):
        func_name, func_code, func_imports, func_dependencies = func
        func_file_path = os.path.join(target_directory, f"{func_name}.py")

        if os.path.exists(func_file_path):
            print(f"Skipping function '{func_name}' as the file already exists.")
            continue

        print(f"Processing function '{func_name}' ({i}/{num_functions})...")
        create_function_file(func_file_path, func_name, func_code, func_imports, func_dependencies, all_function_names)

    print("Creating/updating __init__.py file with imports...")
    create_init_file(target_directory, functions)

    # Update __init__.py files in parent directories
    update_parent_init_files(file_path, target_directory)

    print("Done!")


def extract_functions(code: str) -> Tuple[List[Tuple[str, str, Set[str], Set[str]]], Set[str]]:
    tree = ast.parse(code)
    functions = []
    imports = extract_imports(code, tree)
    all_function_names = set(node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef))

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            func_code = ast.get_source_segment(code, node)
            func_imports = find_function_imports(node, imports)
            func_dependencies = find_function_dependencies(node, all_function_names)
            functions.append((func_name, func_code, func_imports, func_dependencies))

    return functions, all_function_names


def extract_imports(code: str, tree: ast.AST) -> Set[str]:
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            import_code = ast.get_source_segment(code, node)
            imports.add(import_code)
    return imports


def find_function_imports(func_node: ast.FunctionDef, imports: Set[str]) -> Set[str]:
    func_imports = set()
    for node in ast.walk(func_node):
        if isinstance(node, ast.Name):
            for imp in imports:
                if node.id in imp:
                    func_imports.add(imp)
    return func_imports


def find_function_dependencies(func_node: ast.FunctionDef, all_function_names: Set[str]) -> Set[str]:
    dependencies = set()
    for node in ast.walk(func_node):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in all_function_names:
                dependencies.add(node.func.id)
    return dependencies


def create_function_file(
        file_path: str, func_name: str, func_code: str, func_imports: Set[str],
        func_dependencies: Set[str], all_function_names: Set[str]
) -> None:
    with open(file_path, "w") as file:
        file.write("\n".join(func_imports) + "\n\n")
        for dep in func_dependencies:
            if dep in all_function_names and dep != func_name:
                file.write(f"from . import {dep}\n")
        file.write("\n" + func_code)


def create_init_file(
        directory: str, functions: List[Tuple[str, str, Set[str], Set[str]]]
) -> None:
    init_file_path = os.path.join(directory, "__init__.py")
    imports = [f"from .{func_name} import {func_name}" for func_name, _, _, _ in functions]

    if os.path.exists(init_file_path):
        with open(init_file_path, "r") as file:
            existing_imports = file.readlines()

        # Remove existing imports
        imports = [imp for imp in imports if imp not in existing_imports]

        # Combine existing and new imports
        imports = existing_imports + imports

    with open(init_file_path, "w") as file:
        file.write("\n".join(imports))


def update_parent_init_files(file_path: str, target_directory: str) -> None:
    relative_path = os.path.relpath(target_directory, os.path.dirname(file_path))
    relative_parts = relative_path.split(os.sep)

    current_directory = os.path.dirname(file_path)
    for part in relative_parts:
        init_file_path = os.path.join(current_directory, "__init__.py")
        if not os.path.exists(init_file_path):
            with open(init_file_path, "w") as file:
                file.write("")

        current_directory = os.path.join(current_directory, part)

    parent_init_file_path = os.path.join(os.path.dirname(current_directory), "__init__.py")
    module_name = os.path.basename(current_directory)
    with open(parent_init_file_path, "a") as file:
        file.write(f"from .{module_name} import *\n")


if __name__ == "__main__":
    file_path = input("Enter the path to the file containing functions: ")
    target_directory = input("Enter the target directory for the extracted functions: ")
    separate_functions(file_path, target_directory)
