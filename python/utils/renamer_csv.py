import os
import shutil


def rename_csv():
    SPARK_RESULT_DIR = os.environ['SPARK_RESULT_DIR']
    SPARK_PRETTY_OUT_DIR = os.environ['SPARK_PRETTY_OUT_DIR']

    if not os.path.exists(SPARK_PRETTY_OUT_DIR):
        os.makedirs(SPARK_PRETTY_OUT_DIR)

    for root, dirs, files in os.walk(SPARK_RESULT_DIR):
        for file in files:
            if file.endswith('.csv'):
                new_name = root.split('/')[-1]
                shutil.copy(f'{root}/{file}', f'{SPARK_PRETTY_OUT_DIR}/{new_name}.csv')
