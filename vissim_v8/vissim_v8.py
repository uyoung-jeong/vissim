#!/usr/bin/env python
""" VISSIM Tools """
from lxml import etree


class Vissim(object):
    def __init__(self, filename):
        self.filename = filename
        self.data = self._load(filename)

        def _getParams(path):
            return [i for i in self.data.xpath(path)]
        self._colorDistribution = _getParams('./colorDistributions/colorDistribution/@no')
        self._conflictArea = _getParams('./conflictAreas/conflictArea/@no')
        self._desAcceleration = _getParams('./desAccelerationFunctions/desAccelerationFunction/@no')
        self._desDeceleration = _getParams('./desDecelerationFunctions/desDecelerationFunction/@no')
        self._desSpeedDistribution = _getParams('./desSpeedDistributions/desSpeedDistribution/@no')
        self._displayType = _getParams('./displayTypes/displayType/@no')
        self._drivingBehavior = _getParams('./drivingBehaviors/drivingBehavior/@no')
        self._linkBehavType = _getParams('./linkBehaviorTypes/linkBehaviorType/@no')
        self._link = _getParams('./links/link/@no')
        self._locationDistribution = _getParams('./locationDistributions/locationDistribution/@no')
        self._maxAcceleration = _getParams('./maxAccelerationFunctions/maxAcceleration/@no')
        self._maxDeceleration = _getParams('./maxDecelerationFunctions/maxDeceleration/@no')
        self._modelDistribution = _getParams('./model2D3DDistributions/model2D3DDistribution/@no')
        self._model = _getParams('./models2D3D/model2D3D/@no')
        self._occupancy = _getParams('./occupancyDistributions/occupancyDistribution/@no')
        self._pedestrianClass = _getParams('./pedestrianClasses/pedestrianClass/@no')
        self._pedestrianComposition = _getParams('./pedestrianCompositions/pedestrianComposition/@no')
        self._pedestrianType = _getParams('./pedestrianTypes/pedestrianType/@no')
        self._powerDistribution = _getParams('./powerDistributions/powerDistribution/@no')
        self._timeDistribution = _getParams('./timeDistributions/timeDistribution/@no')
        self._vehicleClass = _getParams('./vehicleClasses/vehicleClass/@no')
        self._vehicleComposition = _getParams('./vehicleCompositions/vehicleComposition/@no')
        self._vehicleInput = _getParams('./vehicleInputs/vehicleInput/@no')
        self._vehicleType = _getParams('./vehicleTypes/vehicleType/@no')
        self._walkingBehavior = _getParams('./walkingBehaviors/walkingBehavior/@no')
        self._weightDistribution = _getParams('./weightDistributions/weightDistribution/@no')

    def _load(self, filename):
        """ Load XML file """
        f = open(filename, 'r')
        return etree.parse(f)

    def export(self, filename):
        """ Write XML file to disk """
        self.data.write(filename, encoding="UTF-8", standalone=False)

    def _getAttributes(self, path):
        data = self.data.xpath(path)
        if len(data) > 1:
            raise KeyError('Number of elements > 1')
        else:
            return data[0].attrib

    def _getChildren(self, path):
        return [i.attrib for i in self.data.xpath(path)]

    def _setAttribute(self, path, attr, value):
        data = self.data.xpath(path)
        if len(data) > 1:
            raise KeyError('Number of elements > 1')
        if attr in data[0].attrib.keys():
            data[0].set(attr, str(value))
        else:
            raise KeyError('%s not an attribute of element') % (attr)

    def _setChild(self, path, element, attr):
        data = self.data.xpath(path)
        if len(data) > 1:
            raise KeyError('Number of elements > 1')
        attr = {str(k): str(v) for k, v in attr.items()}
        etree.SubElement(data[0], element, attrib=attr)

    def _removeChild(self, parent, child):
        data = self.data.xpath(parent)
        data.remove(self.data.xpath(child))

    def _getNewNum(self, nums):
        if len(nums) == 0:
            return 1
        else:
            return max(nums) + 1

    def _getDefaultNum(self, nums):
        return nums[0]


