@echo off
REM ========================================
REM Script para ejecutar tests usando Docker
REM ========================================

:menu
cls
echo ========================================
echo    VITAWALLET QA - DOCKER TESTS
echo ========================================
echo.
echo Seleccione una opcion:
echo.
echo 1. Ejecutar API Tests (Pytest)
echo 2. Ejecutar API Tests (Newman)
echo 3. Ejecutar Mobile Tests
echo 4. Iniciar Appium Server
echo 5. Ver logs de Appium
echo 6. Detener todos los contenedores
echo 7. Limpiar imagenes y contenedores
echo 8. Salir
echo.
set /p option="Opcion: "

if "%option%"=="1" goto api_pytest
if "%option%"=="2" goto api_newman
if "%option%"=="3" goto mobile_tests
if "%option%"=="4" goto start_appium
if "%option%"=="5" goto appium_logs
if "%option%"=="6" goto stop_all
if "%option%"=="7" goto cleanup
if "%option%"=="8" goto end
echo Opcion invalida
pause
goto menu

:api_pytest
cls
echo Ejecutando API Tests con Pytest en Docker...
echo.
docker-compose run --rm api-tests
echo.
echo Reporte generado en: reports\pytest\api_report.html
pause
goto menu

:api_newman
cls
echo Ejecutando API Tests con Newman en Docker...
echo.
docker-compose run --rm newman-tests
echo.
echo Reporte generado en: reports\newman\newman_report.html
pause
goto menu

:mobile_tests
cls
echo Verificando archivo .env...
if not exist .env (
    echo [ERROR] Archivo .env no encontrado.
    echo Copia .env.example a .env y completa las credenciales.
    pause
    goto menu
)
echo [OK] Archivo .env encontrado
echo.
echo Iniciando Appium Server y Mobile Tests...
echo.
docker-compose up -d appium
echo Esperando que Appium este listo...
timeout /t 10 /nobreak
docker-compose run --rm mobile-tests
echo.
echo Reporte generado en: reports\mobile\mobile_report.html
pause
goto menu

:start_appium
cls
echo Iniciando Appium Server en Docker...
echo.
docker-compose up -d appium
echo.
echo Appium Server corriendo en http://localhost:4723
echo Usa la opcion 5 para ver los logs
pause
goto menu

:appium_logs
cls
echo Logs de Appium Server (Ctrl+C para salir):
echo.
docker-compose logs -f appium
goto menu

:stop_all
cls
echo Deteniendo todos los contenedores...
docker-compose down
echo [OK] Contenedores detenidos
pause
goto menu

:cleanup
cls
echo Limpiando imagenes y contenedores...
echo.
docker-compose down -v
docker system prune -f
echo.
echo [OK] Limpieza completada
pause
goto menu

:end
echo Saliendo...
exit
