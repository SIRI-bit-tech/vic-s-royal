from django.db import connection
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class QueryOptimizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Reset query log at the start of each request
        if settings.DEBUG:
            connection.queries_log.clear()
        
        response = self.get_response(request)
        
        # Log and analyze queries in debug mode
        if settings.DEBUG:
            total_queries = len(connection.queries)
            if total_queries > 10:  # Threshold for excessive queries
                logger.warning(f"Request to {request.path} generated {total_queries} queries")
                
                # Log duplicate queries
                queries = {}
                for query in connection.queries:
                    sql = query['sql']
                    if sql in queries:
                        queries[sql] += 1
                    else:
                        queries[sql] = 1
                
                for sql, count in queries.items():
                    if count > 1:
                        logger.warning(f"Duplicate query executed {count} times: {sql}")
        
        return response
