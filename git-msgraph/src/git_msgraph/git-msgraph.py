#!/usr/bin/env python3
#
# Copyright 2012 Google Inc.
# Copyright 2025 Aditya Garg
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#	http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import base64
import keyring
import os
import requests
import time
import urllib.parse

# https://github.com/mozilla/releases-comm-central/blob/master/mailnews/base/src/OAuth2Providers.sys.mjs
ClientId_Thunderbird = "9e5f94bc-e8a4-4e73-b8be-63364c29d753"
Redirect_URI_Thunderbird = "https://login.microsoftonline.com/common/oauth2/nativeclient"

# https://gitlab.gnome.org/GNOME/evolution-data-server/-/commit/7554d3b95124486ac98d9a5052e069e46242a216
ClientId_Evolution = "cc6e0693-0e26-4220-8322-9d363e308fc6"
Redirect_URI_Evolution = "https://login.microsoftonline.com/common/oauth2/nativeclient"

# https://gitlab.gnome.org/GNOME/gnome-online-accounts/-/blob/master/meson_options.txt
ClientId_Gnome = "8ef61e06-9fd5-49af-9b63-6983aede4213"
Redirect_URI_Gnome = "goa-oauth2://localhost"

Scopes = 'Mail.Send offline_access openid profile'
ServiceName = "git-msgraph"

def save_refresh_token(refresh_token):
	keyring.set_password(ServiceName, "refresh_token", refresh_token)

def load_refresh_token():
	return keyring.get_password(ServiceName, "refresh_token")

def delete_refresh_token():
	keyring.delete_password(ServiceName, "refresh_token")

def save_access_token(access_token, expiry):
	keyring.set_password(ServiceName, "access_token", access_token)
	keyring.set_password(ServiceName, "access_token_expiry", expiry)

def load_access_token():
	return keyring.get_password(ServiceName, "access_token")

def load_access_token_expiry():
	return keyring.get_password(ServiceName, "access_token_expiry")

def delete_access_token():
	keyring.delete_password(ServiceName, "access_token")
	keyring.delete_password(ServiceName, "access_token_expiry")

def set_client(client_id, redirect_uri):
	keyring.set_password(ServiceName, "client_id", client_id)
	keyring.set_password(ServiceName, "redirect_uri", redirect_uri)

def load_client_id():
	return keyring.get_password(ServiceName, "client_id")

def load_redirect_uri():
	return keyring.get_password(ServiceName, "redirect_uri")

def delete_client():
	keyring.delete_password(ServiceName, "client_id")
	keyring.delete_password(ServiceName, "redirect_uri")

def qr_encode(url):
	try:
		try:
			import qrcode
			qr = qrcode.QRCode(border=2)
			qr.add_data(url)
			qr.make(fit=True)
			qr.print_ascii(invert=True)
		except Exception:
			headers = {'User-Agent': 'curl'}
			url_qr = f"https://qrenco.de/{url}"
			response = requests.get(url_qr, headers=headers)
			response.raise_for_status()
			content = response.text
			print(content)
	except Exception:
		# let's not interrupt the process if qrenco.de is down
		pass

def get_code_from_url(url):
	parsed_url = urllib.parse.urlparse(url)
	parsed_query = urllib.parse.parse_qs(parsed_url.query)
	return parsed_query.get('code', [''])[0]

def AccountsUrl(command):
	return '%s/%s' % ('https://login.microsoftonline.com', command)

def UrlEscape(text):
	return urllib.parse.quote(text, safe='~-._')

def FormatUrlParams(params):
	param_fragments = []
	for param in sorted(params.items(), key=lambda x: x[0]):
		param_fragments.append('%s=%s' % (param[0], UrlEscape(param[1])))
	return '&'.join(param_fragments)

def GeneratePermissionUrl(redirect_uri):
	params = {}
	params['client_id'] = ClientId
	params['redirect_uri'] = redirect_uri
	params['response_type'] = 'code'
	params['response_mode'] = 'query'
	params['scope'] = Scopes
	return '%s?%s' % (AccountsUrl('common/oauth2/v2.0/authorize'), FormatUrlParams(params))

