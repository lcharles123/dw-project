import duckdb
import glob
import os
import config


#DuckDB is an embedded database, similar to SQLite, but designed for OLAP-style analytics instead of OLTP. The only configuration parameter that is required in your profile (in addition to type: duckdb) is the path field, which should refer to a path on your local filesystem where you would like the DuckDB database file (and it's associated write-ahead log) to be written. You can also specify the schema parameter if you would like to use a schema besides the default (which is called main).
def detect_delimiter(file_path):
    with open(file_path, 'r', encoding='latin-1') as f:
        first_line = f.readline()
        for delim in [',', '\t', ';']:
            if delim in first_line:
                return delim,len(first_line.split(delim))
    raise ValueError("Delimiter not recognized, supported types are ';' and '\t'.")

def detect_columns(csv_files):
    """Return a list like: [{'link', 'delim', number_of_columns},]"""
    csv = []
    for f in csv_files:
        file_path = { 'link': f }
        file_path['delim'], file_path['columns'] =  detect_delimiter(f)
        csv.append(file_path)
    return csv

def import_csv(csv_files):
    """Import csv from list of files"""
    for csv in csv_files:
        if csv['columns'] == 27:
            conn.execute(f"""
            CREATE TABLE IF NOT EXISTS atendimentoporfornecedor AS
            SELECT * FROM read_csv('{csv["link"]}', delim='{csv["delim"]}', all_varchar=false, ignore_errors=true) LIMIT 0;
            
            INSERT INTO atendimentoporfornecedor
            SELECT * FROM read_csv('{csv["link"]}', delim='{csv["delim"]}', union_by_name = true, ignore_errors=true);
        """)
        elif csv['columns'] == 18:
            conn.execute(f"""
            CREATE TABLE IF NOT EXISTS atendimento AS
            SELECT * FROM read_csv('{csv["link"]}', delim='{csv["delim"]}', all_varchar=false, ignore_errors=true) LIMIT 0;
            
            INSERT INTO atendimento
            SELECT * FROM read_csv('{csv["link"]}', delim='{csv["delim"]}', union_by_name = true, ignore_errors=true);
        """)
        else:
            raise ValueError("Unrecgonized number of columns, accepted values: 18, 27")

# Main execution
conn = duckdb.connect(database=config.DUCKDB_FILE, read_only=False)  
csv_dir = config.DOWNLOAD_DIR
file_paths = glob.glob(os.path.join(csv_dir, '*.csv'))

csv_files = detect_columns(file_paths)

import_csv(csv_files)

print("\nAll imported.")
# Verify results
print("\nFinal table schema:")
print(conn.sql("DESCRIBE atendimentoporfornecedor"))
print(conn.sql("SELECT COUNT(*) FROM atendimentoporfornecedor"))
print(conn.sql("DESCRIBE atendimento"))
print(conn.sql("SELECT COUNT(*) FROM atendimento"))

