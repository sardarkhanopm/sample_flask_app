import traceback
# from uuid import uuid4
from flask import current_app as app
from flask import request, jsonify, Response
from . import logger
from .snowflake_connector import SnowFlake
from .tasks import long_running_task_celery
ANOTHER_TASK_RUNNING_MSG = "Currently another task is in progress. Please wait for it complete"


def custom_response(status_code: int, message: str | None, output: dict | None,
                    success: bool, **kwargs) -> tuple[Response, int]:
    # sourcery skip: merge-dict-assign
    response = dict()
    response['status_code'] = status_code
    response['message'] = message
    response['output'] = output
    response['success'] = success
    for key in kwargs:
        response[key] = kwargs[key]
    return jsonify(response), status_code


@app.route("/list_databases", methods=["GET"])
def list_databases() -> custom_response:
    try:
        query_params = request.args
        if 'connection_id' in query_params:
            connection_id = query_params['connection_id']
        elif 'connection_name' in query_params:
            connection_id = query_params['connection_name']
        external = bool(query_params.get("external", False))
        snowflake = SnowFlake(connection_id=connection_id, external=external)
        con = snowflake.connect()
        if con is None:
            raise ConnectionError(f"No Connection With {connection_id=}")
        database_list = snowflake.get_database_list()
    except Exception as exp:
        logger.exception(traceback.format_exc())
        return custom_response(status_code=500, message=str(exp), success=False, output=None)
    return custom_response(status_code=200, message=None, success=True, output=database_list)


@app.route("/long_running_task", methods=["POST"])
def long_running_task() -> custom_response:
    try:
        query_params = request.json
        connection_id = query_params['connection_id']
        kwargs = {'connection_id': connection_id}
        long_running_task_celery.apply_async(
            (), kwargs=kwargs, queue='long_running_queue')
    except Exception as exp:
        logger.exception(traceback.format_exc())
        return custom_response(status_code=500, message=str(exp), success=False, output=None)
    return custom_response(status_code=200, message="long running task started started", success=True, output=None)
