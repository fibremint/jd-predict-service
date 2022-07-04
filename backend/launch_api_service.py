import os

from decouple import config
import uvicorn

from util import get_project_root


if __name__ == '__main__':
    os.environ['JD_SERVICE_PATH'] = get_project_root()

    uvicorn.run('app.api:app',
                host=config('API_EXPOSE_HOST_ADDR'), 
                port=int(config('API_EXPOSE_PORT')),
                reload=True)
