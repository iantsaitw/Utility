# core_logic.py
# Core business logic for ETL conversion and file splitting.
# Reverted to single traceview conversion mode for maximum compatibility.

import os
import subprocess
import psutil
from utils import resource_path

def run_conversion(etl_path, pdb_path, callbacks):
    """
    Runs the ETL conversion using the bundled traceview.exe.
    This tool handles special characters and Traditional Chinese environments better.
    """
    etl_path = os.path.abspath(etl_path)
    pdb_path = os.path.abspath(pdb_path)
    output_txt = os.path.abspath(os.path.join(os.path.dirname(etl_path), os.path.splitext(os.path.basename(etl_path))[0] + ".txt"))
    
    tools_dir = os.path.abspath(resource_path("trace_tools"))
    executable = os.path.join(tools_dir, "traceview.exe")

    if not os.path.exists(executable):
        callbacks['log'](f"ERROR: Tool not found: {executable}\n")
        callbacks['failure']("Required tool 'traceview.exe' is missing in trace_tools.")
        return

    callbacks['log'](f"INFO: Using bundled traceview.exe\n")
    
    # Traceview usage: traceview -process <etl> -pdb <pdb> -o <output>
    command = [executable, "-process", etl_path, "-pdb", pdb_path, "-o", output_txt]
    callbacks['log'](f"Executing: {' '.join(command)}\n\n")

    try:
        # Show window (creationflags=0) for maximum legacy compatibility
        process = subprocess.Popen(
            command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True, 
            encoding='utf-8', 
            errors='replace',
            cwd=tools_dir,
            creationflags=0
        )
        
        # High Priority
        try:
            p = psutil.Process(process.pid)
            p.nice(psutil.HIGH_PRIORITY_CLASS)
        except: pass

        for line in iter(process.stdout.readline, ''):
            callbacks['log'](line)
            
        process.stdout.close()
        return_code = process.wait()
        
        if os.path.exists(output_txt):
            callbacks['log'](f"\n--- SUCCESS: Conversion complete. ---\n")
            callbacks['success'](output_txt)
        else:
            callbacks['log'](f"\n--- ERROR: Output file not found. Exit code: {return_code} ---\n")
            callbacks['failure']("Conversion failed.")
            
    except Exception as e:
        callbacks['log'](f"\n--- FATAL ERROR: {e} ---\n")
        callbacks['failure'](str(e))

def run_file_splitting(txt_path, split_size, unit, estimated_files, callbacks):
    try:
        import math
        chunk_size = (split_size * 1024) if unit == "KB" else (split_size * 1024 * 1024)
        file_count = 0
        with open(txt_path, 'r', encoding='utf-8', errors='ignore') as f_in:
            directory = os.path.dirname(txt_path)
            base_name = os.path.splitext(os.path.basename(txt_path))[0]
            while True:
                chunk = f_in.read(chunk_size)
                if not chunk: break
                file_count += 1
                callbacks['status'](f"Splitting: Part {file_count}...")
                with open(os.path.join(directory, f"{base_name}_part_{file_count}.txt"), 'w', encoding='utf-8') as f_out:
                    f_out.write(chunk)
        callbacks['log'](f"SUCCESS: {file_count} parts created.\n")
        callbacks['success']("Split complete!")
    except Exception as e: callbacks['failure'](str(e))
