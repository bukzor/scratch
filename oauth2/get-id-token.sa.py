from typing import cast

from google.auth import impersonated_credentials
from google.oauth2.credentials import Credentials

# get target_credentials from a source_credential


Environ = dict[str, str]
CLOUDSDK_AUTH_ACCESS_TOKEN = "CLOUDSDK_AUTH_ACCESS_TOKEN"
DEFAULT_SCOPES = ["openid", "https://www.googleapis.com/auth/userinfo.email"]
URL = "https://deploy-staging.getsentry.net/go/api/current_user"
IAP_AUDIENCE = (
    "279793202318-qthcho2scvefo0mse11giihlpesdcprg.apps.googleusercontent.com"
)

# TODO: create a new SA that is granted the relevant IAP access, and use it here
SERVICE_ACCOUNT = "terraformer@devinfra-dev-sa.iam.gserviceaccount.com"


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


def sudo_gcp(
    creds, service_account, scopes=DEFAULT_SCOPES, lifetime=500
) -> Credentials:
    result = impersonated_credentials.Credentials(
        source_credentials=creds,
        target_principal=service_account,
        target_scopes=scopes,
        lifetime=lifetime,
    )

    return cast(Credentials, result)


def get_id_token(creds, audience):
    creds = impersonated_credentials.IDTokenCredentials(
        creds,
        target_audience=audience,
        include_email=True,
    )
    return creds


def main():
    from os import environ

    env = dict(environ)

    user_creds = access_token_creds(env)
    print(get_userinfo(user_creds))
    robot_creds = sudo_gcp(user_creds, SERVICE_ACCOUNT)
    print(get_userinfo(robot_creds))  # this works!

    robot_id_token = get_id_token(robot_creds, IAP_AUDIENCE)

    # Userinfo endpoint doesn't like id-token creds, shrug
    # print(get_userinfo(robot_id_token))

    from google.auth.transport.requests import AuthorizedSession

    response = AuthorizedSession(robot_id_token).get(URL)
    print("RESPONSE")
    print(response)
    print(response.text)


if __name__ == "__main__":
    exit(main())
