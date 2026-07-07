"""Main entry point for the cross-module agent and FastAPI route."""

import asyncio
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from .command_parser import parse_command, is_cross_module
from .executor import CrossModuleExecutor


class CrossModuleAgent:
    def __init__(self, page=None, on_step=None) -> None:
        self.page = page
        self.on_step = on_step

    async def run(self, command: str, context: Optional[dict] = None) -> dict:
        print(f"\n🤖 Processing: {command}\n")
        steps = parse_command(command, context)
        if not steps:
            return {"success": False, "error": "Could not parse command into steps"}
        executor = CrossModuleExecutor(page=self.page, on_step=self.on_step)
        return await executor.execute(steps)


router = APIRouter(prefix="/agent", tags=["Cross-Module Agent"])


class CommandRequest(BaseModel):
    command: str
    context: dict = {}


@router.post("/run")
async def run_command(data: CommandRequest):
    agent = CrossModuleAgent()
    return await agent.run(data.command, data.context)


@router.post("/parse")
async def parse_only(data: CommandRequest):
    steps = parse_command(data.command, data.context)
    return {"steps": steps, "is_cross_module": is_cross_module(data.command)}


async def main() -> None:
    while True:
        command = input("Command: ").strip()
        if not command or command.lower() in {"quit", "exit"}:
            break
        agent = CrossModuleAgent()
        result = await agent.run(command)
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
