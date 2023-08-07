#!/usr/bin/env python3.11
from google.oauth2.credentials import Credentials

Environ = dict[str, str]
OAUTH2_CLIENT_FILE = "oauth2.installed.keys.json"
CLOUDSDK_AUTH_ACCESS_TOKEN = "CLOUDSDK_AUTH_ACCESS_TOKEN"


# https://oauth2.googleapis.com/$discovery/rest

### uri: https://oauth2.googleapis.com/token


def gcloud_auth_print_access_token(env: Environ) -> str:
    from subprocess import check_output  # assert encapsulation

    try:
        token = check_output(("gcloud", "auth", "print-access-token"), env=env)
    except Exception as error:
        raise Exception("failed to get access token") from error
    else:
        token = token.decode("US-ASCII").strip()
        return token


def access_token_creds(env: Environ) -> Credentials:
    token = env.get(CLOUDSDK_AUTH_ACCESS_TOKEN)
    if token is None:
        token = gcloud_auth_print_access_token(env)
    return Credentials(token=token)


def get_userinfo(creds: Credentials):
    # this local import is used to assert encapsulation
    from google.auth.transport.requests import AuthorizedSession

    # remove quota project to avoid weird error:
    #   "User must be authenticated when user project is provided"
    creds = creds.with_quota_project(None)
    authed_session = AuthorizedSession(creds)
    # see "userinfo_endpoint":
    #   https://developers.google.com/identity/openid-connect/openid-connect
    response = authed_session.get("https://openidconnect.googleapis.com/v1/userinfo")
    return response.json()


def main():
    from os import environ

    env = dict(environ)
    from json import load

    oauth_client = load(open(OAUTH2_CLIENT_FILE))["installed"]

    creds = access_token_creds(env)
    import google.auth.transport.requests
    import google.oauth2.id_token

    # this local import is used to assert encapsulation
    from google.auth.transport.requests import AuthorizedSession

    # remove quota project to avoid weird error:
    #   "User must be authenticated when user project is provided"
    creds = creds.with_quota_project(None)
    with AuthorizedSession(creds) as session:
        result = session.post(
            oauth_client["token_uri"],
            data=dict(
                grant_type="authorization_code",
                code="1234",
                client_id=oauth_client["client_id"],
                client_secret=oauth_client["client_secret"],
                scope=[
                    "openid",
                    "https://www.googleapis.com/auth/userinfo.email",
                    "https://www.googleapis.com/auth/cloud-platform",
                    "https://www.googleapis.com/auth/appengine.admin",
                    "https://www.googleapis.com/auth/sqlservice.login",
                    "https://www.googleapis.com/auth/compute",
                    "https://www.googleapis.com/auth/accounts.reauth",
                ],
            ),
        )

    print("ID TOKEN:")
    print(result)
    print(result.text)


if __name__ == "__main__":
    exit(main())
