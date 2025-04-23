FROM bitnami/spark:3.5.0

USER root

RUN pip install pyspark kafka-python cassandra-driver

WORKDIR /app

COPY app/ .

CMD ["spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,com.datastax.spark:spark-cassandra-connector_2.12:3.2.0", "spark_job.py"]
