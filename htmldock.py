#!/usr/bin/python

import os
import gtk 
import wnck
import json
import time
import webkit

view = webkit.WebView() 

sw = gtk.ScrolledWindow() 
sw.add(view) 

win = gtk.Window(gtk.WINDOW_TOPLEVEL) 
win.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DOCK)
win.set_keep_above(True)
w = 400
h = 12
win.set_size_request(w, h)
screen = win.get_screen()
win.move(screen.get_width()-w, screen.get_height()-h)
win.set_decorated(False)
win.set_has_frame(False)
win.add(sw) 
win.show_all() 

view.open('file://'+os.path.dirname(os.path.abspath(__file__)) + '/htmldock.html') 

screenW = wnck.screen_get_default();
screenW.force_update()

def get_window_by_xid(xid):
  windows = screenW.get_windows()
  for window in windows:
    if window.get_xid() == int(xid):
      return window
  return False

def title_changed(widget, frame, title):
  if title == 'getWindowslist':
    send_windows()
  elif title != 'null':
    #print "title changer: " + title
    window = get_window_by_xid(title)
    if window:
      #print "window clicked: " + window.get_name()
      now = gtk.gdk.x11_get_server_time(gtk.gdk.get_default_root_window())
      window.activate(now)

def send_windows():
  windows = screenW.get_windows()
  list = []
  for window in windows:
    if window.get_window_type().value_name == 'WNCK_WINDOW_NORMAL':
      list.append({ 'name': window.get_name(), 
                           'app_name': window.get_application ().get_name(),
                           'xid' : window.get_xid() })
  view.execute_script('wnckWindows('+json.dumps(list)+');')

def window_opened(widget, frame):
  send_windows()

view.connect('title-changed', title_changed)
screenW.connect('window-opened', window_opened)
screenW.connect('window-closed', window_opened)

gtk.main()

#time.sleep(1)
print "test test"
send_windows() # actually we dont need cause we open a window, but sometime the javascript is not ready