from __future__ import annotations
from typing import List, Dict, TypedDict, Optional

from lib.state_machine import StateMachine, Step, EntryPoint, Termination, Run
from lib.llm import LLM
from lib.messages import SystemMessage, UserMessage
from lib.game_tools import retrieve_game, evaluate_retrieval, game_web_search, EvaluationReport


class GameAgentState(TypedDict):
    question: str
    retrieved_docs: List[Dict]
    evaluation: Optional[EvaluationReport]
    web_results: List[Dict]
    answer: Optional[str]


class GameAgent:
    def __init__(self):
        self.workflow = self._create_state_machine()

    # Step implementations
    def _retrieve(self, state: GameAgentState) -> GameAgentState:
        docs = retrieve_game(state["question"])
        return {"retrieved_docs": docs}

    def _evaluate(self, state: GameAgentState) -> GameAgentState:
        docs_content = [d.get("Description", "") for d in state.get("retrieved_docs", [])]
        report = evaluate_retrieval(state["question"], docs_content)
        return {"evaluation": report}

    def _web_search(self, state: GameAgentState) -> GameAgentState:
        results = game_web_search(state["question"])
        return {"web_results": results}

    def _generate(self, state: GameAgentState) -> GameAgentState:
        llm = LLM(model="gpt-4o-mini")
        context_parts = []
        for d in state.get("retrieved_docs", []):
            context_parts.append(
                f"[{d.get('Platform')}] {d.get('Name')} ({d.get('YearOfRelease')}) - {d.get('Description')}"
            )
        for r in state.get("web_results", []):
            if isinstance(r, dict):
                context_parts.append(r.get("content") or str(r))
            else:
                context_parts.append(str(r))
        context = "\n".join(context_parts)
        messages = [
            SystemMessage(content="You are a helpful assistant for video game questions."),
            UserMessage(content=f"Question: {state['question']}\nContext:\n{context}\nAnswer:")
        ]
        ai_msg = llm.invoke(messages)
        return {"answer": ai_msg.content}

    def _create_state_machine(self) -> StateMachine[GameAgentState]:
        machine = StateMachine[GameAgentState](GameAgentState)
        entry = EntryPoint[GameAgentState]()
        retrieve = Step[GameAgentState]("retrieve", self._retrieve)
        evaluate = Step[GameAgentState]("evaluate", self._evaluate)
        web = Step[GameAgentState]("web_search", self._web_search)
        generate = Step[GameAgentState]("generate", self._generate)
        termination = Termination[GameAgentState]()

        machine.add_steps([entry, retrieve, evaluate, web, generate, termination])
        machine.connect(entry, retrieve)
        machine.connect(retrieve, evaluate)

        def check_useful(state: GameAgentState):
            if state.get("evaluation") and not state["evaluation"].useful:
                return web
            return generate

        machine.connect(evaluate, [web, generate], check_useful)
        machine.connect(web, generate)
        machine.connect(generate, termination)
        return machine

    def invoke(self, question: str) -> Run:
        initial_state: GameAgentState = {"question": question}
        run = self.workflow.run(initial_state)
        return run


def report_run(run: Run) -> None:
    print("\n=== RUN REPORT ===")
    for snap in run.snapshots:
        print(f"Step: {snap.step_id}")
        for k, v in snap.state_data.items():
            print(f"  {k}: {v}")
    final = run.get_final_state()
    if final and final.get("answer"):
        print("\nAnswer:\n" + final["answer"])

