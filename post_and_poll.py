import requests
import json
import ast
from logger import log
from results_poller import poller

results_file = 'results.json'
API_KEY = 'my_API_KEY'  # REPLACE WITH YOUR API KEY


root_url = 'https://developer.nrel.gov/api/reopt'
post_url = f'{root_url}/v1/job/?api_key={API_KEY}'
results_url = f'{root_url}/v1/job/<run_uuid>/results/?api_key={API_KEY}'

post = json.load(open('Scenario_POST.json'))

resp = requests.post(post_url, json=post)

if not resp.ok:
    log.error(f"Status code {resp.status_code}. {resp.content}")
else:
    log.info(f"Response OK from {post_url}.")

    run_id_dict = ast.literal_eval(resp.content)

    try:
        run_id = run_id_dict['run_uuid']
    except KeyError:
        msg = f"Response from {post_url} did not contain run_uuid."
        log.error(msg)
        raise KeyError(msg)

    results = poller(url=results_url.replace('<run_uuid>', run_id))

    with open(results_file, 'wb') as fp:
        json.dump(obj=results, fp=fp)

    log.info(f"Saved results to {results_file}")
