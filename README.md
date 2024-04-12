# Tesla Smart City Ride

The Tesla SmartRide project is designed as a real-time data streaming and visualization system, intended to monitor a Tesla vehicle on its journey from Seattle to Cupertino. Although the typical setup would involve using IoT devices to capture diverse data points like vehicle telemetry, GPS coordinates, weather updates, and emergency incidents along the route, this project adapts by simulating this data. This approach mimics real-time IoT data streams, allowing the system to still effectively gather and process information as if it were coming directly from actual devices installed in the vehicle. The data, once collected, is processed and visualized on-the-fly using an integrated suite of Apache and AWS technologies. This not only provides instant insights into the vehicle’s performance in self driving environment and trip dynamics but also enhances the capability to make informed decisions and responses to any incidents or environmental changes during the trip. This setup is ideal for testing and demonstrating the potential of real-time data applications in smart city projects, even without access to physical IoT devices.

![Pasted Graphic](https://github.com/TVR28/Tesla-SmartRide/assets/91713140/087d7dbf-ee01-4710-a81e-de4f004ce321)

## Table of Contents

- [System Architecture](#system-architecture)
- [Data Flow](#data-flow)
- [Installation and Configuration](#installation-and-configuration)
- [Application Details](#application-details)
- [Future Work](#future-work)
- [Contributing](#contributing)
- [License](#license)



## System Architecture
<img width="1251" alt="SYSTEM ARCHITECTURE" src="https://github.com/TVR28/Tesla-SmartRide/assets/91713140/e8aa6848-af5e-4e70-bad2-bc877b009f56">

## Components

## 1. IoT Devices:
   - IoT devices in the Tesla vehicles collect a myriad of data in real-time, which includes GPS tracking for location, various vehicle telemetry data to assess performance and condition, and emergency data to respond to critical situations promptly. These devices are crucial for gathering the raw data needed for further processing and insights.

## 2. Apache Zookeeper:
   - Apache Zookeeper plays a pivotal role in managing and synchronizing the distributed services within the ecosystem, specifically focusing on Kafka brokers. It helps maintain configuration information, naming, providing distributed synchronization, and providing group services to ensure that the Kafka cluster operates smoothly and consistently without data loss.

## 3. Apache Kafka:
   - Serving as the central hub for all data streams, Apache Kafka handles the ingestion of massive streams of data from multiple sources, including the IoT devices. It ensures efficient and reliable transfer of data between data producers (IoT devices) and data consumers (Apache Spark), capable of handling high-throughput and low-latency messaging.

## 4. Apache Spark:
   - Apache Spark consumes the data streamed by Kafka, processing it in real-time to perform complex analyses and calculations. The processed data is then pushed to AWS S3 for permanent storage. Spark's ability to handle live data streams makes it ideal for immediate data manipulation and aggregation needed in dynamic environments like smart cities.

## 5. AWS S3:
   - AWS S3 acts as the storage solution within the project, where all the processed data is stored. S3 provides a highly durable, scalable, and secure object storage which makes it perfect for storing large volumes of data that can be accessed and analyzed later for further insights.

## 6. AWS Glue and Data Catalog:
   - AWS Glue is used to extract, transform, and load (ETL) data from AWS S3 into usable formats for analysis. Along with the Data Catalog—a metadata storage system—it organizes data into catalogs and makes it searchable, and readily available for querying and analytics, bridging the gap between raw data storage and actionable insights.

## 7. AWS Redshift/Athena:
   - AWS Redshift and Athena serve as the data warehousing and querying solutions respectively. Redshift provides a fast, fully managed data warehouse that makes it simple and cost-effective to analyze all your data using standard SQL and your existing Business Intelligence tools. Athena allows users to directly query the data stored in S3 using SQL, thus making it easier to perform ad-hoc analysis.

## 8. Visualization Tools (PowerBI, Tableau, Looker Studio):
   - These tools are intended to be implemented to enable the visualization of the processed data into interpretable and interactive dashboards. PowerBI, Tableau, and Looker Studio can transform the structured data into visually appealing reports and dashboards that provide actionable insights, allowing stakeholders to make informed decisions based on the latest data.


## Data Flow

- Data simulated instead of IoT devices(since I doon't have one but would love to implement) in the Tesla is sent to Apache Kafka and monitored using Zookeeper.
- Apache Spark consumes this streaming data from Kafka.
- The processed data is stored in AWS S3.
- AWS Glue transforms and catalogs the data, making it available for querying.
- Data is loaded into AWS Redshift or queried through Athena for further analysis.
- Final data visualizations are prepared in BI tools like PowerBI, Tableau, or Looker Studio.

## Installation and Configuration

### Prerequisites

- Python 3.9.6
- Docker and Docker Compose installed
- An active AWS account
- Database Viewer like DBViewer or SQLiteViewer

### Setup Instructions

1. **Initial Setup**:
   Create `docker-compose.yml` to orchestrate Zookeeper and Kafka services:
   ```bash
   touch docker-compose.yml
   docker-compose up -d
   ```
   ![Screenshot 2024-04-08 at 2 14 31 PM](https://github.com/TVR28/Tesla-SmartRide/assets/91713140/c4bb8b55-0938-4077-9e9d-e701f6a4ac50)

2. **Create Spark Job Script:**
   ```bash
   touch jobs/spark-city.py
   ```
   
3. **Install Required Python Packages:**

   ```bash
   pip install confluent_kafka simplejson pyspark
   pip freeze > requirements.txt
   ```
   
4. **Run the Spark Application:**
   
   ```bash
   docker exec -it smartcity-spark-master-1 spark-submit \ --master spark://spark-master:7077 \ --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.apache.hadoop:hadoop-aws:3.3.1,com.amazonaws:aws-java-sdk:1.11.469 jobs/spark-city.py
   ```
5. **Monitoring the Application:**

   Access the Spark UI at `http://localhost:9090` to monitor the streaming process.

   ![spark](https://github.com/TVR28/Tesla-SmartRide/assets/91713140/3d290928-706a-452b-94a7-ae72cee7e880)

   


## Application Details
The Tesla SmartRide application is designed to gather and analyze data instantly, offering vital information about how the vehicle is performing, the best routes to take, and the current weather conditions. This is especially important for projects aimed at improving self driving assistance, city living, where making decisions based on accurate, up-to-date data can greatly enhance safety and operational efficiency. By processing this data in real time, the application helps ensure that both drivers and city planners have the insights they need to make informed decisions quickly, which is crucial in dynamic urban environments where conditions can change rapidly. This capability not only improves how well a vehicle operates on own but also contributes to broader smart city goals like enhanced and safe self driving capability and enhancing public safety.

## Data Management and Visualization with AWS and DB Viewer

Our Tesla SmartRide project's data management and visualization components are a testament to the seamless integration of various AWS services and sophisticated database tools. Each part of our system plays a pivotal role in transforming raw data into actionable insights.

### AWS Glue and Crawlers

In the AWS Glue console image, we see multiple data crawlers listed, each corresponding to different data sets such as emergency data, GPS data, and weather data. These crawlers automatically discover and catalog metadata from the stored data, making it easy to maintain a current schema and prepare for analysis.

![awsglue](https://github.com/TVR28/Tesla-SmartRide/assets/91713140/ce44bf7b-1464-48f3-867f-6104a84af395)

### Amazon S3 Data Storage

The images show the S3 bucket structure, organizing data into folders corresponding to different data streams. Here, data is stored in the Parquet format, a columnar storage file format optimized for speed in analytics workloads. This structure demonstrates how data is segmented and stored for efficient access and analysis.

![weather_data_s3](https://github.com/TVR28/Tesla-SmartRide/assets/91713140/bbbc5332-7af8-4ac6-8153-3f3728673be5)

![s3-smartcity](https://github.com/TVR28/Tesla-SmartRide/assets/91713140/7ea1874e-9d93-493d-958c-b6ef97242bac)


### AWS Glue Data Catalog Tables

AWS Glue's Data Catalog provides a unified metadata repository across AWS services. The screenshot displays various tables created by the crawlers, now a part of the data catalog. These tables are used as sources or targets in ETL jobs and for query purposes, which enables streamlined data management and retrieval processes.

![awsgluetables](https://github.com/TVR28/Tesla-SmartRide/assets/91713140/d24521f3-e136-46eb-9f27-98733ed4f984)

### Database Viewer with DBeaver

DBeaver, a powerful DB viewer, is depicted showing a detailed view of the `emergency_data` table. It allows us to query and manipulate the data visually, making it easier to perform complex SQL queries and data analysis. This database viewer serves as an interface between the user and the stored data, which could be in Redshift or another database system, for comprehensive data investigation and manipulation.

![dbeaver](https://github.com/TVR28/Tesla-SmartRide/assets/91713140/a13f5520-d9d0-4d58-9643-14aede6a6d8b)


## Future Work
- Implementing the visualization layer using PowerBI, Tableau, or Looker Studio.
- Enhancing data processing and analysis features.

## Contributing
Interested in contributing? Great! Here are a few areas where you can help:

- **Data Visualization:** Implement the visualization layer using PowerBI, Tableau, or Looker Studio.
- **Adding new features:** Have an idea for an improvement? Fork the repo, make your updates, and submit a pull request.
- **Bug fixes:** Noticed a problem? Open an issue or submit a fix.
- **Documentation:** Help keep our docs up to date and clear.

For major changes, please open an issue first to discuss what you would like to change.

