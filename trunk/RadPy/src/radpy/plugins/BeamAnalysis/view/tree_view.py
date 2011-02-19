# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

# This tree model class is based heavily on the tree model class in 
# "Rapid GUI Programming with Qt and Python" by Mark Summerfield.  
# Chapter 16 of that book in the section titled "Representing Tabular
# Data in Trees" provides the best description of the operation of this
# class.  
#
# Copyright (c) 2009 by Radpy.
# http://code.google.com/p/radpy/  

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import Model as Model
COLUMNS = ['File Name','Machine', 'Energy', 'Field Size']
from radpy.plugins.BeamAnalysis.view.ChacoPlot import ChacoPlot, ChacoPlotEditor
from radpy.plugins.BeamAnalysis.view.Plot3D import Plot3D, Plot3DEditor
from radpy.plugins.BeamAnalysis.preferences.api import BeamAnalysisPreferencesHelper

# Enthought library imports.
from enthought.pyface.workbench.api import View
from enthought.traits.api import HasTraits, Str, List, Dict
from enthought.traits.ui.api import Item, SetEditor
from enthought.traits.ui.api import View as TraitsView
from enthought.traits.ui.menu import OKButton, CancelButton
#from enthought.etsconfig.api import ETSConfig
#from enthought.preferences.api import Preferences
#from os.path import join

class MatchDialog(HasTraits):
    choices = List(Str)
    selection = List(Str)
    
    view = TraitsView(Item('selection', editor=SetEditor(name='choices',
                    can_move_all=True, ordered=False),show_label=False),
                    buttons = [OKButton, CancelButton],kind='livemodal')


    


class TreeWidget(QTreeView):
    #The window that organizes scans from opened files in a tree
    #structure.  The branches of the tree are defined by the 
    #COLUMNS global variable defined at the top of this file.
    #activate_event = Event
    
    def __init__(self, parent=None):
        super(TreeWidget, self).__init__(parent)
        self.setSelectionBehavior(QTreeView.SelectItems)
        self.setUniformRowHeights(True)
        self.setSortingEnabled(True)
        
        model = Model.TreeModel(COLUMNS, self)
        
        #The ProxyModel acts as a wrapper to the underlying
        #tree model and enables custom sorting of tree columns.
        #For example, it can sort field sizes by equivalent 
        #square instead of strictly alphabetically.
        proxy = Model.ProxyModel(self)
        proxy.setDynamicSortFilter(True)
        proxy.setSourceModel(model)
        self.setModel(proxy)
        
        
        self.connect(self, SIGNAL("activated(QModelIndex)"),
                     self.activated)
        self.connect(self, SIGNAL("expanded(QModelIndex)"),
                     self.expanded)
        self.expanded()
        self.load("radpy/plugins/BeamAnalysis/view/RFB/Unit Tests/Test1.rfb")
        #self.load("c:/users/steve/desktop/xml test/test.xml")
        #self.load("radpy/plugins/BeamAnalysis/view/DicomRT/tests/3d_dose_wedge.dcm")
      
        
    def load(self, filename):
        #Passes lists of scans to tree model class.
        nesting = len(COLUMNS)
        try:
            self.model().load(filename, nesting, COLUMNS)
        except IOError, e:
            QMessageBox.warning(self, "Server Info - Error",
                                unicode(e))
