from typing import Union

from fastapi import FastAPI
import redis
import debugpy  # For debugging

# Debug
debugpy.listen(("0.0.0.0", 5678))

# Create the FastAPI app
app = FastAPI()
redis = redis.Redis(host="redis", port=6379)

# Routes


# Root route
@app.get("/")
def read_root():
    return {"Container FastAPI and Docker!"}


# Each call increments a counter in redis
@app.get("/hits")
def get_hits():
    hits = redis.incr("hits", 1)
    return {"hits": hits}
