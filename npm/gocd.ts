"use strict";

import { GoogleAuth } from "google-auth-library";
import { OAuth2Client } from "google-auth-library";
import { OAuth2ClientOptions } from "google-auth-library";
import { IdTokenClient } from "google-auth-library";
import { JWT } from "google-auth-library";

const iap_client = {
  id: "279793202318-qthcho2scvefo0mse11giihlpesdcprg.apps.googleusercontent.com",
  secret: "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",
  redirect:
    "https://iap.googleapis.com/v1/oauth/clientIds/279793202318-qthcho2scvefo0mse11giihlpesdcprg.apps.googleusercontent.com:handleRedirect",
  audience: "/projects/279793202318/global/backendServices/1262922268840097096",
};
const url = "https://deploy-staging.getsentry.net/go/api/current_user";

const GOCD_TOKEN = "5e838e80c9409d5b8e3f4cc0170860c24761b170";

async function main3() {
  const auth = new GoogleAuth({
    scopes: "https://www.googleapis.com/auth/cloud-platform",
  });
  const client = await auth.getClient();
  console.log(await client.getRequestHeaders());
}

async function main4() {
  // const auth1 = new GoogleAuth({
  //   scopes: "https://www.googleapis.com/auth/cloud-platform",
  // });
  // const client1 = await auth1.getClient();
  const auth2 = new GoogleAuth({
    scopes: ["https://www.googleapis.com/auth/cloud-platform"],
    clientOptions: {
      clientId: iap_client.id,
      clientSecret: iap_client.secret,
      redirectUri: iap_client.redirect,
    },
  });
  const client2 = await auth2.getIdTokenClient(iap_client.audience);
  const res = await client2.request({ url });

  console.log(res.data);
}

async function main() {
  const clientOptions: OAuth2ClientOptions = {
    clientId: iap_client.id,
    clientSecret: iap_client.secret,
    redirectUri: iap_client.redirect,
  };

  const auth = new GoogleAuth({
    scopes: ["https://www.googleapis.com/auth/cloud-platform"],
    clientOptions: clientOptions,
  });
  const client = await auth.getClient();
  const id_client = new IdTokenClient({
    targetAudience: iap_client.audience,
    idTokenProvider: client,
  });
  const res = await id_client.request({ url });

  console.log(res.data);

  // const client = new JWT({
  //   email: oauth_client.id,
  //   key: oauth_client.secret,
  // });

  // client.request({
  //   url: url,
  // });
  // console.log("CREDS", client.credentials);
  //const id_token = await client.fetchIdToken(iap_audience);

  /// const idToken = process.env.CLOUDSDK_OAUTH2_ID_TOKEN;
  /// if (!idToken) {
  ///   throw new Error(`
  ///     The $CLOUDSDK_OAUTH2_ACCESS_TOKEN environment variable is required for
  ///     this sample.
  ///   `);
  /// }

  // const gocdRes = await fetch(url, {
  //   headers: {
  //     Accept: "application/vnd.go.cd.v1+json",
  //     Authorization: `Bearer ${GOCD_TOKEN}`,
  //     "Proxy-Authorization": `Bearer ${id_token}`,
  //   },
  // });

  // console.log(gocdRes);
}

main().catch(console.error);