class Links(Vissim):
    def __init__(self, filename):
        self.path = './links'
        super(Links, self).__init__(filename)
        self.links = self.data.xpath(self.path)
        self.types = {'assumSpeedOncom': float, 'costPerKm': float,
                      'direction': str, 'displayType': int,
                      'emergStopDist': float, 'gradient': float,
                      'hasOvtLn': bool, 'isPedArea': bool, 'level': int,
                      'linkBehavType': int, 'linkEvalAct': bool,
                      'linkEvalSegLen': float, 'lnChgDist': float,
                      'lnChgEvalAct': bool, 'lookAheadDistOvt': float,
                      'mesoFollowUpGap': float, 'mesoSpeed': float,
                      'mesoSpeedModel': str, 'name': str, 'no': int,
                      'ovtOnlyPT': bool, 'ovtSpeedFact': float,
                      'showClsfValues': bool, 'showLinkBar': bool,
                      'showVeh': bool, 'surch1': float, 'surch2': float,
                      'thickness': float, 'vehRecAct': bool, 'geometry': list,
                      'lanes': list}

    def getLink(self, linkNum):
        """ Get attributes of link.
            Input: link number
            Output: Dict of link attributes
        """
        xpath = self.path + '/link[@no="' + str(linkNum) + '"]'
        return self._getAttributes(xpath)

    def setLink(self, linkNum, attr, value):
        """ Set attribute of link.
            Input: link number
            Output: Changed link attribute
        """
        xpath = self.path + '/link[@no="' + str(linkNum) + '"]'
        return self._setAttribute(xpath, attr, value)

    def getGeometry(self, linkNum):
        """ Get link geometry.
            Input: link number
            Output: List of x,y,z tuples
        """
        xpath = (self.path + '/link[@no="' + str(linkNum) +
                 '"]/geometry/points3D/point3D')
        return self._getChildren(xpath)

    def setGeometry(self, linkNum, points):
        """ Set link geometry.
            Input: link number, list of x,y,z tuples
            Output: Added <point3D> elements to <points3D> elements
        """
        xpath = (self.path + '/link[@no="' + str(linkNum) +
                 '"]/geometry/points3D')
        if isinstance(points, list):
            for x, y, z in points:
                a = {'x': x, 'y': y, 'zOffset': z}
                self._setChild(xpath, 'point3D', a)
        else:
            raise TypeError('points must be list of tuples')

    def getLanes(self, linkNum):
        """ Get lane widths.
            Input: link number
            Output: List of lane widths beginning with lane 1 (in meters)
        """
        xpath = self.path + '/link[@no="' + str(linkNum) + '"]/lanes/lane'
        return self._getChildren(xpath)

    def setLanes(self, linkNum, lanes):
        """ Set lane widths.
            Input: link number, list of lane widths beginning with lane 1 (in
            meters)
            Output: Added <lane> elements to <lanes> element
        """
        xpath = self.path + '/link[@no="' + str(linkNum) + '"]/lanes'
        if isinstance(lanes, list):
            for width in lanes:
                self._setChild(xpath, 'lane', {'width': width})
        else:
            raise TypeError('lanes must be a list of width values')

    def createLink(self, linkNum, **kwargs):
        """ Create a new link in the model.
            Input: link number, link, point3D and lane attributes as dict
            Output: Added <link> element to <links> element.
        """
        num = self._getNewNum(self._link)
        defaults = {'assumSpeedOncom': '60.00000', 'costPerKm': '0.00000',
                    'direction': 'ALL',
                    'displayType': _self._getDefaultNum(self._displayType),
                    'emergStopDist': '5.00000', 'gradient': '0.00000',
                    'hasOvtLn': 'false', 'isPedArea': 'false', 'level': '1',
                    'linkBehavType': self._getDefaultNum(self._linkBehavType),
                    'linkEvalAct': 'false',
                    'linkEvalSegLen': '10.00000', 'lnChgDist': '200.00000',
                    'lnChgEvalAct': 'true', 'lookAheadDistOvt': '250.00000',
                    'mesoFollowUpGap': '0.00000', 'mesoSpeed': '50.00000',
                    'mesoSpeedModel': 'VEHICLEBASED', 'name': '',
                    'ovtOnlyPT': 'false', 'ovtSpeedFact': '1.300000',
                    'showClsfValues': 'true', 'showLinkBar': 'true',
                    'showVeh': 'true', 'surch1': '0.00000',
                    'surch2': '0.00000', 'thickness': '0.00000',
                    'vehRecAct': 'true', 'no': num}
        data = self.data
        a = {k: kwargs.get(k, v) for k, v in defaults.items()}
        self._setChild(self.path, 'link', a)
        xpath = self.path + '/link[@no="' + str(linkNum) + '"]'
        self._setChild(xpath, 'geometry', None)
        self._setChild(xpath + '/geometry', 'points3D', None)
        self.setGeometry(linkNum, kwargs.get('point3D',
                         [('0', '0', '0'), ('1', '1', '0')]))
        self._setChild(xpath, 'lanes', None)
        self.setLanes(linkNum, kwargs.get('lane', ['3.500000']))

    def removeLink(self, linkNum):
        """ Remove an existing link from the model.
            Input: link number
            Output: Removed <link> element from <links> element
        """
        parent = self.path
        child = self.path + '/link[@no="' + str(linkNum) + '"]'
        self._removeChild(parent, child)


