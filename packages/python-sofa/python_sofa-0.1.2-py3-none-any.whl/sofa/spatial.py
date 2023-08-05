# Copyright (c) 2019 Jannika Lossner
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

__all__ =["Coordinates", "Set", "Object"]

from .datatypes import dimensions

from . import access
import numpy as np

# for coordinate transformations
from scipy.spatial.transform import Rotation ## requires scipy 1.2.0

def sph2cart(alpha, beta, r):
    r"""Spherical to cartesian coordinate transform.
    .. math::
        x = r \cos \alpha \sin \beta \\
        y = r \sin \alpha \sin \beta \\
        z = r \cos \beta
    with :math:`\alpha \in [0, 2\pi), \beta \in [0, \pi], r \geq 0`
    Parameters
    ----------
    alpha : float or array_like
            Azimuth angle in radians
    beta : float or array_like
            Colatitude angle in radians (with 0 denoting North pole)
    r : float or array_like
            Radius
    Returns
    -------
    x : float or `numpy.ndarray`
        x-component of Cartesian coordinates
    y : float or `numpy.ndarray`
        y-component of Cartesian coordinates
    z : float or `numpy.ndarray`
        z-component of Cartesian coordinates
    """
    x = r * np.cos(alpha) * np.sin(beta)
    y = r * np.sin(alpha) * np.sin(beta)
    z = r * np.cos(beta)
    return x, y, z

def cart2sph(x, y, z):
    r"""Cartesian to spherical coordinate transform.
    .. math::
        \alpha = \arctan \left( \frac{y}{x} \right) \\
        \beta = \arccos \left( \frac{z}{r} \right) \\
        r = \sqrt{x^2 + y^2 + z^2}
    with :math:`\alpha \in [-pi, pi], \beta \in [0, \pi], r \geq 0`
    Parameters
    ----------
    x : float or array_like
        x-component of Cartesian coordinates
    y : float or array_like
        y-component of Cartesian coordinates
    z : float or array_like
        z-component of Cartesian coordinates
    Returns
    -------
    alpha : float or `numpy.ndarray`
            Azimuth angle in radians
    beta : float or `numpy.ndarray`
            Colatitude angle in radians (with 0 denoting North pole)
    r : float or `numpy.ndarray`
            Radius
    """
    r = np.sqrt(x**2 + y**2 + z**2)
    alpha = np.arctan2(y, x)
    beta = np.arccos(z / np.where(r != 0, r, 1))
    return alpha, beta, r

def transform(u, rot, x0, invert):
    if not invert: u = u-x0
    t = rot.apply(u, inverse= not invert)
    if invert: t = t + x0
    return t

