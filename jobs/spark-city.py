import config
from pyspark.sql import SparkSession, DataFrame
from config import configuration
from pyspark.sql.types import StructField, StructType, StringType, TimestampType, DoubleType, IntegerType
from pyspark.sql.functions import from_json, col

def main():
    spark = SparkSession.builder.appName("TeslaSmartCityStreaming ")\
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.0", 
            "org.apache.hadoop:hadoop-aws:3.3.1",
            "com.amazonaws:aws-java-sdk:1.11.469")\
    .config("spark.hadoop.f2.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")\
    .config("spark.hadoop.f2.s3a.access.key", configuration.get('AWS_ACCESS_KEY'))\
    .config("spark.hadoop.f2.s3a.access.key", configuration.get('AWS_SECRET_KEY'))\
    .config('spark.hadoop.f2.s3a.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.impl.SimpleAWSCredentialsProvider')\
    .getOrCreate()
    
    #Adjust the log level to minimize the console output on executors
    spark.sparkContext.setLogLevel('WARN')
    
    #Vehicle schema
    vehicleSchema = StructType([
        StructField("id", StringType(), True),
        StructField("deviceId", StringType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("location", StringType(), True),
        StructField("speed", DoubleType(), True),
        StructField("direction", StringType(), True),
        StructField("make", StringType(), True),
        StructField("model", StringType(), True),
        StructField("year", IntegerType(), True),
        StructField("fuelType", StringType(), True)
    ])
    
    #GPS Schema
    gpsSchema = StructType([
        StructField("id", StringType(), True),
        StructField("deviceId", StringType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("speed", DoubleType(), True),
        StructField("direction", StringType(), True),
        StructField("VehicleType", StringType(), True)
    ])
    
    #Traffic Schema
    trafficSchema = StructType([
        StructField("id", StringType(), True),
        StructField("deviceId", StringType(), True),
        StructField("cameraId", StringType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("location", StringType(), True),
        StructField("snapshot", StringType(), True)
    ])
    
    #Weather Schema
    weatherSchema = StructType([
        StructField("id", StringType(), True),
        StructField("deviceId", StringType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("location", StringType(), True),
        StructField("temperature", DoubleType(), True),
        StructField("weatherCondition", StringType(), True),
        StructField("precipitation", DoubleType(), True),
        StructField("windspeed", DoubleType(), True),
        StructField("humidity", IntegerType(), True),
        StructField("airQualityIndex", DoubleType(), True)
    ])
    
    #Emergency Data Schema
    emergencySchema = StructType([
        StructField("id", StringType(), True),
        StructField("deviceId", StringType(), True),
        StructField("incidentId", StringType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("location", StringType(), True),
        StructField("type", StringType(), True),
        StructField("status", StringType(), True),
        StructField("description", StringType(), True)
    ])
    
    def read_kafka_topic(topic, schema):
        return (spark.readStream
                .format('kafka')
                .option('kafka.bootstrap.servers', 'broker:29092')
                .option('subscribe', topic)
                .option('startingOffsets', 'earliest')
                .load()
                .selectExpr('CAST(value AS STRING)')
                .select(from_json(col('value'), schema).alias('data'))
                .select('data.*')
                .withWatermark('timestamp', '2 minutes') #delayed threshold is 2 min - max delay
                )
    
    vehicleDF = read_kafka_topic('vehicle_data', vehicleSchema).alias('vehicle')
    gpdDF = read_kafka_topic('gps_data', gpsSchema).alias('gps')
    trafficDF = read_kafka_topic('traffic_data', trafficSchema).alias('traffic')
    weatherDF = read_kafka_topic('weather_data', weatherSchema).alias('weather')
    emergencyDF = read_kafka_topic('emergency_data', emergencySchema).alias('emergency')
    
    #join all the dfs with id and timestamps
    #join
    
    query1 = streamWriter(vehicleDF, 's3a://spark-streaming/checkpoints/vehicle_data',
                's3a://spark-streaming-data/data/vehicle_data')
    query2 = streamWriter(gpdDF, 's3a://spark-streaming/checkpoints/gps_data',
                's3a://spark-streaming-data/data/gps_data')
    query3 = streamWriter(trafficDF, 's3a://spark-streaming/checkpoints/traffic_data',
                's3a://spark-streaming-data/data/traffic_data')
    query4 = streamWriter(weatherDF, 's3a://spark-streaming/checkpoints/weather_data',
                's3a://spark-streaming-data/data/weather_data')
    query5 = streamWriter(emergencyDF, 's3a://spark-streaming/checkpoints/emergency__data',
                's3a://spark-streaming-data/data/emergency__data')
    
    query5.awaitTermination() # Running parallel and concurrrently
    
    def streamWriter(input: DataFrame, checkpointFolder, output):
        return(input.writeStream
                .format('paruet')
                .option('checkpointLocation', checkpointFolder)
                .option('path', output)
                .outputMode('append')
                .start())
    
    
    
if __name__ == "__main__":
    main()
