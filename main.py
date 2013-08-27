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

#===================================================================================================
class myGLCanvas(GLCanvas):
    def __init__(self, *args, **kwargs):
        GLCanvas.__init__(self, *args, **kwargs)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnResize)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        self.Bind(wx.EVT_MOTION, self.OnMouse)

        self.init = False
        self.width, self.height = self.GetSize()

        self.alpha = 0
        self.beta = 0
        self.distance = 5.0

        self.oldX = 0
        self.oldY = 0
        self.leftDown = False
        self.rightDown = False

        self.axes = False

    #-----------------------------------------------------------------------------------------------
    def Axes(self, allow):
        self.axes = allow

    def SomeText(self):        
        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)
        glColor3f(0.0, 1.0, 0.0)
        glRasterPos3f(0, 0, 0.0)
        #glutBitmapString(GLUT_BITMAP_9_BY_15, "abcdef")        
        glutBitmapString(GLUT_BITMAP_9_BY_15, "Some text")
        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)
    
    #-----------------------------------------------------------------------------------------------
    def OnDraw(self):
        glutInit()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (0.5, 0.5, 1.0, 1.0))
        glutSolidSphere(0.5, 20, 20)

        if self.axes:
            self.ShowAxes()
            
        self.SomeText() 
        self.SwapBuffers()

    #-----------------------------------------------------------------------------------------------
    def ChangeView(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslate(0.0, 0.0, -self.distance)
        glRotate(-90, 0.0, 1.0, 0.0)
        glRotate(-90, 1.0, 0.0, 0.0)

        glRotate(self.alpha, 0.0, 0.0, 1.0)
        glRotate(self.beta, 0.0, 1.0, 0.0)

        self.OnDraw()

    #-----------------------------------------------------------------------------------------------
    def Resize(self):
        ratio = float(self.width) / self.height;

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glViewport(0, 0, self.width, self.height)
        gluPerspective(45, ratio, 1, 1000)

        self.ChangeView()

    #-----------------------------------------------------------------------------------------------
    def OnPaint(self, event):
        wx.PaintDC(self)
        self.SetCurrent()
        if not self.init:
            self.InitGL()
            self.init = True
        self.OnDraw()

    #-----------------------------------------------------------------------------------------------
    def OnLeftDown(self, event):
        self.oldX, self.oldY = event.GetPosition()
        self.leftDown = True

    def OnRightDown(self, event):
        self.oldX, self.oldY = event.GetPosition()
        self.rightDown = True

    def OnLeftUp(self, event):
        self.leftDown = False

    def OnRightUp(self, event):
        self.rightDown = False

    def OnMouse(self, event):
        if self.leftDown or self.rightDown:
            X, Y = event.GetPosition()
            if self.rightDown:
                self.distance += (Y - self.oldY) * 0.05

            if self.leftDown:
                self.alpha += (X - self.oldX) * 0.5
                self.beta += (Y - self.oldY) * 0.5

            self.ChangeView()
            self.oldX, self.oldY = X, Y

    #-----------------------------------------------------------------------------------------------
    def OnResize(self, e):
        self.width, self.height = e.GetSize()
        self.Resize()

    #-----------------------------------------------------------------------------------------------
    def ShowAxes(self):
        glDisable(GL_LIGHTING)

        glColor3f(1.0, 1.0, 0.0)
        glRasterPos3f(1.2, 0.0, 0.0)
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord('x'))
        glRasterPos3f(0.0, 1.2, 0.0)
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord('y'))
        glRasterPos3f(0.0, 0.0, 1.2)
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord('z'))

        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_QUADS)
        glVertex3f(0, 0, 0)
        glVertex3f(1, 0, 0)
        glVertex3f(1, 1, 0)
        glVertex3f(0, 1, 0)
        glEnd()
        glColor3f(0.0, 1.0, 0.0)
        glBegin(GL_QUADS)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 1)
        glVertex3f(0, 1, 1)
        glVertex3f(0, 1, 0)
        glEnd()
        glColor3f(0.0, 0.0, 1.0)
        glBegin(GL_QUADS)
        glVertex3f(0, 0, 0)
        glVertex3f(1, 0, 0)
        glVertex3f(1, 0, 1)
        glVertex3f(0, 0, 1)
        glEnd()

        glEnable(GL_LIGHTING)

    #-----------------------------------------------------------------------------------------------
    def InitGL(self):
        glLightfv(GL_LIGHT0, GL_DIFFUSE,  (0.8, 0.8, 0.8, 1.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT,  (0.2, 0.2, 0.2, 1.0))
        glLightfv(GL_LIGHT0, GL_POSITION, (1.0, 1.0, 1.0, 0.0))
        glEnable(GL_LIGHT0)

#        glShadeModel(GL_SMOOTH)
        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0)

        self.Resize()

#===================================================================================================
class ToolPanel(wx.Panel):
    def __init__(self, parent, canvas, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.canvas = canvas

        self.button1 = wx.Button(self, label="TEXT 1")
        self.button2 = wx.Button(self, label="TEXT 2")
        self.check1 = wx.CheckBox(self, label="Show Axes")
        self.Bind(wx.EVT_CHECKBOX, self.Check1)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.button1, flag=wx.BOTTOM, border=5)
        self.sizer.Add(self.button2, flag=wx.BOTTOM, border=5)
        self.sizer.Add(self.check1)

        self.border = wx.BoxSizer()
        self.border.Add(self.sizer, flag=wx.ALL | wx.EXPAND, border=5)

        self.SetSizerAndFit(self.border)

    #-----------------------------------------------------------------------------------------------
    def Check1(self, e):
        self.canvas.Axes(e.Checked())
        self.canvas.OnDraw()

#===================================================================================================
class MainWin(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, title='OpenGL', *args, **kwargs)

        self.canvas = myGLCanvas(self, size=(640, 480))
        self.panel = ToolPanel(self, canvas=self.canvas)

        self.sizer = wx.BoxSizer()
        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        self.sizer.Add(self.panel, 0, wx.EXPAND)
        self.SetSizerAndFit(self.sizer)

        self.Show()

#===================================================================================================
app = wx.App(False)
main_win = MainWin(None)
app.MainLoop()