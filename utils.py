# utils.py
import os
import sys

def resource_path(relative_path):
    """ 
    取得資源的絕對路徑。
    如果是開發環境，回傳當前目錄下的路徑。
    如果是打包後的 EXE，回傳解壓後的暫存目錄 (_MEIPASS) 下的路徑。
    """
    try:
        # PyInstaller 創建的暫存資料夾
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)