# Wording

## How to use api
```bash
# navigate to directory
cd api
# Set up envoirement
./reset-database.sh
./create-env.sh
# Create test data
python3 database_test.py
# Run the API
python3 api.py 


# In another terminal window
curl http://127.0.0.1:5000/cor
```

## How to use web
```bash
cd web
python -m "SimpleHTTPServer"
open http://127.0.0.1:8000/
```

## How to use web/Philip
```bash
cd web/Philip
./create-env.sh
python main.py
```

## How to use web/Leon
- Uncomment line 63 
```bash # @crossdomain(origin='*')```
and make line 56 
```bash api.add_resource(User, '/<username>')``` 
a comment in api.py
- Make sure you start the api script from above too
```bash
cd web/Leon
python -m "SimpleHTTPServer"
open http://127.0.0.1#username
```

