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

python3 -m http.server
open http://127.0.0.1:5001/
```

## How to use web/Philip
```bash
cd web/Philip
./create-env.sh
python main.py
```

