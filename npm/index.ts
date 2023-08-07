"use strict";

/**
 * Import the GoogleAuth library, and create a new GoogleAuth client.
 */
//const { GoogleAuth } = require("google-auth-library");
import { GoogleAuth } from "google-auth-library";

/**
 * This sample demonstrates passing a `credentials` object directly into the
 * `getClient` method.  This is useful if you're storing the fields required
 * in environment variables.  The original `client_email` and `private_key`
 * values are obtained from a service account credential file.
 */
async function main() {
  const accessToken = process.env.CLOUDSDK_OAUTH2_ACCESS_TOKEN;
  if (!accessToken) {
    throw new Error(`
      The $CLOUDSDK_OAUTH2_ACCESS_TOKEN environment variable is required for
      this sample.
    `);
  }
  const auth = new GoogleAuth({
    authClient
    credentials: {

      client_email: clientEmail,
      private_key: privateKey,
    },
    scopes: "https://www.googleapis.com/auth/cloud-platform",
  });
  const client = await auth.getClient();
  const projectId = await auth.getProjectId();
  const url = `https://dns.googleapis.com/dns/v1/projects/${projectId}`;
  const res = await client.request({ url });
  console.log("DNS Info:");
  console.log(res.data);
}

main().catch(console.error);
