woording-api
============

[![Join the chat at https://gitter.im/cor/Wording](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/cor/Wording?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


## How to use
```bash
./initalize.sh
./start-server.sh
```

### Other required plugins
```bash
npm install ng-dialog
```

## How to use the API
You will need to get a token from the server, to do this, send a POST to request to http://api.woording.com/authenticate containing the username and password in json format, for example:
```json
{
	"username" : "cor",
	"password" : "Hunter2"
}
```

This will send you a new JSON object containing the token:
```
{
	"token" : "jkdlf;adsfkjl;adsjkfk;lasdfjkdfjk3849347"
}
```

### For registering users, do:
```bash
curl -i -X POST -H "Content-Type: application/json" -d '{"username":"username","password":"password","email":"valid_email"}' http://127.0.0.1:5000/register
```
