"""Exceptions for Autarco."""


class AutarcoError(Exception):
    """Generic Autarco exception."""


class AutarcoConnectionError(AutarcoError):
    """Autarco connection exception."""


class AutarcoAuthenticationError(AutarcoError):
    """Autarco Authentication exception."""


class AutarcoConnectionTimeoutError(AutarcoError):
    """Autarco connection timeout exception."""
