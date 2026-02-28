import os

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        dir_list = os.scandir(target_dir)
        
        file_data = []

        for file in dir_list:
            file_data.append({
                'name': file.name,
                'size': file.stat().st_size,
                'is_dir': file.is_dir()
            })
        
        return_file_data = "\n".join(
        f"- {file['name']}: file_size={file['size']} bytes, is_dir={file['is_dir']}" 
        for file in file_data
        )
        
        return return_file_data
    except Exception as e:
        return f"Error:{e}"
