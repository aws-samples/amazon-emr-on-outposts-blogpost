import os
from pyspark.sql import SparkSession

if __name__ == "__main__":

    # ---------------------------------------------------------------------
    # Step 1: Get the database connection information from the EMR cluster 
    #         configuration
    dbconnection = os.environ.get('DBCONNECTION')
    #    Remove brackets
    dbconnection_info = (dbconnection[1:-1]).split(",")
    #    Initialize variables
    dbusername = ''
    dbpassword = ''
    dbhost = ''
    dbport = ''
    dbname = ''
    dburl = ''
    #    Parse the database connection information
    for dbconnection_attribute in dbconnection_info:
        (key_data, key_value) = dbconnection_attribute.split(":", 1)

        if key_data == "username":
            dbusername = key_value
        elif key_data == "password":
            dbpassword = key_value
        elif key_data == 'host':
            dbhost = key_value
        elif key_data == 'port':
            dbport = key_value
        elif key_data == 'dbname':
            dbname = key_value

    dburl = "jdbc:postgresql://" + dbhost + ":" + dbport + "/" + dbname

    # ---------------------------------------------------------------------
    # Step 2: Connect to the PostgreSQL database and select data from the 
    #         pg_catalog.pg_tables table
    spark_db = SparkSession.builder.config("spark.driver.extraClassPath",                                          
               "/opt/spark/postgresql/driver/postgresql-42.6.0.jar") \
               .appName("Connecting to PostgreSQL") \
               .getOrCreate()

    #    Connect to the database
    data_db = spark_db.read.format("jdbc") \
        .option("url", dburl) \
        .option("driver", "org.postgresql.Driver") \
        .option("query", "select count(*) from pg_catalog.pg_tables") \
        .option("user", dbusername) \
        .option("password", dbpassword) \
        .load()

    # ---------------------------------------------------------------------
    # Step 3: To do the data processing
    #
    #    TO-DO

    # ---------------------------------------------------------------------
    # Step 4: Save the data into the new table in the PostgreSQL database
    #
    data_db.write \
        .format("jdbc") \
        .option("url", dburl) \
        .option("dbtable", "results_proc") \
        .option("user", dbusername) \
        .option("password", dbpassword) \
        .save()

    # ---------------------------------------------------------------------
    # Step 5: Close the Spark session
    #
    spark_db.stop()
    # ---------------------------------------------------------------------
