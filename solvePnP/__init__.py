import logging

import azure.functions as func
import json
import base64
from src.Camera import Camera

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    data = req.params.get('data')

    if not data:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            data = req_body.get('data')

    if data:
        data = json.loads(base64.b64decode(data).decode('utf-8'))
        config = data['config']
        
        camera = Camera(config)
        camera_position,rotM = camera.camera_position()

        output = dict()
        output['rotM'] = str(rotM)
        output['camera_position'] = str(camera_position)

        return func.HttpResponse(f"{output}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

