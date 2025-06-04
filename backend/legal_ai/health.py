from __future__ import annotations

import os
import redis
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL)


@api_view(["GET"])
@permission_classes([AllowAny])
def healthz(_request):
    try:
        redis_client.ping()
        redis_status = "ok"
    except Exception:
        redis_status = "error"
    return Response({"status": "ok", "redis": redis_status})
