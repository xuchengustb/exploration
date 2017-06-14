#!/usr/bin/python

import rospy
from planner import *
from exploration.msg import MarkerPath, MarkerState

COLOR_BLACK   = [   0,   0,   0]
COLOR_RED     = [ 255,   0,   0]
COLOR_YELLOW  = [ 255, 255,   0]
COLOR_GREEN   = [   0, 255,   0]
COLOR_CYAN    = [   0, 255, 255]
COLOR_BLUE    = [   0,   0, 255]
COLOR_MAGENTA = [ 255,   0, 255]
COLOR_WHITE   = [ 255, 255, 255]

PIXELS_SPECTRUM = [COLOR_RED, COLOR_YELLOW, COLOR_GREEN, COLOR_CYAN, COLOR_BLUE, COLOR_MAGENTA]
PIXELS_BLACK    = 6*[COLOR_BLACK]
PIXELS_WHITE    = 6*[COLOR_WHITE]

def states_to_path(self, pixel_states=[PIXELS_SPECTRUM], stamp=None):
  marker_path = empty_stamped_path(MarkerPath,stamp)
  marker_path.states = [MarkerState(reduce(list.__add__,state)) for state in pixel_states]
  return marker_path

class MarkerPlanner(Planner):
  def __init__(self, node_name='marker_planner'):
    super(MarkerPlanner, self).__init__(MarkerPath, node_name)

  def states_to_path(self, pixel_states=[PIXELS_SPECTRUM], stamp=None):
    marker_path = self.empty_stamped_path(stamp)
    marker_path.states = [MarkerState(reduce(list.__add__,state)) for state in pixel_states]
    return marker_path

  def set_markers(self, pixel_states=[PIXELS_SPECTRUM], stamp=None):
    self.goal_pub.publish(self.states_to_path(pixel_states,stamp))
    
  def spectrum_demo(self):
    rotation = []
    for i in range(6):
      rotation.extend(5*[PIXELS_SPECTRUM[i:] + PIXELS_SPECTRUM[:i]])
    rotation.extend([PIXELS_BLACK])
    rate = rospy.Rate(1.0/4.0)
    while not rospy.is_shutdown():
      self.set_markers(rotation)
      rate.sleep()

if __name__ == '__main__':
  mp = MarkerPlanner()
  mp.spectrum_demo()
