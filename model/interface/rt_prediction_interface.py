from model.brain.rt_predict import rt_predictor

def rt_prediction_interface(text):
  predicted_rt = rt_predictor(text)
  return "予測fav数: " + str(predicted_rt)
