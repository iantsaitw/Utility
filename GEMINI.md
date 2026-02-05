# Driver Deck

Driver Deck 是一個專用於管理與建置 Windows 驅動程式（PCIE/USB）的 GUI 工具。

## 專案概覽
- **主要框架**: Python, Tkinter, sv-ttk (Win11 風格主題)
- **核心功能**:
    - 自動掃描專案目錄。
    - 支援 PCIE 與 USB 驅動建置。
    - 整合終端機輸出。
    - 支援深色/淺色模式切換。
- **目標驅動**:
    - PCIE: `RTLWlanE_WindowsDriver`
    - USB: `RTLWlanU_WindowsDriver`

## 關鍵檔案
- `main.py`: 應用程式入口點。
- `config.py`: 全域設定與常數定義。
- `project_tab.py`: 專案分頁邏輯。
- `driver_utils.py`: 驅動程式相關操作工具。
- `ui_factory.py`: UI 元件工廠。

## 開發備註
- 使用 `sv_ttk` 提供現代化的介面。
- 透過 `ctypes` 啟用 Windows 11 的沉浸式深色模式。
- 設定儲存於 `settings.json`。
