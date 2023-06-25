import json
import csv
import pymysql


def create_database(cursor):
    try:
        name = input("Write title: ")
        create_db_query = "CREATE DATABASE {};".format(name)
        cursor.execute(create_db_query)
        print("Database {} was created successful...".format(name))
    except Exception as ex:
        print("Creation error...")
        print(ex)


def delete_database(cursor):
    try:
        name = input("Write title: ")
        create_db_query = "DROP DATABASE {};".format(name)
        cursor.execute(create_db_query)
        print("Database {} was deleted successful...".format(name))
    except Exception as ex:
        print("Deleting error...")
        print(ex)


def select_database(cursor):
    while True:
        show_query = "SHOW DATABASES;"
        cursor.execute(show_query)
        databases = cursor.fetchall()
        print("Databases:")
        for i in range(len(databases)):
            print(databases[i]['Database'])

        print("NAME - choose database\n1 - create database\n2 - delete database\n0 - exit")
        command = input()

        if command == '1':
            create_database(cursor)
        elif command == '2':
            delete_database(cursor)
        elif command == '0':
            return None
        else:
            try:
                select_database_query = "USE {};".format(command)
                cursor.execute(select_database_query)
                temp = select_table(cursor, command)
                if temp != None:
                    return temp
            except Exception as ex:
                print(ex)


def select_table(cursor, dbtitle):
    while True:
        show_query = "SHOW TABLES;"
        cursor.execute(show_query)
        tables = cursor.fetchall()
        print(f"{dbtitle}:")
        for i in range(len(tables)):
            print(f"--{tables[i]['Tables_in_{}'.format(dbtitle)]}")
        print("NAME - choose table\n1 - create table\n2 - delete table\n0 - back")
        command = input()

        if command == '1':
            create_table(cursor, dbtitle)
        elif command == '2':
            delete_table(cursor)
        elif command == '0':
            return None
        else:
            try:
                check = "DESC `{}`".format(command)
                cursor.execute(check)
                temp = table_settings(cursor, command)
                if temp != None:
                    return temp
            except Exception as ex:
                print(ex)


def table_settings(cursor, table_name):
    while True:
        print("Table name: {}".format(table_name))
        print("1 - insert data in table\n2 - show first 10 rows\n3 - download table\n4 - use this table for graphs\n0 - back")
        command = input()

        if command == '1':
            new_row(cursor, table_name)
        elif command == '2':
            show_10_rows(cursor, table_name)
        elif command == '3':
            type = input("Write type of file (csv/json): ")
            if type == 'csv':
                data = show_all_rows(cursor, table_name)
                file_name = input("Write file name:")
                with open(f"{file_name}.csv", "w", encoding="utf-8") as f:
                    csvwrite = csv.writer(f, lineterminator="\r", quoting=csv.QUOTE_NONE, escapechar='\\')
                    csvwrite.writerow(data[0])
                    for i in range(len(data)):
                        csvwrite.writerow([i, *data[i].values()])

            elif type == 'json':
                data = show_all_rows(cursor, table_name)
                file_name = input("Write file name:")
                with open(f"{file_name}.json", "w") as f:
                    f.write( json.dumps(data) )

            else:
                print("Wrong command...")
        elif command == '4':
            return table_name
        elif command == '0':
            return None
        else:
            print("Wrong command...")


def create_table(cursor, dbtitle):
    try:
        table_name = input("Write title:")
        create_table_query = "CREATE TABLE `{}`.`{}` " \
                             "(`id` INT(10) NOT NULL AUTO_INCREMENT ," \
                             " `Formula` VARCHAR(255) NOT NULL ," \
                             " `Temperature(K)` INT(10) NULL ," \
                             " `Seebeck_coefficient(μV/K)` FLOAT NULL , " \
                             " `Electrical_conductivity(S/m)` FLOAT NULL , " \
                             " `Thermal_conductivity(W/mK)` FLOAT NULL , " \
                             " `Power_factor(W/mK2)` FLOAT NULL , " \
                             " `ZT` FLOAT NULL , " \
                             " `Reference` VARCHAR(255) NULL , " \
                             " PRIMARY KEY (`id`)) ENGINE = InnoDB" \
                             " CHARSET=utf8mb4 COLLATE utf8mb4_general_ci;".format(dbtitle, table_name)

        cursor.execute(create_table_query)
        print("Table done...")
    except Exception as ex:
        print("Creating error...")
        print(ex)


def delete_table(cursor):
    try:
        table_name = input("Write title:")
        drop_table_query = "DROP TABLE `{}`;".format(table_name)
        cursor.execute(drop_table_query)
    except Exception as ex:
        print("Deleting error...")
        print(ex)


def new_row(cursor, table_name):
    try:
        with open("database.json", "r") as f:
            js = json.loads( f.read() )

        for i in range(len(js)):
            mass = list(js[i].values())
            insert_query = """INSERT INTO `{}` (`Formula`, `Temperature(K)`, `Seebeck_coefficient(μV/K)`, `Electrical_conductivity(S/m)`, `Thermal_conductivity(W/mK)`, `Power_factor(W/mK2)`, `ZT`, `Reference`) VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}");""".format(table_name, *mass)
            cursor.execute(insert_query)

    except Exception as ex:
        print("Upload error...")
        print(ex)


def show_10_rows(cursor, table_name):
    select_10_rows = "SELECT * FROM `{}` LIMIT 10;".format(table_name)
    cursor.execute(select_10_rows)
    rows = cursor.fetchall()
    print(f"{table_name}:")
    for row in rows:
        print(f"--{row}")


def show_all_rows(cursor, table_name):
    select_all_rows = "SELECT `Name`, `Temperature_Value`, `ZT`, `PF`, `S^2`, `s`, `k`, `Original_Counts`, `New_Counts`, `Inference`, `Editing`, `Pressure`, `Process`, `Label`, `Direction_of_Measurement`, `DOI`, `Publisher`, `Access_Type`, `Publication_Year`, `Authors`, `Journal`, `Comparison` FROM `{}`;".format(table_name)
    cursor.execute(select_all_rows)
    return cursor.fetchall()


def start():
    try:
        connection = pymysql.connect(
            user='root',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)
        print("Connection success...")
        return True, connection
    except Exception as ex:
        print("Connection error...")
        print(ex)
        return False, None