class Coordinates(access.ArrayVariable):
    """Specialized :class:`sofa.access.ArrayVariable` for spatial coordinates"""
    class System:
        """Enum of valid coordinate systems"""
        Cartesian = "cartesian"
        Spherical = "spherical"
        
        class Units:
            Meter = {"meter", "metre", "m"}
            Degree = {"degree", "°", "deg"}
            Radians = {"radians", "rad"}
            
        @staticmethod
        def convert_angle_units(coords, dimensions, old_units, new_units):
            """
            Parameters
            ----------
            coords : array_like
                Array of spherical coordinate values
            dimensions : tuple of str
                Names of the array dimensions in order, must contain "C"
            old_units : str
                Units of the angle values in the array
            new_units : str
                Target angle units

            Returns
            -------
            new_coords : np.ndarray
                Array of converted spherical coordinate values in identical dimension order
            """
            if dimensions == None: raise Exception("missing dimension order for unit conversion")
            if new_units == None: return coords
            if old_units == None: raise Exception("missing original unit for unit conversion")

            conversion = np.ones_like(coords)
            indices = access.get_slice_tuple(dimensions, {"C":slice(2)})
            
            if (old_units in Coordinates.System.Units.Degree and new_units in Coordinates.System.Units.Degree) or (old_units in Coordinates.System.Units.Radians and new_units in Coordinates.System.Units.Radians):
                return coords
            elif old_units in Coordinates.System.Units.Degree and new_units in Coordinates.System.Units.Radians: 
                conversion[indices] = np.pi/180
            elif old_units in Coordinates.System.Units.Radians and new_units in Coordinates.System.Units.Degree: 
                conversion[indices] = 180/np.pi
            else: raise Exception("invalid angle unit in conversion from {0} to {1}".format(old_units, new_units))

            return np.multiply(coords, conversion)

        @staticmethod
        def convert(coords, dimensions, old_system, new_system, old_angle_unit=None, new_angle_unit=None): #need to take care of degree/radians unit mess.
            """
            Parameters
            ----------
            coords : array_like
                Array of coordinate values
            dimensions : tuple of str
                Names of the array dimensions in order, must contain "C"
            old_system : str
                Coordinate system of the values in the array
            new_system : str
                Target coordinate system
            old_angle_unit : str, optional
                Unit of the angular spherical coordinates
            new_angle_unit : str, optional
                Target unit of the angular spherical coordinates

            Returns
            -------
            new_coords : np.ndarray
                Array of converted coordinate values in identical dimension order
            """
            if dimensions == None: raise Exception("missing dimension order for coordinate conversion")
            if new_system == None or old_system == new_system:
                if old_system != Coordinates.System.Spherical: return coords
                return Coordinates.System.convert_angle_units(coords, dimensions, old_angle_unit, new_angle_unit)

            old = None
            conversion = None
            if old_system == Coordinates.System.Cartesian and new_system == Coordinates.System.Spherical: 
                conversion = cart2sph
                old = coords
            elif old_system == Coordinates.System.Spherical and new_system == Coordinates.System.Cartesian: 
                conversion = sph2cart
                old = Coordinates.System.convert_angle_units(coords, dimensions, old_angle_unit, "radians")
            else: raise Exception("unknown coordinate conversion from {0} to {1}".format(old_system, new_system))

            c_axis = dimensions.index("C")
            #a, b, c = np.split(old, 3, c_axis)
            a = old[access.get_slice_tuple(dimensions, {"C":0})]
            b = old[access.get_slice_tuple(dimensions, {"C":1})]
            c = old[access.get_slice_tuple(dimensions, {"C":2})]
            
            new = np.moveaxis(np.asarray(conversion(a,b,c)), 0, c_axis)

            if new_system != Coordinates.System.Spherical: return new
            return Coordinates.System.convert_angle_units(new, dimensions, "radians", new_angle_unit)

    class State:
        """Enum of valid coordinate systems"""
        Unused = None
        Fixed = False
        Varying = True

        @staticmethod
        def is_used(state): return state !=Coordinates.State.Unused

    def __init__(self, obj, descriptor):
        self.database = obj.database
        access.ArrayVariable.__init__(self, self.database.dataset, obj.name+descriptor)
        self.obj_name = obj.name
        self.descriptor = descriptor
        if descriptor == "Up": self.unit_proxy = obj.View

    @property
    def Type(self):
        """Coordinate system of the values"""
        if not self.exists():
            raise Exception("failed to get Type of {0}, variable not initialized".format(self.name))
        if self.unit_proxy == None: return self._Matrix.Type
        return self.unit_proxy._Matrix.Type
    @Type.setter
    def Type(self, value): 
        if not self.exists():
            raise Exception("failed to set Type of {0}, variable not initialized".format(self.name))
        if type(value) == str:
            self._Matrix.Type = value
            return
        self._Matrix.Type = value.value

    def _get_global_ref_object(self):
        if self.obj_name == "Receiver": return self.database.Listener
        if self.obj_name == "Emitter": return self.database.Source
        return None

    def get_values(self, indices=None, dim_order=None, system=None, angle_unit=None):
        """Gets the coordinates in their original reference system
        
        Parameters
        ----------
        indices : dict(key:str, value:int or slice), optional
            Key: dimension name, value: indices to be returned, complete axis assumed if not provided
        dim_order : tuple of str, optional
            Desired order of dimensions in the output array
        system : str, optional
            Target coordinate system
        angle_unit : str, optional
            Unit for spherical angles in the output array

        Returns
        -------
        values : np.ndarray
            Coordinates in the original reference system
        """
        values = access.ArrayVariable.get_values(self, indices, dim_order)
        if system == None or system == self.Type:
            if self.Type != Coordinates.System.Spherical or angle_unit == None: return values
            system = self.Type
        old_angle_unit = self.Units.split(",")[0]
        if angle_unit == None: angle_unit = "degree"
        if dim_order == None: dim_order = access.get_default_dimension_order(self.dimensions(), indices)
        return Coordinates.System.convert(values, dim_order, 
                                        self.Type, system,
                                        old_angle_unit, angle_unit)

    def get_global_values(self, indices=None, dim_order=None, system=None, angle_unit=None):
        """Transform local coordinates (such as Receiver or Emitter) into the global reference system
        
        Parameters
        ----------
        indices : dict(key:str, value:int or slice), optional
            Key: dimension name, value: indices to be returned, complete axis assumed if not provided
        dim_order : tuple of str, optional
            Desired order of dimensions in the output array
        system : str, optional
            Target coordinate system
        angle_unit : str, optional
            Unit for spherical angles in the output array

        Returns
        -------
        global_values : np.ndarray
            Transformed coordinates in global reference system
        """
        return self.get_relative_values(None, indices, dim_order, system, angle_unit)

    def get_relative_values(self, ref_object, indices=None, dim_order=None, system=None, angle_unit=None):
        """Transform coordinates (such as Receiver or Emitter) into the reference system of a given :class:`sofa.spatial.Object`, aligning the x-axis with View and the z-axis with Up
        
        Parameters
        ----------
        ref_obj : :class:`sofa.spatial.Object`
            Spatial object providing the reference system, None for 
        indices : dict(key:str, value:int or slice), optional
            Key: dimension name, value: indices to be returned, complete axis assumed if not provided
        dim_order : tuple of str, optional
            Desired order of dimensions in the output array
        system : str, optional
            Target coordinate system
        angle_unit : str, optional
            Unit for spherical angles in the output array

        Returns
        -------
        relative_values : np.ndarray
            Transformed coordinates in original or provided reference system
        """
        if system is None: system=self.Type
        ldim = dimensions.Definitions.names.get(self.obj_name, None)
        
        # get transforms
        anchor_transform, at_order = _get_object_transform(self._get_global_ref_object())
        ref_transform, rt_order = _get_object_transform(ref_object)        

        # transform values
        if ldim is None:
            original_values = self.get_values(dim_order=at_order, system=Coordinates.System.Cartesian)
            transformed_values = ref_transform(anchor_transform(original_values, invert=True))
            order = rt_order
        else:
            original_values_stack = self.get_values(dim_order=(ldim,)+at_order, system=Coordinates.System.Cartesian)
            transformed_values = np.asarray([ref_transform(anchor_transform(original_values, invert=True)) for original_values in original_values_stack])
            order = (ldim,)+rt_order

        # return in proper system, units and order
        if system == Coordinates.System.Spherical and angle_unit == None:
            angle_unit = self.Units.split(",")[0] if self.Type == Coordinates.System.Spherical else "degree"

        default_dimensions = self.dimensions()
        if len(rt_order)>2 : default_dimensions = (rt_order[0],)+default_dimensions

        if dim_order == None: dim_order = access.get_default_dimension_order(default_dimensions, indices)
        
        if indices is None or "C" not in indices:
            return Coordinates.System.convert(access.get_values_from_array(transformed_values, order, 
                        indices=indices, dim_order=dim_order),
                    dim_order,
                    Coordinates.System.Cartesian, system,
                    new_angle_unit=angle_unit)
        else: # only apply "C" index after coordinate system conversion!
            return Coordinates.System.convert(access.get_values_from_array(transformed_values, order, 
                        indices={i:indices[i] for i in indices if i!="C"}, dim_order=("C",)+dim_order),
                    ("C",)+dim_order,
                    Coordinates.System.Cartesian, system,
                    new_angle_unit=angle_unit)[indices["C"]]
                    
                    
        

    def set_system(self, ctype=None, cunits=None):
        """Set the coordinate Type and Units"""
        if ctype == None: ctype = Coordinates.System.Cartesian
        if type(ctype) != str: ctype = ctype.value
        self.Type = str(ctype)
        if cunits == None: cunits=dimensions.default_units[ctype]
        self.Units = str(cunits)      

