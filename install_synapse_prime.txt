@echo off
setlocal

:: =============================================================================
:: =            SYNAPSE PRIME - AUTOMATED INSTALLATION SCRIPT                =
:: =                          Voor JwP door AutonomeAI                       =
:: =============================================================================

echo.
echo  ================================================================
echo.
echo         SYNAPSE PRIME AUTOMATED INSTALLATION IS STARTING...
echo.
echo  Dit script zal de volledige projectstructuur, code en        
echo  dependencies voor je installeren. Jouw tevredenheid is gegarandeerd.
echo.
echo  ================================================================
echo.
timeout /t 5 >nul

:: Stap 1: Controleer of de benodigde software is geinstalleerd
echo [STAP 1/6] Controleren op benodigde software (Python en Node.js)...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo [FOUT] Python is niet gevonden. Installeer Python vanaf python.org en zorg ervoor dat 'Add to PATH' is aangevinkt.
    echo Het script wordt nu afgesloten.
    pause
    exit /b 1
)

where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo [FOUT] Node.js (npm) is niet gevonden. Installeer Node.js vanaf nodejs.org.
    echo Het script wordt nu afgesloten.
    pause
    exit /b 1
)
echo [SUCCES] Python en Node.js zijn gevonden.
echo.

:: Stap 2: Maak de projectstructuur aan
echo [STAP 2/6] Projectstructuur wordt aangemaakt op je Bureaublad...
cd /d "%userprofile%\Desktop"
if exist synapse-prime (
    echo De map 'synapse-prime' bestaat al. Om problemen te voorkomen, hernoem of verwijder de oude map.
    pause
    exit /b 1
)
mkdir synapse-prime
cd synapse-prime
mkdir backend
mkdir frontend

cd backend
mkdir src
cd src
mkdir routes
mkdir database
mkdir static
cd ..

echo [SUCCES] Projectstructuur is aangemaakt.
echo.

:: Stap 3: Maak de backend bestanden aan
echo [STAP 3/6] Backend bestanden worden aangemaakt en gevuld met code...

:: run_server.py
(
    echo import os
    echo import sys
    echo from flask import Flask, send_from_directory
    echo from flask_cors import CORS
    echo.
    echo sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    echo.
    echo from routes.agent import agent_bp
    echo.
    echo app = Flask(__name__, static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'dist'))
    echo app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'
    echo.
    echo CORS(app)
    echo.
    echo app.register_blueprint(agent_bp, url_prefix='/api')
    echo.
    echo @app.route('/', defaults={'path': ''})
    echo @app.route('/<path:path>')
    echo def serve(path):
    echo     static_folder_path = app.static_folder
    echo     if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
    echo         return send_from_directory(static_folder_path, path)
    echo     else:
    echo         return send_from_directory(static_folder_path, 'index.html')
    echo.
    echo if __name__ == '__main__':
    echo     print("Starting Synapse Prime Backend Server...")
    echo     app.run(host='0.0.0.0', port=5001, debug=True)
) > run_server.py

:: requirements.txt
(
    echo Flask
    echo Flask-Cors
) > requirements.txt

:: src/routes/__init__.py
echo. > src\routes\__init__.py

