@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo FastViewer のアプリアイコンおよびファイル関連付けを登録中...

set "ICO_PATH=%~dp0app_icon.ico"
set "BAT_PATH=%~dp0FastViewer起動.bat"

reg add "HKCU\Software\Classes\FastViewer.Image" /ve /d "FastViewer 画像ファイル" /f >nul
reg add "HKCU\Software\Classes\FastViewer.Image\DefaultIcon" /ve /d "%ICO_PATH%,0" /f >nul
reg add "HKCU\Software\Classes\FastViewer.Image\shell\open\command" /ve /d "\"%BAT_PATH%\" \"%%1\"" /f >nul

for %%E in (.png .jpg .jpeg .bmp .webp .gif) do (
    reg add "HKCU\Software\Classes\%%E" /ve /d "FastViewer.Image" /f >nul
)

ie4uinit.exe -show
echo 【完了】アイコンの登録が完了しました！エクスプローラーを再起動または更新するとアイコンが変わります。
pause
