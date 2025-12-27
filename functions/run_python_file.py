import os, subprocess
from google.genai import types



schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Writes content to the specified file",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="File path to execute specified python file, relative to the working directory",
                ),
                "args": types.Schema(
                    type=types.Type.ARRAY,
                    description="Optional arguments to pass to the Python file",
                    items=types.Schema(
                        type=types.Type.STRING,
                        description="Single command-line argument",
                     ),
                ),
            },
            required= ["file_path"],
            
            
        ),
    )



def run_python_file(working_directory, file_path, args=None):
        try:
            working_dir_abs = os.path.abspath(working_directory)
            target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
            
            valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
            
            if not valid_target_file:
                return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory' 
            
            if not os.path.isfile(target_file):
                return f'Error: "{file_path}" does not exist or is not a regular file' 

            if not target_file.endswith('.py'):
                return f'Error: "{file_path}" is not a Python file'
            
            command = ["python", target_file]

            if args:
                command.extend(args)

            output = subprocess.run(command, cwd = working_dir_abs, capture_output=True, text=True, timeout=30)
            exit_string = str()

            if output.returncode != 0:
                exit_string += f'Process exited with code {output.returncode}\n'

            if not output.stderr and not output.stdout:
                exit_string += f'No output produced'

            else:
                exit_string += f'STDOUT: {output.stdout}STDERR: {output.stderr}'
            
            return exit_string







        except Exception as e:
            return f"Error: executing Python file: {e}"
        




