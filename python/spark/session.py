from pyspark.sql import SparkSession
import pyspark.sql.functions as f
import time
import functools
import os

DATA_DIR = os.environ['DB_DATA_DIR']
DB_URL = os.environ['DB_URL']
DB_NAME = os.environ['DB_NAME']
DB_COLLECTION = os.environ['DB_COLLECTION']
SPARK_RESULT_DIR = os.environ['SPARK_RESULT_DIR']


def time_counter(function_class: str):
    def auxiliary_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f'---{function_class}---')
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            print('function [{}] finished in {} ms\n'.format(args[1] + '_counter', int(elapsed_time * 1_000)))
            return result

        return wrapper

    return auxiliary_decorator


class Session:
    def __init__(self, storage: str = DB_URL, output_dir: str = SPARK_RESULT_DIR):
        self.session = SparkSession.builder \
            .master('local') \
            .appName('JSON') \
            .config('spark.mongodb.input.uri', DB_URL + '/' + DB_NAME + '.' + DB_COLLECTION) \
            .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.1') \
            .getOrCreate()

        self.data_frame = self.session.read.format('mongo').option('uri',
                                                                   DB_URL + '/' + DB_NAME + '.' + DB_COLLECTION).load()

        self.storage = storage
        self.output_dir = output_dir

        self.single_value_fields = ['fork', 'language', 'has_issues', 'has_projects', 'has_downloads', 'has_wiki',
                                    'has_pages', 'has_discussions']
        self.star_value_fields = ['language', 'has_issues', 'has_projects', 'has_downloads', 'has_wiki',
                                  'has_pages', 'has_discussions']
        self.time_value_fields = ['language']

    @time_counter('single_field_count')
    def __count_single_field(self, field: str):
        self.data_frame.groupBy(field) \
            .agg(f.count(field).alias(field + '_count')) \
            .sort(field + '_count', ascending=False) \
            .write.format('csv').mode('overwrite').save(self.output_dir + '/' + field + '_count')

    def count_fields(self):
        for field in self.single_value_fields:
            self.__count_single_field(field)

    @time_counter('star-field_count')
    def __count_single_star_value_field(self, star_field: str):
        self.data_frame.groupby(star_field) \
            .agg(f.sum('stargazers_count').alias('stars')) \
            .sort('stars', ascending=False) \
            .write.format('csv').mode('overwrite').save(self.output_dir + '/' + 'star_' + star_field + '_count')

    def count_star_value_fields(self):
        for field in self.star_value_fields:
            self.__count_single_star_value_field(field)

    @time_counter('time-field_count')
    def __count_single_time_value_field(self, time_field):
        days = f.split(self.data_frame['created_at'], 'T')
        tmp_df = self.data_frame.withColumn('created_at_day', days.getItem(0))
        tmp_df.groupby('created_at_day', time_field) \
            .agg(f.count(time_field).alias(time_field + '_count')) \
            .sort('created_at_day', ascending=False) \
            .write.format('csv').mode('overwrite').save(self.output_dir + '/' + 'time_' + time_field + '_count')

    def count_time_value_fields(self):
        for field in self.time_value_fields:
            self.__count_single_time_value_field(field)

    def start(self):
        self.count_fields()
        self.count_star_value_fields()
        self.count_time_value_fields()
