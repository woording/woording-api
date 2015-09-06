# Wording

## How to use
```bash
# Start api server and web server
./start_all.sh

# Use servers
open http://127.0.0.1:5001/cor
curl http://127.0.0.1:5000/cor

# Stop api server and web server
./stop_all.sh
```



#### How to only use api
```bash
cd api
./initialize.sh
python3 api.py 

# In another terminal window
curl http://127.0.0.1:5000/cor
```

#### How to only use web
```bash
# Start api server first
cd web
python3 site.py

# Go to site
open http://127.0.0.1:5001/
```

#### How to only use login
```bash
cd login
./create-env.sh
python main.py
```