class Inputs(Vissim):
    def __init__(self, filename):
        self.path = './vehicleInputs'
        super(Inputs, self).__init__(filename)
        self.inputs = self.data.xpath(self.path)
        self.links = self.data.xpath('./links/link')
        self.types = {'anmFlag': bool, 'link': int, 'name': str, 'no': int}

    def getInput(self, attr, value):
        """ Get attributes for a given input based on input attribute value.
            Input: Input attribute = value
            Output: dict of attributes
        """
        if attr not in self.types:
            raise KeyError('%s not a valid attribute' % (attr))
        xpath = (self.path + '/vehicleInput[@' + str(attr) + '="' +
                 str(value) + '"]')
        return self._getAttributes(xpath)

    def setInput(self, inputNum, attr, value):
        """ Set attribute of input.
            Input: input number
            Output: Changed input attribute
        """
        xpath = self.path + '/vehicleInput[@no="' + str(inputNum) + '"]'
        return self._setAttribute(xpath, attr, value)

    def getVols(self, inputNum):
        """ Get attributes of volume.
            Input: input number
            Output: Dict of volume attributes
        """
        xpath = (self.path + '/vehicleInput[@no="' + str(inputNum) +
                 '"]/timeIntVehVols/timeIntervalVehVolume')
        return self._getChildren(xpath)

    def setVols(self, inputNum, vol, **kwargs):
        """ Set attribute of volume.
            Input: input number
            Output: Changed volume attribute
        """
        defaults = {'cont': 'false', 'timeInt': '1 0',
                    'vehComp': self._getDefaultNum(self._vehicleComposition),
                    'volType': 'EXACT'}
        xpath = (self.path + '/vehicleInput[@no="' + str(inputNum) +
                 '"]/timeIntVehVols')
        a = {k: kwargs.get(k, v) for k, v in defaults.items()}
        a['volume'] = vol
        self._setChild(xpath, 'timeIntervalVehVolume', a)

    def createInput(self, inputNum, linkNum, vol, **kwargs):
        """ Create a new input in the model.
            Input: input number, input and volume attributes as dict
            Output: Added <vehicleInput> element to <vehicleInputs> element.
        """
        defaults = {'anmFlag': 'false', 'name': '',
                    'no': self._getNewNum(self._vehicleInput)}
        data = self.data
        a = {k: kwargs.get(k, v) for k, v in defaults.items()}
        a['link'] = linkNum
        self._setChild(self.path, 'vehicleInput', a)
        xpath = self.path + '/vehicleInput[@no="' + str(inputNum) + '"]'
        self._setChild(xpath, 'timeIntVehVols', None)
        self.setVols(inputNum, vol, kwargs)

    def removeInput(self, inputNum):
        """ Remove an existing input from the model.
            Input: input number
            Output: Removed <vehicleInput> element from <vehicleInputs> element
        """
        parent = self.path
        child = self.path + '/vehicleInput[@no="' + str(inputNum) + '"]'
        self._removeChild(parent, child)


