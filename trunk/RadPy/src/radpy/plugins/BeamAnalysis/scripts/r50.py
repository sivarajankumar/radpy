# Major library imports.
import numpy
import scipy
from scipy import interpolate

## Enthought library imports.
from enthought.traits.ui.api import Item

class UserParameter(object):
       
    name = 'r50'
    style = 'readonly'
    #tooltip = 'Smooth the scan plot'
    visible_when = 'scan_type == "Depth Dose"'
    #format_func = lambda v: '%.2f' % v 
    
    
    
    def get_item(self):
        
        return Item(name = self.name, style = self.style,
                                visible_when = self.visible_when,
                                format_func = lambda v: '%.2f' % v)
        
    def calc(self, beam):
        
        dmax = beam.abscissa[numpy.argmax(beam.ordinate)]
        x_axis = numpy.where(beam.abscissa > dmax)
        tck = interpolate.splrep(beam.abscissa[x_axis], 
                                 beam.ordinate[x_axis])
        return interpolate.splev(50, tck)