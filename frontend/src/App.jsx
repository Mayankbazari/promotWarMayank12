import { useState } from 'react';
import { analyzeEmergency } from './api';

/* ────────── Quick example prompts ────────── */
const QUICK_EXAMPLES = [
  'My father has chest pain and sweating',
  'Road accident with head injury',
  'Child fell from stairs and cannot move leg',
  'Person choking on food',
  'Severe burns from cooking oil',
];

/* ────────── Loading stage labels ────────── */
const LOADING_STAGES = [
  'Classifying emergency…',
  'Planning agent dispatch…',
  'Generating action plan…',
  'Compiling response…',
];

/* ════════════════════════════════════════════
   App Component
   ════════════════════════════════════════════ */

export default function App() {
  const [input, setInput] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [loadingStage, setLoadingStage] = useState(0);

  async function handleAnalyze() {
    if (!input.trim() || input.trim().length < 3) return;

    setLoading(true);
    setError(null);
    setResult(null);
    setLoadingStage(0);

    // Simulate progressive loading stages
    const stageInterval = setInterval(() => {
      setLoadingStage((prev) => Math.min(prev + 1, LOADING_STAGES.length - 1));
    }, 1500);

    try {
      const data = await analyzeEmergency(input.trim());
      setResult(data);
    } catch (err) {
      setError(err.message || 'Failed to analyze emergency');
    } finally {
      clearInterval(stageInterval);
      setLoading(false);
    }
  }

  function handleClear() {
    setInput('');
    setResult(null);
    setError(null);
  }

  function handleQuickAction(text) {
    setInput(text);
    setResult(null);
    setError(null);
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
      handleAnalyze();
    }
  }

  return (
    <>
      {/* ── Header ── */}
      <header className="header" role="banner">
        <span className="header__icon" aria-hidden="true">🚨</span>
        <h1 className="header__title">Emergency Decision Agent</h1>
        <p className="header__subtitle">
          AI-powered multi-agent system for instant emergency analysis and structured action plans
        </p>
      </header>

      {/* ── Input ── */}
      <main role="main">
        <section className="input-card" aria-label="Emergency description input">
          <label className="input-card__label" htmlFor="emergency-input">
            Describe the emergency
          </label>
          <textarea
            id="emergency-input"
            className="input-card__textarea"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="e.g. My father has chest pain and sweating…"
            disabled={loading}
            aria-describedby="char-count"
            maxLength={2000}
          />

          {/* Quick Actions */}
          <div className="quick-actions" role="group" aria-label="Example emergency descriptions">
            {QUICK_EXAMPLES.map((example, i) => (
              <button
                key={i}
                className="quick-action"
                onClick={() => handleQuickAction(example)}
                disabled={loading}
                type="button"
              >
                {example}
              </button>
            ))}
          </div>

          <div className="input-card__actions">
            <span id="char-count" className="input-card__charcount">
              {input.length} / 2000 · ⌘+Enter to analyze
            </span>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              {(input || result) && (
                <button
                  className="btn btn--ghost"
                  onClick={handleClear}
                  disabled={loading}
                  type="button"
                  aria-label="Clear input and results"
                >
                  Clear
                </button>
              )}
              <button
                id="analyze-button"
                className="btn btn--primary"
                onClick={handleAnalyze}
                disabled={loading || input.trim().length < 3}
                type="button"
              >
                {loading ? (
                  <>
                    <span className="loading__spinner" style={{ width: 16, height: 16, borderWidth: 2 }} />
                    Analyzing…
                  </>
                ) : (
                  <>⚡ Analyze Emergency</>
                )}
              </button>
            </div>
          </div>
        </section>

        {/* ── Error ── */}
        {error && (
          <div className="error-banner" role="alert">
            <span className="error-banner__icon" aria-hidden="true">⚠️</span>
            <span className="error-banner__text">{error}</span>
          </div>
        )}

        {/* ── Loading ── */}
        {loading && (
          <div className="loading" aria-live="polite" aria-label="Analysis in progress">
            <div className="loading__spinner" />
            <span className="loading__text">Agent pipeline running…</span>
            <div className="loading__stages">
              {LOADING_STAGES.map((stage, i) => (
                <div
                  key={i}
                  className={`loading__stage ${
                    i < loadingStage ? 'loading__stage--done' :
                    i === loadingStage ? 'loading__stage--active' : ''
                  }`}
                >
                  <span className="loading__stage-dot" />
                  <span>{i < loadingStage ? '✓ ' : ''}{stage}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ── Results ── */}
        {result && <ResultsView data={result} />}
      </main>

      {/* ── Footer ── */}
      <footer className="footer" role="contentinfo">
        <p>
          Powered by <a href="https://ai.google.dev/" target="_blank" rel="noopener noreferrer">
            Google Gemini
          </a> · Multi-Agent Architecture
        </p>
      </footer>
    </>
  );
}


/* ════════════════════════════════════════════
   Results View
   ════════════════════════════════════════════ */

function ResultsView({ data }) {
  const { classification, plan, actions, emergency_numbers, summary } = data;

  return (
    <div className="results" aria-label="Analysis results">

      {/* Summary */}
      {summary && (
        <div className="summary-banner" role="status">
          <span className="summary-banner__icon" aria-hidden="true">📋</span>
          {summary}
        </div>
      )}

      {/* Classification */}
      <div className="result-card">
        <div className="result-card__header">
          <span className="result-card__icon" aria-hidden="true">🏷️</span>
          <h2 className="result-card__title">Classification</h2>
        </div>
        <div className="result-card__body">
          <div className="classification-grid">
            <div className="classification-item">
              <div className="classification-item__label">Type</div>
              <div className="classification-item__value classification-item__value--type">
                {classification.type}
              </div>
            </div>
            <div className="classification-item">
              <div className="classification-item__label">Severity</div>
              <div className={`classification-item__value classification-item__value--severity-${classification.severity}`}>
                {classification.severity}
              </div>
            </div>
            <div className="classification-item">
              <div className="classification-item__label">Confidence</div>
              <div className="classification-item__value" style={{ color: 'var(--text-primary)' }}>
                {(classification.confidence * 100).toFixed(0)}%
              </div>
            </div>
          </div>
          <div className="confidence-bar">
            <div className="confidence-bar__track">
              <div
                className="confidence-bar__fill"
                style={{ width: `${classification.confidence * 100}%` }}
              />
            </div>
            <div className="confidence-bar__label">
              Confidence: {(classification.confidence * 100).toFixed(1)}%
            </div>
          </div>

          {/* Reasoning */}
          {classification.reasoning && (
            <div className="reasoning-box" style={{ marginTop: '1.5rem', borderTop: '1px solid var(--border-subtle)', paddingTop: '1rem' }}>
              <div className="classification-item__label" style={{ marginBottom: '0.5rem', display: 'flex', alignItems: 'center' }}>
                <span style={{ fontSize: '1rem', marginRight: '0.5rem' }}>💬</span>
                Agent Analysis
              </div>
              <p className="reasoning-text" style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: 1.6, fontStyle: 'italic' }}>
                "{classification.reasoning}"
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Agent Dispatch */}
      <div className="result-card">
        <div className="result-card__header">
          <span className="result-card__icon" aria-hidden="true">📋</span>
          <h2 className="result-card__title">Agent Dispatch</h2>
        </div>
        <div className="result-card__body">
          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            {plan.agents.map((agent, i) => (
              <span
                key={i}
                className="condition-badge condition-badge--high"
              >
                🤖 {agent.replace('_', ' ')}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Action Plans from each agent */}
      {actions.map((action, idx) => (
        <div className="result-card" key={idx}>
          <div className="result-card__header">
            <span className="result-card__icon" aria-hidden="true">
              {action.agent_name === 'medical_agent' ? '🏥' : '🚨'}
            </span>
            <h2 className="result-card__title">
              {action.agent_name.replace('_', ' ')} Response
            </h2>
          </div>
          <div className="result-card__body">
            {/* Condition (medical agent only) */}
            {action.result.condition && (
              <div className={`condition-badge condition-badge--${action.result.risk}`}>
                💊 {action.result.condition}
              </div>
            )}

            {/* Risk */}
            <div className={`condition-badge condition-badge--${action.result.risk}`} style={{ marginLeft: action.result.condition ? '0.5rem' : 0 }}>
              Risk: {action.result.risk}
            </div>

            {/* Actions */}
            <ol className="action-list" aria-label="Recommended actions">
              {action.result.actions.map((step, i) => (
                <li key={i} className="action-item">
                  <span className="action-item__number">{String(i + 1).padStart(2, '0')}</span>
                  <span className="action-item__text">{step}</span>
                </li>
              ))}
            </ol>
          </div>
        </div>
      ))}

      {/* Emergency Numbers */}
      <div className="result-card">
        <div className="result-card__header">
          <span className="result-card__icon" aria-hidden="true">📞</span>
          <h2 className="result-card__title">Emergency Numbers</h2>
        </div>
        <div className="result-card__body">
          <div className="emergency-numbers">
            <div className="emergency-number" role="listitem">
              <span className="emergency-number__icon" aria-hidden="true">🚑</span>
              <div className="emergency-number__label">Ambulance</div>
              <div className="emergency-number__value" aria-label="Ambulance number 108">
                {emergency_numbers.ambulance}
              </div>
            </div>
            <div className="emergency-number" role="listitem">
              <span className="emergency-number__icon" aria-hidden="true">👮</span>
              <div className="emergency-number__label">Police</div>
              <div className="emergency-number__value" aria-label="Police number 100">
                {emergency_numbers.police}
              </div>
            </div>
            <div className="emergency-number" role="listitem">
              <span className="emergency-number__icon" aria-hidden="true">🚒</span>
              <div className="emergency-number__label">Fire</div>
              <div className="emergency-number__value" aria-label="Fire department number 101">
                {emergency_numbers.fire}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