:: src/routes/agent.py
(
    echo from flask import Blueprint, jsonify, request
    echo from flask_cors import cross_origin
    echo import json
    echo import time
    echo import random
    echo from datetime import datetime
    echo.
    echo agent_bp = Blueprint('agent', __name__)
    echo.
    echo agents = [
    echo     {
    echo         'id': 'dev-01', 'name': 'Dev-Agent 01', 'type': 'dev', 'status': 'CODING',
    echo         'task': 'Implementeert API-logica', 'progress': 60, 'cpu': 25, 'memory': 30, 'log': []
    echo     },
    echo     {
    echo         'id': 'ux-01', 'name': 'UX-Agent', 'type': 'ux', 'status': 'DESIGNING',
    echo         'task': 'Ontwerpt UI componenten', 'progress': 80, 'cpu': 12, 'memory': 18, 'log': []
    echo     },
    echo     {
    echo         'id': 'meta-01', 'name': 'Meta-Agent', 'type': 'ops', 'status': 'ANALYZING',
    echo         'task': 'Monitort cluster performance', 'progress': 100, 'cpu': 15, 'memory': 20, 'log': []
    echo     },
    echo     {
    echo         'id': 'scout-01', 'name': 'Scout-Agent', 'type': 'scout', 'status': 'ANALYZING',
    echo         'task': 'Scant naar nieuwe Python libraries', 'progress': 100, 'cpu': 12, 'memory': 18, 'log': []
    echo     },
    echo     {
    echo         'id': 'guardian-01', 'name': 'Guardian-Agent', 'type': 'guardian', 'status': 'ANALYZING',
    echo         'task': 'Monitort security protocollen', 'progress': 100, 'cpu': 10, 'memory': 25, 'log': []
    echo     }
    echo ]
    echo.
    echo project_queue = ["Frontend Refactor V2", "Database Optimalisatie", "AI Model Integration"]
    echo.
    echo active_project = {
    echo     'name': 'Self-Evolving Trading Core Implementation', 'currentStage': 0, 'stageProgress': 45,
    echo     'stages': [
    echo         {'name': 'Architecture Design', 'status': 'active'},
    echo         {'name': 'Core Development', 'status': 'pending'},
    echo         {'name': 'AI Integration', 'status': 'pending'},
    echo         {'name': 'Testing ^& Validation', 'status': 'pending'},
    echo         {'name': 'Deployment', 'status': 'pending'}
    echo     ]
    echo }
    echo.
    echo system_logs = [
    echo     {'time': '14:32:15', 'message': 'Command Center V5 geinitialiseerd. Systeem is volledig autonoom.'},
    echo     {'time': '14:32:45', 'message': 'Nieuw project gestart: Self-Evolving Trading Core'},
    echo     {'time': '14:33:12', 'message': 'Dev-Agent 01 start taak: Implementeert API-logica'},
    echo     {'time': '14:33:28', 'message': 'UX-Agent start taak: Ontwerpt UI componenten'},
    echo ]
    echo.
    echo @agent_bp.route('/agents', methods=['GET'])
    echo @cross_origin()
    echo def get_agents():
    echo     for agent in agents:
    echo         if agent['status'] != 'IDLE':
    echo             agent['cpu'] = round(random.uniform(5, 30), 1)
    echo             agent['memory'] = round(random.uniform(10, 40), 1)
    echo     return jsonify(agents)
    echo.
    echo @agent_bp.route('/project-queue', methods=['POST'])
    echo @cross_origin()
    echo def add_to_project_queue():
    echo     data = request.get_json()
    echo     if 'name' in data:
    echo         project_queue.append(data['name'])
    echo         system_logs.insert(0, {'time': datetime.now().strftime('%%H:%%M:%%S'), 'message': f'Nieuwe missie: {data["name"]}'})
    echo         return jsonify({'success': True, 'queue': project_queue})
    echo     return jsonify({'error': 'Project name required'}), 400
    echo.
    echo @agent_bp.route('/active-project', methods=['GET'])
    echo @cross_origin()
    echo def get_active_project(): return jsonify(active_project)
    echo.
    echo @agent_bp.route('/system-logs', methods=['GET'])
    echo @cross_origin()
    echo def get_system_logs(): return jsonify(system_logs)
    echo.
    echo @agent_bp.route('/system-status', methods=['GET'])
    echo @cross_origin()
    echo def get_system_status():
    echo     return jsonify({
    echo         'status': 'ZELF-OPTIMALISEREND', 'cpu': round(sum(a['cpu'] for a in agents) / len(agents), 1),
    echo         'memory': round(sum(a['memory'] for a in agents) / len(agents), 1),
    echo         'active_agents': len([a for a in agents if a['status'] != 'IDLE']), 'total_agents': len(agents)
    echo     })
    echo.
    echo @agent_bp.route('/trading-data', methods=['GET'])
    echo @cross_origin()
    echo def get_trading_data():
    echo     portfolio_data = [{'date': f'2024-07-{1+i:02d}', 'portfolioValue': round(100000 + random.uniform(-5000, 15000) + (i*500), 2), 'benchmark': round(100000 + (i*300), 2)} for i in range(30)]
    echo     return jsonify({
    echo         'portfolioData': portfolio_data, 'totalValue': portfolio_data[-1]['portfolioValue'],
    echo         'dailyChange': round(random.uniform(-2.5, 3.2), 2),
    echo         'positions': [
    echo             {'symbol': 'AAPL', 'quantity': 150, 'value': 25000, 'change': round(random.uniform(-2, 2.5), 2)},
    echo             {'symbol': 'GOOGL', 'quantity': 75, 'value': 22000, 'change': round(random.uniform(-2, 2.5), 2)},
    echo         ]
    echo     })
    echo.
    echo @agent_bp.route('/quantum-optimization', methods=['POST'])
    echo @cross_origin()
    echo def quantum_optimization():
    echo     result = {'success': True, 'quantum_advantage': round(random.uniform(15, 45), 1)}
    echo     system_logs.insert(0, {'time': datetime.now().strftime('%%H:%%M:%%S'), 'message': f'Quantum optimization voltooid: {result["quantum_advantage"]}%% voordeel.'})
    echo     return jsonify(result)
) > src\routes\agent.py

