from model.param.rtwitter import *
from model.generator.generate_data import *
from keras.models import load_model

model_status_quo = load_model(MODEL_PATH)

def rt_predictor(l, max_length=INPUT_LENGTH):
  # predict number of favs
  # CNN モデルでの判定
  x_vec = phrase_to_numpy_array(l).reshape(-1,max_length)
  out_prob = model_status_quo.predict(x_vec)
  out = np.argmax(out_prob[0])
  if out == 0:
    result = "⭐️ (~ 50 fav)"
  elif out == 1:
    result = "⭐⭐ (50 ~ 300 fav)"
  elif out == 2:
    result = "⭐⭐⭐ (300+ fav)"
  if np.max(out_prob[0]) > 0.9:
    result += "（断言）"
  return result
