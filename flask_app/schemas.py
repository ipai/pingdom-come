from marshmallow import Schema, fields

class EndpointSchema(Schema):
    """Schema for API endpoint information"""
    available_endpoints = fields.Dict(keys=fields.Str(), values=fields.Str())

class StatusSchema(Schema):
    """Schema for API status response"""
    status = fields.Str(required=True)
    timestamp = fields.DateTime(required=True)

class EchoSchema(Schema):
    """Schema for echo message response"""
    message = fields.Str(required=True)
    received_at = fields.DateTime(required=True)

class DataRequestSchema(Schema):
    """Schema for data request payload"""
    data = fields.Dict(required=True)

class DataResponseSchema(Schema):
    """Schema for data response"""
    received_data = fields.Dict(required=True)
    status = fields.Str(required=True)

class ErrorSchema(Schema):
    """Schema for error responses"""
    error = fields.Str(required=True)
    status_code = fields.Int(required=True)