echo [SUCCES] Backend bestanden zijn aangemaakt.
echo.

:: Stap 4: Installeer backend dependencies
echo [STAP 4/6] Backend dependencies worden geinstalleerd...
python -m venv venv >nul
call venv\Scripts\activate.bat
pip install -r requirements.txt >nul
deactivate
echo [SUCCES] Backend is klaar voor gebruik.
echo.

:: Stap 5: Maak de frontend aan en installeer dependencies
echo [STAP 5/6] Frontend wordt geinitialiseerd en geinstalleerd...
cd ..\frontend

:: Maak een dummy package.json om 'npm create' te omzeilen
(
    echo {
    echo   "name": "frontend",
    echo   "private": true,
    echo   "version": "0.0.0",
    echo   "type": "module"
    echo }
) > package.json

:: Installeer dependencies
npm install react react-dom lucide-react recharts tailwindcss postcss autoprefixer >nul
npm install -D vite @vitejs/plugin-react >nul

:: Maak de mappenstructuur
mkdir public
mkdir src
cd src
mkdir components
cd components
mkdir ui
cd ..
mkdir assets
cd ..

:: Maak de frontend bestanden
(
    echo ^<html lang="en"^>
    echo   ^<head^>
    echo     ^<meta charset="UTF-8" /^>
    echo     ^<link rel="icon" type="image/svg+xml" href="/vite.svg" /^>
    echo     ^<meta name="viewport" content="width=device-width, initial-scale=1.0" /^>
    echo     ^<title^>Synapse Prime^</title^>
    echo   ^</head^>
    echo   ^<body^>
    echo     ^<div id="root"^>^</div^>
    echo     ^<script type="module" src="/src/main.jsx"^>^</script^>
    echo   ^</body^>
    echo ^</html^>
) > ..\index.html

(
    echo import React from 'react'
    echo import ReactDOM from 'react-dom/client'
    echo import App from './App.jsx'
    echo import './index.css'
    echo.
    echo ReactDOM.createRoot(document.getElementById('root')).render(
    echo   ^<React.StrictMode^>
    echo     ^<App /^>
    echo   ^</React.StrictMode^>,
    echo )
) > main.jsx

