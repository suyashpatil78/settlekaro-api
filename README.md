## How to run Docker locally

```
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" settlekaro-api sh -c "flask run --host 0.0.0.0"
```