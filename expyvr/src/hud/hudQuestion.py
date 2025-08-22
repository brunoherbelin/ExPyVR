# -*- coding: utf-8 -*-
#===============================================================================
# Copyright (c) 2009-2011 EPFL (Ecole Polytechnique federale de Lausanne) 
# Laboratory of Cognitive Neuroscience (LNCO) 
# 
# ExpyVR is free software ; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation ; either version 2 of the License, or (at your option) any later version.
# 
# ExpyVR is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY ; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along with ExpyVR ; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA.
# 
# Authors : Tobias Leugger leugger.tobias@web.de
#          Bruno Herbelin bruno.herbelin@epfl.ch
#          Nathan Evans   nathan.evans@epfl.ch
# Web site : http://lnco.epfl.ch/expyvr
#===============================================================================

'''
hudText.py
Created on Jan 2012
@author: bruno 
'''

from random import randint
from pyglet.gl import *
import pywidget 
from abstract.AbstractClasses import DrawableHUDModule


class ModuleMain(DrawableHUDModule):
    """
    A  module to display a question and get response
    """
    defaultInitConf = {
        'name': 'hudQuestion',
        'endRoutine': True
    }
    
    defaultRunConf = {    
        'text': 'Any text\nincluding line breaks',
        'posX': 50.0,
        'posY': 50.0,
        'width': 50.0,
        'minimum': 0.0,
        'maximum': 1.0,
        'initial': 'median',
        'step': 0.1,
        'show_value' : False,
        'ticks' : []
    }
    
    confDescription = [
        ('name', 'str', "Question"),
        ('endRoutine', 'bool', "End the current routine when Ok button pressed"),
        ('text', 'str', "The text to be displayed"),
        ('minimum', 'float', "Value on the left of the scale "),  
        ('maximum', 'float', "Value on the right of the scale "),  
        ('initial', 'str', "Initial value", ['minimum', 'median', 'maximum','random']),
        ('step', 'float', "Size of a single step "),  
        ('show_value', 'bool', "Display the current value bellow the cursor"),
        ('ticks', 'code', "Array of strings used as ticks above the scale, e.g. ['low','medium','high']"),
        ('posX', 'float', "Horizontal position in % of the window width "),  
        ('posY', 'float', "Vertical position in % of the window height "),
        ('width', 'float', "Width in % of the window width"),
        ('value', 'info', "Current value of the slider.")
    ]
    
    pause = False
    
    def __init__(self, controller, initConfig=None, runConfigs=None):
        DrawableHUDModule.__init__(self, controller, initConfig, runConfigs)
        
        self.widgets = {}
        self.window_width = 0
        self.window_height = 0
        self.value = 0
        
        for conf in self.runConfs.values():
            # pywidget label (with HTML text)
            txtformated = conf['text'].replace('\n', '<br>')
            txtformated = '<font face="Helvetica,Arial" size=4 color=white>%s</font>'%txtformated
            label = pywidget.Label(width=500, text=txtformated)
            h = label.height
            slider = pywidget.Slider(value=conf['minimum'], minimum=conf['minimum'], maximum=conf['maximum'], step=conf['step'], 
                                     label=conf['show_value'], ticks=conf['ticks'])
            # ok button
            button = pywidget.Button(text="Ok")
            hlayout = pywidget.HBox(width=500, elements=[pywidget.Widget(), button], proportions=[70,30]) 
            # vertical layout
            widget = pywidget.VBox(height = 210, elements=[label,slider,hlayout], proportions=[30, 40, 20]) 
            self.widgets[conf['text']] = widget
            
            @button.event
            def on_button_press(button):
                self.widget._hidden = True
                
            @slider.event
            def on_value_change(value):
                self.value = value
    
    def draw(self, window_width, window_height):
        DrawableHUDModule.draw(self, window_width, window_height)
        
        if self.widget is None:
            return
        
        # resolution changed ? -> recenter and rescale the widget as asked in config
        if self.window_width != window_width or self.window_height != window_height:
            self.window_width = window_width
            self.window_height = window_height
            # adjust widget            
            self.widget.width = self.window_width * self.activeConf['width'] / 100.0 
            self.widget.update_width()
            self.widget.update_height()
            self.widget.x = self.window_width * self.activeConf['posX'] / 100.0 - self.widget.width / 2
            self.widget.y = self.window_height * self.activeConf['posY'] / 100.0 - self.widget.height / 2
            
        # draw the widget
        self.widget.draw()
        
        if self.widget._hidden and self.initConf['endRoutine']:
            self.controller.endCurrentRoutine()
        
    def start(self, dt=0, duration=-1, configName=None):
        """
        Activate the widget with the parameters passed in the conf
        """
        DrawableHUDModule.start(self, dt, duration, configName)
                 
        # choose appropriate widget
        self.widget = self.widgets[self.activeConf['text']]
        
        # set initial value to the slider object of the widget
        if self.activeConf['initial'] == 'minimum':
            self.widget._elements[1].set_cursor(self.activeConf['minimum'])
        elif self.activeConf['initial'] == 'maximum':
            self.widget._elements[1].set_cursor(self.activeConf['maximum'])
        else:
            n = int((self.activeConf['maximum'] - self.activeConf['minimum'])/self.activeConf['step'])
            if self.activeConf['initial'] == 'random':
                self.widget._elements[1].set_cursor(self.activeConf['minimum'] + float(randint(0,n)) * self.activeConf['step'])
            else:
                self.widget._elements[1].set_cursor(self.activeConf['minimum'] + float(n/2) * self.activeConf['step'])
                        
        # register the widget for windows events
        self.controller.registerWidget(self.widget)
        self.controller.registerKeyboardAction('RETURN ENTER', self.onKeyPress)

    def stop(self, dt=0):
        # unregister the widget 
        self.controller.unregisterWidget(self.widget)
        self.controller.unregisterKeyboardAction('RETURN ENTER', self.onKeyPress)
        # stop module
        DrawableHUDModule.stop(self, dt)

    def onKeyPress(self, keypressed=None):
        self.widget._hidden = True
