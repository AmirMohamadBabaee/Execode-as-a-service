import os
import sys
from urllib import parse

sys.path.append('/mnt/d/Semester 8/Cloud Javadi/HW/HW1/code/')
from Handler.utils.rabbitmq import RabbitMQHandler
from Handler.utils.db import DatabaseHandler
from Handler.utils.s3 import S3Handler
print(sys.path)

def main():
    rabbitmq_handler = RabbitMQHandler()

    def callback(ch, method, properties, body):
        upload_id = int(body.decode('utf-8'))
        print(f" [x] Received {upload_id}")

        s3_handler = S3Handler()
        with DatabaseHandler() as db_handler:
            row = db_handler.find('UPLOADS', row_id=upload_id)
            s3_handler.download(filename=f"{upload_id}")
            if row:
                data = {
                    'code': s3_handler.read_file(f'{upload_id}'),
                    'language': row['language'], 
                    'input': row['inputs']
                }
                query_str = parse.urlencode(data)
                job_id = db_handler.insert_jobs(upload_id=upload_id,
                                                job=query_str)
                db_handler.insert_results(job_id=job_id)

    print('[*] Waiting for messages. To exit press CTRL+C')
    rabbitmq_handler.consume_on_queue(callback=callback)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)