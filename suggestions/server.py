from concurrent import futures
import time

import grpc

import suggestions_pb2
import suggestions_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Suggestions(suggestions_pb2_grpc.SuggestionsServicer):
    def Suggest(self, request, context):
        user_id = request.user_id
        
        # TODO: using user_id get the list of suggestions here
        # 
        suggestions = [5, 6]

        response = suggestions_pb2.SuggestionsReply()
        response.suggestions.extend(suggestions)
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    suggestions_pb2_grpc.add_SuggestionsServicer_to_server(Suggestions(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print 'Starting suggestions server. Listening on port 50051.'
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
