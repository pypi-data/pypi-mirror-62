from requests.auth import HTTPBasicAuth
import json

from .api_endpoints import *
from .api_requests import *

class DeepCrawlIssue:

	def __init__(self, issue_data):
		
		self.assigned_to = issue_data['assigned_to']
		self.deadline_at = issue_data['deadline_at']
		self.description = issue_data['description']
		self.dismissed = issue_data['dismissed']
		self.filters = issue_data['filters']
		self.priority = issue_data['priority']
		self.report_template = issue_data['report_template']
		self.report_type = issue_data['report_type']
		self.title = issue_data['title']
		self.id = issue_data['_href'].split('/')[-1]

		self.issue_data = issue_data

	def delete(self, connection):
		delete_issue(connection, self.account_id, self.project_id, self.id)


def create_issue(connection, account_id, project_id, issue_json):
		response = api_request(url=api_request_url_issues(account_id, project_id), method='post', data=issue_json, headers=request_headers(connection))

def delete_issue(connection, account_id, project_id, issue_id):

	endpoint_url = api_endpoint(endpoint='issue', account_id=account_id, project_id=project_id, issue_id=issue_id)
	headers = request_headers(connection)

	response = api_request(url=endpoint_url, method='delete', headers=headers)
	return

def get_issues(connection, account_id, project_id, nrows=1000):

	endpoint_url = api_endpoint(endpoint='issues', account_id=account_id, project_id=project_id)
	headers = request_headers(connection)

	issues_reponse = get_api_data(connection, endpoint_url, method='get', nrows=nrows)
	list_of_issues = []

	for issue in issues_reponse:
			list_of_issues.append(DeepCrawlIssue(issue_data=issue, project_id=project_id, account_id=account_id))

	return list_of_issues