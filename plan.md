# Driver Deck - 開發計畫書 (Plan.md)

Driver Deck 是一個專為 Windows 驅動程式（PCIE/USB）設計的現代化 GUI 管理與建置工具。

## 1. 專案核心目標
- **自動化管理**: 簡化驅動程式開發過程中的版本追蹤、備份與匯出。
- **一致性**: 提供統一的介面來處理 PCIE (`RTLWlanE`) 與 USB (`RTLWlanU`) 驅動。
- **安全性**: 整合數位簽章流程，確保驅動程式符合 Windows 載入要求。
- **現代化體驗**: 採用 Windows 11 風格 UI，提升開發者的使用效率。

## 2. 當前版本與功能 (v5.3.1)
### 已實現功能
- [x] **多專案管理**: 自動掃描 Root 目錄下的驅動專案（依據 `setenv-...bat` 識別）。
- [x] **驅動版本識別**: 自動讀取 `.sys` 檔案的版本資訊與數位簽章狀態。
- [x] **自動分類**: 支援 PCIE 與 USB 驅動的分頁顯示與類別過濾。
- [x] **備份機制**: 支援帶有時間戳記的一鍵資料夾備份。
- [x] **靈活匯出**: 提供全資料夾複製或僅匯出 `.sys` 驅動檔的功能。
- [x] **數位簽章整合**: 內建 `signtool.exe` 調用邏輯，支援使用 PFX 憑證進行簽章。
- [x] **自訂化設定**: 支援深色/淺色模式、自訂字體、強調色（Accent Color）以及路徑管理。
- [x] **UI 佈局優化**: 優化內距與按鈕位置，減少空間擠迫感，提升垂直顯示效率。

### 系統架構
- **GUI 框架**: Python + Tkinter + `sv-ttk` (Sun Valley Theme)。
- **設定管理**: `settings.json` 與 `config.py`。
- **底層工具**: `driver_utils.py` (封裝 `ctypes` 調用 Windows API 與 `subprocess` 指令)。
- **元件化工廠**: `ui_factory.py` 負責生產風格一致的 UI 元件。

## 3. 待開發與優化清單 (Roadmap)

### 第一階段：基礎設施強化 (High Priority)
- [x] **終端機組件整合**: 將 `terminal_widget.py` 整合進主介面左側。
- [ ] **建置流程自動化**: 在 UI 中整合驅動建置按鈕，自動調用環境設定與 MSBuild。

### 第二階段：效能與穩定性 (Medium Priority)
- [ ] **多執行緒優化**: 將掃描驅動版本與驗證數位簽章改為非同步執行，避免 UI 凍結。
- [ ] **匯出歷史紀錄**: 記錄匯出時間、版本與目的地，方便日後追蹤。

### 第三階段：進階功能 (Low Priority)
- [ ] **多語言支援 (i18n)**: 支援繁體中文、英文等介面切換。
- [ ] **驅動安裝工具**: 整合簡單的 `devcon` 或 `PnPUtil` 操作，方便本地測試。

## 4. 關鍵檔案說明
- `main.py`: 程式入口點，管理主視窗與專案分頁載入。
- `project_tab.py`: 單一專案的操作面板，包含版本列表與功能按鈕。
- `config.py`: 管理全域設定、顏色主題與預設路徑。
- `driver_utils.py`: 負責 Windows API 互動、版本讀取與簽章驗證。
- `terminal_widget.py`: 互動式 CMD 終端機組件 (目前獨立存在)。
- `ui_factory.py`: 現代化 Tkinter 元件工廠。
- `settings_dialog.py`: 使用者設定視窗。
- `build.bat`: 自動化打包應用程式之腳本。