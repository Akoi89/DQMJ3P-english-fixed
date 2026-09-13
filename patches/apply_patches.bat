@echo off
setlocal
rem Apply the two xdelta patches to the decrypted Japanese files.
rem   apply_patches.bat "<japanese base decrypted .cci>" "<japanese Ver.1.3 update decrypted .cia>"
rem or drag both files onto this .bat (either order; it tells them apart by size).
rem Output: DQMJ3P-base-fixed-0.1.0.cia and DQMJ3P-update-fixed-3.4.0.cia next to this file.
set "HERE=%~dp0"
if "%~2"=="" (
  echo Usage: apply_patches.bat "<japanese base decrypted .cci>" "<japanese update decrypted .cia>"
  echo Or drag both decrypted files onto this .bat.
  pause
  exit /b 1
)
set "BASE=%~1"
set "UPD=%~2"
if %~z1 LSS %~z2 (
  set "BASE=%~2"
  set "UPD=%~1"
)
echo Base source:   "%BASE%"
echo Update source: "%UPD%"
echo.
echo Patching the update (a few seconds)...
"%HERE%xdelta3.exe" -d -f -B 268435456 -s "%UPD%" "%HERE%DQMJ3P-update-fixed-3.4.0.xdelta" "%HERE%DQMJ3P-update-fixed-3.4.0.cia"
if errorlevel 1 goto fail
echo Patching the base (a minute or two, needs about 2 GB of free RAM)...
"%HERE%xdelta3.exe" -d -f -B 1879048192 -s "%BASE%" "%HERE%DQMJ3P-base-fixed-0.1.0.xdelta" "%HERE%DQMJ3P-base-fixed-0.1.0.cia"
if errorlevel 1 goto fail
echo.
echo Done. Check the two CIAs against the SHA-256 values in README.md, then install base first, update second.
pause
exit /b 0
:fail
echo.
echo xdelta3 reported an error. The usual cause is a source file that is not the decrypted Japanese file
echo described in README.md (compare its SHA-256), or the two arguments swapped with equal sizes.
pause
exit /b 1
