@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo Windows のエクスプローラー詳細ペインに FastViewer アプリアイコンを登録中...

set "ICO_PATH=%~dp0app_icon.ico"
set "BAT_PATH=%~dp0FastViewer起動.bat"

:: ProgID 登録
reg add "HKCU\Software\Classes\FastViewer.Image" /ve /d "FastViewer 画像ファイル" /f >nul
reg add "HKCU\Software\Classes\FastViewer.Image\DefaultIcon" /ve /d "%ICO_PATH%,0" /f >nul
reg add "HKCU\Software\Classes\FastViewer.Image\shell\open\command" /ve /d "\"%BAT_PATH%\" \"%%1\"" /f >nul

:: Applications 登録
reg add "HKCU\Software\Classes\Applications\FastViewer.exe\DefaultIcon" /ve /d "%ICO_PATH%,0" /f >nul
reg add "HKCU\Software\Classes\Applications\FastViewer.exe\shell\open\command" /ve /d "\"%BAT_PATH%\" \"%%1\"" /f >nul

:: SystemFileAssociations (詳細ペイン・表示領域) 登録
for %%E in (.png .jpg .jpeg .bmp .webp .gif) do (
    reg add "HKCU\Software\Classes\%%E" /ve /d "FastViewer.Image" /f >nul
    reg add "HKCU\Software\Classes\SystemFileAssociations\%%E\DefaultIcon" /ve /d "%ICO_PATH%,0" /f >nul
)

:: エクスプローラー再起動でアイコンキャッシュを更新
taskkill /F /IM explorer.exe >nul 2>&1
timeout /t 1 /nobreak >nul
start explorer.exe

echo 【完了】アプリアイコンがエクスプローラーの詳細ペインおよび画像アイコンに反映されました！
