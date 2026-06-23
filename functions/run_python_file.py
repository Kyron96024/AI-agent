import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to be executed, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of arguments to pass to the Python file",
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir :
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not target_dir.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_dir]

        if args != None:
            command.extend(args)
        
        subproc = subprocess.run(command,cwd=working_directory, capture_output=True, text=True,timeout=30)

        outputstr = ""

        if subproc.returncode != 0 :
            outputstr+= f"Process exited with code {subproc.returncode}\n"
        if subproc.stdout == "" and subproc.stderr == "" :
            outputstr += "No output produced\n"
        else:
            if subproc.stdout:
                outputstr += f"STDOUT:{subproc.stdout}\n"
            if subproc.stderr:
                outputstr += f"STDERR:{subproc.stderr}\n"
        return outputstr
    except Exception as e:
        return f"Error: executing Python file: {e}"