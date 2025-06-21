# git-credential-email

Git credential helpers to get OAuth2 token for Microsoft Outlook, Gmail and Yahoo accounts.

This repo contains 3 helpers:

- `git-credential-gmail`: For Gmail accounts.
- `git-credential-outlook`: For Microsoft Outlook accounts.
- `git-credential-yahoo`: For Yahoo accounts.

They can be used with `git send-email`, especially when Outlook no longer supports app passwords.

## How does this work?

It is a simple python script, based on https://github.com/google/gmail-oauth2-tools/blob/master/python/oauth2.py. It does the following:

- Uses an OAuth2.0 `client_id` and `client_secret` to authenticate with Microsoft/Google/Yahoo and retrieve a refresh token.
- As per demand, it uses the refresh token to generate OAuth2 access tokens as and when required.
- The refresh token and access token is stored securely using the `keyring` module of pip. More information about this can be read from https://pypi.org/project/keyring/.
- Everytime the helper is called, it passes the stored access token to git. If the access token has expired, the helper first refreshes it automatically and passes the new access token.

## Installation

### All platforms

- Download the python script `git-credential-gmail`, `git-credential-outlook` and/or `git-credential-yahoo` from [here](https://github.com/AdityaGarg8/git-credential-email/releases/latest).

- Make sure that the script is [located in the path](https://superuser.com/a/284351/62691) and [is executable](https://askubuntu.com/a/229592/18504).

- Install the `keyring` pip module:

  ```bash
  pip install keyring
  ```

### Linux

#### Ubuntu/Debian

Run the following to add the apt repo and install the `git-credential-gmail`, `git-credential-outlook` and `git-credential-yahoo` package:

```bash
curl -L "https://github.com/AdityaGarg8/git-credential-email/releases/download/debian/KEY.gpg" \
	| gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/git-credential-email.gpg >/dev/null \
	&& echo "deb [signed-by=/etc/apt/trusted.gpg.d/git-credential-email.gpg] \
	https://github.com/AdityaGarg8/git-credential-email/releases/download/debian ./" \
	| sudo tee -a /etc/apt/sources.list.d/git-credential-email.list \
	&& sudo apt-get update \
	&& sudo apt-get install -y git-credential-gmail git-credential-outlook git-credential-yahoo
```

#### Fedora

Run the following to add the copr repo and install the `git-credential-gmail`, `git-credential-outlook` and `git-credential-yahoo` package:

```bash
sudo dnf copr enable -y adityagarg8/git-credential-email
sudo dnf install -y git-credential-gmail git-credential-outlook git-credential-yahoo
```

### macOS

[Install Homebrew](https://brew.sh/). Then run the following to add the brew tap and install the `git-credential-gmail`, `git-credential-outlook` and `git-credential-yahoo` package:

```bash
brew tap adityagarg8/git-credential-email
brew install git-credential-gmail git-credential-outlook git-credential-yahoo
```

### Windows

Precompiled binaries for Windows are available. You can download the zip containing them from [here](https://github.com/AdityaGarg8/git-credential-email/releases/latest). Extract all the contents of the zip [in your path](https://superuser.com/a/284351/62691). `%ProgramFiles%\Git\mingw64\libexec\git-core` is also a part of `%PATH%` when git is installed on Windows. As an example, to install `git-credential-gmail` on Windows over there, open **Command Prompt as administrator** and run the following:

```batch
curl -L -o %temp%\cred.zip https://github.com/AdityaGarg8/git-credential-email/releases/latest/download/git-credential-gmail_win64.zip
tar -xf %temp%\cred.zip -C "%ProgramFiles%\Git\mingw64\libexec\git-core"
```

## Setting up OAuth 2.0 client credentials

In order to use OAuth2.0, you need to provide an OAuth 2.0 `client_id` and a `client_secret` (secret not needed in Outlook) to allow the helper to authenticate with email servers on your behalf.

If not configured, it will use Thunderbird's `client_id` and `client_secret` by default.

The helpers include the client credentials of the following popular email clients:

- Thunderbird
- GNOME Evolution
- GNOME Online Accounts (only available for Gmail and Outlook)

In order to set the client credentials of your choice, run (taking `git credential-gmail` as an example):

```bash
git credential-gmail --set-client
```

Here you can either choose from the pre-configured client credentials, or choose to use your own registered client. Instructions for registering your own client are given below:

- Gmail: You can register a [Google API desktop app client](https://developers.google.com/identity/protocols/oauth2/native-app) and use its client credentials.
- Outlook: If you are part of the Microsoft 365 Developer Programme or have an Azure account (including free accounts), you can create your own app registration in the [Entra admin centre](https://learn.microsoft.com/entra/identity-platform/quickstart-register-app). Make you also set a **Redirect URI**, since in case of Outlook, you also need to specify that when setting the client. It is also recommended to enable device flow for your client if you want to use the `--device` option. If you cannot create your own app registration, use client credentials of any email client.
- Yahoo: Currently no option to register your own client is available. You will have to use client credentials of any email client.

In case you want to delete the client credentials you stored and go back to the default behaviour, run:

```bash
git credential-gmail --delete-client
```

## Authenticating with your email provider

### Gmail

- First of all we need to authenticate with our Gmail credentials and get a refresh token. For that run:

  ```bash
  git credential-gmail --authenticate
  ```

- By default it opens a browser window dedicated for authentication. You can choose to use your own browser by adding `--external-auth`. This shall be useful in case of systems without a GUI as well, where you can use the browser of another system:

  ```bash
  git credential-gmail --authenticate --external-auth
  ```

### Outlook

- Similar to Gmail, we need to get a refresh token for Outlook as well. For that run:

  ```bash
  git credential-outlook --authenticate
  ```

- Similarly, you can also choose to use your own browser by adding `--external-auth`:

  ```bash
  git credential-outlook --authenticate --external-auth
  ```

- You can also add `--device` to authenticate on another device like in case of systems without a GUI. This feature is exclusive to Outlook.

  ```bash
  git credential-outlook --authenticate --device
  ```

### Yahoo

- Yahoo is quite similar to Gmail. We need to authenticate with our Yahoo credentials and get a refresh token. For that run:

  ```bash
  git credential-yahoo --authenticate
  ```

- `--external-auth` is also supported:

  ```bash
  git credential-yahoo --authenticate --external-auth
  ```

## Usage

- Once authenticated, the refresh token gets saved in your keyring. You can run `git credential-outlook`, `git credential-gmail` and/or `git credential-yahoo` to confirm the same. It's output should now show an access token.

- Now run:

  ```bash
  git config --global --edit
  ```

  And add the following at the end to setup `git send-email`:

### Gmail

  ```config
  [credential "smtp://smtp.gmail.com:587"]
        helper = gmail
  [sendemail]
        smtpEncryption = tls
        smtpServer = smtp.gmail.com
        smtpUser = someone@gmail.com # Replace this with your email address.
        smtpServerPort = 587
        smtpAuth = OAUTHBEARER
  ```

### Outlook

  ```config
  [credential "smtp://smtp.office365.com:587"]
        helper = outlook
  [sendemail]
        smtpEncryption = tls
        smtpServer = smtp.office365.com
        smtpUser = someone@outlook.com # Replace this with your email address.
        smtpServerPort = 587
        smtpAuth = XOAUTH2
  ```

### Yahoo

  ```config
  [credential "smtp://smtp.mail.yahoo.com:587"]
        helper = yahoo
  [sendemail]
        smtpEncryption = tls
        smtpServer = smtp.mail.yahoo.com
        smtpUser = someone@yahoo.com # Replace this with your email address.
        smtpServerPort = 587
        smtpAuth = OAUTHBEARER
  ```

  **Note: Make sure you have atleast version 2.1800 of perl's [Authen::SASL](https://metacpan.org/dist/Authen-SASL) library in order to be able to use XOAUTH2 and OAUTHBEARER. You can run `cpan install Authen::SASL` to install the latest version of this library.**

## Deleting the stored authentication details

In case you want to delete the refresh token, that was stored by the helper, as mentioned [here](#authenticating-with-your-email-provider), simply run (taking `git credential-gmail` as an example):

```bash
git credential-gmail --delete-token
```

## Troubleshooting

In case authentication fails:

1. Try force refreshing the access token by running (taking `git credential-gmail` as an example):

   ```bash
   git credential-gmail --force-refresh-token
   ```

2. If `--force-refresh-token` does not work, try [authenticating again](#authenticating-with-your-email-provider).

## References:

- https://github.com/google/gmail-oauth2-tools/blob/master/python/oauth2.py (As a skeleton for all helpers and also Gmail support).
- https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow (For Outlook).
- https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-device-code (For adding device flow support to Outlook).
- https://developer.yahoo.com/oauth2/guide/flows_authcode/ (For Yahoo).
