from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.adk.errors.already_exists_error import AlreadyExistsError
from google.adk.errors.not_found_error import NotFoundError
from .agent import call_agent, runner, session_service

app = FastAPI(title="ADK Agent API")

class RunRequest(BaseModel):
    appName: str
    userId: str
    sessionId: str
    newMessage: dict

class SessionRequest(BaseModel):
    appName: str
    userId: str
    sessionId: str

# -----------------------------
# Create session endpoint
# -----------------------------
@app.post("/session")
async def create_session(request: SessionRequest):
    try:
        await session_service.create_session(
            app_name=request.appName,
            user_id=request.userId,
            session_id=request.sessionId
        )
        return {"status": "success", "message": f"Session {request.sessionId} created"}
    except AlreadyExistsError:
        return {"status": "exists", "message": f"Session {request.sessionId} already exists"}

# -----------------------------
# Run agent endpoint
# -----------------------------
@app.post("/run")
async def run_agent(request: RunRequest):
    user_id = request.userId
    session_id = request.sessionId
    query = request.newMessage.get("parts")[0].get("text")


    # -----------------------------
    # Validate session exists
    # -----------------------------
    try:
        await session_service.get_session(
            app_name=request.appName,
            user_id=user_id,
            session_id=session_id
        )
    except NotFoundError:
        # Raise proper 404 HTTP error
        raise HTTPException(
            status_code=404,
            detail=f"Session '{session_id}' for user '{user_id}' not found"
        )

    try:
        response_text = await call_agent(query, runner, user_id, session_id)
        if not response_text:
            raise HTTPException(
                status_code=500,
                detail="Agent did not produce a final response."
            )
        return {"response": response_text}

    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Agent execution error: {str(e)}"
        )

# -----------------------------
# Run FastAPI
# -----------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("my_agent.server:app", host="0.0.0.0", port=8000, reload=True)
