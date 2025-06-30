main:
	cat Makefile

#1
download:
	python3 download.py

#2
import:
	python3 csv_to_duckdb.py

#3
transform:
	python3 transform.py

#4
metabase:
	cd Metabase && make drun
	# Wait some time and open metabase interface in http://localhost:3000


