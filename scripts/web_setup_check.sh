#!/usr/bin/env bash
# Checks the tools the website team needs. Prints OK or MISSING per tool. Installs nothing.
ok(){ echo "OK       $1"; }; miss(){ echo "MISSING  $1  ->  $2"; rc=1; }
rc=0
command -v node >/dev/null && ok "node $(node -v)" || miss node "ask Rahul before installing"
command -v npm  >/dev/null && ok "npm $(npm -v)"   || miss npm  "ask Rahul before installing"
command -v git  >/dev/null && ok "git $(git --version | cut -d' ' -f3)" || miss git "n/a"
command -v python3 >/dev/null && ok "python3 $(python3 -V | cut -d' ' -f2)" || miss python3 "n/a"
G=$(npm root -g 2>/dev/null)
if node -e "require('playwright')" 2>/dev/null || (cd "$G/.." 2>/dev/null && NODE_PATH="$G" node -e "require('playwright')" 2>/dev/null); then ok "playwright (node)"; else miss "playwright (node)" "ask Rahul before: npm i -g playwright"; fi
if [ -d /opt/pw-browsers ] && ls /opt/pw-browsers | grep -q chromium; then ok "chromium at /opt/pw-browsers"; else miss "chromium" "ask Rahul before installing a browser"; fi
echo "Outside API keys needed for web work: none."
exit $rc
