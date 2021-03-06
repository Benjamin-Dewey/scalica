# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import suggestions_pb2 as suggestions__pb2


class SuggestionsStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Suggest = channel.unary_unary(
        '/Suggestions/Suggest',
        request_serializer=suggestions__pb2.SuggestionsRequest.SerializeToString,
        response_deserializer=suggestions__pb2.SuggestionsReply.FromString,
        )


class SuggestionsServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def Suggest(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_SuggestionsServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Suggest': grpc.unary_unary_rpc_method_handler(
          servicer.Suggest,
          request_deserializer=suggestions__pb2.SuggestionsRequest.FromString,
          response_serializer=suggestions__pb2.SuggestionsReply.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'Suggestions', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
