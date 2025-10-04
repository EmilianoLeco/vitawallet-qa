@echo off
REM Script para ejecutar tests de API con Pytest y generar reporte HTML
REM Vita Wallet - QA Automation

cls
echo ==========================================
echo  Ejecutando API Tests con Pytest
echo ==========================================
echo.

REM Verificar que estamos en la carpeta correcta
if not exist "api-tests\pytest\test_petstore_api.py" (
    echo [ERROR] No se encuentra test_pet_api.py
    echo Ejecuta este script desde la raiz del proyecto
    pause
    exit /b 1
)

REM Activar entorno virtual
if exist "venv\Scripts\activate.bat" (
    echo Activando entorno virtual...
    call venv\Scripts\activate.bat
) else (
    echo [ERROR] No se encuentra el entorno virtual
    echo Ejecuta setup.bat primero
    pause
    exit /b 1
)

REM Crear carpeta de reportes si no existe
if not exist "reports\pytest" mkdir reports\pytest

REM Obtener timestamp para el reporte
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
set mytime=%mytime: =0%
set TIMESTAMP=%mydate%_%mytime%

echo.
echo Ejecutando tests...
echo.

REM Ejecutar pytest con reporte HTML
python -m pytest api-tests\pytest\ ^
    -v ^
    --tb=short ^
    --html=reports\pytest\api_report_%TIMESTAMP%.html ^
    --self-contained-html ^
    --capture=no

REM Guardar código de salida
set EXIT_CODE=%ERRORLEVEL%

echo.
echo ==========================================

if %EXIT_CODE% EQU 0 (
    echo [OK] Todos los tests pasaron!
    echo.
    echo Reporte generado:
    echo reports\pytest\api_report_%TIMESTAMP%.html
    echo.
    
    REM Abrir reporte en navegador
    echo Abriendo reporte en el navegador...
    start reports\pytest\api_report_%TIMESTAMP%.html
) else (
    echo [ERROR] Algunos tests fallaron
    echo Revisa el reporte para mas detalles:
    echo reports\pytest\api_report_%TIMESTAMP%.html
)

echo ==========================================
echo.
pause