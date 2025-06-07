import time
import json
from fastapi import Request
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from fastapi.responses import JSONResponse

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request
        body = await self._get_request_body(request)
        logger.info(f"Request: {request.method} {request.url}\nBody: {body}")
        
        try:
            # Get the original response
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Create new response with same content
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk
            
            # Log response with body
            body = self._get_response_body(response_body)
            logger.info(
                f"Response: {request.method} {request.url}\n"
                f"Status: {response.status_code}\n"
                f"Body: {body}\n"
                f"Completed in {process_time:.3f}s"
            )
            
            # Return a new response with the captured body
            return Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type
            )
            
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            raise e
    
    async def _get_request_body(self, request: Request) -> str:
        """Get request body content"""
        try:
            body = await request.body()
            return body.decode() if body else ""
        except Exception:
            return ""
    
    def _get_response_body(self, body: bytes) -> str:
        """Get response body content"""
        try:
            body_str = body.decode()
            return json.dumps(json.loads(body_str), indent=2)  # Pretty print JSON
        except Exception:
            return "" 