import { CognitoAuthProvider } from 'ra-auth-cognito'
import { settings } from '@/settings'

const baseProvider = CognitoAuthProvider({
  mode: 'oauth',
  clientId: settings.client.cognito_client_id,
  userPoolId: settings.client.cognito_user_pool_id,
  hostedUIUrl: settings.client.cognito_auth_domain_name,
  redirect_uri: `${settings.client.my_domain_name}/auth/callback/`,
  scope: ["email", "openid", "profile", "aws.cognito.signin.user.admin"],
  oauthGrantType: 'code',

});

export const authProvider = {
  ...baseProvider,
  login: async () => {},
}