class StaticRouting(Vissim):
    def __init__(self, filename):
        self.path = './vehicleRoutingDecisionsStatic'
        super(StaticRouting, self).__init__(filename)
        self.routing = self.data.xpath(self.path)
        self.links = self.data.xpath('./links/link')
        self.types = {'allVehTypes': bool, 'anmFlag': bool,
                      'combineStaRoutDec': bool, 'link': int, 'name': str,
                      'no': int, 'pos': float}

    def getRouting(self, attr, value):
        """ Get attributes for a given routing decision based on attribute
            value.
            Input: Routing decision attribute = value
            Output: dict of attributes
        """
        if attr not in self.types:
            raise KeyError('%s not a valid attribute' % (attr))
        xpath = (self.path + '/vehicleRoutingDecisionStatic[@' + str(attr) +
                 '="' + str(value) + '"]')
        return self._getAttributes(xpath)

    def setRouting(self, routingNum, attr, value):
        """ Set attribute of routing decision.
            Input: routing decision number, attribute, set value
            Output: Changed routing decision attribute
        """
        xpath = (self.path + '/vehicleRoutingDecisionStatic[@no="' +
                 str(routingNum) + '"]')
        return self._setAttribute(xpath, attr, value)

    def getVehicleClasses(self, routingNum):
        """ Get vehicle classes associated with routing decision.
            Input: routing decision number
            Output: list of vehicle classes
        """
        xpath = (self.path + '/vehicleRoutingDecisionStatic[@no="' +
                 str(routingNum) + '"]' + '/vehClasses/intObjectRef')
        return self._getChildren(xpath)

    def setVehicleClasses(self, routingNum, classes):
        """ Set vehicle classes.
            Input: routing decision number, list of vehicle classes
            Output: Added <intObjectRef> elements to <vehClasses> element
        """
        xpath = (self.path + '/vehicleRoutingDecisionStatic[@no="' +
                 str(routingNum) + '"]' + '/vehClasses')
        if isinstance(classes, list):
            for c in classes:
                self._setChild(xpath, 'intObjectRef', {'key': c})
        else:
            raise TypeError('classes must be a list of vehicle classes')

    def getRoute(self, routingNum, attr, value):
        """ Get attributes for a given route based on attribute value.
            Input: Routing decision number, Route attribute = value
            Output: dict of attributes
        """
        routeTypes = ['destLink', 'destPos', 'name', 'no', 'relFlow']
        if attr not in routeTypes:
            raise KeyError('%s not a valid attribute' % (attr))
        xpath = (self.path + '/vehicleRoutingDecisionStatic[@no="' +
                 str(routingNum) + '"]' +
                 '/vehRouteSta/vehicleRouteStatic[@' + str(attr) + '="' +
                 str(value) + '"]')
        return self._getAttributes(xpath)

    def setRoute(self, routingNum, routeNum, attr, value):
        """ Set attribute of route.
            Input: routing decision number, route number, attribute, set value
            Output: Changed route attribute
        """
        xpath = (self.path + '/vehicleRoutingDecisionStatic[@no="' +
                 str(routingNum) + '"]' +
                 '/vehRouteSta/vehicleRouteStatic[@no="' + str(routingNum) +
                 '"]/vehRouteSta/vehicleRouteStatic[@no="' + str(routeNum) +
                 '"]')
        return self._setAttribute(xpath, attr, value)

    def getRouteSeq(self, routingNum, routeNum):
        """ Get sequence of links that a given route traverses.
            Input: routing decision number, route number
            Output: list of links in order
        """
        xpath = (self.path + '/vehicleRoutingDecisionStatic[@no="' +
                 str(routingNum) + '"]' +
                 '/vehRouteSta/vehicleRouteStatic[@no="' + str(routingNum) +
                 '"]/vehRouteSta/vehicleRouteStatic[@no="' + str(routeNum) +
                 '"]/linkSeq/intObjectRef')
        return self._getChildren(xpath)

    def setRouteSeq(self, routingNum, routeNum, links):
        """ Set sequence of links that a given route traverses.
            Input: routing decision number, route number, list of links
            Output: Added <intObjectRef> elements to <linkSeq> element
        """
        xpath = (self.path + '/vehicleRoutingDecisionStatic[@no="' +
                 str(routingNum) + '"]' +
                 '/vehRouteSta/vehicleRouteStatic[@no="' + str(routingNum) +
                 '"]/vehRouteSta/vehicleRouteStatic[@no="' + str(routeNum) +
                 '"]/linkSeq')
        if isinstance(links, list):
            for link in links:
                a = {'key': int(link)}
                self._setChild(xpath, 'intObjectRef', a)
        else:
            raise TypeError('links must be list of integers')

    def createRoute(self, routingNum, destLink, **kwargs):
        num = self._getNums(self.path +
                            '/vehicleRoutingDecisionsStatic[@no="' +
                            str(routingNum) + '/vehicleRouteStatic/@no')
        defaults = {'destPos': '0.000', 'name': '', 'no': num, 'relFlow': ''}
        data = self.data
        a = {k: kwargs.get(k, v) for k, v in defaults.items()}
        a['destLink'] = destLink
        xpath = (self.path + '/vehicleRoutingDecisionStatic[@no="' +
                 str(routingNum) + '/vehRoutSta')
        self._setChild(xpath, 'vehicleRouteStatic', a)
        xpath2 = xpath + '/vehicleRouteStatic[@no="' + str(num) + '"]'
        self.setChild(xpath2, 'linkSeq')
        self.setRouteSeq(routingNum, num, kwargs.get('linkSeq', []))

    def createRouting(self, linkNum, **kwargs):
        """ Create a new link in the model.
            Input: link number, link, point3D and lane attributes as dict
            Output: Added <link> element to <links> element.
        """
        num = self._getNums('./links/link/@no')
        defaults = {'allVehTypes': 'false', 'anmFlag': 'false', 'no': num,
                    'combineStaRoutDec': 'false', 'name': '', 'pos': '0.0000',
                    'vehClasses': self._getDefaultNum(self._vehicleClass)}
        data = self.data
        a = {k: kwargs.get(k, v) for k, v in defaults.items()}
        a['link'] = linkNum
        self._setChild(self.path, 'vehicleRoutingDecisionStatic', a)
        xpath = (self.path + '/vehicleRoutingDecisionStatic[@no="' +
                 str(linkNum) + '"]')
        self._setChild(xpath, 'vehClasses', None)
        self.setVehicleClasses(a['no'], a['vehClasses'])
        self._setChild(xpath, 'vehRoutSta', None)