#        except PlanError as e:
#            QMessageBox.warning(self,'''Gantry and collimator angles must be 0 
#                (IEC Scale).  Instead the plan has a gantry angle of ''' + \
#                str(e.gantry) + ' and a collimator angle of ' + \
#                str(e.collimator) + '.')
            
    def currentFields(self):
        return self.model().asRecord(self.currentIndex())


    def activated(self, index):
       
        self.emit(SIGNAL("activated"), self.model().asRecord(index))
        #self.activated = self.model().asRecord(index)

    def expanded(self):
        for column in range(self.model().columnCount(QModelIndex())):
            self.resizeColumnToContents(column)
            
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        
        if isinstance(self.model().nodeFromIndex(self.currentIndex()),
                      Model.LeafNode):
                     
            addAction = menu.addAction("&Add to plot")        
            self.connect(addAction, SIGNAL("triggered()"), self.addPlot)
            
            editAction = menu.addAction("&Edit beam parameters")
            self.connect(editAction, SIGNAL("triggered()"), self.editPlot)
            
        else:
            
            addMultiAction = menu.addAction("&Add all to plot")
            self.connect(addMultiAction, SIGNAL("triggered()"), self.addMultiPlot)
            
            addAsRefAction = menu.addAction("Add &matching beams")
            self.connect(addAsRefAction, SIGNAL("triggered()"), self.addAsRef)
            
        menu.exec_(event.globalPos())
        
    def editPlot(self):
        self.currentFields()[1].edit_traits()
        

    def addPlot(self):
        self.emit(SIGNAL("activated"), self.currentFields())
        
    def addMultiPlot(self):
        temp  = self.model().asRecord(self.currentIndex())
        for i in temp:
            self.emit(SIGNAL('activated'), i)
    
    def addAsRef(self):
        
        #app_home = ETSConfig.get_application_home()
       
        helper = BeamAnalysisPreferencesHelper()
        choices = {'Energy':'BeamDetails_Energy',
                   'Field Size':'field_size',
                   'Scan Type':'scan_type',
                   'SSD':'BeamDetails_SSD',
                   'Wedge Angle':'BeamDetails_Wedge_Angle',
                   'Applicator':'BeamDetails_Applicator',
                   'Linac Model':'BeamDetails_RadiationDevice_Model'}
        
        dialog = MatchDialog(choices=choices.keys())
        dialog.selection = helper.match_traits
        dialog.configure_traits()
        match_traits = [choices[x] for x in dialog.selection[:]]
        helper.match_traits = dialog.selection
        helper.preferences.flush()
        
        temp  = self.model().asRecord(self.currentIndex())
        for i in temp:
            self.emit(SIGNAL('reference'), i, match_traits)
            
   
class TreeView(View):
    
    name = 'TreeView'
    id = 'radpy.plugins.BeamAnalysis.TreeView'         
    def __init__(self, *args, **kwds):    
        super(View, self).__init__()
        self.widget = TreeWidget()
        QObject.connect(self.widget, SIGNAL('activated'),self.activated)
        QObject.connect(self.widget, SIGNAL('reference'), self.reference)
    
#    def _id_default(self):
#        """ Trait initializer. """
#
#        return self.id
    def reference(self, record, parameters):
        label, beam = record
        if self.window.active_editor is not None:
            for i in self.window.active_editor.obj.beams.values():
                traits_to_match =  beam.trait_get(parameters)
                if i.does_it_match(traits_to_match):
                    title = self.window.active_editor.obj.add_plot(label, beam)
                    if title is not None:
                        self.window.active_editor.name = title
            
        
    def activated(self, record):
        """ Adds the selected beam object to the active Chaco Plot editor.  If
        there is no active window, it creates one first.  If the active editor
        is not the right scan type (crossplane etc.) then it creates a new one.
        """
        
        label, beam = record
        scan_type_list = ['None', beam.get_scan_type()]
        if self.window.active_editor is not None:
            
            if self.window.active_editor.obj.plot_type in scan_type_list:
                title = self.window.active_editor.obj.add_plot(label, beam)
                if title is not None:
                    self.window.active_editor.name = title
            else:
                self.create_new_plot_editor(label, beam)
        
        #If the tree view is undocked, there may not be an active_editor 
        #property, even if there is an active editor. 
          
        elif len(self.window.editors) > 0:   
            
            if self.window.editors[-1].obj.plot_type in scan_type_list:
                title = self.window.editors[-1].obj.add_plot(label, beam)
                if title is not None:
                    self.window.editors[-1].name = title
            else: 
                self.create_new_plot_editor(label, beam)
        
        else:
            
            self.create_new_plot_editor(label, beam)
          
    def create_new_plot_editor(self, label, beam):
        """Create new ChacoPlot editor window"""
        tmp = beam.get_scan_descriptor()
        if beam.get_scan_descriptor() == "Dicom_3D_Dose":
            plot = Plot3D()
            self.window.workbench.edit(plot, kind=Plot3DEditor)
        else:   
            plot = ChacoPlot()
            self.window.workbench.edit(plot, kind=ChacoPlotEditor)
        title = self.window.editors[-1].obj.add_plot(label, beam)
        self.window.editors[-1].name = title
        self.window.editors[-1].set_focus()
        
    

    #### Methods ##############################################################

    def create_control(self, parent):
       
        return self.widget
        
    

#### EOF ######################################################################