def AuthorizeTokens(authorization_code):
	params = {}
	params['client_id'] = ClientId
	params['code'] = authorization_code
	params['redirect_uri'] = Redirect_URI
	params['grant_type'] = 'authorization_code'
	request_url = AccountsUrl('common/oauth2/v2.0/token')

	try:
		response = requests.post(request_url, data=params)
		response.raise_for_status()
		return response.json()
	except requests.exceptions.HTTPError:
		print(f"HTTP Error {response.status_code}: {response.reason}")
		print("Response Body:", response.text)
		sys.exit("\nFailed to get refresh token due to an HTTP error.")
	except Exception as e:
		print(f"Unexpected error: {e}")
		sys.exit("\nFailed to get refresh token due to an unexpected error.")

def RefreshToken(refresh_token):
	params = {}
	params['client_id'] = ClientId
	params['refresh_token'] = refresh_token
	params['grant_type'] = 'refresh_token'
	params['redirect_uri'] = Redirect_URI
	request_url = AccountsUrl('common/oauth2/v2.0/token')

	try:
		response = requests.post(request_url, data=params)
		response.raise_for_status()
		return response.json()
	except requests.exceptions.HTTPError:
		print(f"HTTP Error {response.status_code}: {response.reason}")
		print("Response Body:", response.text)
		sys.exit("\nFailed to get access token due to an HTTP error.\nTry running `git msgraph --authenticate` to get a new refresh token.")
	except Exception as e:
		print(f"Unexpected error: {e}")
		sys.exit("\nFailed to get access token due to an unexpected error.\nTry running `git msgraph --authenticate` to get a new refresh token.")

def DeviceFlowCode():
	params = {}
	params['client_id'] = ClientId
	params['tenant'] = 'common'
	params['scope'] = Scopes
	request_url = AccountsUrl('common/oauth2/v2.0/devicecode')

	try:
		response = requests.post(request_url, data=params)
		response.raise_for_status()
		return response.json()
	except requests.exceptions.HTTPError:
		return response.text
	except Exception as e:
		return str(e)

def PollDeviceToken(device_code):
	params = {}
	params['client_id'] = ClientId
	params['tenant'] = 'common'
	params['grant_type'] = 'urn:ietf:params:oauth:grant-type:device_code'
	params['device_code'] = device_code
	request_url = AccountsUrl('common/oauth2/v2.0/token')

	while True:
		try:
			response = requests.post(request_url, data=params)
			response.raise_for_status()
			return response.json()
		except requests.exceptions.HTTPError:
			error = response.json()
			if error['error'] == 'authorization_pending':
				time.sleep(5)
			else:
				print(f"HTTP Error {response.status_code}: {response.reason}")
				print("Response Body:", response.text)
				sys.exit("\nFailed to get refresh token due to an HTTP error.")
		except Exception as e:
			print(f"Unexpected error: {e}")
			sys.exit("\nFailed to get refresh token due to an unexpected error.")

def get_code_from_device_flow(open_browser=False):
	device_flow = DeviceFlowCode()
	if "error" in device_flow:
		if open_browser:
			raise Exception
		else:
			sys.exit(f"Failed to initiate device flow: {device_flow}")

	if open_browser:
		print(f"Enter this code when asked to do so by your browser: \033[1m{device_flow['user_code']}\033[0m\n")
		webbrowser.open(device_flow['verification_uri'])
	else:
		qr_encode(device_flow['verification_uri'])
		print(f"Visit {device_flow['verification_uri']} on a web browser.\nEnter this code when asked to do so: \033[1m{device_flow['user_code']}\033[0m\n")
	return PollDeviceToken(device_flow['device_code'])

