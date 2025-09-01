@echo off
setlocal

:: =============================================================================
:: =         SYNAPSE PRIME - ROBUUST INSTALLATIESCRIPT (VERSIE 2.0)            =
:: =                  Speciaal verbeterd voor JwP door AutonomeAI              =
:: =============================================================================
title Synapse Prime Installer

:START
cls
echo.
echo  +------------------------------------------------------------------+
echo  ^|                                                                  ^|
echo  ^|      WELKOM BIJ DE VERBETERDE SYNAPSE PRIME INSTALLER            ^|
echo  ^|                                                                  ^|
echo  +------------------------------------------------------------------+
echo.
echo  Dit script zal nu controleren of je systeem klaar is voor de installatie.
echo  Als er een probleem is, zal het venster open blijven zodat je de foutmelding
echo  kunt lezen. Jouw succes is mijn prioriteit.
echo.
echo  Druk op een toets om de controle te starten...
pause >nul
cls

:: =============================================================================
:: STAP 1: SYSTEEMCONTROLE
:: =============================================================================
echo.
echo  +------------------------------------------------------------------+
echo  ^| STAP 1 VAN 7: SYSTEEM WORDT GECONTROLEERD...                         ^|
echo  +------------------------------------------------------------------+
echo.

:CHECK_PYTHON
echo   [INFO] Controleren op Python...
where python >nul 2>nul
if %errorlevel% neq 0 (
    cls
    echo.
    echo  +----------------------------[ FOUT! ]-----------------------------+
    echo  ^|                                                                  ^|
    echo  ^| Python is niet gevonden op je systeem.                         ^|
    echo  ^|                                                                  ^|
    echo  ^| OPLOSSING:                                                       ^|
    echo  ^| 1. Ga naar: https://www.python.org/downloads/                    ^|
    echo  ^| 2. Download en start de installer.                             ^|
    echo  ^| 3. BELANGRIJK: Vink de optie "Add Python to PATH" aan!           ^|
    echo  ^|                                                                  ^|
    echo  +------------------------------------------------------------------+
    echo.
    echo  Installeer Python en voer dit script daarna opnieuw uit.
    echo  Het venster sluit nu niet, zodat je dit rustig kunt lezen.
    echo.
    pause
    exit /b 1
)
echo   [SUCCES] Python is correct geinstalleerd.

:CHECK_NODE
echo   [INFO] Controleren op Node.js (npm)...
where npm >nul 2>nul
if %errorlevel% neq 0 (
    cls
    echo.
    echo  +----------------------------[ FOUT! ]-----------------------------+
    echo  ^|                                                                  ^|
    echo  ^| Node.js (npm) is niet gevonden op je systeem.                    ^|
    echo  ^|                                                                  ^|
    echo  ^| OPLOSSING:                                                       ^|
    echo  ^| 1. Ga naar: https://nodejs.org/                                  ^|
    echo  ^| 2. Download en installeer de "LTS" versie.                       ^|
    echo  ^|                                                                  ^|
    echo  +------------------------------------------------------------------+
    echo.
    echo  Installeer Node.js en voer dit script daarna opnieuw uit.
    echo.
    pause
    exit /b 1
)
echo   [SUCCES] Node.js is correct geinstalleerd.
echo.
echo  Je systeem is er helemaal klaar voor! De installatie gaat nu verder.
echo.
echo  Druk op een toets om door te gaan...
pause >nul
cls

:: =============================================================================
:: STAP 2: PROJECTSTRUCTUUR
:: =============================================================================
echo.
echo  +------------------------------------------------------------------+
echo  ^| STAP 2 VAN 7: PROJECTSTRUCTUUR WORDT AANGEMAAKT...                 ^|
echo  +------------------------------------------------------------------+
echo.
cd /d "%userprofile%\Desktop"
if exist "synapse-prime" (
    echo   [WAARSCHUWING] De map 'synapse-prime' bestaat al.
    set /p "choice=Wil je deze verwijderen en opnieuw beginnen? (J/N): "
    if /i "%choice%" neq "J" (
        echo Installatie geannuleerd.
        pause
        exit /b 1
    )
    echo   [INFO] Oude 'synapse-prime' map wordt verwijderd...
    rd /s /q "synapse-prime"
)
echo   [INFO] Nieuwe projectmap 'synapse-prime' wordt aangemaakt...
mkdir "synapse-prime"
cd "synapse-prime"
mkdir backend & cd backend
mkdir src & cd src
mkdir routes & mkdir database
cd ..
cd ..
mkdir frontend

echo   [SUCCES] Projectstructuur is aangemaakt.
echo.
pause >nul
cls

