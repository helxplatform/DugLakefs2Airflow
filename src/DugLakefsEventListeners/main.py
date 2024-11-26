import json
import logging
import os
import requests

from flask import Flask, request, jsonify

INVOKE_AIRFLOW_WITH_DIFF = "invoke_airflow_with_diff"
AIRFLOW_URL = "http://airflow:airflow@127.0.0.1:8080/api/v1/"

app = Flask(__name__)


def invoke_airflow_dag(dag_id, repository_id, branch_name, last_commit_id, new_commit_id) -> bool:

    params = \
        {
            'conf':
                  {
                      'repository_id': repository_id,
                      'branch_name': branch_name,
                      'commitid_from' : last_commit_id,
                      'commitid_to' : new_commit_id
                  }
        }
    url = AIRFLOW_URL + f"dags/{dag_id}/dagRuns"
    logging.info("Calling Airflow DAG {}".format(dag_id))
    logging.info("Url: {}".format(url))
    logging.info("Params: {}".format(params))
    resp = requests.post(url, json=params)
    logging.info(resp.json())
    if resp.status_code == 200:
        return True
    else:
        return False


@app.route('/' + INVOKE_AIRFLOW_WITH_DIFF, methods=["POST"])
def invoke_airflow_with_diff():
    input_data = request.json
    logging.info(INVOKE_AIRFLOW_WITH_DIFF)
    logging.info(input_data)

    config = {}
    config_json = f"./data/{INVOKE_AIRFLOW_WITH_DIFF}_config.json"

    if not os.path.isfile(config_json):
        logging.error(f"{config_json} not found!")
        output_data = {'status': 'error'}
        return jsonify(output_data)

    with open(config_json, "r") as f:
        config = json.load(f)

    repository_id = input_data["repository_id"]
    source_ref = input_data["source_ref"]

    dags = config["dags"]

    for dag in dags:
        if dag["repository_id"] == repository_id:
            res = invoke_airflow_dag(dag["dag_id"], repository_id, dag["branch_name"], dag["last_commit_id"], source_ref)
            if res:
                dag["last_commit_id"] = source_ref

    with open(config_json, "w") as f:
        json.dump(config, f, indent=4)

    output_data = {'status': 'OK'}
    return jsonify(output_data)

if __name__ == '__main__':
    AIRFLOW_URL = os.environ.get("AIRFLOW_URL", AIRFLOW_URL)
    app.debug = True
    app.run(host='0.0.0.0', port=8001)