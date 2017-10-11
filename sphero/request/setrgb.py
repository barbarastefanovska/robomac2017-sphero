from sphero.request.spherorequest import SpheroRequest


class SetRGB(SpheroRequest):

    CID = 0x20
    FMT = '!BBBB'
