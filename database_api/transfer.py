# postgres
import psycopg2 as pg

config_in = {
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres',
    'password': 'VOXmuno98',
    'database': 'ParsissCRM'
}


in_conn = pg.connect(**config_in)

in_cur = in_conn.cursor()

in_cur.execute('SELECT * FROM public.patient_informations')

rows = in_cur.fetchall()

in_cur.close()
in_conn.close()