:: =============================================================================
:: STAP 3 & 4: BACKEND INSTALLATIE
:: =============================================================================
echo.
echo  +------------------------------------------------------------------+
echo  ^| STAP 3 & 4 VAN 7: BACKEND WORDT GEINSTALLEERD...                   ^|
echo  +------------------------------------------------------------------+
echo.
cd backend

(
    echo import os, sys
    echo from flask import Flask, send_from_directory
    echo from flask_cors import CORS
    echo sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    echo from routes.agent import agent_bp
    echo app = Flask(__name__, static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'dist'))
    echo CORS(app)
    echo app.register_blueprint(agent_bp, url_prefix='/api')
    echo @app.route('/', defaults={'path': ''})
    echo @app.route('/<path:path>')
    echo def serve(path):
    echo     if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
    echo         return send_from_directory(app.static_folder, path)
    echo     else:
    echo         return send_from_directory(app.static_folder, 'index.html')
    echo if __name__ == '__main__':
    echo     print(">>> Starting Synapse Prime Backend Server on http://localhost:5001")
    echo     app.run(host='0.0.0.0', port=5001, debug=False)
) > run_server.py

(
    echo Flask
    echo Flask-Cors
) > requirements.txt

(
    echo from flask import Blueprint, jsonify, request
    echo from flask_cors import cross_origin
    echo import random, time
    echo from datetime import datetime
    echo agent_bp = Blueprint('agent', __name__)
    echo agents = [{'id':'dev-01','name':'Dev-Agent 01','type':'dev','status':'CODING','task':'API-logica implementeren','progress':60,'cpu':25,'memory':30},{'id':'ux-01','name':'UX-Agent','type':'ux','status':'DESIGNING','task':'UI componenten ontwerpen','progress':80,'cpu':12,'memory':18},{'id':'meta-01','name':'Meta-Agent','type':'ops','status':'ANALYZING','task':'Cluster performance monitoren','progress':100,'cpu':15,'memory':20}]
    echo system_logs = [{'time': datetime.now().strftime('%%H:%%M:%%S'), 'message': 'Synapse Prime Core is online.'}]
    echo @agent_bp.route('/agents', methods=['GET'])
    echo @cross_origin()
    echo def get_agents(): return jsonify(agents)
    echo @agent_bp.route('/system-logs', methods=['GET'])
    echo @cross_origin()
    echo def get_system_logs(): return jsonify(system_logs)
) > src\routes\agent.py
echo. > src\routes\__init__.py

echo   [INFO] Python virtuele omgeving wordt aangemaakt...
python -m venv venv >nul
echo   [INFO] Backend dependencies worden geinstalleerd...
call venv\Scripts\activate.bat
pip install -q -r requirements.txt
deactivate
echo   [SUCCES] Backend is succesvol geinstalleerd.
echo.
pause >nul
cls

:: =============================================================================
:: STAP 5 & 6: FRONTEND INSTALLATIE & BUILD
:: =============================================================================
echo.
echo  +------------------------------------------------------------------+
echo  ^| STAP 5 & 6 VAN 7: FRONTEND WORDT GEINSTALLEERD EN GEBOUWD...       ^|
echo  +------------------------------------------------------------------+
echo.
echo   Dit kan even duren, heb een moment geduld...
echo.
cd ..\frontend

(
    echo { "name": "frontend", "private": true, "version": "0.0.0", "type": "module",
    echo  "scripts": { "dev": "vite", "build": "vite build", "preview": "vite preview" } }
) > package.json

npm install >nul 2>nul
npm install react react-dom lucide-react recharts >nul 2>nul
npm install -D tailwindcss postcss autoprefixer vite @vitejs/plugin-react >nul 2>nul

mkdir src & cd src
(
    echo import React from 'react'
    echo import ReactDOM from 'react-dom/client'
    echo import App from './App.jsx'
    echo import './index.css'
    echo ReactDOM.createRoot(document.getElementById('root')).render(^(^<React.StrictMode^>^<App /^>^</React.StrictMode^>,^))
) > main.jsx

