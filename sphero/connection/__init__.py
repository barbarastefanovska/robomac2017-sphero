try:
    import bluetooth
    from sphero.connection.bluezconnection import Connection
except ImportError:
    import socket

    if not hasattr(socket, 'AF_BLUETOOTH'):
        raise

    from sphero.connection.socketconnection import Connection

__all__ = ['Connection']