def main():
	if "--help" in sys.argv:
		print("""
Usage: git-msgraph [OPTIONS]

Options:
  --help                 * Show this help message and exit.
  --set-client           * Set the client details to use for authentication.
  --delete-client        * Delete the client details set using --set-client.
  --authenticate         * Authenticate with Microsoft Graph API using OAuth2.
  --device               * Use device code flow for authentication.
                           Use this option with --authenticate.
  --external-auth        * Authenticate using an external browser.
                           Use this option with --authenticate.
  --force-refresh-token  * Force refresh the access token.
  --delete-token         * Delete the credentials saved using --authenticate.

Description:
  This script allows you to authenticate with Microsoft Graph API using
  OAuth2 and retrieve access tokens to send emails using the API.

Examples:
  Authenticate using the browser-based flow:
  git-msgraph --authenticate

  Authenticate using the device code flow:
  git-msgraph --authenticate --device
""")
		sys.exit(0)

	ClientId = load_client_id()
	Redirect_URI = load_redirect_uri()

	if ClientId is None:
		ClientId = ClientId_Thunderbird
		Redirect_URI = Redirect_URI_Thunderbird

	elif Redirect_URI is None:
		Redirect_URI = 'https://login.microsoftonline.com/common/oauth2/nativeclient'

	if "--set-client" in sys.argv:
		print("What client details do you want to use?\n")
		print("1. Thunderbird")
		print("2. GNOME Evolution")
		print("3. GNOME Online Accounts")
		print("4. Use your own custom client details")
		answer = input("\nType the number of your choice and press enter: ")

		if answer == "1":
			ClientId = ClientId_Thunderbird
			Redirect_URI = Redirect_URI_Thunderbird
		elif answer == "2":
			ClientId = ClientId_Evolution
			Redirect_URI = Redirect_URI_Evolution
		elif answer == "3":
			ClientId = ClientId_Gnome
			Redirect_URI = Redirect_URI_Gnome
		elif answer == "4":
			ClientId = input("\nEnter the Client ID: ")
			Redirect_URI = input("Enter the Redirect URI: ")
		else:
			sys.exit("\nInvalid choice")

		set_client(ClientId, Redirect_URI)
		print("\nClient details saved to keyring")

	elif "--delete-client" in sys.argv:
		try:
			delete_client()
			print("Client details deleted from keyring")
		except keyring.errors.PasswordDeleteError:
			sys.exit("No client details found in keyring")

	elif "--authenticate" in sys.argv:
		if "--device" in sys.argv:
			token = get_code_from_device_flow()
		else:
			Redirect_URI_is_http = 'false'
			if Redirect_URI.startswith('http://') or Redirect_URI.startswith('https://'):
				Redirect_URI_is_http = 'true'
			url = GeneratePermissionUrl(Redirect_URI)
			code = ''

			if "--external-auth" in sys.argv:
				# Use external browser for authentication
				qr_encode(url)
				print("Navigate to the following URL in a web browser:\n")
				print(url)
				if Redirect_URI_is_http == 'true':
					print("\nAfter login, you will be redirected to a blank or error page.")
					codeurl = input("Copy the URL of that page and paste it here:\n")
				else:
					print("\nThis client uses a non-http redirect URI.")
					print("Before login enable network logging in your browser.")
					print("After login, check the network logs for a URL with \"code\" in it.")
					codeurl = input("Copy that URL and paste it here:\n")
				code = get_code_from_url(codeurl)
				token = AuthorizeTokens(code)
				print()

			else:
				print("Opening a browser window for authentication...\n")
				if Redirect_URI_is_http == 'true': # NEED HELP: How to intercept non http urls in PyQt6?
					try:
						from PyQt6.QtWidgets import QApplication, QMainWindow
						from PyQt6.QtWebEngineWidgets import QWebEngineView
						from PyQt6.QtCore import QUrl, QLoggingCategory
						qt_available = True
					except Exception:
						import webbrowser
						qt_available = False
				else:
					import webbrowser
					qt_available = False

				if qt_available:
					if "--verbose" in sys.argv:
						loglevel = 0
					else:
						loglevel = 3
						QLoggingCategory("qt.webenginecontext").setFilterRules("*.info=false") # Suppress info logs

					os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = f"--enable-logging --log-level={loglevel}"

					class BrowserWindow(QMainWindow):

						def handle_url_change(self, url):
							if "code=" in url.toString():
								global code
								code = get_code_from_url(url.toString())
								self.close()

						def __init__(self):
							super().__init__()
							self.setWindowTitle("OAuth2 Login")
							self.resize(800, 600)
							self.browser = QWebEngineView()
							self.setCentralWidget(self.browser)
							self.browser.load(QUrl(url))
							self.browser.urlChanged.connect(self.handle_url_change)
							self.show()

					webapp = QApplication(sys.argv)
					window = BrowserWindow()
					webapp.exec()
					token = AuthorizeTokens(code)
				else:
					try:
						# Lets try to use device code flow first
						token = get_code_from_device_flow(open_browser=True)
					except Exception:
						webbrowser.open(url)
						print("Authenticate in the browser window that opened.")
						if Redirect_URI_is_http == 'true':
							print("After login, you will be redirected to a blank or error page.")
							codeurl = input("Copy the URL of that page and paste it here:\n")
						else:
							print("This client uses a non-http redirect URI.")
							print("Before login enable network logging in your browser.")
							print("After login, check the network logs for a URL with \"code\" in it.")
							codeurl = input("Copy that URL and paste it here:\n")
						code = get_code_from_url(codeurl)
						print()
						token = AuthorizeTokens(code)

		if 'error' in token:
			print(token)
			sys.exit("\nFailed to get refresh token")

		save_refresh_token(token['refresh_token'])
		try:
			delete_access_token()
		except keyring.errors.PasswordDeleteError:
			pass
		print('Saved refresh token to keyring')

	elif "--delete-token" in sys.argv:
		exit_error = 0
		try:
			delete_refresh_token()
			print("Refresh token deleted from keyring")
		except keyring.errors.PasswordDeleteError:
			print("No refresh token found in keyring")
			exit_error = 1

		try:
			delete_access_token()
			print("Access token deleted from keyring")
		except keyring.errors.PasswordDeleteError:
			print("No access token found in keyring")
			exit_error = 1

		sys.exit(exit_error)

	else:
		need_new_access_token = False
		access_token = load_access_token()
		access_token_expiry = load_access_token_expiry()

		if access_token is None or access_token_expiry is None or (int(access_token_expiry) - int(time.time())) <= 0 or "--force-refresh-token" in sys.argv:
			need_new_access_token = True

		if need_new_access_token:
			# Lets use the refresh token to get a new access token
			refresh_token = load_refresh_token()

			if refresh_token is None:
				sys.exit("No refresh token found.\nPlease authenticate first by running `git msgraph --authenticate`")

			token = RefreshToken(refresh_token)

			if 'error' in token:
				print(token)
				sys.exit("Failed to get access token from the server")
			else:
				access_token = token['access_token']
				access_token_expiry = int(time.time()) + int(token['expires_in']) - 120 # Subtract 2 minutes to ensure we never get an expired token
				try: # Some credential helpers hate such long access tokens (looking at you Windows). Still we can refresh the token right ;)
					save_access_token(access_token, str(access_token_expiry))
				except Exception:
					pass

		if "-i" in sys.argv:
			import argparse
			import re
			from email import message_from_file
			from email.utils import getaddresses

			parser = argparse.ArgumentParser()
			parser.add_argument('-i', nargs='+', help='Recipient email addresses')
			args, unknown = parser.parse_known_args()
			recipients = args.i if args.i else []

			raw_message = message_from_file(sys.stdin)

			# Find Bcc addresses
			to = [addr for name, addr in getaddresses(raw_message.get_all('To', []))]
			cc = [addr for name, addr in getaddresses(raw_message.get_all('Cc', []))]
			bcc = [r for r in recipients if r not in to and r not in cc]
			from_address = raw_message.get('From', '')
			match = re.match(r'^(.*?)\s*<([^>]+)>$', from_address)
			if match:
				from_address = match.group(2).strip()
			elif from_address.startswith('<') and from_address.endswith('>'):
				from_address = from_address[1:-1]

			# Add Bcc header if there are Bcc addresses
			if bcc:
				raw_message['Bcc'] = ', '.join(bcc)

			message = raw_message.as_string()

			message_bytes = message.encode("utf-8")
			encoded_string = base64.b64encode(message_bytes).decode("utf-8")
			email_url = f"https://graph.microsoft.com/v1.0/users/{from_address}/sendMail"
			email_headers = {
				"Authorization": f"Bearer {access_token}",
				"Content-Type": "text/plain"
			}

			email_response = requests.post(email_url, headers=email_headers, data=encoded_string)

			if email_response.status_code == 202:
				print("Email sent successfully.")
			else:
				sys.exit(f"Failed to send email: {email_response.status_code}, {email_response.text}")

		else:
			print(access_token)

if __name__ == "__main__":
	main()
