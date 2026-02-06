# Driver Deck - 專案狀態紀錄

## 專案概覽
Driver Deck 是一個專用於管理與建置 Windows 驅動程式的 GUI 工具，採用 Python + Tkinter + sv-ttk 構建。

## 當前版本特性 (v5.3.2 - UI 優化版)

### 1. 介面佈局 (UI Layout)
- **佈局對調**：將「專案管理分頁」移至左側，「終端機」移至右側，優化視覺重心。
- **視窗尺寸**：預設 geometry 設為 `1400x850`。
- **欄位優化**：優化「Files」清單欄位寬度，設定 `Name` 與 `Digital Signature` 自動伸縮，防止啟動時欄位被擠壓。
- **按鈕簡化**：將 Export 區域的按鈕文字從「Export Folder/Sys」簡化為「Folder/Sys」。
- **主題樣式**：使用 `sv-ttk` 提供深色模式，並透過 Win32 API 啟用 Windows 11 沉浸式標題列。

### 2. 整合終端機 (Terminal Widget)
- **Win32 嵌入**：透過 `SetParent` 與樣式修改將 CMD 視窗完美嵌入 Tkinter。
- **強效焦點管理**：
    - 實作 `AttachThreadInput` 技術，確保點擊或進入終端機區域時，鍵盤輸入能即時導向至內嵌的 CMD。
    - 支援 `Tab` 鍵輪巡：攔截 Tkinter 的 Tab 焦點切換，將 Tab 鍵傳遞給 CMD 進行路徑補全。
- **預設目錄**：終端機固定開啟於設定的「Root Path」(如 `E:\Project`)，確保啟動穩定性。

### 3. 設定持久化 (Settings Persistence)
- **絕對路徑修復**：修正 `settings.json` 的儲存路徑為 EXE 所在目錄，確保 PFX 等設定在不同啟動方式下皆能正確保留。

### 4. 建置系統 (Build System)
- **避開檔案鎖定**：`build.bat` 採用「暫存檔名建置法」。
    - 建置時先產出 `DriverDeck_Pro.exe` 以避開 Windows 系統對舊檔案的資源鎖定。
    - 建置成功後自動更名回 `Driver Deck.exe`，確保資源嵌入成功。

## 關鍵檔案說明
- `main.py`: 應用程式入口，處理佈局、DPI 意識與核心元件初始化。
- `terminal_widget.py`: 核心 Win32 視窗操作，處理嵌入、焦點管理與 Tab 鍵傳遞。
- `config.py`: 全域設定、顏色定義與 `settings.json` 絕對路徑處理。
- `project_tab.py`: 驅動清單邏輯、文件列表渲染與備份/匯出功能。
- `build.bat`: 穩定版 PyInstaller 打包腳本。

## 開發備註
- **管理員權限**：在管理員模式下，Windows 核心會限制部分 UI 渲染（如 Scrollbar 顏色），目前策略以功能穩定性為優先。
- **事件機制**：列表選取使用 `<<TreeviewSelect>>` 事件。

---
*最後更新日期：2026-02-05*