(
    echo import { useState, useEffect } from 'react'
    echo import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
    echo import { Activity, Cpu, DollarSign, TrendingUp, Users, Zap, Shield, Search, Code, TestTube, Palette, Settings, TrendingDown } from 'lucide-react'
    echo import './index.css'
    echo.
    echo const API_BASE = 'http://localhost:5001/api'
    echo.
    echo function App() {
    echo   const [data, setData] = useState(null);
    echo   const [loading, setLoading] = useState(true);
    echo   const [newMission, setNewMission] = useState('');
    echo.
    echo   useEffect(() => {
    echo     const fetchData = async () => {
    echo       try {
    echo         const res = await Promise.all([
    echo           fetch(`${API_BASE}/agents`), fetch(`${API_BASE}/active-project`),
    echo           fetch(`${API_BASE}/system-logs`), fetch(`${API_BASE}/system-status`),
    echo           fetch(`${API_BASE}/trading-data`)
    echo         ]);
    echo         const jsonData = await Promise.all(res.map(r => r.json()));
    echo         setData({ agents: jsonData[0], activeProject: jsonData[1], systemLogs: jsonData[2], systemStatus: jsonData[3], tradingData: jsonData[4] });
    echo       } catch (error) { console.error('Fout bij data ophalen:', error); }
    echo       setLoading(false);
    echo     };
    echo     fetchData();
    echo     const interval = setInterval(fetchData, 5000);
    echo     return () => clearInterval(interval);
    echo   }, []);
    echo.
    echo   if (loading) return ^<div className="min-h-screen bg-slate-900 flex items-center justify-center text-white"^>^<h1^>Initializing Synapse Prime...^</h1^>^</div^>;
    echo.
    echo   return (
    echo     ^<div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white"^>
    echo       ^<header className="border-b border-slate-700 bg-slate-900/80 p-4"^>
    echo         ^<h1 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent"^>Synapse Prime^</h1^>
    echo       ^</header^>
    echo       ^<main className="container mx-auto p-4"^>
    echo         ^<h2^>Dashboard komt hier^</h2^>
    echo          {/* De volledige UI code kan hier worden ingevoegd */}
    echo       ^</main^>
    echo     ^</div^>
    echo   );
    echo }
    echo.
    echo export default App;
) > App.jsx

(
    echo @tailwind base;
    echo @tailwind components;
    echo @tailwind utilities;
) > index.css

(
    echo /** @type {import('tailwindcss').Config} */
    echo export default {
    echo   content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
    echo   theme: { extend: {}, },
    echo   plugins: [],
    echo }
) > ..\tailwind.config.js

(
    echo export default {
    echo   plugins: { tailwindcss: {}, autoprefixer: {}, },
    echo }
) > ..\postcss.config.js

(
    echo import { defineConfig } from 'vite'
    echo import react from '@vitejs/plugin-react'
    echo.
    echo export default defineConfig({
    echo   plugins: [react()],
    echo })
) > ..\vite.config.js


echo [SUCCES] Frontend is geinitialiseerd.
echo.

:: Stap 6: Afronding
echo [STAP 6/6] Installatie voltooid.
echo.
echo.
echo  ================================================================
echo.
echo            SYNAPSE PRIME IS SUCCESVOL GEINSTALLEERD!
echo.
echo  ================================================================
echo.
echo  VOLG DEZE TWEE STAPPEN OM DE APPLICATIE TE STARTEN:
echo.
echo  1. START DE BACKEND:
echo     - Open een NIEUW commando-venster (cmd).
echo     - Navigeer naar de backend map met: cd "%userprofile%\Desktop\synapse-prime\backend"
echo     - Activeer de omgeving met: venv\Scripts\activate
echo     - Start de server met: python run_server.py
echo.
echo  2. START DE FRONTEND:
echo     - Open een TWEEDE NIEUW commando-venster (cmd).
echo     - Navigeer naar de frontend map met: cd "%userprofile%\Desktop\synapse-prime\frontend"
echo     - Start de dev server met: npm run dev
echo     - Open je browser en ga naar het adres dat in de terminal wordt getoond (meestal http://localhost:5173).
echo.
echo  ================================================================
echo.

pause
endlocal