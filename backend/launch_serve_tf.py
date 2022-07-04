import os

from decouple import config
import uvicorn

from util import get_project_root


if __name__ == '__main__':
    os.environ['JD_SERVICE_PATH'] = get_project_root()

    uvicorn.run('app.serve_tf:app',
                host=config('SERVE_TF_MODEL_EXPOSE_HOST_ADDR'), 
                port=int(config('SERVE_TF_MODEL_EXPOSE_PORT')),
                reload=False)
