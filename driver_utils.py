# driver_utils.py
import os
import ctypes
from ctypes import wintypes
import subprocess
import glob
import datetime
import config 

def get_file_version(path):
    try:
        if not os.path.exists(path): return ""
        size = ctypes.windll.version.GetFileVersionInfoSizeW(path, None)
        if not size: return ""
        res = ctypes.create_string_buffer(size)
        if not ctypes.windll.version.GetFileVersionInfoW(path, 0, size, res): return ""
        r = ctypes.c_void_p()
        l = ctypes.c_uint()
        if not ctypes.windll.version.VerQueryValueW(res, "\\", ctypes.byref(r), ctypes.byref(l)): return ""
        if not l.value: return ""
        class VS_FIXEDFILEINFO(ctypes.Structure):
            _fields_ = [
                ("dwSignature", wintypes.DWORD), ("dwStrucVersion", wintypes.DWORD),
                ("dwFileVersionMS", wintypes.DWORD), ("dwFileVersionLS", wintypes.DWORD),
                ("dwProductVersionMS", wintypes.DWORD), ("dwProductVersionLS", wintypes.DWORD),
                ("dwFileFlagsMask", wintypes.DWORD), ("dwFileFlags", wintypes.DWORD),
                ("dwFileOS", wintypes.DWORD), ("dwFileType", wintypes.DWORD),
                ("dwFileSubtype", wintypes.DWORD), ("dwFileDateMS", wintypes.DWORD),
                ("dwFileDateLS", wintypes.DWORD),
            ]
        ver_info = ctypes.cast(r, ctypes.POINTER(VS_FIXEDFILEINFO)).contents
        major = (ver_info.dwFileVersionMS >> 16) & 0xFFFF
        minor = ver_info.dwFileVersionMS & 0xFFFF
        build = (ver_info.dwFileVersionLS >> 16) & 0xFFFF
        revision = ver_info.dwFileVersionLS & 0xFFFF
        return f"{major}.{minor}.{build}.{revision}"
    except Exception: return ""

def find_signtool():
    base_paths = [
        r"C:\Program Files (x86)\Windows Kits\10\bin",
        r"C:\Program Files\Windows Kits\10\bin"
    ]
    candidates = []
    for base in base_paths:
        if os.path.exists(base):
            pattern = os.path.join(base, "*", "x64", "signtool.exe")
            found = glob.glob(pattern)
            candidates.extend(found)
    if candidates:
        candidates.sort(reverse=True)
        return candidates[0]
    return None

def check_file_signature(path):
    tool = config.current_settings.get("signtool_path", "")
    if not tool or not os.path.exists(tool):
        tool = find_signtool()
    if not tool: return "?" 

    cmd = f'"{tool}" verify /pa /v /all "{path}"'
    
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                 startupinfo=startupinfo, shell=True)
        stdout, stderr = process.communicate()
        
        try:
            output = stdout.decode('cp950', errors='ignore') + stderr.decode('cp950', errors='ignore')
        except:
            output = stdout.decode('utf-8', errors='ignore') + stderr.decode('utf-8', errors='ignore')

        signers = []
        current_signer_candidate = None 
        is_timestamp_section = False    

        for line in output.splitlines():
            line = line.strip()
            if line.startswith("Signature Index:"):
                if current_signer_candidate:
                    if current_signer_candidate not in signers:
                        signers.append(current_signer_candidate)
                current_signer_candidate = None
                is_timestamp_section = False
                continue

            if "Timestamp Verified by:" in line or "The signature is timestamped:" in line:
                is_timestamp_section = True
                continue

            token = None
            if "Issued to:" in line: token = "Issued to:"
            elif "發給:" in line: token = "發給:"
            
            if token and not is_timestamp_section:
                parts = line.split(token, 1)
                if len(parts) > 1:
                    current_signer_candidate = parts[1].strip()

        if current_signer_candidate and current_signer_candidate not in signers:
            signers.append(current_signer_candidate)

        if not signers:
            if "No signature found" in output or "找不到簽章" in output:
                return "Unsigned"
            return "Unsigned"
        
        result_str = ", ".join(signers)
        if process.returncode != 0:
            result_str += " (Untrusted)"
            
        return result_str
    except:
        return "Error"

def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024: return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

def get_time_suffix():
    return "_" + datetime.datetime.now().strftime("%Y%m%d_%H%M")