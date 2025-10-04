@echo off
REM ========================================
REM Script para ejecutar tests de mobile-tests
REM ========================================

REM Validar que el entorno virtual esta activado
echo Verificando entorno virtual...
python -c "import sys; exit(0 if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else 1)" 2>nul
if errorlevel 1 (
    echo [ERROR] El entorno virtual no esta activado.
    echo Por favor, active el entorno virtual con: venv\Scripts\activate
    echo.
    pause
    exit /b 1
)
echo [OK] Entorno virtual activado
echo.

REM Validar que Appium Server esta corriendo
echo Verificando Appium Server...
curl -s http://localhost:4723/status >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Appium Server no esta corriendo en el puerto 4723.
    echo Por favor, inicie Appium Server antes de continuar.
    echo.
    pause
    exit /b 1
)
echo [OK] Appium Server esta corriendo
echo.

REM Crear carpeta de reportes si no existe
if not exist "reports\mobile" mkdir reports\mobile

REM Limpiar screenshots anteriores
echo Limpiando screenshots anteriores...
if exist "reports\screenshots" (
    del /Q reports\screenshots\*.png 2>nul
    echo [OK] Screenshots eliminados
) else (
    echo [INFO] No hay screenshots para limpiar
)
echo.

REM Obtener timestamp para el reporte
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
set mytime=%mytime: =0%
set TIMESTAMP=%mydate%_%mytime%

pause

:menu
cls
echo ========================================
echo    MOBILE TESTS - QA AUTOMATION
echo ========================================
echo.
echo Seleccione una opcion:
echo.
echo 1. Ejecutar flujo completo de Crypto Exchange
echo 2. Ejecutar todos los tests de Crypto Exchange
echo 3. Ejecutar todos los tests de mobile-tests
echo 4. Ejecutar test especifico (ingresar ruta)
echo 5. Salir
echo.
set /p option="Opcion: "

if "%option%"=="1" goto test_complete_flow
if "%option%"=="2" goto test_crypto_all
if "%option%"=="3" goto test_all
if "%option%"=="4" goto test_custom
if "%option%"=="5" goto end
echo Opcion invalida
pause
goto menu

:test_complete_flow
cls
echo Ejecutando flujo completo de Crypto Exchange...
echo.
pytest mobile-tests/tests/test_crypto_exchange.py::TestCryptoExchange::test_complete_crypto_exchange_flow -v -s --html=reports/mobile/mobile_report_%TIMESTAMP%.html --self-contained-html
goto test_end

:test_crypto_all
cls
echo Ejecutando todos los tests de Crypto Exchange...
echo.
pytest mobile-tests/tests/test_crypto_exchange.py -v -s --html=reports/mobile/mobile_report_%TIMESTAMP%.html --self-contained-html
goto test_end

:test_all
cls
echo Ejecutando todos los tests de mobile-tests...
echo.
pytest mobile-tests/ -v -s --html=reports/mobile/mobile_report_%TIMESTAMP%.html --self-contained-html
goto test_end

:test_custom
cls
echo.
set /p test_path="Ingrese la ruta del test (ejemplo: mobile-tests/tests/test_crypto_exchange.py): "
echo.
echo Ejecutando: %test_path%
echo.
pytest %test_path% -v -s --html=reports/mobile/mobile_report_%TIMESTAMP%.html --self-contained-html
goto test_end

:test_end
echo.
echo ========================================
echo Tests finalizados
echo Reporte generado: reports\mobile\mobile_report_%TIMESTAMP%.html
echo ========================================
echo.
set /p open_report="Desea abrir el reporte HTML? (s/n): "
if /i "%open_report%"=="s" start reports\mobile\mobile_report_%TIMESTAMP%.html
echo.
pause
goto menu

:end
echo Saliendo...
exit
