# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 17:32:47 2013

@author: map
"""
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from wx.glcanvas import GLCanvas
import wx



class MyFrame(wx.Frame):
    """ derive from wx.Frame """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(200,200))
        #self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.canvas = MyGLCanvas(self)
        self.Show(True)
        glutInit()        
        glut_write(5,5, None, "hello")
        #glutSwapBuffers()

class MyGLCanvas(GLCanvas):
    def __init__(self, *args, **kwargs):
        GLCanvas.__init__(self, *args, **kwargs)
        self.width, self.height = self.GetSize()


def glut_write(x, y, font, text):
    if font is None:
        font = GLUT_BITMAP_9_BY_15
        
    glColor3f(0,0,0)
    glRasterPos2f(x,y)
    glutBitmapString(font, text)

app = wx.App(False) # Create new app. Don't redirect stdout/stderr to a window.
frame = MyFrame(None, "Mick's wxApp")
frame.Show(True)
app.MainLoop()
        