class Set:
    """Descriptors or data for a spatial entity (Listener, Source, Receiver, Emitter)"""

    def __init__(self, Position, View=Coordinates.State.Unused, Up=Coordinates.State.Unused):
        """Parameters
        ----------
        Position : :class:`sofa.spatial.Coordinates.State`
        View : :class:`sofa.spatial.Coordinates.State`, optional
        Up : :class:`sofa.spatial.Coordinates.State`, optional
        """
        self.Position=Position
        self.View=View
        self.Up=Up

#    @property
#    def Position(self): return self._Position
#    @Position.setter
#    def Position(self, value): self._Position = value
#    @property
#    def View(self): return self._View
#    @View.setter
#    def View(self, value): self._View = value
#    @property
#    def Up(self): return self._Up
#    @Up.setter
#    def Up(self, value): self._Up = value

class Object:
    """Spatial object such as Listener, Receiver, Source, Emitter"""
    def __init__(self, database, name):
        self.database = database
        self.dataset = database.dataset
        self.name = name
        return

    @property
    def Description(self):
        """Informal description of the spatial object"""
        return self.database.Metadata.get_attribute(self.name+"Description")
    @Description.setter
    def Description(self, value): self.database.Metadata.set_attribute(self.name+"Description", value)
    
    @property
    def Position(self): 
        """Position of the spatial object relative to its reference system"""
        return Coordinates(self, "Position")
    @property
    def View(self): 
        """View (x-axis) of the spatial object relative to its reference system"""
        return Coordinates(self, "View")
    @property
    def Up(self): 
        """Up (z-axis) of the spatial object relative to its reference system"""
        return Coordinates(self, "Up")

    def initialize(self, info_states, count=None):
        """Create the necessary variables and attributes

        Parameters
        ----------
        info_states : :class:`sofa.spatial.Set`
            Usage states for the object coordinates
        count : int, optional
            Number of objects (such as Emitters or Receivers)
        """
        if count == None: 
            if "count" in self.database._convention.default_objects[self.name].keys(): 
                count = self.database._convention.default_objects[self.name]["count"]
            else: raise Exception(self.name, "count missing!")
        print(self.name, "count = ", str(count))
        self.database._convention.validate_spatial_object_settings(self.name, info_states, count)

        if self.name == "Emitter" or self.name == "Receiver":
            if dimensions.Definitions.names[self.name] not in self.dataset.dimensions.keys():
                self.dataset.createDimension(dimensions.Definitions.names[self.name], count)
        self._create_coordinates(info_states)
        self.database._convention.set_default_spatial_values(self)

    def _create_coordinates(self, info_states):
        rd = tuple(x for x in getattr(dimensions.Definitions, self.name)(Coordinates.State.Varying) if x!="C")
        if info_states.Position != Coordinates.State.Unused: 
            self.Position.initialize(getattr(dimensions.Definitions, self.name)(info_states.Position))
        if info_states.View != Coordinates.State.Unused: 
            self.View.initialize(getattr(dimensions.Definitions, self.name)(info_states.View))
        if info_states.Up != Coordinates.State.Unused: 
            self.Up.initialize(getattr(dimensions.Definitions, self.name)(info_states.Up))

    def get_pose(self, indices=None, dim_order=None, system=None, angle_unit=None):
        """ Gets the spatial object coordinates or their defaults if they have not been defined. Relative spatial objects return their global pose, or their reference object's pose values if theirs are undefined.

        Parameters
        ----------
        indices : dict(key:str, value:int or slice), optional
            Key: dimension name, value: indices to be returned, complete axis assumed if not provided
        dim_order : tuple of str, optional
            Desired order of dimensions in the output arrays
        system : str, optional
            Target coordinate system
        angle_unit : str, optional
            Unit for spherical angles in the output arrays

        Returns
        -------
        position, view, up : np.ndarray, np.ndarray, np.ndarray
            Spatial object reference system

        """
        
        if angle_unit is None: angle_unit = "rad"
        anchor = self.Position._get_global_ref_object()
        if anchor is None: # this is an object in the global coordinate system
            default_order = ("I","C")
            position = np.asarray([[0, 0, 0]])
            view = np.asarray([[1, 0, 0]])
            up = np.asarray([[0, 0, 1]])

        else: # this is an object defined relative to another
            ldim = dimensions.Definitions.names[self.name]
            lcount = self.database.Dimensions._dim_size(ldim)
            
            anchor_order = ("I", "C")
            default_order = (ldim,) + anchor_order
            if dim_order is None: dim_order = access.get_default_dimension_order(self.Position.dimensions(), indices)

            anchor_position, anchor_view, anchor_up = anchor.get_pose(indices=indices, dim_order=anchor_order, system=Coordinates.System.Cartesian)
            position = np.repeat(np.expand_dims(anchor_position, 0), lcount, axis=0)
            view = np.repeat(np.expand_dims(anchor_view, 0), lcount, axis=0)
            up = np.repeat(np.expand_dims(anchor_up, 0), lcount, axis=0)

        # get existing values or use defaults
        if self.Position.exists(): position = self.Position.get_global_values(indices, dim_order, system, angle_unit)
        else: position = access.get_values_from_array(
                Coordinates.System.convert(position, default_order, Coordinates.System.Cartesian, system, angle_unit, angle_unit),
                default_order, dim_order=dim_order)

        if self.View.exists(): view = self.View.get_global_values(indices, dim_order, system, angle_unit)        
        else: view = access.get_values_from_array(
                Coordinates.System.convert(view, default_order, Coordinates.System.Cartesian, system, angle_unit, angle_unit),
                default_order, dim_order=dim_order)

        if self.Up.exists(): up = self.Up.get_global_values(indices, dim_order, system, angle_unit)
        else: up = access.get_values_from_array(
                Coordinates.System.convert(up, default_order, Coordinates.System.Cartesian, system, angle_unit, angle_unit),
                default_order, dim_order=dim_order)

        return position, view, up

