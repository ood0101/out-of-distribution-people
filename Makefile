# OOD People — daily ritual + maintenance commands.
# Run `make help` to see what's available.

.PHONY: help morning today triage clusters promote mark refresh render install-alias

help:
	@echo ""
	@echo "Daily ritual:"
	@echo "  make morning       Full daily ritual (refresh + clusters + triage + today's 5)"
	@echo "  make today         Just today's 5 names"
	@echo "  make triage        Top 15 untriaged entries by signal score"
	@echo "  make clusters      Cluster activity in last 14 days"
	@echo "  make promote       Delta Fellows ready for full dossier upgrade"
	@echo ""
	@echo "Maintenance:"
	@echo "  make refresh       Rebuild state from dossiers"
	@echo "  make render        Re-render index outreach panel"
	@echo ""
	@echo "Setup:"
	@echo "  make install-alias Add 'morning' shell alias to ~/.zshrc"
	@echo ""

morning:
	@python3 scripts/morning.py

today:
	@python3 scripts/today.py

triage:
	@python3 scripts/suggest_urgency.py

clusters:
	@python3 scripts/cluster_check.py

promote:
	@python3 scripts/promote_candidates.py

refresh:
	@python3 data/build_outreach_state.py > /dev/null && echo "✓ state refreshed"

render:
	@python3 data/build_outreach_view.py

install-alias:
	@if ! grep -q "alias morning=" ~/.zshrc 2>/dev/null; then \
		echo "" >> ~/.zshrc; \
		echo "# OOD People daily ritual" >> ~/.zshrc; \
		echo "alias morning='cd \"$(CURDIR)\" && make morning'" >> ~/.zshrc; \
		echo "alias today='cd \"$(CURDIR)\" && make today'" >> ~/.zshrc; \
		echo "✓ Aliases added to ~/.zshrc"; \
		echo "  Run: source ~/.zshrc"; \
		echo "  Then type: morning"; \
	else \
		echo "✓ Aliases already installed in ~/.zshrc"; \
	fi
