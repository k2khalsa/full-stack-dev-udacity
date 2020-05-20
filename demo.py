import psycopg2

connection = psycopg2.connect('dbname=postgres user=postgres password=password')

cursor = connection.cursor()

cursor.execute('DROP TABLE IF EXISTS table2;')

cursor.execute('''
    CREATE TABLE table2 (
        id INTEGER PRIMARY KEY,
        completed BOOLEAN NOT NULL DEFAULT FALSE
    );
''')

cursor.execute('INSERT INTO table2 (id, completed) VALUES (1, true);')

cursor.execute('SELECT * FROM table2;')

results = cursor.fetchall()

print (results)

connection.commit()

connection.close()

cursor.close()