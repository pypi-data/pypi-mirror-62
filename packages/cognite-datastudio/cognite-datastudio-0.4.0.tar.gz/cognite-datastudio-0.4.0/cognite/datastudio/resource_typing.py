import math
import time
from typing import List, Union

from typing_extensions import TypedDict

from cognite.client.data_classes._base import CogniteResource, CogniteResourceList
from cognite.datastudio.exceptions import ModelFailedException


def request(client, path, request_type, data=None):
    project = client._config.project
    url = f"/api/playground/projects/{project}/context/resource_typing{path}"
    if request_type == "GET":
        response = client._api_client._get(url)
    else:
        response = client._api_client._post(url, json=data, headers={"Content-Type": "application/json"})

    return response


class TypingFitData(TypedDict):
    data: List[str]
    target: str


class TypingPredictData(TypedDict):
    data: List[str]


def convert_nan_to_empty_string_in_list(strings: List[str]):
    for i, string in enumerate(strings):
        if isinstance(string, float) and math.isnan(string):
            strings[i] = ""


class ResourceTypingModel(CogniteResource):
    def __init__(self, model_id=None, status=None, error_message: str = None, cognite_client=None):
        self.model_id = model_id
        self.status = status
        self._cognite_client = cognite_client
        self.error_message = error_message

    def __repr__(self):
        return "Model(id: %d,status: %s)" % (self.model_id, self.status)

    def predict(self, y: List[TypingPredictData]):
        y = list(y)
        for entities in y:
            convert_nan_to_empty_string_in_list(entities["data"])

        response = request(self._cognite_client, f"/{self.model_id}/predict", "POST", data={"items": y})
        data = response.json()
        job_id = data["jobId"]
        while data["status"] != "Completed":
            response = request(self._cognite_client, f"/{self.model_id}/predict/{job_id}", "GET")
            data = response.json()
            if data["status"] == "Failed":
                raise ModelFailedException(f"model_id: {self.model_id} error: {data.get('errorMessage')}")
            time.sleep(1)
        return data["items"]


class ResourceTypingModelList(CogniteResourceList):
    _RESOURCE = ResourceTypingModel
    _ASSERT_CLASSES = False


class ResourceTyping:
    def __init__(self, client):
        self.client = client

    def fit(
        self, items: List[TypingFitData], algorithm="open_set_nearest_neighbors", targets_to_classify: List[str] = None
    ):
        items = list(items)
        for entities in items:
            convert_nan_to_empty_string_in_list(entities["data"])
        json = {"items": items, "algorithm": algorithm}
        if targets_to_classify:
            json["targetsToClassify"] = targets_to_classify  # we don't like nulls
        response = request(self.client, "/fit", "POST", data=json)

        data = response.json()
        model_id = data["modelId"]
        while data["status"] != "Completed":
            response = request(self.client, f"/{model_id}", "GET")
            data = response.json()
            if data["status"] == "Failed":
                raise ModelFailedException(f"model_id: {model_id} error: {data.get('errorMessage')}")
            time.sleep(1)
        return ResourceTypingModel(
            model_id=model_id,
            status=data["status"],
            error_message=data.get("error_message"),
            cognite_client=self.client,
        )

    def retrieve(self, model_id: int) -> ResourceTypingModel:
        response = request(self.client, f"/{model_id}", "GET")
        return ResourceTypingModel._load(response.json())

    def list(self) -> ResourceTypingModelList:
        response = request(self.client, "/", "GET")
        return ResourceTypingModelList._load(response.json()["items"])

    def delete(self, model_id: Union[list, int]):
        if not isinstance(model_id, (list, ResourceTypingModelList)):
            model_id = [model_id]
        model_id = [m.model_id if isinstance(m, ResourceTypingModel) else m for m in model_id]
        request(self.client, "/delete", "POST", data={"items": [{"modelId": id} for id in model_id]})
