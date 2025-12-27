import os
from config import MAX_CHARS
from google.genai import types



schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets content from a file, truncating at the configured MAX_CHARS limit.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to get content from file, relative to the working directory",
            ),
        
        },
        required= ["file_path"]
    ),
)


def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        
        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory' 
        
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"' 
        
        with open(target_file) as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content

    except Exception as e:
        return f'Error reading file "{file_path}": {e}'



