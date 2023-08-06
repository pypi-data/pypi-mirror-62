# OAPI2MOCKSERVER

## What does it do
It creates expectations for mockserver based on an OpenAPI2 yaml.

If no scenarios are provided, it creates expectations for all endpoints with the first status-code defined. If example values are given in contract, these values will be used for response body.

If scenarios are provided, they must match the defined endpoints in the OpenAPI2 file.

## Usage
start a mockserver:
`docker run -it --rm -P jamesdbloom/mockserver`

Create expectations:
`oapi2mockserver mock localhost:<port_of_mockserver_docker_container> <path_to_open_api_2_contract_yaml>`

### Scenario Parameter
`-s` json of scenarios to push to the mockserver

**Example:**
`oapi2mockserver mock localhost:32768 foo.yaml -s '{"scenarios":[["\/v1\/foo\/{id}","get","200", "{\"foo\":\"bar\"}", "application/json"]]}'`

This pushes one scenario to mockserver with path `/v1/foo/{id}`, operation `get`, expected status-code `200`, expected response-body `{"foo":"bar"}` and expected response Content-Type header `application/json`

Response-Body and Content-Type are optional and will be generated out of the contract if not given.
If the Response-Body is a json, it will be validated against the schema defined in the contract before the scenario will be send to mock-server.
Also the Content-Type header needs to be defined in [produces part](https://swagger.io/docs/specification/2-0/mime-types/) of contract before the scenario will be send to mock-server.

## Development
run current development state:

- cd into package root directory
- install dependencies with `pip3 install -r requirements.txt` (just before first run or after adding new dependencies)
- run `python3 run.py mock <url_to_mockserver> <path_to_open_api_2_contract_yaml>`

### Tests
cd into package root directory and run `python3 -m unittest discover -s tests -v`

### Build
cd into package root directory and run `pip3 install ./`

### Upload to pypi.org
**WARNING: This will overwrite the current version on pypi.org!** 

raise version in `setup.py`, then run ./upload
