@echo off
NET START | FIND "OracleServiceKHV" > nul IF errorlevel 2 ECHO True