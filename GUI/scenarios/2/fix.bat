echo "fehlendes Datenfile reset"
net stop OracleServiceKHV
rman
connect target sys/oracle@KHV
restore datafile 6;
recover datafile 6;
alter database open;