#!/usr/bin/env bash
# Maak uitvoerbaar met: chmod +x ./scripts/repair_project.sh
set -euo pipefail

LOG_DIR="./repair_logs"
REPORT="$LOG_DIR/repair_report.txt"
TIMESTAMP="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

mkdir -p "$LOG_DIR"
echo "Repair report - $TIMESTAMP" > "$REPORT"
echo "" >> "$REPORT"

log() {
  echo "[$(date +"%H:%M:%S")] $*" | tee -a "$REPORT"
}

detect_pkg_manager() {
  if [ -f pnpm-lock.yaml ]; then echo "pnpm"
  elif [ -f yarn.lock ]; then echo "yarn"
  elif [ -f package-lock.json ] || [ -f package.json ]; then echo "npm"
  else echo "none"; fi
}

run_cmd_safe() {
  local label="$1"; shift
  echo "---- $label ----" >> "$REPORT"
  if "$@" >> "$LOG_DIR/${label// /_}.log" 2>&1; then
    echo "$label: OK" | tee -a "$REPORT"
  else
    echo "$label: FAILED (see $LOG_DIR/${label// /_}.log)" | tee -a "$REPORT"
  fi
  echo "" >> "$REPORT"
}

main() {
  log "Start reparatie script"

  PKG_MANAGER=$(detect_pkg_manager)
  log "Detected package manager: $PKG_MANAGER"

  if [ "$PKG_MANAGER" = "none" ]; then
    log "Geen package manager gevonden. Controleer of je in de juiste map zit."
  else
    case "$PKG_MANAGER" in
      pnpm) run_cmd_safe "install_deps" pnpm install ;;
      yarn) run_cmd_safe "install_deps" yarn install ;;
      npm)  run_cmd_safe "install_deps" npm install ;;
    esac
  fi

  # ESLint auto-fix
  if command -v npx >/dev/null 2>&1 && grep -q eslint package.json 2>/dev/null || [ -f .eslintrc.json ] || [ -f .eslintrc.js ]; then
    log "ESLint gevonden, probeer --fix"
    run_cmd_safe "eslint_fix" npx eslint . --ext .js,.jsx,.ts,.tsx --fix || true
  else
    log "Geen eslint-config gedetecteerd of npx niet beschikbaar."
  fi

  # TypeScript check
  if [ -f tsconfig.json ]; then
    if command -v npx >/dev/null 2>&1; then
      log "tsconfig.json gevonden, run tsc --noEmit"
      run_cmd_safe "tsc_check" npx tsc --noEmit
    else
      log "npx niet beschikbaar om tsc te runnen."
    fi
  fi

  # Run build and test scripts if aanwezig
  if [ -f package.json ]; then
    if grep -q "\"build\"" package.json 2>/dev/null; then
      log "build script aanwezig in package.json"
      run_cmd_safe "npm_build" ${PKG_MANAGER:--} run build || true
    fi
    if grep -q "\"test\"" package.json 2>/dev/null; then
      log "test script aanwezig in package.json"
      run_cmd_safe "npm_test" ${PKG_MANAGER:--} run test || true
    fi
  fi

  # Python requirements
  if [ -f requirements.txt ]; then
    if command -v python3 >/dev/null 2>&1; then
      log "requirements.txt gevonden, probeer pip install in venv"
      python3 -m venv "$LOG_DIR/venv" || true
      # shellcheck disable=SC1090
      source "$LOG_DIR/venv/bin/activate"
      pip install -r requirements.txt >> "$LOG_DIR/pip_install.log" 2>&1 || true
      deactivate
      echo "pip install logs: $LOG_DIR/pip_install.log" >> "$REPORT"
    else
      log "Python3 niet gevonden op PATH."
    fi
  fi

  # Parse logs for common issues
  log "Parsing logs op veelvoorkomende fouten"
  echo "" >> "$REPORT"
  echo "Common issues found:" >> "$REPORT"
  grep -E "Error:|ERR_|Module not found|Cannot find module|TS[0-9]{1,4}" -R "$LOG_DIR" || echo "Geen expliciete fouten gevonden in logs." >> "$REPORT"
  echo "" >> "$REPORT"

  # Repair/overwrite VS Code launch.json (Node.js friendly)
  mkdir -p .vscode
  cat > .vscode/launch.json <<'JSON'
{
  // filepath: .vscode/launch.json
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Launch Program (pwa-node)",
      "type": "pwa-node",
      "request": "launch",
      "program": "${workspaceFolder}/index.js",
      "cwd": "${workspaceFolder}",
      "console": "integratedTerminal",
      "internalConsoleOptions": "neverOpen"
    },
    {
      "name": "Attach to Process",
      "type": "pwa-node",
      "request": "attach",
      "processId": "${command:PickProcess}",
      "cwd": "${workspaceFolder}"
    },
    {
      "name": "Attach to port 9229 (AI Debugger fallback)",
      "type": "pwa-node",
      "request": "attach",
      "port": 9229,
      "address": "localhost",
      "restart": false,
      "localRoot": "${workspaceFolder}",
      "remoteRoot": null
    }
  ]
}
JSON

  echo ".vscode/launch.json aangemaakt/overschreven" | tee -a "$REPORT"

  # AI Debugger troubleshooting hints
  {
    echo ""
    echo "AI Debugger troubleshooting:"
    echo "- Als je een AI-debugger extensie gebruikt: probeer de extensie te herinstalleren via Extensions pane (Uninstall -> Install)."
    echo "- Open 'Help > Toggle Developer Tools' in VS Code en kijk in Console voor extensie fouten."
    echo "- Open de Extension Host logs: Command Palette -> 'Developer: Open Logs Folder' -> kies 'exthost'."
    echo "- Als de AI Debugger een aparte service of CLI gebruikt, controleer of die service draait en op de juiste poorten luistert."
    echo "- Probeer debug session te starten met de hierboven aangemaakte 'Attach to port 9229 (AI Debugger fallback)' nadat je node --inspect=9229 hebt gestart."
  } >> "$REPORT"

  log "Klaar. Zie $REPORT en $LOG_DIR voor details."
}

main "$@"