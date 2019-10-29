import pprint

import requests

from config import server_url, access_token


class GoApiServer(object):
    headers = {}
    server = server_url
    app_versions = {
        "v1": "vnd.go.cd.v1+json"
    }

    def __init__(self):
        self.headers = self._auth()

    def _auth(self):
        return {'Authorization': 'bearer {}'.format(access_token)}

    def get_request_headers(self, api_version=None):
        req_headers = {}
        if api_version is not None:
            version_header = {'Accept': 'application/{}'.format(api_version)}
            print("VERSION_HEADER : {}".format(version_header))
            req_headers.update(version_header)
        return req_headers

    def go_request(self, endpoint, method="GET", api_version=None, data=None, extra_header=None):
        req_headers = self.headers
        if extra_header:
            req_headers.update(extra_header)
        request_url = "{}/go/api/{}".format(server_url, endpoint)
        req_headers.update(self.get_request_headers(api_version))

        if method == "GET":
            print(req_headers)
            return requests.get(url=request_url, headers=req_headers)
        elif method == "POST":
            print(req_headers)

            if data is not None:

                return requests.post(url=request_url, headers=req_headers, data=data)
            else:
                req = requests.post(url=request_url, headers=req_headers)
                print(req.content)
                return req

        else:
            raise Exception("Method not supported")

    def get_current_user(self):
        response = self.go_request("current_user", api_version=self.app_versions['v1'])
        return response

    def get_pipelines(self):
        pipelines = []
        endpoint = "config/pipeline_groups"
        response = self.go_request(endpoint=endpoint, api_version=None)
        for group in response.json():
            for data in group['pipelines']:
                pipelines.append(data['name'])
        return pipelines

    def get_pipeline_group(self, pgroup):
        pipelines = []
        endpoint = "config/pipeline_groups"
        response = self.go_request(endpoint=endpoint, api_version=None)
        for group in response.json():
            if group['name'] == pgroup:
                for data in group['pipelines']:
                    pipelines.append(data['name'])
        return pipelines

    def run_pipeline_group(self, group, dry_mode=True):
        scheduled_pipelines = []
        for p in self.get_pipeline_group(group):
            print("Scheduling pipeline {}".format(p))
            scheduled_pipelines.append(p)
            if dry_mode is False:
                self.schedule_pipeline(p)

    def schedule_pipeline(self, pipeline_name):
        extra_headers = {'X-GoCD-Confirm': 'true', 'Content-Type': 'application/json'}
        response = self.go_request(endpoint="pipelines/{}/schedule".format(pipeline_name),
                                   method="POST",
                                   api_version=self.app_versions['v1'],
                                   extra_header=extra_headers)
        return response


def main():
    go = GoApiServer()

    # pipelines = go.get_pipelines()

    # pipeline_group = go.run_pipeline_group("<PIPELINE GROUP>", dry_mode=False)

    # pprint.pprint(pipeline_group)


if __name__ == '__main__':
    main()