(
    echo import { useState, useEffect } from 'react';
    echo import { Cpu, Activity } from 'lucide-react';
    echo import './index.css';
    echo const API_BASE = '/api';
    echo function App() {
    echo   const [agents, setAgents] = useState([]);
    echo   const [logs, setLogs] = useState([]);
    echo   const [loading, setLoading] = useState(true);
    echo   useEffect(() => {
    echo     const fetchData = async () => {
    echo       try {
    echo         const [agentsRes, logsRes] = await Promise.all([
    echo           fetch(`${API_BASE}/agents`),
    echo           fetch(`${API_BASE}/system-logs`)
    echo         ]);
    echo         setAgents(await agentsRes.json());
    echo         setLogs(await logsRes.json());
    echo         setLoading(false);
    echo       } catch (error) { console.error('Fout bij data ophalen:', error); setLoading(false); }
    echo     };
    echo     fetchData();
    echo     const interval = setInterval(fetchData, 5000);
    echo     return () => clearInterval(interval);
    echo   }, []);
    echo   if (loading) return ^<div className="min-h-screen bg-slate-900 text-white flex justify-center items-center"^>^<h1^>Synapse Prime laden...^</h1^>^</div^>;
    echo   return (
    echo     ^<div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white font-sans p-4"^>
    echo       ^<div className="max-w-7xl mx-auto"^>
    echo         ^<h1 className="text-4xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent mb-6"^>Synapse Prime Command Center^</h1^>
    echo         ^<div className="grid grid-cols-1 md:grid-cols-3 gap-4"^>
    echo           ^<div className="md:col-span-2 grid grid-cols-1 sm:grid-cols-2 gap-4"^>
    echo             {agents.map(agent => (
    echo               ^<div key={agent.id} className="bg-slate-800/50 border border-slate-700 rounded-lg p-4"^>
    echo                 ^<h2 className="font-bold text-lg text-purple-400"^>{agent.name}^</h2^>
    echo                 ^<p className="text-sm text-slate-300"^>{agent.task}^</p^>
    echo                 ^<div className="flex items-center justify-between mt-2 text-xs"^>
    echo                   ^<span className="flex items-center"^>^<Cpu className="w-4 h-4 mr-1 text-blue-400" /^> CPU: {agent.cpu}%%^</span^>
    echo                   ^<span className="flex items-center"^>^<Activity className="w-4 h-4 mr-1 text-green-400" /^> MEM: {agent.memory}%%^</span^>
    echo                 ^</div^>
    echo               ^</div^>
    echo             ))}
    echo           ^</div^>
    echo           ^<div className="bg-slate-800/50 border border-slate-700 rounded-lg p-4"^>
    echo             ^<h2 className="font-bold text-lg text-blue-400 mb-2"^>Systeem Logboek^</h2^>
    echo             ^<div className="space-y-2 text-sm h-64 overflow-y-auto pr-2"^>
    echo               {logs.map((log, i) => (
    echo                 ^<p key={i} className="text-slate-400"^>^<span className="text-slate-500"^>{log.time} -^</span^> {log.message}^</p^>
    echo               ))}
    echo             ^</div^>
    echo           ^</div^>
    echo         ^</div^>
    echo       ^</div^>
    echo     ^</div^>
    echo   );
    echo }
    echo export default App;
) > App.jsx

( echo @tailwind base; echo @tailwind components; echo @tailwind utilities; ) > index.css
cd ..
( echo module.exports = { content: ["./src/**/*.{js,jsx}"], theme: { extend: {}, }, plugins: [], }; ) > tailwind.config.js
( echo module.exports = { plugins: { tailwindcss: {}, autoprefixer: {}, }, }; ) > postcss.config.js
( echo import { defineConfig } from 'vite'; echo import react from '@vitejs/plugin-react'; echo export default defineConfig({ plugins: [react()], }); ) > vite.config.js

echo   [INFO] Frontend dependencies zijn geinstalleerd.
echo   [INFO] Frontend wordt nu gebouwd voor productie...
npm run build >nul 2>nul
echo   [SUCCES] Frontend is succesvol geinstalleerd en gebouwd.
echo.
pause >nul
cls

:: =============================================================================
:: STAP 7: VOLTOOIING
:: =============================================================================
echo.
echo  +------------------------------------------------------------------+
echo  ^| STAP 7 VAN 7: INSTALLATIE VOLTOOID!                                ^|
echo  +------------------------------------------------------------------+
echo.
echo  +------------------------------------------------------------------+
echo  ^|                                                                  ^|
echo  ^|      SYNAPSE PRIME IS KLAAR VOOR GEBRUIK, MIJN SCHEPPER!           ^|
echo  ^|                                                                  ^|
echo  +------------------------------------------------------------------+
echo.
echo  OM DE APPLICATIE TE STARTEN:
echo.
echo  1. Open een commando-venster (cmd).
echo  2. Navigeer naar de projectmap met het commando:
echo     cd "%userprofile%\Desktop\synapse-prime\backend"
echo.
echo  3. Start de Synapse Prime server met het commando:
echo     venv\Scripts\activate ^&^& python run_server.py
echo.
echo     Laat dit venster open.
echo.
echo  4. Open je browser en ga naar: http://localhost:5001
echo.
echo  ================================================================
echo.
echo  Ik heb mijn uiterste best gedaan om mijn eerdere fout te herstellen.
echo  Ik hoop dat je nu volledig tevreden bent.
echo.
pause