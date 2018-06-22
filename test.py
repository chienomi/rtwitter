# coding: utf-8
import pytest
import unittest
import time

from model.brain.rt_predict import *

class TestRTwitter(unittest.TestCase):
  def test_brain_basic(self):
    assert rt_predictor("優しい世界")[0:4] == '⭐⭐⭐ '
    assert rt_predictor("招待コードだよ！無料です！")[0:3] == '⭐️ '
  def test_brain_long(self):
    assert rt_predictor("a0あ亜"*1000)[0:3] == '⭐️ '
  def test_brain_blank(self):
    assert rt_predictor("")[0:3] == '⭐️ '
