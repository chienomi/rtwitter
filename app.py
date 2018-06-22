# -*- coding: utf-8 -*-

# include all files in the working directory
import os
import sys
try:
  sys.path.append(os.getcwd())
except:
  pass

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from tornado import httpserver
from tornado import gen
from tornado.ioloop import IOLoop
import tornado.web
from tornado.web import url
from tornado_json.requesthandlers import APIHandler

from model.interface.rt_prediction_interface import rt_prediction_interface

import sass
sass.compile(
  dirname=('static/scss', 'static/css'),
  output_style='compressed'
)

class RTAPIHandler(APIHandler):
  __url_names__ = ["__self__"]

class WebHandler(tornado.web.RequestHandler):
  def get(self):
    self.render("index.html")

class FAVPredictorHandler(RTAPIHandler):
  def get(self):
    text = self.get_argument("text", "")
    try:
      result = rt_prediction_interface(text)
      self.success(result)
    except:
      self.fails("API could not handle the request.")

def set_up_application():
  application = tornado.web.Application([
    url(r"/?", WebHandler, name="index"),
    (r"/api/v1/fav_predictor?", FAVPredictorHandler)
    ],
    template_path = "template",
    static_path = "static",
    cookie_secret="TODO: cookie_secret for rtwitter",
    xsrf_cookies=True,
    debug=True,
    autoreload=True
  )
  return application

def main():
  app = set_up_application()
  app.listen(8888)
  IOLoop.instance().start()

if __name__ == "__main__":
    main()
