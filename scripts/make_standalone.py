"""Gera index.html (versão standalone, pronta para GitHub Pages) a partir de artifact/covid-dashboard.html.

A página do artefato usa a API `dash` do tipo Dashboard do Claude. Aqui ela é emulada:
os dados vêm de data/covid_mexico_agregado.csv e os filtros ficam em memória.

Uso: python3 scripts/make_standalone.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
page = (ROOT / "artifact" / "covid-dashboard.html").read_text(encoding="utf-8")
page = page.replace('<meta name="dash-one-writer">\n', "")

HEAD = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>COVID-19 no México</title>
<meta name="description" content="Dashboard interativo de 1,05 milhão de pacientes de COVID-19 no México: letalidade por idade, sexo, doenças preexistentes e unidade médica.">
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js"></script>
<style>
  :root {
    color-scheme: light;
    --color-fg: #1b1c1f; --color-fg-muted: #64666d; --color-bg: #ffffff; --color-panel: #f6f7f8;
    --color-border-line: #e1e3e6; --color-bad: #c8332f;
    --font-anthropic-sans: "Inter Tight", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
    --font-anthropic-serif: "Source Serif 4", Georgia, "Times New Roman", serif;
    --cds-font-size-caption: 12px; --cds-font-size-body: 14px; --cds-font-size-heading: 16px; --cds-font-size-title: 28px;
    --cds-font-weight-medium: 500;
    --cds-gap-xs: 4px; --cds-gap-sm: 8px; --cds-gap-md: 12px; --cds-gap-lg: 16px; --cds-gap-xl: 28px;
    --cds-pad-xs: 4px; --cds-pad-sm: 8px; --cds-pad-md: 12px; --cds-pad-lg: 16px; --cds-radius: 6px;
    --cds-chart-muted: #b8bbc1; --cds-chart-grid: #eceef0; --cds-chart-axis: #c6c9ce; --cds-chart-reference: #868a92;
    --cds-chart-status-critical: #d23b3b; --cds-surface-popover: #ffffff; --cds-border: #e1e3e6;
    --cds-shadow-popover: 0 6px 18px rgba(0, 0, 0, .12); --cds-text-secondary: #64666d; --cds-dur-slow: .3s;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      color-scheme: dark;
      --color-fg: #eeeff1; --color-fg-muted: #a3a6ad; --color-bg: #15161a; --color-panel: #1d1f24;
      --color-border-line: #2e3138; --color-bad: #f07070;
      --cds-chart-muted: #5b5f68; --cds-chart-grid: #272a30; --cds-chart-axis: #41454d; --cds-chart-reference: #8d919a;
      --cds-chart-status-critical: #e66767; --cds-surface-popover: #24272d; --cds-border: #353941;
      --cds-shadow-popover: 0 6px 18px rgba(0, 0, 0, .5); --cds-text-secondary: #a3a6ad;
    }
  }
  body { margin: 0; background: var(--color-bg); color: var(--color-fg); font: 14px/1.4 var(--font-anthropic-sans); }
  #dash-root { padding-block: 32px 48px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
  [hidden] { display: none !important; }
  .dash-skeleton { background: var(--color-bg); border-radius: var(--cds-radius); animation: sk 1.2s ease-in-out infinite alternate; }
  @keyframes sk { from { opacity: .5; } to { opacity: 1; } }
  @media (prefers-reduced-motion: reduce) { .dash-skeleton { animation: none; } }
</style>
<script>
  // Emulação mínima da API `dash` usada pela página do artefato.
  (() => {
    const DEFAULTS = { resultado: 'pos', sexo: null, atendimento: null, unidade: null, idade_de: 0, idade_ate: 90, comorb: [] };
    const dark = matchMedia('(prefers-color-scheme: dark)');
    const LIGHT = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#008300', '#6250d6', '#e34948'];
    const DARK = ['#3987e5', '#d95926', '#199e70', '#c98500', '#d55181', '#008300', '#9085e9', '#e66767'];
    let params = { ...DEFAULTS }, state = { status: 'loading', data: [] };
    const draws = [], listeners = [];
    const run = () => {
      listeners.forEach((f) => f());
      for (const [name, fn] of draws) document.querySelectorAll(`[data-draw="${name}"]`).forEach((el) => fn(el));
    };
    window.dash = {
      get colors() { return dark.matches ? DARK : LIGHT; },
      data: () => state,
      params: () => params,
      setParams: (o) => { params = { ...params, ...o }; run(); },
      resetParams: () => { params = { ...DEFAULTS }; run(); },
      onData: (fn) => { listeners.push(fn); fn(); },
      draw: (name, fn) => draws.push([name, fn]),
      setLink: () => {},
    };
    let raf = 0;
    const schedule = () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(run); };
    addEventListener('resize', schedule);
    dark.addEventListener('change', schedule);
    addEventListener('DOMContentLoaded', () => {
      run();
      fetch('data/covid_mexico_agregado.csv')
        .then((r) => { if (!r.ok) throw new Error(r.status); return r.text(); })
        .then((t) => { state = { status: 'ok', data: d3.csvParse(t) }; run(); })
        .catch(() => { state = { status: 'error', data: [] }; run(); });
    });
  })();
</script>
</head>
<body>
<div id="dash-root">
"""

TAIL = """
</div>
</body>
</html>
"""

(ROOT / "index.html").write_text(HEAD + page + TAIL, encoding="utf-8")
print("index.html gerado")
