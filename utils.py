import pymysql

def store_metric_to_db(metric_name, source_ip, destination_ip, metric_value):

    if metric_name != "delay" and metric_name != "rtt":
        print("Error, metric_name is invalid")
        return

    connection = pymysql.connect('s4', "admin", "homework5", "orangedb")

    try:

        with connection.cursor() as cursor:

            sql = ("INSERT INTO {table} (source_ip, destination_ip, metric) VALUES (%s, %s, %s)").format(table=metric_name)
            result = cursor.execute(sql, (source_ip, destination_ip, metric_value))
            connection.commit()

        if result:
            print("Succes")
            print(metric_name, source_ip, destination_ip, metric_value)
        else:
            print("Error")

    finally:
        connection.close()



# store_metric_to_db("delay", "172.20.20.10", "172.20.20.13", 1.6)
