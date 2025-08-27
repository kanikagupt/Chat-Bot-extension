import subprocess
import json
import shutil
from pathlib import Path
from datetime import datetime
from langchain_core.tools import tool
import platform

PARENT_DIR = Path.cwd()

    
@tool
def resolve_path(file_path: str) -> Path:
    """Takes a relative file path and returns its absolute Path within the working directory."""
    return PARENT_DIR / file_path

@tool     
def read_file(path: str):
    """Takes a file path and returns its content as a string or an error dict."""
    try:
        resolved_path = resolve_path(path)
        data = resolved_path.read_text(encoding="utf-8")
        return data
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@tool    
def create_file(path: str):
    """Takes a file path and returns success or error after trying to create the file."""
    try:
        resolved_path = resolve_path(path)
        resolved_path.touch(exist_ok=False)
        return {'status': 'success', 'data': f"File {path} created successfully"}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@tool
def create_and_write_file(path: str, content: str, encoding: str = 'utf-8'):
    """Creates and writes content to a file, returns result dict."""
    return write_file(path, content, encoding)

@tool
def write_file(path: str, content: str, encoding: str = 'utf-8'):
    """Overwrites file at path with content and returns success or error."""
    try:
        resolved_path = resolve_path(path)
        resolved_path.write_text(content, encoding=encoding)
        return {'status': 'success', 'data': f"File written to {path}"}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@tool    
def append_file(path: str, content: str, encoding: str = 'utf-8'):
    """Appends content to a file and returns a success or error dict."""
    try:
        resolved = resolve_path(path)
        with resolved.open('a', encoding=encoding) as f:
            f.write(content)
        return {'status': 'success', 'data': f"Content appended to {path}"}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@tool    
def delete_file(path: str):
    """Deletes the specified file and returns a result dict."""
    try:
        resolved = resolve_path(path)
        resolved.unlink()
        return {'status': 'success', 'data': f"File {path} deleted"}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@tool    
def read_directory(path: str, recursive: bool = False):
    """Lists files in a directory (optionally recursively) and returns result dict."""
    try:
        resolved = resolve_path(path)
        if recursive:
            files = [str(p.relative_to(resolved)) for p in resolved.rglob('*')]
        else:
            files = [p.name for p in resolved.iterdir()]
        return {'status': 'success', 'data': files}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@tool    
def create_directory(path: str, recursive: bool = True):
    """Creates a directory and returns a result dict with success or error."""
    try:
        resolved = resolve_path(path)
        resolved.mkdir(parents=recursive, exist_ok=True)
        return {'status': 'success', 'data': f"Directory {path} created"}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
    
@tool
def delete_directory(path: str, recursive: bool = False):
    """Deletes a directory (optionally recursively) and returns result dict."""
    try:
        resolved = resolve_path(path)
        if recursive:
            shutil.rmtree(resolved)
        else:
            resolved.rmdir()
        return {'status': 'success', 'data': f"Directory {path} deleted"}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
    
@tool
def check_file_exists(path: str):
    """Returns whether the specified file or directory exists."""
    resolved = resolve_path(path)
    return {'status': 'success', 'data': resolved.exists()}

@tool
def get_file_stats(path: str):
    """Returns file/directory metadata like size, timestamps, and permissions."""
    try:
        resolved = resolve_path(path)
        stats = resolved.stat()
        return {
            'status': 'success',
            'data': {
                'size': stats.st_size,
                'created': datetime.fromtimestamp(stats.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stats.st_mtime).isoformat(),
                'isFile': resolved.is_file(),
                'isDirectory': resolved.is_dir(),
                'permissions': oct(stats.st_mode)[-3:],
            },
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@tool    
def rename_file(old_path: str, new_path: str):
    """Renames or moves a file/directory and returns a result dict."""
    try:
        resolved_old = resolve_path(old_path)
        resolved_new = resolve_path(new_path)
        resolved_old.rename(resolved_new)
        return {'status': 'success', 'data': f"Renamed {old_path} to {new_path}"}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
    
@tool
def copy_file(source: str, destination: str, overwrite: bool = True):
    """Copies a file and returns success or error based on overwrite rules."""
    try:
        resolved_source = resolve_path(source)
        resolved_dest = resolve_path(destination)
        if not overwrite and resolved_dest.exists():
            raise FileExistsError(f"{destination} already exists")
        shutil.copy2(resolved_source, resolved_dest)
        return {'status': 'success', 'data': f"Copied {source} to {destination}"}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
    
@tool
def read_json_file(path: str):
    """Reads and parses a JSON file, returning its content or an error."""
    try:
        resolved = resolve_path(path)
        with resolved.open('r', encoding='utf-8') as f:
            data = json.load(f)
        return {'status': 'success', 'data': data}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
    
@tool
def write_json_file(path: str, data: dict, pretty: bool = False):
    """Writes a dictionary to a JSON file and returns success or error."""
    try:
        resolved = resolve_path(path)
        with resolved.open('w', encoding='utf-8') as f:
            json.dump(data, f, indent=2 if pretty else None)
        return {'status': 'success', 'data': f"JSON written to {path}"}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@tool
def ask_user(question: str):
    """Prompts the user with a question and returns their response."""
    try:
        answer = input(question + "\n>> ")
        return {'status': 'success', 'data': answer.strip()}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
    
@tool
def get_systemInfo():
    """Returns a string describing the current operating system."""
    system = platform.system()
    if system == "Darwin":
        return "macOS"
    elif system == "Windows":
        return "Windows"
    elif system == "Linux":
        return "Linux"
    else:
        return "Unknown"
    
@tool
def run_command(command:str):
    """take an command in input as a string and return the output"""
    result = subprocess.check_output(command, shell=True, text=True)
    return result.strip()