def _rotation_from_view_up(view, up):
    if len(view)!=len(up):
        vlen = len(view)
        ulen = len(up)
        view = np.repeat(view, ulen, axis=0)
        up = np.repeat(up, vlen, axis=0)
    y_axis = np.cross(up, view)
    return Rotation.from_dcm(np.moveaxis(np.asarray([view, y_axis, up]),0,-1))

def _get_object_transform(ref_object):
    order = ("M","C")
    if ref_object is None:
        # global coordinate system
        position = np.asarray([[0, 0, 0]])
        view = np.asarray([[1, 0, 0]])
        up = np.asarray([[0, 0, 1]])
    else:
        if ref_object.name == "Receiver" or ref_object.name == "Emitter":
            ldim = dimensions.Definitions.names[ref_object.name]
            if ldim not in order:
                order = (ldim,) + order
        position, view, up = ref_object.get_pose(dim_order=order, system=Coordinates.System.Cartesian)
    if np.size(position.shape)<3: 
        def apply_transform(values, invert=False):
            rotation = _rotation_from_view_up(view, up)
            return transform(values, rotation, position, invert=invert)
        return apply_transform, order

    def apply_transform(values, invert=False):
        rotations = [_rotation_from_view_up(v, u) for v,u in zip(view, up)]
        return np.asarray([transform(values, rot, pos, invert=invert) for rot,pos in zip(rotations, position)])
    return apply_transform, order

