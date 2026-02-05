# core_logic.py
# Core business logic for Traceview conversion and file splitting.
# This module is UI-agnostic.

import os
import subprocess
from utils import resource_path

def run_traceview_conversion(etl_path, pdb_path, callbacks):
    """
    Runs the traceview command in a subprocess and reports progress
    through callbacks.
    """
    output_txt = os.path.join(os.path.dirname(etl_path), os.path.splitext(os.path.basename(etl_path))[0] + ".txt")
    
    traceview_exe = resource_path(os.path.join("traceview", "traceview.exe"))
    executable_to_run = "traceview"
    
    if os.path.isfile(traceview_exe):
        executable_to_run = traceview_exe
        callbacks['log']("INFO: Found bundled 'traceview.exe'. Using it.\n")
    else:
        callbacks['log']("WARNING: Bundled 'traceview.exe' not found. Assuming it's in the system PATH.\n")
        
    command = [executable_to_run, "-process", etl_path, "-pdb", pdb_path, "-o", output_txt]
    callbacks['log'](f"Executing command:\n{' '.join(command)}\n\n")

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace', creationflags=subprocess.CREATE_NO_WINDOW)
        for line in iter(process.stdout.readline, ''):
            callbacks['log'](line)
        process.stdout.close()
        return_code = process.wait()
        
        if return_code == 0:
            callbacks['log'](f"\n--- SUCCESS: Conversion complete. Output saved to:\n{output_txt} ---\n")
            callbacks['success'](output_txt)
        else:
            callbacks['log'](f"\n--- ERROR: Traceview process failed with return code {return_code}. ---\n")
            callbacks['failure']("Traceview conversion failed.")
    except FileNotFoundError:
        error_msg = f"'{executable_to_run}' not found."
        callbacks['log'](f"\n--- FATAL ERROR: {error_msg} ---\n")
        callbacks['log']("Please ensure 'traceview.exe' is bundled or is in your system's PATH.")
        callbacks['failure'](error_msg)
    except Exception as e:
        callbacks['log'](f"\n--- An unexpected error occurred: {e} ---\n")
        callbacks['failure']("An unexpected error occurred during conversion.")

def run_file_splitting(txt_path, split_size, unit, estimated_files, callbacks):
    """
    Runs the file splitting logic and reports progress through callbacks.
    """
    callbacks['log'](f"Source file: {txt_path}\n")
    try:
        if split_size <= 0: raise ValueError("Split size must be greater than 0")
        chunk_size = (split_size * 1024) if unit == "KB" else (split_size * 1024 * 1024)
        callbacks['log'](f"Settings: Split size per file = {split_size} {unit}\n\n")
        
        file_count = 0
        with open(txt_path, 'r', encoding='utf-8', errors='ignore') as f_in:
            directory, base_name = os.path.dirname(txt_path), os.path.splitext(os.path.basename(txt_path))[0]
            while True:
                chunk = f_in.read(chunk_size)
                if not chunk: break
                file_count += 1
                callbacks['status'](f"Splitting: File {file_count} of {estimated_files}...")
                
                output_filename = f"{base_name}_part_{file_count}.txt"
                output_path = os.path.join(directory, output_filename)
                callbacks['log'](f"INFO: Creating part {file_count}: {output_filename}\n")
                
                with open(output_path, 'w', encoding='utf-8') as f_out:
                    f_out.write(chunk)
                    
        callbacks['status'](f"Split complete! {file_count} files created.")
        callbacks['log'](f"\n--- SUCCESS: Split complete! {file_count} files created. ---\n")
        callbacks['success'](f"File successfully split into {file_count} parts!")
    except Exception as e:
        error_msg = f"An error occurred: {e}"
        callbacks['status'](error_msg)
        callbacks['log'](f"\n--- ERROR: An unexpected error occurred during splitting: ---\n{e}\n")
        callbacks['failure'](f"An error occurred during splitting:\n{e}")