import { DataProvider as BaseDataProvider } from "react-admin";
import { fetchUtils } from "react-admin";
import simpleRestProvider from 'ra-data-simple-rest';
import { settings } from '@/settings'
import { CognitoUserPool, CognitoUserSession } from 'amazon-cognito-identity-js';

const internal_url = settings.client.internal_url_domain_name

const userPool = new CognitoUserPool({
  UserPoolId: settings.client.cognito_user_pool_id,
  ClientId: settings.client.cognito_client_id,
});

const getJwtToken = async () => {
  return new Promise((resolve, reject) => {
      const user = userPool.getCurrentUser();

      if (!user) {
          return reject();
      }

      user.getSession((err: Error | null, session: CognitoUserSession | null) => {
        if (err || !session || !session.isValid()) {
            return reject(err ?? new Error('Invalid session'));
        }
    
        const token = session.getIdToken().getJwtToken();
        return resolve(token);
    });
  });
}

const httpClient = async (
  url: string,
  options: fetchUtils.Options = {}
) => {
  const idToken = await getJwtToken()

  const headers = new Headers(options.headers || { Accept: 'application/json' });

  if (idToken) {
    headers.set('Authorization', `Bearer ${idToken}`);
  }

  options.headers = headers;

  return fetchUtils.fetchJson(url, options);
};


const baseDataProvider = simpleRestProvider(internal_url, httpClient)

const structryDataProvider: BaseDataProvider = {
    ...baseDataProvider,
    getAccountInfo: async () => {
      const { json } = await httpClient(`${internal_url}/accounts/me`, {
        credentials: 'include',
      });
  
      return json;
    },
    create: async (resource, params) => {
      if (resource === "documents") {
        const formData = new FormData();
        const { file, structure_id } = params.data;
    
        if (file?.rawFile instanceof File) {
          formData.append("file", file.rawFile);
        } else {
          throw new Error("Missing file");
        }
    
        if (structure_id) {
          formData.append("structure_id", structure_id);
        }
    
        const idToken = await getJwtToken();
    
        return fetch(`${internal_url}/${resource}`, {
          method: "POST",
          body: formData,
          headers: {
            ...(idToken ? { Authorization: `Bearer ${idToken}` } : {}),
          },
        })
          .then((response) => response.json())
          .then((json) => ({ data: json }));
      }
      return baseDataProvider.create(resource, params);
    },
    createSubscription: async (data: { type: string; interval: string }) => {
      const idToken = await getJwtToken();
  
      const response = await fetch(`${internal_url}/accounts/subscriptions`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(idToken ? { Authorization: `Bearer ${idToken}` } : {}),
        },
        body: JSON.stringify(data),
      });
  
      if (!response.ok) {
        const error = await response.text();
        throw new Error(`Subscription error: ${error}`);
      }
  
      const json = await response.json();
      return json; // <-- { url: "..." }
    },
  };
  

export default structryDataProvider;
