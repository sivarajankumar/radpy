'''
Created on Nov 7, 2010

@author: Steve
'''

from radpy.plugins.BeamAnalysis.view.beam_xml import Beam
from RTDoseRead import RTDose

class DicomBeam(Beam):
    
    def __init__(self):
        super(DicomBeam, self).__init__()
        
    def get_scan_descriptor(self):
        return "Dicom_3D_Dose"


def load_dicom_data(infile):
    """Read in a file in RFB format and return a list of Beam objects"""
    
    
    
    f = RTDose(infile)
           
    xml_class = DicomBeam()
    xml_class.BeamDetails_CollimatorAngle = f.collimator_angle
    xml_class.BeamDetails_GantryAngle = f.gantry_angle
    xml_class.BeamDetails_Energy = float(f.energy)
    #xml_class.BeamDetails_RadiationDevice_Model = f.machine
    xml_class.Data = f
    #For right now, assume x is crossplane direction and y is inplane
    xml_class.BeamDetails_CrossplaneJawPositions_NegativeJaw = -f.coll_x_neg
    xml_class.BeamDetails_CrossplaneJawPositions_PositiveJaw = f.coll_x_pos
    xml_class.BeamDetails_InplaneJawPositions_NegativeJaw = -f.coll_y_neg
    xml_class.BeamDetails_InplaneJawPositions_PositiveJaw = f.coll_y_pos
    xml_class.BeamDetails_Particle = f.particle
    try:
        xml_class.BeamDetails_Wedge_Type = f.wedge_type
        xml_class.BeamDetails_Wedge_Angle = f.wedge_angle
    except:
        pass
    xml_class.MeasurementDetails_Isocenter_x = f.isocenter[0]
    xml_class.MeasurementDetails_Isocenter_y = f.isocenter[1]
    xml_class.MeasurementDetails_Isocenter_z = f.isocenter[2]
    xml_class.MeasurementDetails_MeasuringDevice_Manufacturer = f.meas_manu
    xml_class.MeasurementDetails_MeasuringDevice_Model = f.meas_model
    xml_class.BeamDetails_RadiationDevice_Vendor = f.rad_vend
    xml_class.BeamDetails_RadiationDevice_Model = f.rad_model
    xml_class.BeamDetails_RadiationDevice_SerialNumber = f.rad_serial
#    xml_class.Data_Abscissa = i.abscissa
#    xml_class.Data_Ordinate = i.ordinate
#    xml_class.initialize_traits()
#    b.append(xml_class)
#    f.close()
    return [xml_class]
    
