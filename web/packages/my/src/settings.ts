const isDev = process.env.NODE_ENV === 'development';
//
//export const server = {
//    cognito_client_id: process.env.COGNITO_CLIENT_ID ? process.env.COGNITO_CLIENT_ID : "",
//    my_domain_name: process.env.MY_DOMAIN_NAME ? process.env.MY_DOMAIN_NAME : '',
//    cognito_auth_domain_name: process.env.COGNITO_AUTH_DOMAIN_NAME ? process.env.COGNITO_AUTH_DOMAIN_NAME : '',
//    my_s3_bucket_domain_name: `https://${process.env.MY_S3_BUCKET_DOMAIN_NAME}` || '',
//
//}
//
//export const client = {
//    cognito_client_id: process.env.NEXT_PUBLIC_COGNITO_CLIENT_ID ? process.env.NEXT_PUBLIC_COGNITO_CLIENT_ID : '',
//    my_domain_name: process.env.NEXT_PUBLIC_MY_DOMAIN_NAME ? process.env.NEXT_PUBLIC_MY_DOMAIN_NAME : '',
//    cognito_auth_domain_name: process.env.NEXT_PUBLIC_COGNITO_AUTH_DOMAIN_NAME ? process.env.NEXT_PUBLIC_COGNITO_AUTH_DOMAIN_NAME : '',
//    api_url_domain_name: process.env.NEXT_PUBLIC_API_URL_DOMAIN_NAME ? process.env.NEXT_PUBLIC_API_URL_DOMAIN_NAME : '',
//
//}

export const server = {
    cognito_client_id: process.env.COGNITO_CLIENT_ID ? process.env.COGNITO_CLIENT_ID : "",
    my_domain_name: process.env.MY_DOMAIN_NAME ? process.env.MY_DOMAIN_NAME : '',
    cognito_auth_domain_name: process.env.COGNITO_AUTH_DOMAIN_NAME ? process.env.COGNITO_AUTH_DOMAIN_NAME : '',
    my_s3_bucket_domain_name: process.env.MY_S3_BUCKET_DOMAIN_NAME || ''

}

export const client = {
    cognito_client_id: process.env.NEXT_PUBLIC_COGNITO_CLIENT_ID ? process.env.NEXT_PUBLIC_COGNITO_CLIENT_ID : '',
    cognito_user_pool_id: process.env.NEXT_PUBLIC_COGNITO_USER_POOL_ID ? process.env.NEXT_PUBLIC_COGNITO_USER_POOL_ID : '',
    my_domain_name: process.env.NEXT_PUBLIC_MY_DOMAIN_NAME ? process.env.NEXT_PUBLIC_MY_DOMAIN_NAME : '',
    cognito_auth_domain_name: process.env.NEXT_PUBLIC_COGNITO_AUTH_DOMAIN_NAME ? process.env.NEXT_PUBLIC_COGNITO_AUTH_DOMAIN_NAME : '',
    internal_url_domain_name: process.env.NEXT_PUBLIC_INTERNAL_URL_DOMAIN_NAME ? process.env.NEXT_PUBLIC_INTERNAL_URL_DOMAIN_NAME : '',
    www_domain_name: process.env.NEXT_PUBLIC_WWW_DOMAIN_NAME ? process.env.NEXT_PUBLIC_WWW_DOMAIN_NAME : '',
}

export const settings = {
    isDev,
    "server": {...server},
    "client": {...client}
}