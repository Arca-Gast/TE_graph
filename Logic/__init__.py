def graph_select(cursor, table_name):
    print("You chose {}".format(table_name))
    print("1 - graph 'Seebeck - Electrical conductivity' for T=const\n"
          "2 - graph 'ZT from compound'\n"
          "3 - graph 'Parameters from temperature'\n"
          "0 - exit")
    command = input()

    if command == '0':
        return command, None
    if command == '1':
        return command, graph_Seebeck_Electrical_conductivity(cursor, table_name)
    if command == '2':
        return command, graph_ZT_from_compound(cursor, table_name)
    if command == '3':
        return command, graph_Parameters_from_temperature(cursor, table_name)


def graph_Seebeck_Electrical_conductivity(cursor, table_name):
    try:
        type = input("Select type p/n: ").lower()
        if type == 'p':
            symbol = '>'
        elif type == 'n':
            symbol = '<'
        else:
            print("Wrong command...")
            return None

        show_temperature = "SELECT DISTINCT `Temperature(K)` from `{}` ORDER BY `Temperature(K)` ASC;".format(table_name)
        cursor.execute(show_temperature)
        temperatures = cursor.fetchall()
        print("Choose temperature:")
        for temp in temperatures:
            print(temp)

        command = input()
        select_rows = "SELECT `id`, `Formula`, `Seebeck_coefficient(μV/K)`, `Electrical_conductivity(S/m)`, `ZT` FROM `{}` WHERE `Temperature(K)` = '{}' AND `Seebeck_coefficient(μV/K)` {} '0';".format(table_name, command, symbol)
        cursor.execute(select_rows)
        data = cursor.fetchall()
        return data

    except Exception as ex:
        print(ex)


def graph_ZT_from_compound(cursor, table_name):
    try:
        type = input("Select type p/n: ").lower()
        if type == 'p':
            symbol = '>'
        elif type == 'n':
            symbol = '<'
        else:
            print("Wrong command...")
            return None

        select_rows = "SELECT `id`, `Formula`, `ZT`, `Temperature(K)` FROM `{}` WHERE `Seebeck_coefficient(μV/K)` {} '0';".format(table_name, symbol)
        cursor.execute(select_rows)
        data = cursor.fetchall()
        compound = {}
        for row in data:
            temp = parse(row['Formula'])
            for i in range(len(temp)):
                if compound.get(temp[i]) is not None:
                    compound[temp[i]].append({"ZT": row["ZT"], "Formula": row["Formula"], "Temperature(K)": row["Temperature(K)"]})
                else:
                    compound[temp[i]] = []
                    compound[temp[i]].append({"ZT": row["ZT"], "Formula": row["Formula"], "Temperature(K)": row["Temperature(K)"]})

        return compound
    except Exception as ex:
        print(ex)


def graph_Parameters_from_temperature(cursor, table_name):
    try:
        Formula = input("Write formula without coefficients (for example: H2O -> HO): ")
        Formula = parse(Formula)
        Formula = "%".join(Formula)
        show_compound_rows = "SELECT DISTINCT `Formula` FROM `{}` WHERE `Formula` LIKE '%{}%';".format(table_name, Formula)
        cursor.execute(show_compound_rows)
        compounds = cursor.fetchall()
        print("Choose one:")
        for compound in compounds:
            print(compound)
        Formula = input()

        upload_parameters = "SELECT * FROM `{}` WHERE `Formula` = '{}' ORDER BY `Temperature(K)` ASC;".format(table_name, Formula)
        cursor.execute(upload_parameters)
        data = cursor.fetchall()
        return data
    except Exception as ex:
        print(ex)


def parse(row):
    Formula = str(row)
    temp = ''
    data = []
    n = len(Formula)
    for i in range( n ):
        if Formula[i] >= "A" and Formula[i] <= "Z":
            if temp == '':
                temp = Formula[i]
            else:
                data.append(temp)
                temp = Formula[i]
        elif Formula[i] >= "a" and Formula[i] <= "z":
            temp += Formula[i]
        else:
            if temp != '':
                data.append(temp)
                temp = ''

        if i == n-1:
            if temp != '':
                data.append(temp)

    return data
