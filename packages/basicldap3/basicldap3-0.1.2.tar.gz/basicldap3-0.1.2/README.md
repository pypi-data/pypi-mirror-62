# Basic LDAP3

Basic LDAP is a small package that uses the ldap3 library. It can be used to authenticate a user against an LDAP server and can check whether the users is in a specific group. In addition it is possible to get user attributes if the authentication is successful.

## Basic example

### Import basicldap and define the server
```python
from basicldap import Ldap

LDAP_HOST = 'ldap.server.com'
LDAP_BASE_DN = 'DC=example,DC=com'

conn = Ldap(LDAP_HOST, LDAP_BASE_DN)

# Using SSL
ssl = {"port": 636, "use_ssl": True}
conn = Ldap(LDAP_HOST, LDAP_BASE_DN, ldap3_args=ssl)
```
### Authenticate the user
```python
conn.authenticate(user_name, password)
```

### Get user attributes (requires successful authentication)
```python
# To get all attributes
conn.get_attributes()

# To get specific attributes
conn.get_attributes(['mail', 'cn])
```