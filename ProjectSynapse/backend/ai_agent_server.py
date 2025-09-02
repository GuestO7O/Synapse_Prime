from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import random
import asyncio
from datetime import datetime

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

# Mock data
agents_db = [
    {'id': 'dev-01', 'name': 'Dev-Agent 01', 'type': 'developer', 'status': 'CODING', 'task': 'Implement API logic', 'progress': 60, 'cpu': 25.0, 'memory': 30.0},
    {'id': 'ux-01', 'name': 'UX-Agent', 'type': 'designer', 'status': 'DESIGNING', 'task': 'Design UI components', 'progress': 80, 'cpu': 12.0, 'memory': 18.0},
    {'id': 'ai-01', 'name': 'AI-Agent Alpha', 'type': 'ai', 'status': 'LEARNING', 'task': 'Process neural data', 'progress': 45, 'cpu': 35.0, 'memory': 45.0}
]

evolution_agents = [
    {'agent_id': 'dev-01', 'performance_score': 0.85, 'feedback_count': 12, 'evolution_level': 3, 'traits': {'creativity': 0.8, 'accuracy': 0.9}},
    {'agent_id': 'ux-01', 'performance_score': 0.92, 'feedback_count': 8, 'evolution_level': 4, 'traits': {'creativity': 0.95, 'accuracy': 0.88}}
]

project_queue = ['Frontend Refactor V2', 'Database Optimization', 'AI Model Training']

@app.get('/')
async def root():
    return {'status': 'Project Synapse AI Agent Interface is online!', 'message': 'Backend server werkt met alle AI agent functionaliteit'}

@app.get('/api/v1/agents')
async def get_agents():
    return {'agents': agents_db}

@app.get('/api/v1/project-queue')
async def get_queue():
    return {'queue': project_queue}

@app.post('/api/v1/project-queue')
async def add_to_queue(item: dict):
    if 'name' in item:
        project_queue.append(item['name'])
    return {'success': True, 'queue': project_queue}

@app.post('/api/v1/crew-mission')
async def run_crew_mission(data: dict):
    description = data.get('description', 'Unknown mission')
    agents_count = data.get('agents_count', 2)
    await asyncio.sleep(1)

    mock_results = [
        f'✅ Mission "{description}" completed successfully!',
        f'🚀 Crew of {agents_count} agents deployed for: {description}',
        f'📊 Analysis complete for mission: {description}',
        f'⚡ Task execution finished for: {description}'
    ]

    result = random.choice(mock_results)
    return {
        'result': result,
        'mission': description,
        'agents_used': agents_count,
        'status': 'completed',
        'timestamp': datetime.now().isoformat()
    }

@app.get('/api/v1/evolution/top-agents')
async def get_top_agents(limit: int = 10):
    return {'top_agents': evolution_agents[:limit]}

@app.get('/api/v1/evolution/leaderboard')
async def get_leaderboard():
    return {'leaderboard': sorted(evolution_agents, key=lambda x: x['performance_score'], reverse=True)}

@app.get('/api/v1/evolution/stats')
async def get_evolution_stats():
    return {
        'total_agents': len(evolution_agents),
        'average_score': sum(a['performance_score'] for a in evolution_agents) / len(evolution_agents),
        'total_feedback': sum(a['feedback_count'] for a in evolution_agents)
    }

@app.post('/api/v1/evolution/feedback')
async def submit_feedback(data: dict):
    agent_id = data.get('agent_id')
    score = float(data.get('score', 0.5))

    for agent in evolution_agents:
        if agent['agent_id'] == agent_id:
            agent['performance_score'] = (agent['performance_score'] + score) / 2
            agent['feedback_count'] += 1
            break

    return {'success': True, 'message': f'Feedback submitted for agent {agent_id}'}

@app.post('/api/v1/evolution/register/{agent_id}')
async def register_agent(agent_id: str):
    new_agent = {
        'agent_id': agent_id,
        'performance_score': 0.5,
        'feedback_count': 0,
        'evolution_level': 1,
        'traits': {'creativity': 0.5, 'accuracy': 0.5}
    }
    evolution_agents.append(new_agent)
    return {'success': True, 'message': f'Agent {agent_id} registered'}

if __name__ == "__main__":
    print('🚀 Starting Project Synapse AI Agent Interface...')
    print('📡 Server URL: http://127.0.0.1:8002')
    print('🔄 CORS enabled for all origins')
    print('🤖 AI Agent routes loaded')
    print('📊 Evolution marketplace active')
    print('✅ Ready to accept connections...')
    print('')
    print('Available endpoints:')
    print('  GET  /                           - Status check')
    print('  GET  /api/v1/agents             - List all agents')
    print('  GET  /api/v1/project-queue      - Get project queue')
    print('  POST /api/v1/project-queue      - Add to queue')
    print('  POST /api/v1/crew-mission       - Run crew mission')
    print('  GET  /api/v1/evolution/top-agents - Top evolved agents')
    print('  GET  /api/v1/evolution/leaderboard - Agent leaderboard')
    print('  GET  /api/v1/evolution/stats    - Evolution stats')
    print('  POST /api/v1/evolution/feedback - Submit feedback')
    print('  POST /api/v1/evolution/register/{id} - Register agent')
    print('')

    try:
        uvicorn.run(app, host='127.0.0.1', port=8002, log_level='info')
    except KeyboardInterrupt:
        print('\n✅ Server shutdown gracefully')
    except Exception as e:
        print(f'❌ Server error: {e}')
        import traceback
        traceback.print_exc()
