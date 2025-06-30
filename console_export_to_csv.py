import duckdb


conn = duckdb.connect(database='operdb.duckdb', read_only=False)  

def console():
    while True:
        try:
            print(conn.sql(input("> ")))
        except KeyboardInterrupt:
            exit(0)
        except Exception as e:
            print(e)
            pass

console()
FOLDER="dbt_project/seeds/"

print("exporting atendimento.csv to", FOLDER)
query = "COPY (select * from atendimento where Regiao != 'NULL' and UF != 'NULL' and  DescricaoTipoAtendimento != 'NULL' and  DescricaoAssunto != 'NULL' and GrupoAssunto != 'NULL' and CodigoProblema != 'NULL' and DescricaoProblema != 'NULL' and GrupoProblema != 'NULL' and SexoConsumidor != 'NULL' and FaixaEtariaConsumidor != 'NULL' and CEPConsumidor != 'NULL') TO '"+FOLDER+"atendimento.csv' (HEADER, DELIMITER ';');"
conn.sql(query)
# 10 524523 -> 7 838192

print("exporting atendimentoporfornecedor.csv to", FOLDER)
query = "COPY (select * from atendimentoporfonecedor where Regiao != 'NULL' and UF != 'NULL' and  DescricaoTipoAtendimento != 'NULL' and  DescricaoAssunto != 'NULL' and GrupoAssunto != 'NULL' and DescricaoProblema != 'NULL' and GrupoProblema != 'NULL' and SexoConsumidor != 'NULL' and FaixaEtariaConsumidor != 'NULL' and CEPConsumidor != 'NULL' and RazaoSocialSindec != 'NULL'  and CNPJ != 'NULL' and RadicalCNPJ != 'NULL') TO '"+FOLDER+"atendimentoporfornecedor.csv' (HEADER, DELIMITER ';');"
conn.sql(query)
# 8 212504 -> 6 961160

