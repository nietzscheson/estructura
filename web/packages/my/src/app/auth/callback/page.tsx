'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import {
  CognitoUserPool,
  CognitoUser,
  CognitoUserSession,
  CognitoIdToken,
  CognitoAccessToken,
  CognitoRefreshToken,
} from 'amazon-cognito-identity-js'
import { settings } from '@/settings'

const COGNITO_DOMAIN = settings.client.cognito_auth_domain_name
const CLIENT_ID = settings.client.cognito_client_id
const REDIRECT_URI = `${settings.client.my_domain_name}/auth/callback/`

export default function CallbackPage() {
  const router = useRouter()

  useEffect(() => {
    const handleCallback = async () => {
      const params = new URLSearchParams(window.location.search)
      const code = params.get('code')

      if (!code) {
        console.error('Missing code in callback')
        return
      }

      try {
        const response = await fetch(`${COGNITO_DOMAIN}/oauth2/token`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: new URLSearchParams({
            grant_type: 'authorization_code',
            client_id: CLIENT_ID,
            redirect_uri: REDIRECT_URI,
            code: code,
            // code_verifier: localStorage.getItem('pkce_verifier')!, // only if you manually use PKCE
          }),
        })

        const data = await response.json()
        if (data.id_token && data.access_token) {
          localStorage.setItem('id_token', data.id_token)
          localStorage.setItem('access_token', data.access_token)
          if (data.refresh_token) {
            localStorage.setItem('refresh_token', data.refresh_token)
          }
          const session = new CognitoUserSession({
            IdToken: new CognitoIdToken({ IdToken: data.id_token }),
            AccessToken: new CognitoAccessToken({ AccessToken: data.access_token }),
            RefreshToken: new CognitoRefreshToken({
              RefreshToken: data.refresh_token ?? '',
            }),
          })

          const payload = JSON.parse(atob(data.id_token.split('.')[1]))
          const user = new CognitoUser({
            Username: payload['cognito:username'],
            Pool: new CognitoUserPool({
              UserPoolId: "us-east-2_9pPQodJ9a",
              ClientId: CLIENT_ID,
              Storage: window.localStorage,
            }),
            Storage: window.localStorage,
          })

          user.setSignInUserSession(session)

          router.push('/')
        } else {
          console.error('Token response missing expected fields:', data)
        }
      } catch (error) {
        console.error('Token exchange failed:', error)
      }
    }

    handleCallback()
  }, [router])

  return <p>Signing in...</p>
}
