woording-api
============

[![Join the chat at https://gitter.im/cor/Wording](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/cor/Wording?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


woording-api is a RESTful API that is being used in all other woording projects such as woording-web, woording-ios and woording-android.  

## How to set up woording-api on your machine
First, install `docker`, after that do this
```bash
docker build -t woording-api .
docker run -P -d -v /Users/cor/Developer/woording/woording-api:/source-files woording-api
```
Now run `docker ps` and look for the correct container, and use the mapped port to access the api

## How it works
All user data gets stored in a SQL database, and database.py let's you use that database with Python functions, api.py uses Flask with a REST plug in and calls those functions.


## How to use the API
For full explaination of all different requests, please check the wiki.

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

### How to handle error respones
This is done just by using the standard http status codes wich are defined [here](http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html). I will short descripe some examples of when you get what error below.

##### 400 - Bad request
You get this error when your request is not in JSON format and/or you did not fill in all needed fields. E.g. sending an authorization request without sending an password.

##### 401 - Unauthorized
When you send an expired token or a wrong token get this error. NOTE: When you send no token you get a bad request (400) error.
