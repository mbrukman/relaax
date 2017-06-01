# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc
from grpc.framework.common import cardinality
from grpc.framework.interfaces.face import utilities as face_utilities

import bridge_pb2 as bridge__pb2


class ParameterServerStub(object):

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetGlobalT = channel.unary_unary(
        '/ParameterServer/GetGlobalT',
        request_serializer=bridge__pb2.NullMessage.SerializeToString,
        response_deserializer=bridge__pb2.Step.FromString,
        )
    self.GetFilterState = channel.unary_unary(
        '/ParameterServer/GetFilterState',
        request_serializer=bridge__pb2.NullMessage.SerializeToString,
        response_deserializer=bridge__pb2.FilterState.FromString,
        )
    self.WaitForIteration = channel.unary_unary(
        '/ParameterServer/WaitForIteration',
        request_serializer=bridge__pb2.NullMessage.SerializeToString,
        response_deserializer=bridge__pb2.NIter.FromString,
        )
    self.SendExperience = channel.unary_unary(
        '/ParameterServer/SendExperience',
        request_serializer=bridge__pb2.Experience.SerializeToString,
        response_deserializer=bridge__pb2.NullMessage.FromString,
        )
    self.ReceiveWeights = channel.unary_stream(
        '/ParameterServer/ReceiveWeights',
        request_serializer=bridge__pb2.NIter.SerializeToString,
        response_deserializer=bridge__pb2.NdArray.FromString,
        )
    self.StoreScalarMetric = channel.unary_unary(
        '/ParameterServer/StoreScalarMetric',
        request_serializer=bridge__pb2.ScalarMetric.SerializeToString,
        response_deserializer=bridge__pb2.NullMessage.FromString,
        )


class ParameterServerServicer(object):

  def GetGlobalT(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetFilterState(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def WaitForIteration(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SendExperience(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ReceiveWeights(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def StoreScalarMetric(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ParameterServerServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetGlobalT': grpc.unary_unary_rpc_method_handler(
          servicer.GetGlobalT,
          request_deserializer=bridge__pb2.NullMessage.FromString,
          response_serializer=bridge__pb2.Step.SerializeToString,
      ),
      'GetFilterState': grpc.unary_unary_rpc_method_handler(
          servicer.GetFilterState,
          request_deserializer=bridge__pb2.NullMessage.FromString,
          response_serializer=bridge__pb2.FilterState.SerializeToString,
      ),
      'WaitForIteration': grpc.unary_unary_rpc_method_handler(
          servicer.WaitForIteration,
          request_deserializer=bridge__pb2.NullMessage.FromString,
          response_serializer=bridge__pb2.NIter.SerializeToString,
      ),
      'SendExperience': grpc.unary_unary_rpc_method_handler(
          servicer.SendExperience,
          request_deserializer=bridge__pb2.Experience.FromString,
          response_serializer=bridge__pb2.NullMessage.SerializeToString,
      ),
      'ReceiveWeights': grpc.unary_stream_rpc_method_handler(
          servicer.ReceiveWeights,
          request_deserializer=bridge__pb2.NIter.FromString,
          response_serializer=bridge__pb2.NdArray.SerializeToString,
      ),
      'StoreScalarMetric': grpc.unary_unary_rpc_method_handler(
          servicer.StoreScalarMetric,
          request_deserializer=bridge__pb2.ScalarMetric.FromString,
          response_serializer=bridge__pb2.NullMessage.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'ParameterServer', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
