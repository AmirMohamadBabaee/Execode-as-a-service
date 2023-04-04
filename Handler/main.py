from typing import Union
from typing_extensions import Annotated
from fastapi import FastAPI, File, UploadFile, Body, Response, status
from utils.db import DatabaseHandler
from utils.s3 import S3Handler
from utils.rabbitmq import RabbitMQHandler


app = FastAPI()

@app.post("/upload")
def upload(file: UploadFile, 
           email: Annotated[str, Body()], 
           language: Annotated[str, Body()],
           response: Response,
           inputs: Annotated[str, Body()] = ""):
    try:
        s3_handler = S3Handler()
        db_handler = DatabaseHandler()
        contents = file.file.read()
        upload_id = db_handler.insert_uploads(email, 
                                              inputs, 
                                              language)
        s3_handler.store(body=contents, filename=f"{upload_id}")
    except Exception:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    response.status_code = status.HTTP_200_OK
    return {"upload_id": upload_id, "message": f"Successfully uploaded {file.filename} to S3"}

@app.post("/run")
def run(upload_id: int,
        response: Response):
    if not upload_id:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message":"`upload_id` does not found in request body"}
    try:
        db_handler = DatabaseHandler()
        row = db_handler.find('UPLOADS', row_id=upload_id)
        print
        if row and row['enable'] == 0:
            with RabbitMQHandler() as rabbitmq_handler:
                rabbitmq_handler.publish_on_queue(upload_id)
                return {"message": f"`upload_id`={upload_id} added to queue to execute"}
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": f"`upload_id`={upload_id} not found"}
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": "There was an error in running file"}
