# git-credential-email

This repo contains the following helpers:

- `git-credential-gmail`: For Gmail accounts.
- `git-credential-outlook`: For Microsoft Outlook accounts.
- `git-credential-yahoo`: For Yahoo accounts.
- `git-credential-aol`: For AOL accounts.
- `git-msgraph`: Helper to use Microsoft Graph API instead of SMTP to send emails.
- `git-protonmail`: Helper to use Proton Mail API to send emails.

They can be used with `git send-email`, especially when Outlook no longer supports app passwords.

## How does this work?

It is a simple python script, based on <https://github.com/google/gmail-oauth2-tools/blob/master/python/oauth2.py> and <https://github.com/opulentfox-29/protonmail-api-client>. It does the following:

- Uses an OAuth2.0 `client_id` and `client_secret` to authenticate with Microsoft/Google/Yahoo/AOL and retrieve a refresh token.
- As per demand, it uses the refresh token to generate OAuth2.0 access tokens as and when required.
- The refresh token and access token is stored securely using the `keyring` module of pip. More information about this can be read from <https://pypi.org/project/keyring/>.
- Everytime the helper is called, it passes the stored access token to git. If the access token has expired, the helper first refreshes it automatically and passes the new access token.
- For APIs like Microsoft Graph and Proton Mail, it exploits the sendmail-like command ability of `git send-email`
- For Proton Mail, the authentication flow is different. The helper uses the web API of Proton Mail to get the required keys for end to end encryption, store cookies in form of session file etc.

## Installation

### All platforms

