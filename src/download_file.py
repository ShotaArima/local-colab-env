import io
import os.path

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
CREDENTIALS_PATH = "credentials.json"

def download_file(real_file_id):
	"""Downloads a file
	Args:
		real_file_id: ID of the file to download
	Returns : IO object with location.

	Load pre-authorized user credentials from the environment.
	TODO(developer) - See https://developers.google.com/identity
	for guides on implementing OAuth2 for the application.
	"""
	# creds, _ = google.auth.default()
	# スコープの設定
	creds = None
	# The file token.json stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists("token.json"):
		creds = Credentials.from_authorized_user_file("token.json", SCOPES)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				CREDENTIALS_PATH, SCOPES
			)
			creds = flow.run_local_server(bind_addr="0.0.0.0", port=9005, open_browser=False)
		# Save the credentials for the next run
		with open("token.json", "w") as token:
			token.write(creds.to_json())

	try:
		# create drive api client
		service = build("drive", "v3", credentials=creds)

		file_id = real_file_id

		# pylint: disable=maybe-no-member
		request = service.files().get_media(fileId=file_id)
		file = io.BytesIO()
		downloader = MediaIoBaseDownload(file, request)
		done = False
		while done is False:
			status, done = downloader.next_chunk()
			print(f"Download {int(status.progress() * 100)}.")

		file.seek(0)
		print(file.read().decode("utf-8"))

	except HttpError as error:
		print(f"An error occurred: {error}")
		file = None

	return file.getvalue()


if __name__ == "__main__":
	download_file(real_file_id="1gnTIAuHMYwKlyWxsyOp8uUNurdjRPhY3")