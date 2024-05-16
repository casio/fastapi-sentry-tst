# check home
GET http://localhost:16000/
HTTP 404

# check docs
GET http://localhost:16000/docs
HTTP 200
[Asserts]
xpath "string(//head/title)" contains "Swagger UI"

# ---- AUTH
# create user
# POST http://localhost:16000/auth/users
# {
#   "email": "some@some.net",
#   "password": "s3cr$t!"
# }
# HTTP 201

# create token
POST http://localhost:16000/auth/users/tokens
{
  "email": "some@some.net",
  "password": "s3cr$t!"
}
HTTP 200
[Captures]
access-token: jsonpath "$['access_token']"
refresh-token: jsonpath "$['refresh_token']"

# show _me_
GET http://localhost:16000/auth/users/me
Authorization: Bearer {{access-token}}
HTTP 200

# ---- EXTERNAL
# apis
GET http://localhost:16000/external-service/apis
Authorization: Bearer {{access-token}}
HTTP 200
