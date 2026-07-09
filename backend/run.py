import os
from app import create_app
from app.config import config

# Create Flask application instance via structural factory initialization design pattern
app = create_app()

# -------------------------------------------------------------
# GLOBAL SERVICE HEALTH CROSScheck HOOK
# -------------------------------------------------------------
@app.route("/health", methods=["GET"])
def system_health_check():
    """
    Central operational checking loop for monitoring software orchestration health.
    """
    return {
        "status": "ok",
        "message": "PenHex Security Backend Running 🚀",
        "version": "1.0.0"
    }, 200


if __name__ == "__main__":
    # Pull production operational matrix constraints directly from initialized config instance
    host_target = config.HOST
    port_target = config.PORT
    debug_triage = config.DEBUG

    print(f"[*] Starting PenHex Secure Services Infrastructure Engine...")
    print(f"[*] Binding network listener targeting boundary interface: {host_target}:{port_target}")
    print(f"[*] Hot-reload debugger state variable matrix flagged as: {debug_triage}")

    # Kickstart application server lifecycle hook loop
    app.run(
        host=host_target,
        port=port_target,
        debug=debug_triage
    )