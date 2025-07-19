"""flow_checkpoint_demo – showcase checkpointed vibe flow.

Run once:
    python -m we_we_we.flow_checkpoint_demo --text "lok kkkk jajaja"
Run again with same thread id:
    python -m we_we_we.flow_checkpoint_demo --resume <id>
"""

import argparse
import uuid
import json
from typing import TypedDict, List, Annotated
import operator

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from .vibe_sensor import analyze_text
from .security_sigil import SecuritySigil
from .mesh import _digest_latest

# ------------------ state schema -------------------------------------
class FlowState(TypedDict):
    text: str
    report: dict
    security: dict
    mesh_events: Annotated[List[dict], operator.add]

# ------------------ node workers ------------------------------------

def node_vibe(state: FlowState) -> dict:
    return {"report": analyze_text(state["text"]).to_dict()}

shield = SecuritySigil()

def node_sigil(state: FlowState) -> dict:
    return {"security": shield.evaluate(state["text"])}

def node_mesh(state: FlowState) -> dict:
    return {"mesh_events": [_digest_latest()]}

# ------------------ build graph -------------------------------------

g = StateGraph(FlowState)
g.add_node("vibe", node_vibe)
g.add_node("sigil", node_sigil)
g.add_node("mesh", node_mesh)

g.set_entry_point("vibe")
g.add_edge("vibe", "sigil")
g.add_edge("sigil", "mesh")
g.add_edge("mesh", END)

checkpointer = MemorySaver()
app = g.compile(checkpointer=checkpointer)

# ------------------ CLI ---------------------------------------------

def main():
    p = argparse.ArgumentParser(description="Run checkpointed vibe flow.")
    p.add_argument("--text", help="input text to process")
    p.add_argument("--resume", help="resume with given thread id")
    args = p.parse_args()

    if not args.text and not args.resume:
        p.error("--text or --resume required")

    if args.resume:
        thread_id = args.resume
        cfg = {"configurable": {"thread_id": thread_id}}
        result = app.invoke(None, config=cfg)
        print(json.dumps(result, indent=2))
    else:
        thread_id = str(uuid.uuid4())
        cfg = {"configurable": {"thread_id": thread_id}}
        result = app.invoke({"text": args.text}, config=cfg)
        print(json.dumps(result, indent=2))
        print(f"\nThread saved. Resume with --resume {thread_id}")

if __name__ == "__main__":
    main()