- Download the python script of the helper you want from [here](https://github.com/AdityaGarg8/git-credential-email/releases/latest).

- Make sure that the script is [located in the path](https://superuser.com/a/284351/62691) and [is executable](https://askubuntu.com/a/229592/18504).

- Install the `keyring` and `requests` pip module:

  ```bash
  pip install keyring requests
  ```

- For **Proton Mail**, you also need to install some more modules by running:

  ```bash
  pip install bcrypt cryptography keyring PGPy13 requests requests-toolbelt typing-extensions
  ```

### Linux

#### Ubuntu/Debian

Run the following to add the apt repo and install the helpers:

```bash
curl -L "https://github.com/AdityaGarg8/git-credential-email/releases/download/debian/KEY.gpg" \
	| gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/git-credential-email.gpg >/dev/null \
	&& echo "deb [signed-by=/etc/apt/trusted.gpg.d/git-credential-email.gpg] \
	https://github.com/AdityaGarg8/git-credential-email/releases/download/debian ./" \
	| sudo tee -a /etc/apt/sources.list.d/git-credential-email.list \
	&& sudo apt-get update \
	&& sudo apt-get install -y git-credential-gmail git-credential-outlook git-credential-yahoo git-credential-aol git-msgraph git-protonmail
```

#### Fedora

Run the following to add the copr repo and install the helpers:

```bash
sudo dnf copr enable -y adityagarg8/git-credential-email
sudo dnf install -y git-credential-gmail git-credential-outlook git-credential-yahoo git-credential-aol git-msgraph git-protonmail
```

#### Arch Linux

Edit `/etc/pacman.conf` and add the following at its end:

```bash
[git-credential-email]
Server = https://github.com/AdityaGarg8/git-credential-email/releases/download/archlinux
```

Now import the GPG Key used to sign the packages by running:

```bash
sudo pacman-key --recv-keys 48DC9F9CC66D3FAF --keyserver keyserver.ubuntu.com
sudo pacman-key --lsign-key 48DC9F9CC66D3FAF
```

Finally install the helpers by running:

```bash
sudo pacman -Sy git-credential-gmail git-credential-outlook git-credential-yahoo git-credential-aol git-msgraph git-protonmail
```

**Note:** You may also have to install a supported keyring backend as described in <https://pypi.org/project/keyring/>.

#### OpenSUSE Tumbleweed

Run the following to add the copr repo and install the helpers:

```bash
sudo zypper addrepo https://copr.fedorainfracloud.org/coprs/adityagarg8/git-credential-email/repo/opensuse-tumbleweed/adityagarg8-git-credential-email-opensuse-tumbleweed.repo
sudo zypper install git-credential-gmail git-credential-outlook git-credential-yahoo git-credential-aol git-msgraph git-protonmail
```

(Thanks to [@IsaacOscar](https://github.com/IsaacOscar) for adding support for OpenSUSE Tumbleweed!)

### macOS

[Install Homebrew](https://brew.sh/). Then run the following to add the brew tap and install the helpers:

```bash
brew tap adityagarg8/git-credential-email
brew install git-credential-gmail git-credential-outlook git-credential-yahoo git-credential-aol git-msgraph git-protonmail
```

### Windows

Precompiled binaries for Windows are available. You can download the zip containing them from [here](https://github.com/AdityaGarg8/git-credential-email/releases/latest). Extract all the contents of the zip [in your path](https://superuser.com/a/284351/62691). `%ProgramFiles%\Git\mingw64\libexec\git-core` is also a part of `%PATH%` when git is installed on Windows. As an example, to install `git-credential-gmail` on Windows over there, open **Command Prompt as administrator** and run the following:

```batch
curl -L -o %temp%\cred.zip https://github.com/AdityaGarg8/git-credential-email/releases/latest/download/git-credential-gmail_win64.zip
tar -xf %temp%\cred.zip -C "%ProgramFiles%\Git\mingw64\libexec\git-core"
```

## Setting up OAuth 2.0 client credentials

**You can skip this section if you are using Proton Mail**

In order to use OAuth2.0, you need to provide an OAuth 2.0 `client_id` and a `client_secret` (secret not needed in Outlook) to allow the helper to authenticate with email servers on your behalf.

If not configured, it will use Thunderbird's `client_id` and `client_secret` by default.

The helpers include the client credentials of the following popular email clients:

- Thunderbird
- GNOME Evolution (only available for Gmail, Outlook and Yahoo)
- GNOME Online Accounts (only available for Gmail and Outlook)

In order to set the client credentials of your choice, run (taking `git credential-gmail` as an example):

```bash
git credential-gmail --set-client
```

Here you can either choose from the pre-configured client credentials, or choose to use your own registered client. Instructions for registering your own client are given below:

- Gmail: You can register a [Google API desktop app client](https://developers.google.com/identity/protocols/oauth2/native-app) and use its client credentials.
- Outlook: If you are part of the Microsoft 365 Developer Programme or have an Azure account (including free accounts), you can create your own app registration in the [Entra admin centre](https://learn.microsoft.com/entra/identity-platform/quickstart-register-app). Make sure you also set a **Redirect URI**, since in case of Outlook, you also need to specify that when setting the client. It is also recommended to enable device flow for your client if you want to use the `--device` option. If you cannot create your own app registration, use client credentials of any email client.
- Yahoo and AOL: Currently no option to register your own client is available. You will have to use client credentials of any email client.

In case you want to delete the client credentials you stored and go back to the default behaviour, run:

```bash
git credential-gmail --delete-client
```

## Authenticating with your email provider

Now we need to authenticate with our email provider to get the necessary tokens to authenticate using OAuth2.0.

**Note: Except for `git-msgraph` and `git-protonmail`, make sure you have atleast version 2.1800 of perl's [Authen::SASL](https://metacpan.org/dist/Authen-SASL) library in order to be able to use OAuth2.0. You can run `cpan install Authen::SASL` to install the latest version of this library. `git-msgraph` and `git-protonmail` do not require this library.**

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

#### Using the SMTP server

Microsoft Outlook accounts can send emails using two methods. First is their SMTP server, which is similar to what most email providers use. Second is Microsoft Graph API. These instructions are in case you want to use the SMTP server.

**Note: It is recommended to use atleast git 2.50 for threads to properly work with Outlook's SMTP server. If you are using an older version of git, then its better to use [Microsoft Graph API](#using-microsoft-graph-api) using `git-msgraph` for threads to work properly.**

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

#### Using Microsoft Graph API

Microsoft Graph API can be used instead of Outlook's SMTP server to send emails. Microsoft Graph API tends to be faster than SMTP. If you want to use Microsoft Graph API to send emails, follow these instructions.

- Similar to SMTP helper, we need to get a refresh token for Microsoft Graph API as well. For that run:

  ```bash
  git msgraph --authenticate
  ```

- Similarly, you can also choose to use your own browser by adding `--external-auth`:

  ```bash
  git msgraph --authenticate --external-auth
  ```

- You can also add `--device` to authenticate on another device like in case of systems without a GUI. This feature is exclusive to Outlook.

  ```bash
  git msgraph --authenticate --device
  ```

**Note:** When sending/cc'ing an email to yourself, Microsoft Graph may incorrectly re-encode your message when you receive it, in case you are using special characters like non breaking space. However, the email stored in your *Sent* folder and received by *other email addresses* should be correct, so you do not need to worry at all!

### Yahoo

- Yahoo is quite similar to Gmail. We need to authenticate with our Yahoo credentials and get a refresh token. For that run:

  ```bash
  git credential-yahoo --authenticate
  ```

- `--external-auth` is also supported:

  ```bash
  git credential-yahoo --authenticate --external-auth
  ```

### AOL

- AOL is same as Yahoo. We need to authenticate with our AOL credentials and get a refresh token. For that run:

  ```bash
  git credential-aol --authenticate
  ```

- `--external-auth` is also supported:

  ```bash
  git credential-aol --authenticate --external-auth
  ```

### Proton Mail

- You can authenticate with your Proton Mail credentials by running:

  ```bash
  git protonmail --authenticate
  ```

- If `--authenticate` does not work, you try adding `--alternate-auth`:

  ```bash
  git protonmail --authenticate --alternate-auth
  ```

#### Solving CAPTCHA while authenticating in Proton Mail

There is a high chance that you will be asked to solve a CAPTCHA when you try to authenticate for Proton Mail. The on-screen instructions should be followed while solving the CAPTCHA.

For an easier CAPTCHA solving experience, you can install either `PyQt6-WebEngine` or `OpenCV`.

`PyQt6-WebEngine` will open a dedicated broswer window for solving CAPTCHA for you to solve and send the solved CAPTCHA to the credential helper. It occupies around 100-200MBs depending on your OS.

`OpenCV` is more advanced and can automatically solve the CAPTCHA 99% times, without you needing to solve it at all! But it also occupies around 600MBs. An alternate is `opencv-python-headless` available using `pip` that is lighter, and is the best option for headless systems. It is not available if you are using apt/dnf/brew to install the helper. If you are using a [Windows binary](#windows), `opencv-python-headless` is bundled by default.

I would recommend installing `PyQt6-WebEngine` if you are on a system with GUI and `OpenCV` for headless systems.

You can install them by running (modify the commands accordingly if you want to install only one of them):

- For all platforms: `pip install PyQt6-WebEngine opencv-python`
- If you have a headless system: `pip install opencv-python-headless` (PyQt6-WebEngine is a GUI app, so will not work in headless systems)
- Ubuntu/Debian: `sudo apt-get install -y python3-pyqt6.qtwebengine python3-opencv`
- Fedora: `sudo dnf install -y python-pyqt6-webengine python-opencv`
- macOS: `brew install pyqt@6 opencv`

## Usage

- Once authenticated, the refresh token gets saved in your keyring. You can run your helper to confirm the same. For example, for **Gmail** run `git credential-gmail`. It's output should now show an access token.
- For **Proton Mail** users instead of a refresh token, a session file is stored in your `$HOME` folder and is encrypted with a random key. That key is stored in your keyring. To check if its authenticated, check for presence of `.git-protonmail.pickle` file in your `$HOME` folder. Note that this file may be hidden by default on Linux and macOS.

- Now run:

  ```bash
  git config --global --edit
  ```

  And add the following at the end to setup `git send-email`:

### Gmail

  ```config
  [credential "smtp://smtp.gmail.com:465"]
        helper = 
        helper = gmail
  [sendemail]
        smtpEncryption = ssl
        smtpServer = smtp.gmail.com
        smtpUser = someone@gmail.com # Replace this with your email address
        smtpServerPort = 465
        smtpAuth = OAUTHBEARER
        from = Your Name <someone@gmail.com> # Replace this with your name and email address
  ```

### Outlook

#### Using the SMTP server

  ```config
  [credential "smtp://smtp.office365.com:587"]
        helper = 
        helper = outlook
  [sendemail]
        smtpEncryption = tls
        smtpServer = smtp.office365.com
        smtpUser = someone@outlook.com # Replace this with your email address
        smtpServerPort = 587
        smtpAuth = XOAUTH2
        from = Your Name <someone@outlook.com> # Replace this with your name and email address
  ```

#### Using Microsoft Graph API

  ```config
  [sendemail]
        sendmailCmd = git-msgraph
        from = someone@outlook.com # Replace this with your email address
  ```

### Yahoo

  ```config
  [credential "smtp://smtp.mail.yahoo.com:465"]
        helper = 
        helper = yahoo
  [sendemail]
        smtpEncryption = ssl
        smtpServer = smtp.mail.yahoo.com
        smtpUser = someone@yahoo.com # Replace this with your email address
        smtpServerPort = 465
        smtpAuth = OAUTHBEARER
        from = Your Name <someone@yahoo.com> # Replace this with your name and email address
  ```

### AOL

  ```config
  [credential "smtp://smtp.aol.com:465"]
        helper = 
        helper = aol
  [sendemail]
        smtpEncryption = ssl
        smtpServer = smtp.aol.com
        smtpUser = someone@aol.com # Replace this with your email address
        smtpServerPort = 465
        smtpAuth = OAUTHBEARER
        from = Your Name <someone@aol.com> # Replace this with your name and email address
  ```

### Proton Mail

  ```config
  [sendemail]
        sendmailCmd = git-protonmail
        from = someone@proton.me # Replace this with your email address. If you have multiple addresses (seen in paid accounts), use the address you want to send from.
  ```

## Deleting the stored authentication details

In case you want to delete the refresh token, that was stored by the helper, as mentioned [here](#authenticating-with-your-email-provider), simply run (taking `git credential-gmail` as an example):

```bash
git credential-gmail --delete-token
```

For **Proton Mail**, you need to delete both the session file and the key that encrypted it. This command will help you for that:

```bash
git protonmail --delete-session
```

## Troubleshooting

In case authentication fails:

1. Try force refreshing the access token by running (taking `git credential-gmail` as an example):

   ```bash
   git credential-gmail --force-refresh-token
   ```

2. If `--force-refresh-token` does not work, try [authenticating again](#authenticating-with-your-email-provider).

## References and useful links:

- <https://github.com/google/gmail-oauth2-tools/blob/master/python/oauth2.py> (As a skeleton for all helpers and also Gmail support).
- <https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow> (For Outlook).
- <https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-device-code> (For adding device flow support to Outlook).
- <https://learn.microsoft.com/en-us/graph/api/user-sendmail> (For Microsoft Graph API)
- <https://developer.yahoo.com/oauth2/guide/flows_authcode> (For Yahoo).
- <https://github.com/opulentfox-29/protonmail-api-client> (For Proton Mail).
- <https://github.com/AdityaGarg8/git-credential-email/releases/tag/debian> (GitHub release that hosts the apt repo).
- <https://github.com/AdityaGarg8/git-credential-email/releases/tag/archlinux> (GitHub release that hosts the pacman repo).
- <https://copr.fedorainfracloud.org/coprs/adityagarg8/git-credential-email/> (Copr repo).
