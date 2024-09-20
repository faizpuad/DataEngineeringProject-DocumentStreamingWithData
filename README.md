# Credit Card Fraud Transaction as Document Streaming Practice

## Introduction & Goals
This project is focused on practicing document streaming using a simulated dataset of credit card transactions obtained from Kaggle. The dataset covers legitimate and fraudulent transactions from 1st January 2019 to 31st December 2020, including 1000 customers and transactions across 800 merchants. The goal is to stream, process, and analyze this data to practice core data engineering tasks using modern tools and technologies such as Python, Kafka, Spark, and MongoDB.

The main objectives of the project are:
- To simulate the data engineering pipeline, covering stages from data extraction to storage and visualization.
- To implement real-time data streaming and batch processing, using tools such as Kafka for message buffering and Spark for data processing.
- To apply data storage techniques using MongoDB, focusing on handling unstandardized datetime formats and ensuring data validation through Pydantic.

Once the pipeline is established, the processed data can be used for analytical purposes, such as identifying fraudulent transactions, and the results will be visualized using BI tools like Streamlit or PowerBI.

## Contents

- [The Data Set](#the-data-set)
- [Used Tools](#used-tools)
  - [Connect](#connect)
  - [Buffer](#buffer)
  - [Processing](#processing)
  - [Storage](#storage)
  - [Visualization](#visualization)
- [Pipelines](#pipelines)
  - [Stream Processing](#stream-processing)
    - [Storing Data Stream](#storing-data-stream)
    - [Processing Data Stream](#processing-data-stream)
  - [Batch Processing](#batch-processing)
  - [Visualizations](#visualizations)
- [Demo](#demo)
- [Conclusion](#conclusion)
- [Follow Me On](#follow-me-on)
- [Appendix](#appendix)

## The Data Set
The dataset chosen is a simulated credit card fraud dataset from Kaggle. It contains both legitimate and fraudulent transactions, and includes a wide range of attributes such as transaction time, merchant details, customer information, and fraud flags. I selected this dataset because it offers a comprehensive view of typical transactional data and has a clear target variable (`is_fraud`) for classification tasks.

| **Attribute**              | **Description**                        |
|----------------------------|----------------------------------------|
| `index`                    | Unique Identifier for each row         |
| `trans_date_trans_time`     | Transaction DateTime                   |
| `cc_num`                   | Credit Card Number of Customer         |
| `merchant`                 | Merchant Name                          |
| `category`                 | Merchant Category                      |
| `amt`                      | Transaction Amount                     |
| `first, last`              | Name of Credit Card Holder             |
| `is_fraud`                 | Fraud Flag (Target Variable)           |

This dataset provides an ideal setting for experimenting with data streaming, real-time fraud detection, and data processing.

## Used Tools
The project leverages several key technologies:

- **Python**: Used for data extraction, transformation, and scripting.
- **Kafka**: Acts as a buffer, allowing streaming data to be processed in real-time. Producers push transaction data, and consumers read and process the messages.
- **Spark**: Processes data from Kafka and transforms it into usable JSON for storage.
- **MongoDB**: Stores the processed data, which is well-suited for storing JSON documents.
- **Pydantic**: Used for data validation in the API layer, ensuring correct data types and formats.
- **BI Tool**: For visualization, either Streamlit or PowerBI will be used to present analytical results.

### Connect
Python scripts are used to extract data from CSV, convert each row into JSON format, and send it to an API endpoint for further processing.

### Buffer
Kafka is used to handle real-time streaming. A Kafka topic is set up, where the API acts as the producer, and Spark consumes the data for further processing.

### Processing
Spark processes the raw data from Kafka, converting unstructured or single-line text into proper JSON objects. Data cleaning and transformations, such as standardizing date formats, are performed at this stage.

### Storage
MongoDB is the chosen NoSQL database due to its ability to efficiently store JSON documents. Two collections are created: one for test data and one for training data.

### Visualization
A BI tool like Streamlit or PowerBI will be used for visualizing the stored data, with a focus on detecting fraud patterns and summarizing transaction insights.

## Pipelines
This project builds two main pipelines: one for real-time stream processing and another for batch processing.

### Stream Processing
- **Storing Data Stream**: Transaction data is streamed into Kafka topics, where each transaction is pushed in real-time.
- **Processing Data Stream**: Spark consumes the Kafka data stream, processes it, and sends the transformed data to MongoDB.

### Batch Processing
Batch processing will also be implemented to process large chunks of data at scheduled intervals, complementing the real-time stream.

### Visualizations
Visualizations will be created to monitor transaction patterns and detect anomalies using a BI tool.

## Demo
A demo video or presentation link will be provided to showcase the project.

## Conclusion
This project demonstrates the end-to-end process of document streaming and real-time data processing, from data extraction to storage and visualization. Key learnings include the effective use of Kafka for streaming, Spark for processing, and MongoDB for storing JSON data. The biggest challenge was handling unstandardized datetime formats and ensuring the correctness of real-time data flow.

## Follow Me On
[LinkedIn](https://www.linkedin.com/in/faizpuad/)

## Appendix
[Kaggle Dataset](https://www.kaggle.com/datasets/kartik2112/fraud-detection?select=fraudTrain.csv)
