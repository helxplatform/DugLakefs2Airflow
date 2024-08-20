# DugLakefsEventListeners

The purpose of this project is to add ability custom python code that can be triggered from LakeFS.

Structure:

      main.py - flask server that exposes different endpoints
      /test folder contains sample requests that invoke endpoints
      /data folder contains list of json config files for each endpoint
      /helm helm chart for deploying on kubernetes  


Currently supported endpoints:

      /invoke_airflow_with_diff

It supports POST requests and listens for coming requests from LakeFS on `post-create-tag` event. It will invoke Airflow API to run a specified dag and supply dag with following parameters:


     repository_id
     branch_name
     commitid_from
     commitid_to 

If Airflow API returns status code 200, then commitid_to saved to 
`invoke_airflow_with_diff_config.json` in last_commit_id field.

invoke_airflow_with_diff_config.json contains information about dags, which each endpoint call will trigger and provide parameters for requests:

    {
        "dags": [
            {
                "dag_id": "dag_id1",
                "repository_id": "repo1",
                "branch_name": "branch1",
                "last_commit_id": "cad1136eb748603c3379cda715d23422126af9ae6ebd541a52e28c61011bd57c"
            }
        ]
    }


Helm chart requires Airflow.url to be updated in Values file according to your setup.
