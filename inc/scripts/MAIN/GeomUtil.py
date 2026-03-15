import math

class GeomUtil:
    PI = 3.141592653589793
    toRADIANS = PI / 180
    toDEGREES = 180 / PI

    @staticmethod
    def degreesToRadians(degrees):
        return degrees * GeomUtil.toRADIANS

    @staticmethod
    def getPositionOnCircle(centerX, centerY, angleInDegrees, radiusX, radiusY):
        radians = GeomUtil.degreesToRadians(angleInDegrees)
        return (centerX + radiusX * math.cos(radians), centerY + radiusY * math.sin(radians))