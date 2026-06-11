@echo off
echo ===================================================
echo Instalando dependencias do Batalha Pokemon...
echo ===================================================
python -m pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERRO] Ocorreu uma falha ao instalar as dependencias.
    echo Verifique se o Python esta instalado e no PATH do sistema.
) else (
    echo.
    echo [SUCESSO] Todas as dependencias foram instaladas com sucesso!
)
echo.
pause
