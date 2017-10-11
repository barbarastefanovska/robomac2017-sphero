from sphero.request.corerequest import CoreRequest


class SetInactivityTimeout(CoreRequest):

    CID = 0x25
    FMT = '!H'

