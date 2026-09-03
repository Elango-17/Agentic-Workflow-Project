import os
import ast
import tempfile
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional
from tools.base import BaseTool


class RepositoryAstAnalyzer(BaseTool):
    """
    Accesses a Python source-code repository and extracts its Abstract Syntax Tree (AST)
    structure, metrics, and potentially dangerous patterns using deterministic parsing.
    """

    DANGEROUS_CALLS = {"eval", "exec", "input", "__import__"}
    DANGEROUS_MODULES = {"pickle", "shelve", "subprocess", "os", "sys"}

    def execute(
        self,
        repository_path: str,
        branch_name: Optional[str] = None,
        include_paths: Optional[List[str]] = None,
        max_files: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Executes static AST analysis on a local or remote Python repository.
        """
        if not repository_path or not isinstance(repository_path, str):
            raise ValueError("repository_path must be a non-empty string.")

        target_dir = None
        is_temp = False

        try:
            if self._is_remote_url(repository_path):
                target_dir = tempfile.mkdtemp(prefix="repo_ast_")
                is_temp = True
                self._clone_repository(repository_path, target_dir, branch_name)
            else:
                target_dir = repository_path
                if not os.path.exists(target_dir):
                    raise ValueError(f"Local repository path does not exist: {target_dir}")

            python_files = self._discover_python_files(target_dir, include_paths, max_files)

            analyzed_files = []
            unparseable_files = []
            analysis_errors = []
            total_classes = 0
            total_functions = 0
            total_lines_of_code = 0
            dangerous_patterns_found = []

            for file_path in python_files:
                rel_path = os.path.relpath(file_path, target_dir)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        source_code = f.read()

                    loc = len(source_code.splitlines())
                    total_lines_of_code += loc

                    tree = ast.parse(source_code, filename=rel_path)
                    
                    file_classes = 0
                    file_functions = 0
                    file_imports = []
                    file_dangerous = []

                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef):
                            file_classes += 1
                            total_classes += 1
                        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            file_functions += 1
                            total_functions += 1
                        elif isinstance(node, ast.Import):
                            for alias in node.names:
                                file_imports.append(alias.name)
                                if alias.name.split('.')[0] in self.DANGEROUS_MODULES:
                                    file_dangerous.append({
                                        "type": "dangerous_import",
                                        "detail": f"Import of module '{alias.name}'",
                                        "line": node.lineno
                                    })
                        elif isinstance(node, ast.ImportFrom):
                            if node.module:
                                file_imports.append(node.module)
                                if node.module.split('.')[0] in self.DANGEROUS_MODULES:
                                    file_dangerous.append({
                                        "type": "dangerous_import",
                                        "detail": f"Import from module '{node.module}'",
                                        "line": node.lineno
                                    })
                        elif isinstance(node, ast.Call):
                            if isinstance(node.func, ast.Name):
                                if node.func.id in self.DANGEROUS_CALLS:
                                    file_dangerous.append({
                                        "type": "dangerous_call",
                                        "detail": f"Call to built-in function '{node.func.id}'",
                                        "line": node.lineno
                                    })
                            elif isinstance(node.func, ast.Attribute):
                                if node.func.attr in ("system", "popen", "eval", "exec") and isinstance(node.func.value, ast.Name):
                                    file_dangerous.append({
                                        "type": "dangerous_call",
                                        "detail": f"Call to '{node.func.value.id}.{node.func.attr}'",
                                        "line": node.lineno
                                    })

                    for dp in file_dangerous:
                        dangerous_patterns_found.append({
                            "file": rel_path,
                            **dp
                        })

                    file_ast_dict = self._ast_to_dict(tree)
                    analyzed_files.append({
                        "file_path": rel_path,
                        "lines_of_code": loc,
                        "classes_count": file_classes,
                        "functions_count": file_functions,
                        "imports": sorted(list(set(file_imports))),
                        "ast_structure": file_ast_dict
                    })

                except SyntaxError as se:
                    unparseable_files.append({
                        "file_path": rel_path,
                        "error": str(se),
                        "line": se.lineno
                    })
                except Exception as e:
                    analysis_errors.append({
                        "file_path": rel_path,
                        "error": str(e)
                    })

            result = {
                "repository_info": {
                    "repository_path": repository_path,
                    "branch_name": branch_name,
                    "is_remote": self._is_remote_url(repository_path)
                },
                "analysis_summary": {
                    "total_files_discovered": len(python_files),
                    "total_files_analyzed": len(analyzed_files),
                    "total_unparseable_files": len(unparseable_files),
                    "total_errors": len(analysis_errors)
                },
                "structural_metrics": {
                    "total_lines_of_code": total_lines_of_code,
                    "total_classes": total_classes,
                    "total_functions": total_functions
                },
                "analyzed_files": analyzed_files,
                "unparseable_files": unparseable_files,
                "potentially_dangerous_patterns": dangerous_patterns_found,
                "analysis_errors": analysis_errors
            }

            return result

        finally:
            if is_temp and target_dir and os.path.exists(target_dir):
                import shutil
                shutil.rmtree(target_dir, ignore_errors=True)

    def _is_remote_url(self, path: str) -> bool:
        return path.startswith("http://") or path.startswith("https://") or path.startswith("git://") or path.endswith(".git")

    def _clone_repository(self, repo_url: str, dest_dir: str, branch: Optional[str]) -> None:
        cmd = ["git", "clone", "--depth", "1"]
        if branch:
            cmd.extend(["--branch", branch])
        cmd.extend([repo_url, dest_dir])
        
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to clone repository: {e.stderr.decode('utf-8', errors='ignore')}")
        except subprocess.TimeoutExpired:
            raise RuntimeError("Repository clone timed out.")

    def _discover_python_files(self, base_dir: str, include_paths: Optional[List[str]], max_files: Optional[int]) -> List[str]:
        python_files = []
        
        if include_paths:
            paths_to_check = [os.path.join(base_dir, p) for p in include_paths]
        else:
            paths_to_check = [base_dir]

        for p in paths_to_check:
            if not os.path.exists(p):
                continue
            if os.path.isfile(p) and p.endswith(".py"):
                python_files.append(os.path.abspath(p))
            elif os.path.isdir(p):
                for root, _, files in os.walk(p):
                    if any(ignored in root for ignored in {".git", "__pycache__", ".venv", "venv", "env", "node_modules"}):
                        continue
                    for file in files:
                        if file.endswith(".py"):
                            python_files.append(os.path.abspath(os.path.join(root, file)))

        # Deduplicate and sort
        python_files = sorted(list(set(python_files)))

        if max_files is not None and max_files > 0:
            python_files = python_files[:max_files]

        return python_files

    def _ast_to_dict(self, node: ast.AST) -> Dict[str, Any]:
        node_dict = {"node_type": type(node).__name__}
        if hasattr(node, "lineno"):
            node_dict["lineno"] = node.lineno
        if hasattr(node, "col_offset"):
            node_dict["col_offset"] = node.col_offset

        for field, value in ast.iter_fields(node):
            if isinstance(value, ast.AST):
                node_dict[field] = self._ast_to_dict(value)
            elif isinstance(value, list):
                node_dict[field] = [
                    self._ast_to_dict(item) if isinstance(item, ast.AST) else item
                    for item in value
                ]
            else:
                node_dict[field] = value

        return node_dict
