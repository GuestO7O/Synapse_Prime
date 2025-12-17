from pydantic import BaseModel
from typing import List, Dict
import json
import os


class AgentEvolution(BaseModel):
    agent_id: str
    performance_score: float
    feedback_count: int
    evolution_level: int
    traits: Dict[str, float]  # e.g., {"creativity": 0.8, "accuracy": 0.9}


class EvolutionMarketplace:
    def __init__(self, storage_file: str = "evolution_data.json"):
        self.storage_file = storage_file
        self.agents: Dict[str, AgentEvolution] = {}
        self.load_data()

    def load_data(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
                for agent_id, agent_data in data.items():
                    self.agents[agent_id] = AgentEvolution(**agent_data)

    def save_data(self):
        data = {aid: agent.dict() for aid, agent in self.agents.items()}
        with open(self.storage_file, 'w') as f:
            json.dump(data, f, indent=2)

    def register_agent(self, agent_id: str,
                       initial_traits: Dict[str, float] = None):
        default_traits = {"creativity": 0.5, "accuracy": 0.5, "speed": 0.5}
        if agent_id not in self.agents:
            self.agents[agent_id] = AgentEvolution(
                agent_id=agent_id,
                performance_score=0.5,
                feedback_count=0,
                evolution_level=1,
                traits=initial_traits or default_traits
            )
            self.save_data()
        return self.agents[agent_id]

    def submit_feedback(self, agent_id: str, score: float,
                        trait_updates: Dict[str, float] = None):
        if agent_id not in self.agents:
            return None

        agent = self.agents[agent_id]
        self._update_performance_score(agent, score)
        if trait_updates:
            self._update_traits(agent, trait_updates)
        self._check_evolution(agent)
        self.save_data()
        return agent

    def _update_performance_score(self, agent: AgentEvolution, score: float):
        total_feedback = agent.feedback_count + 1
        agent.performance_score = (
            agent.performance_score * agent.feedback_count + score
        ) / total_feedback
        agent.feedback_count = total_feedback

    def _update_traits(self, agent: AgentEvolution,
                       trait_updates: Dict[str, float]):
        total_feedback = agent.feedback_count
        for trait, value in trait_updates.items():
            if trait in agent.traits:
                agent.traits[trait] = (
                    agent.traits[trait] * (total_feedback - 1) + value
                ) / total_feedback

    def _check_evolution(self, agent: AgentEvolution):
        if agent.performance_score > 0.8 and agent.feedback_count > 10:
            agent.evolution_level += 1
            for trait in agent.traits:
                agent.traits[trait] = min(1.0, agent.traits[trait] + 0.1)

    def get_top_agents(self, limit: int = 10) -> List[AgentEvolution]:
        sorted_agents = sorted(
            self.agents.values(),
            key=lambda x: x.performance_score,
            reverse=True
        )
        return sorted_agents[:limit]

    def get_agent_stats(self, agent_id: str):
        return self.agents.get(agent_id)

    def evolve_agent(self, agent_id: str, new_traits: Dict[str, float]):
        """Manually evolve an agent with new traits"""
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            agent.traits.update(new_traits)
            agent.evolution_level += 1
            self.save_data()
            return agent
        return None

    def get_evolution_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get leaderboard with evolution stats"""
        sorted_agents = sorted(
            self.agents.values(),
            key=lambda x: (x.evolution_level, x.performance_score),
            reverse=True
        )
        leaderboard = []
        for i, agent in enumerate(sorted_agents[:limit], 1):
            leaderboard.append({
                "rank": i,
                "agent_id": agent.agent_id,
                "level": agent.evolution_level,
                "score": round(agent.performance_score, 3),
                "feedback_count": agent.feedback_count,
                "top_trait": (
                    max(agent.traits.items(), key=lambda x: x[1])
                    if agent.traits else None
                )
            })
        return leaderboard

    def get_evolution_stats(self) -> Dict:
        """Get overall marketplace statistics"""
        if not self.agents:
            return {"total_agents": 0, "avg_level": 0, "avg_score": 0}

        total_agents = len(self.agents)
        avg_level = sum(a.evolution_level for a in self.agents.values()) / total_agents
        avg_score = (
            sum(a.performance_score for a in self.agents.values()) / total_agents
        )
        max_level = max(a.evolution_level for a in self.agents.values())

        return {
            "total_agents": total_agents,
            "avg_level": round(avg_level, 2),
            "avg_score": round(avg_score, 3),
            "max_level": max_level,
            "evolved_agents": sum(
                1 for a in self.agents.values() if a.evolution_level > 1
            )
        }


# Global marketplace instance
marketplace = EvolutionMarketplace()
