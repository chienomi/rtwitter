# RT/fav Predictor for Twitter

## how to use
```
pip -r requirement.txt
python app.py
```
## API Endpoint
```
http://localhost:8888/api
```

## how to test
```
pytest test.py
```

## Example Requests & Responses

#### Example Request
```
curl http://localhost:8888/api/v1/fav_predictor?text=優しい世界
```
#### Example Response
```
{
    "data": "予測fav数: ⭐⭐⭐ (300+ fav)",
    "status": "success"
}
```
---
#### Example Request
```
curl http://localhost:8888/api/v1/fav_predictor?text=優しい世界！
```
#### Example Response
```
{
    "data": "予測fav数: ⭐⭐ (50 ~ 300 fav)",
    "status": "success"
}
```
---
#### Example Request
```
curl http://localhost:8888/api/v1/fav_predictor?text=招待コードはこちら！無料です！
```
#### Example Response
```
{
    "data": "予測fav数: ⭐️ (~ 50 fav)",
    "status": "success"
}
```
<!--
## method
#### 1. As a preprocessing, categorize twitter into three categories, which are:
0: tweets that will get 0-10 faves (at least 10 min passed since tweeted)
1: tweets that will get 50-300 faves
2: tweets that will get 300+ faves

#### 2. Predict the number of faves of your tweet (up tp 140 characters)
 -->
## TODO
- make a bot
- deploy /rt_predictor
