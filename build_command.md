# 打包編譯指令紀錄

如果你未來需要手動將 `bmi_score_calculator.py` 打包成可獨立執行的 `.exe` 檔案，請開啟命令提示字元 (CMD) 或 PowerShell，切換到資料夾，並執行以下指令：

```powershell
py -m PyInstaller --onefile --windowed --clean -y --icon="app_icon.ico" --add-data="app_icon.ico;." --name "MJ-Fit_King_Tracker" bmi_score_calculator.py
```

## 參數說明：
- `--onefile`: 將所有依賴檔案打包成單一個 `.exe` 檔案。
- `--windowed`: 隱藏背景的黑色終端機畫面 (Console)，只顯示圖形介面。
- `--clean`: 清除先前的暫存快取，確保乾淨編譯。
- `-y`: 如果輸出資料夾已存在同名檔案，自動覆蓋。
- `--icon="app_icon.ico"`: 設定應用程式 `.exe` 檔案在 Windows 檔案總管裡顯示的圖示。
- `--add-data="app_icon.ico;."`: 將圖示檔隨附打包進 `.exe` 內部，讓應用程式左上角的視窗也能順利載入該圖片。
- `--name "MJ-Fit_King_Tracker"`: 指定輸出執行檔的名稱。
