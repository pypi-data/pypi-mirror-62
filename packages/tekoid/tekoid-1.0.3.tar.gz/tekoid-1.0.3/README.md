# Identity Client Library Python

## How to install
- use pip:
    ```py
    pip install tekoid
    ```

## How to use

- First, import `ClientSDK` into your sourcecode. I.E:

```py
from tekoid import ClientSDK
```


- Second, you need to instantiate ClientSDK. See example:

```py
clientSDK = ClientSDK(client_id=os.getenv("CLIENT_ID"),
                      client_secret=os.getenv("CLIENT_SECRET"),
                      redirect_uri="http://localhost:5000/callback")
```

Note: `redirect_uri` must be declare in iam admin system

|addition field    |type   |default                   |                                
|------------------|-------|--------------------------|
|scope             |array  |[openid,profile]          |                                    
|base_uri          |string |https://oauth.tekoapis.com|                                    
|authorize_path    |string |/oauth/authorize          |                                    
|token_path        |string |/oauth/token              |                                    
|refresh_token_path|string |/oauth/token              |                                    
|revoke_token_path |string |/oauth/revoke             |                                    
|jwks_path         |string |/.well-known/jwks.json    |                                    
|verify_ssl        |boolean|True                      |                          


- Support function:
    - get_authorization_url():
        - return url, state 
        
    - get_token(url, state): 
        - use for authorization code flow, pass url get from authorization server and state get above
        - return token data 
        
    - get_token(): 
        - use for client credentials flow
        - return token data
        
    - get_user_info(token): 
        - pass id_token get above
        - return user data
    - refresh_token(refresh_token):
        - pass refresh token get from get_token()
        - return new token data
        
- you can see the sample code at
https://github.com/teko-vn/tekoid-py/blob/master/example/app.py

## Support
- vietnk: viet.nk@teko.vn
