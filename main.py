import DB
import Graph
import Logic
import json
import pandas

def file_convert(file_name):
    excel_data = pandas.read_excel('{}.xlsx'.format(file_name))
    js = excel_data.to_json()

    dic = json.loads(js)
    for value in dic.values():
        n = len(value)
        break

    mass = list()
    for i in range(n):
        mass.append({})
    for key, value in dic.items():
        for i in range(n):
            mass[i][key] = value[str(i)]

    with open("database.json", "w") as f:
        f.write( json.dumps(mass) )
while True:
    print("Convert file Y/N?")
    command = input().upper()
    if command == 'Y':
        file_name = input("Write file name (without .xlsx): ")
        file_convert(file_name)
        break
    elif command == 'N':
        break
    else:
        print("Wrong command...")

valid = False
try:
    valid, connection = DB.start()
    try:
        if valid:
            with connection.cursor() as cursor:
                table_name = DB.select_database(cursor)
                connection.commit()
                if table_name != None:
                    command, data = Logic.graph_select(cursor, table_name)
                    Graph.start(command, data)
    finally:
        connection.close()
except Exception as ex:
    print(ex)


