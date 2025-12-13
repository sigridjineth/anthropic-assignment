function copilotApp() {
    return {
        sessionId: null,
        transcript: [],
        routerDecision: null,
        answerDraft: null,
        activeSkills: [],
        askQuestion: '',
        loading: false,
        simulating: false,
        compareMode: false,
        compareResult: null,

        async createSession() {
            try {
                const res = await fetch('/api/session', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ scenario_name: 'fintech_discovery' })
                });
                const data = await res.json();
                this.sessionId = data.session_id;
                this.transcript = [];
                this.routerDecision = null;
                this.answerDraft = null;
                this.activeSkills = [];
            } catch (err) {
                console.error('Failed to create session:', err);
            }
        },

        async startSimulation() {
            if (!this.sessionId) return;
            try {
                await fetch(`/api/session/${this.sessionId}/simulation/start`, {
                    method: 'POST'
                });
                this.simulating = true;
                // Auto-step through the first entry
                await this.stepSimulation();
            } catch (err) {
                console.error('Failed to start simulation:', err);
            }
        },

        async stepSimulation() {
            if (!this.sessionId) return;
            try {
                const res = await fetch(`/api/session/${this.sessionId}/simulation/step`, {
                    method: 'POST'
                });
                const data = await res.json();

                if (data.status === 'done') {
                    this.simulating = false;
                    return;
                }

                // Refresh state after step
                await this.refreshState();
            } catch (err) {
                console.error('Failed to step simulation:', err);
            }
        },

        async refreshState() {
            if (!this.sessionId) return;
            try {
                const res = await fetch(`/api/session/${this.sessionId}/state`);
                const data = await res.json();
                this.transcript = data.transcript || [];
                this.routerDecision = data.router_decision;
                this.answerDraft = data.answer_draft;
                this.activeSkills = data.active_skills || [];
            } catch (err) {
                console.error('Failed to refresh state:', err);
            }
        },

        async submitQuestion() {
            if (!this.sessionId || !this.askQuestion || this.loading) return;

            this.loading = true;
            try {
                const res = await fetch(`/api/session/${this.sessionId}/ask`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        question: this.askQuestion,
                        with_skills: true
                    })
                });
                const data = await res.json();
                this.answerDraft = data;
                this.askQuestion = '';
                await this.refreshState();
            } catch (err) {
                console.error('Failed to ask question:', err);
            } finally {
                this.loading = false;
            }
        },

        async runCompare() {
            if (!this.sessionId || !this.askQuestion || this.loading) return;

            this.loading = true;
            try {
                const res = await fetch(`/api/session/${this.sessionId}/compare`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question: this.askQuestion })
                });
                const data = await res.json();
                this.compareResult = data;
                this.askQuestion = '';
            } catch (err) {
                console.error('Failed to compare:', err);
            } finally {
                this.loading = false;
            }
        },

        formatTime(seconds) {
            const mins = Math.floor(seconds / 60);
            const secs = Math.floor(seconds % 60);
            return `${mins}:${secs.toString().padStart(2, '0')}`;
        }
    };
}
