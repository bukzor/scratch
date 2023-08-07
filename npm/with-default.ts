import { GoogleAuth, Impersonated } from "google-auth-library";
import { Credentials } from "google-auth-library";

function main() {
  const accessToken = process.env.CLOUDSDK_OAUTH2_ACCESS_TOKEN;
  if (!accessToken) {
    throw new Error(`
      The $CLOUDSDK_OAUTH2_ACCESS_TOKEN environment variable is required for
      this sample.
    `);
  }

  // [START auth_cloud_idtoken_impersonated_credentials]
  /**
   * TODO(developer):
   *  1. Uncomment and replace these variables before running the sample.
   */
  // const scope = 'https://www.googleapis.com/auth/cloud-platform';
  // const targetAudience = 'http://www.example.com';
  // const impersonatedServiceAccount = 'name@project.service.gserviceaccount.com';

  //const { GoogleAuth, Impersonated } = require("google-auth-library");
  const credential: Credentials = {
    access_token: process.env.CLOUDSDK_OAUTH2_ACCESS_TOKEN,
  };

  async function getIdTokenFromImpersonatedCredentials() {
    const googleAuth = new GoogleAuth();

    // Construct the GoogleCredentials object which obtains the default configuration from your
    // working environment.
    const { credential } = await googleAuth.getApplicationDefault();

    // delegates: The chained list of delegates required to grant the final accessToken.
    // For more information, see:
    // https://cloud.google.com/iam/docs/create-short-lived-credentials-direct#sa-credentials-permissions
    // Delegate is NOT USED here.
    const delegates = [];

    // Create the impersonated credential.
    const impersonatedCredentials = new Impersonated({
      sourceClient: credential,
      delegates,
      targetPrincipal: impersonatedServiceAccount,
      targetScopes: [scope],
      lifetime: 300,
    });

    // Get the ID token.
    // Once you've obtained the ID token, you can use it to make an authenticated call
    // to the target audience.
    await impersonatedCredentials.fetchIdToken(targetAudience, {
      includeEmail: true,
    });
    console.log("Generated ID token.");
  }

  getIdTokenFromImpersonatedCredentials();
  // [END auth_cloud_idtoken_impersonated_credentials]
}

process.on("unhandledRejection", (err) => {
  console.error(err.message);
  process.exitCode = 1;
});

main(...process.argv.slice(2));
