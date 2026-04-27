from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    summary="Liveness check",
    description=(
        "Returns `{\"status\": \"ok\"}` when the process is running. "
        "Use for load balancers, Kubernetes liveness probes, or simple monitoring."
    ),
    responses={
        200: {
            "description": "Service is healthy.",
            "content": {
                "application/json": {
                    "example": {"status": "ok"},
                },
            },
        },
    },
)
async def health() -> dict[str, str]:
    """Report that the API process is up."""
    return {"status": "ok"}
