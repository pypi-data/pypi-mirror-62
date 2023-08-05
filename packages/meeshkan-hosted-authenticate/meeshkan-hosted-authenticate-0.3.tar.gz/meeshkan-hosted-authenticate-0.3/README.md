# meeshkan-hosted-authenticate
Utility python package to verify firebase access tokens on meeshkan.io

```python
from meeshkan_hosted_authenticate import verify_token

decoded_token = verify_token(id_token)
uid = decoded_token['uid']
```
