from aiohttp import web
import json
from .utils import read_body
import asyncio
from ..data.postgres_async_db import AsyncPostgresDB


class MetadataApi(object):
    _metadata_table = None
    lock = asyncio.Lock()

    def __init__(self, app):
        app.router.add_route(
            "GET",
            "/flows/{flow_id}/runs/{run_number}/steps/{step_name}/"
            "tasks/{task_id}/metadata",
            self.get_metadata,
        )
        app.router.add_route(
            "GET",
            "/flows/{flow_id}/runs/{run_number}/metadata",
            self.get_metadata_by_run,
        )
        app.router.add_route(
            "POST",
            "/flows/{flow_id}/runs/{run_number}/steps/{step_name}/"
            "tasks/{task_id}/metadata",
            self.create_metadata,
        )

        self._async_table = AsyncPostgresDB.get_instance().metadata_table_postgres

    async def get_metadata(self, request):
        """
        ---
        description: get all metadata associated with the specified task.
        tags:
        - Metadata
        parameters:
        - name: "flow_id"
          in: "path"
          description: "flow_id"
          required: true
          type: "string"
        - name: "run_number"
          in: "path"
          description: "run_number"
          required: true
          type: "integer"
        - name: "step_name"
          in: "path"
          description: "step_name"
          required: true
          type: "string"
        - name: "task_id"
          in: "path"
          description: "task_id"
          required: true
          type: "integer"
        produces:
        - text/plain
        responses:
            "200":
                description: successful operation
            "405":
                description: invalid HTTP Method
        """
        flow_name = request.match_info.get("flow_id")
        run_number = request.match_info.get("run_number")
        step_name = request.match_info.get("step_name")
        task_id = request.match_info.get("task_id")
        metadata_response = await self._async_table.get_metadata(
            flow_name, run_number, step_name, task_id
        )
        return web.Response(
            status=metadata_response.response_code,
            body=json.dumps(metadata_response.body),
        )

    async def get_metadata_by_run(self, request):
        """
        ---
        description: get all metadata associated with the specified run.
        tags:
        - Metadata
        parameters:
        - name: "flow_id"
          in: "path"
          description: "flow_id"
          required: true
          type: "string"
        - name: "run_number"
          in: "path"
          description: "run_number"
          required: true
          type: "integer"
        produces:
        - text/plain
        responses:
            "200":
                description: successful operation
            "405":
                description: invalid HTTP Method
        """
        flow_name = request.match_info.get("flow_id")
        run_number = request.match_info.get("run_number")
        metadata_runs = await self._async_table.get_metadata_in_runs(
            flow_name, run_number
        )
        return web.Response(
            status=metadata_runs.response_code, body=json.dumps(metadata_runs.body)
        )

    async def create_metadata(self, request):
        """
        ---
        description: persist metadata
        tags:
        - Metadata
        parameters:
        - name: "flow_id"
          in: "path"
          description: "flow_id"
          required: true
          type: "string"
        - name: "run_number"
          in: "path"
          description: "run_number"
          required: true
          type: "integer"
        - name: "step_name"
          in: "path"
          description: "step_name"
          required: true
          type: "string"
        - name: "task_id"
          in: "path"
          description: "task_id"
          required: true
          type: "integer"
        - name: "body"
          in: "body"
          description: "body"
          required: true
          schema:
            type: array
            items:
                type: object
                properties:
                    field_name:
                        type: string
                    value:
                        type: string
                    type:
                        type: string
                    user_name:
                        type: string
                    tags:
                        type: object
                    system_tags:
                        type: object
        produces:
        - 'text/plain'
        responses:
            "202":
                description: successful operation.
            "405":
                description: invalid HTTP Method
        """
        flow_name = request.match_info.get("flow_id")
        run_number = request.match_info.get("run_number")
        step_name = request.match_info.get("step_name")
        task_id = request.match_info.get("task_id")

        body = await read_body(request.content)
        count = 0
        for datum in body:
            values = {
                "flow_id": flow_name,
                "run_number": run_number,
                "step_name": step_name,
                "task_id": task_id,
                "field_name": datum.get("field_name", " "),
                "value": datum.get("value", " "),
                "type": datum.get("type", " "),
                "user_name": datum.get("user_name"),
                "tags": datum.get("tags"),
                "system_tags": datum.get("system_tags"),
            }
            metadata_response = await self._async_table.add_metadata(**values)
            if metadata_response.response_code == 200:
                count = count + 1

        result = {"metadata_created": count}

        return web.Response(body=json.dumps(result))
