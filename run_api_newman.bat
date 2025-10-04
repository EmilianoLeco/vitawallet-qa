@echo off
REM Script para ejecutar tests de API con Newman y generar reporte HTML
REM Vita Wallet - QA Automation

cls
echo ==========================================
echo  Ejecutando API Tests con Newman
echo ==========================================
echo.

REM Verificar que estamos en la carpeta correcta
if not exist "api-tests\postman\Petstore_Collection.json" (
    echo [ERROR] No se encuentra Petstore_Collection.json
    echo Ejecuta este script desde la raiz del proyecto
    pause
    exit /b 1
)

REM Verificar que Newman está instalado
where newman >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Newman no esta instalado
    echo.
    echo Instalalo con:
    echo npm install -g newman newman-reporter-htmlextra
    echo.
    pause
    exit /b 1
)

REM Crear carpeta de reportes si no existe
if not exist "reports\newman" mkdir reports\newman

REM Obtener timestamp para el reporte
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
set mytime=%mytime: =0%
set TIMESTAMP=%mydate%_%mytime%

echo Ejecutando Postman Collection con Newman...
echo Collection: Petstore_Collection.json
echo.

REM Ejecutar Newman con reporte HTML
newman run api-tests\postman\Petstore_Collection.json ^
    -r cli,htmlextra,json ^
    --reporter-htmlextra-export reports\newman\newman_report_%TIMESTAMP%.html ^
    --reporter-htmlextra-darkTheme ^
    --reporter-htmlextra-title "Petstore API - Test Report" ^
    --reporter-htmlextra-showOnlyFails false ^
    --reporter-json-export reports\newman\newman_report_%TIMESTAMP%.json ^
    --delay-request 500 ^
    --timeout-request 10000

REM Guardar código de salida
set EXIT_CODE=%ERRORLEVEL%

echo.
echo ==========================================

if %EXIT_CODE% EQU 0 (
    echo [OK] Todos los tests pasaron exitosamente!
    echo.
    echo Reportes generados:
    echo - HTML: reports\newman\newman_report_%TIMESTAMP%.html
    echo - JSON: reports\newman\newman_report_%TIMESTAMP%.json
    echo.
    
    REM Abrir reporte HTML en navegador
    echo Abriendo reporte en el navegador...
    start reports\newman\newman_report_%TIMESTAMP%.html
) else (
    echo [ERROR] Algunos tests fallaron
    echo.
    echo Revisa el reporte HTML para mas detalles:
    echo reports\newman\newman_report_%TIMESTAMP%.html
    echo.
    
    REM Abrir reporte aunque haya errores
    start reports\newman\newman_report_%TIMESTAMP%.html
)

echo ==========================================
echo.
echo Archivos generados en: reports\newman\
dir /b reports\newman\newman_report_%TIMESTAMP%.*
echo.
pause