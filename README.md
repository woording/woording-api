woording-api
============

[![Join the chat at https://gitter.im/cor/Wording](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/cor/Wording?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


## How to use
```bash
./initalize.sh
./start-server.sh
```

### For registering users, do:
```bash
curl -i -X POST -H "Content-Type: application/json" -d '{"username":"username","password":"password","email":"valid_email"}' http://127.0.0.1:5000/register
```
