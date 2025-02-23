"""Marshmallow schemas for request/response validation and serialization."""

from marshmallow import Schema, fields

__all__ = [
    "EndpointSchema",
    "StatusSchema",
    "EchoSchema",
    "DataRequestSchema",
    "DataResponseSchema",
    "ErrorSchema",
]


class EndpointSchema(Schema):
    """Available API endpoints listing."""

    available_endpoints = fields.Dict(
        keys=fields.Str(),
        values=fields.Str(),
        description="Map of endpoint names to their descriptions",
    )


class StatusSchema(Schema):
    """API health status response."""

    status = fields.Str(required=True, description="Current API health status")
    timestamp = fields.DateTime(
        required=True, description="Time when status was checked"
    )


class EchoSchema(Schema):
    """Echo message response."""

    message = fields.Str(required=True, description="Message that was echoed back")
    received_at = fields.DateTime(
        required=True, description="Time when message was received"
    )


class DataRequestSchema(Schema):
    """JSON data request payload."""

    data = fields.Dict(required=True, description="JSON data to be processed")


class DataResponseSchema(Schema):
    """Processed data response."""

    received_data = fields.Dict(
        required=True, description="Data that was received and processed"
    )
    status = fields.Str(required=True, description="Processing status")
