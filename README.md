woording-api
============

[![Join the chat at https://gitter.im/cor/Wording](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/cor/Wording?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


woording-api is a RESTful API that is being used in all other woording projects such as woording-web, woording-ios and woording-android.  

## How to set up woording-api on your machine
```bash
./initalize.sh
./start-server.sh
```

## How it works
All user data gets stored in a SQL database, and database.py let's you use that database with Python functions, api.py uses Flask with a REST plug in and calls those functions.


## How to use the API
You will first need to get a token from the server, to do this, send a POST to request to http://api.woording.com/authenticate   
This post request should have `Content-Type: application/json` in the header and also contain the username and password in json format as data, like this:
```json
{
	"username" : "cor",
	"password" : "Hunter2"
}
```

This will send you a new JSON object containing the token:
```json
{
	"token" : "jkdlf;adsfkjl;adsjkfk;lasdfjkdfjk3849347"
}
```

To retrieve data from the API, use POST requests with the token json object (see above)  
Then, use the super simple url schema
```
http://api.woording.com/cor                    # loads user cor
http://api.woording.com/cor/engelse_woorden    # loads the cor/engelse_woorden list
```

### For registering users, do:
```bash
curl -i -X POST -H "Content-Type: application/json" -d '{"username":"username","password":"password","email":"valid_email"}' http://127.0.0.1:5000/register
```
