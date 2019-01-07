echo "fehlendes Datenfile"

@echo off
 
net stop OracleServiceKHV

move D:\oracle\oradata\KHV\data\core_IDXXE01.DBF C:\tmp\datafile\CORE_IDXX01.DBF
net 
start OracleServiceKHV