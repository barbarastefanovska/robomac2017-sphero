from sphero.request.spherorequest import SpheroRequest


class SetBackLed(SpheroRequest):

    CID = 0x21
    FMT = '!B'
