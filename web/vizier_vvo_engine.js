// =========================================================================
// VERTEX AI VIZIER LIVE MULTI-SUBSTATION VOLT-VAR STUDIO (KLANG VALLEY)
// =========================================================================

(function(window) {
  'use strict';

  // Substation Database - Klang Valley 500kV/275kV/132kV Ring
  const SUBSTATIONS = {
    BBAD: {
      id: 'BBAD',
      code: 'BBAD',
      name: 'Bukit Badong Substation',
      shortName: 'Bukit Badong',
      fullName: 'Bukit Badong 500/275kV Bulk Supply Point',
      kv: 500,
      x: 135, y: 75,
      role: 'Northern Supergrid Gateway & Hydro Infeed',
      p: 180, q: 45,
      // Base vs Optimized values per scenario
      scenarios: {
        heatwave:    { baseV: 1.028, optV: 1.006, baseTap: 0,  optTap: +1, baseCap: 0,  optCap: 0,  inverterQ: 0,   solarMw: 0 },
        solar_peak:  { baseV: 1.034, optV: 1.008, baseTap: 0,  optTap: 0,  baseCap: 0,  optCap: 0,  inverterQ: 0,   solarMw: 0 },
        nocturnal:   { baseV: 1.048, optV: 1.004, baseTap: +1, optTap: -2, baseCap: 0,  optCap: 50, inverterQ: 0,   solarMw: 0 }, // 50 MVAR reactor
        storm_squall:{ baseV: 1.022, optV: 1.005, baseTap: 0,  optTap: +1, baseCap: 0,  optCap: 0,  inverterQ: 0,   solarMw: 0 }
      },
      vCurve: { v1: 0.92, v2: 0.97, v3: 1.03, v4: 1.08 }
    },
    BANG: {
      id: 'BANG',
      code: 'BANG',
      name: 'PMU Bangsar',
      shortName: 'Bangsar',
      fullName: 'PMU Bangsar 275/132/33kV Urban Hub',
      kv: 275,
      x: 280, y: 195,
      role: 'Central Commercial & Transit Ring (KL Sentral / Mid Valley)',
      p: 260, q: 110,
      scenarios: {
        heatwave:    { baseV: 0.938, optV: 0.998, baseTap: -2, optTap: +2, baseCap: 25, optCap: 50, inverterQ: +14.2, solarMw: 32 },
        solar_peak:  { baseV: 0.985, optV: 1.004, baseTap: 0,  optTap: +1, baseCap: 25, optCap: 25, inverterQ: +4.5,  solarMw: 45 },
        nocturnal:   { baseV: 1.038, optV: 1.002, baseTap: 0,  optTap: -1, baseCap: 0,  optCap: 0,  inverterQ: -6.2,  solarMw: 0 },
        storm_squall:{ baseV: 0.942, optV: 0.996, baseTap: -2, optTap: +2, baseCap: 25, optCap: 75, inverterQ: +18.0, solarMw: 10 }
      },
      vCurve: { v1: 0.92, v2: 0.97, v3: 1.03, v4: 1.08 }
    },
    KLCC: {
      id: 'KLCC',
      code: 'KLCC',
      name: 'PMU KLCC Central',
      shortName: 'KLCC Central',
      fullName: 'PMU KLCC Central 132kV Prestige Hub (Twin Towers / TRX)',
      kv: 132,
      x: 470, y: 80,
      role: 'Financial District & Data Centers (Tight Tolerance Grid)',
      p: 310, q: 95,
      scenarios: {
        heatwave:    { baseV: 0.946, optV: 1.002, baseTap: -1, optTap: +1, baseCap: 0,  optCap: 30, inverterQ: +8.5,  solarMw: 18 },
        solar_peak:  { baseV: 0.992, optV: 1.005, baseTap: 0,  optTap: 0,  baseCap: 0,  optCap: 0,  inverterQ: +2.1,  solarMw: 22 },
        nocturnal:   { baseV: 1.045, optV: 1.004, baseTap: +1, optTap: -1, baseCap: 0,  optCap: 0,  inverterQ: -5.4,  solarMw: 0 },
        storm_squall:{ baseV: 0.950, optV: 1.001, baseTap: -1, optTap: +1, baseCap: 0,  optCap: 30, inverterQ: +12.0, solarMw: 5 }
      },
      vCurve: { v1: 0.93, v2: 0.98, v3: 1.02, v4: 1.07 }
    },
    BUTA: {
      id: 'BUTA',
      code: 'BUTA',
      name: 'PMU Bandar Utama',
      shortName: 'Bandar Utama',
      fullName: 'PMU Bandar Utama 132/33kV Suburban Hub (PJ / Damansara)',
      kv: 132,
      x: 105, y: 280,
      role: 'Dense Suburban & Mega Mall Belt (High Rooftop Solar)',
      p: 140, q: 30,
      scenarios: {
        heatwave:    { baseV: 0.962, optV: 1.004, baseTap: +1, optTap: +1, baseCap: 20, optCap: 20, inverterQ: +6.2,  solarMw: 35 },
        solar_peak:  { baseV: 1.058, optV: 1.006, baseTap: +3, optTap: -1, baseCap: 20, optCap: 0,  inverterQ: -18.4, solarMw: 55 }, // High voltage rise
        nocturnal:   { baseV: 1.025, optV: 1.000, baseTap: 0,  optTap: 0,  baseCap: 0,  optCap: 0,  inverterQ: 0,     solarMw: 0 },
        storm_squall:{ baseV: 0.958, optV: 1.002, baseTap: +1, optTap: +1, baseCap: 20, optCap: 20, inverterQ: +8.0,  solarMw: 12 }
      },
      vCurve: { v1: 0.92, v2: 0.965, v3: 1.025, v4: 1.075 }
    },
    SHAH: {
      id: 'SHAH',
      code: 'SHAH',
      name: 'PMU Shah Alam East',
      shortName: 'Shah Alam',
      fullName: 'PMU Shah Alam Timur 275/132kV Industrial Grid',
      kv: 275,
      x: 245, y: 345,
      role: 'Heavy Industrial & Manufacturing Corridor (Inductive Loads)',
      p: 290, q: 140,
      scenarios: {
        heatwave:    { baseV: 0.932, optV: 0.996, baseTap: -3, optTap: +3, baseCap: 25, optCap: 75, inverterQ: +22.0, solarMw: 45 },
        solar_peak:  { baseV: 1.048, optV: 1.004, baseTap: +2, optTap: 0,  baseCap: 25, optCap: 0,  inverterQ: -12.5, solarMw: 68 },
        nocturnal:   { baseV: 1.028, optV: 1.002, baseTap: 0,  optTap: 0,  baseCap: 0,  optCap: 0,  inverterQ: 0,     solarMw: 0 },
        storm_squall:{ baseV: 0.938, optV: 0.995, baseTap: -3, optTap: +3, baseCap: 25, optCap: 75, inverterQ: +24.0, solarMw: 15 }
      },
      vCurve: { v1: 0.915, v2: 0.965, v3: 1.035, v4: 1.085 }
    },
    PUTR: {
      id: 'PUTR',
      code: 'PUTR',
      name: 'PMU Putrajaya',
      shortName: 'Putrajaya',
      fullName: 'PMU Putrajaya Central 275/132kV Administrative Ring',
      kv: 275,
      x: 635, y: 245,
      role: 'Federal Government Precinct & EV Green Corridor',
      p: 160, q: 50,
      scenarios: {
        heatwave:    { baseV: 0.975, optV: 1.004, baseTap: 0,  optTap: +1, baseCap: 0,  optCap: 25, inverterQ: +4.8,  solarMw: 38 },
        solar_peak:  { baseV: 1.035, optV: 1.005, baseTap: +1, optTap: 0,  baseCap: 0,  optCap: 0,  inverterQ: -4.2,  solarMw: 48 },
        nocturnal:   { baseV: 1.052, optV: 1.002, baseTap: +2, optTap: -2, baseCap: 0,  optCap: 25, inverterQ: 0,     solarMw: 0 }, // Ferranti rise
        storm_squall:{ baseV: 0.972, optV: 1.002, baseTap: 0,  optTap: +1, baseCap: 0,  optCap: 25, inverterQ: +6.5,  solarMw: 14 }
      },
      vCurve: { v1: 0.925, v2: 0.97, v3: 1.03, v4: 1.08 }
    }
  };

  // Transmission Lines Mesh
  const LINES = [
    { id: 'L_BBAD_BANG', from: 'BBAD', to: 'BANG', name: '500/275kV Bukit Badong - Bangsar Corridors', km: 28, baseLoss: 1.84, optLoss: 0.98, baseFlow: '240 MW · 68 MVAR', optFlow: '210 MW · 16 MVAR' },
    { id: 'L_BBAD_KLCC', from: 'BBAD', to: 'KLCC', name: '275kV Bukit Badong - KLCC Link', km: 32, baseLoss: 1.62, optLoss: 0.88, baseFlow: '195 MW · 52 MVAR', optFlow: '180 MW · 14 MVAR' },
    { id: 'L_BANG_KLCC', from: 'BANG', to: 'KLCC', name: '132kV Bangsar - KLCC Urban Cable', km: 8.5, baseLoss: 0.92, optLoss: 0.46, baseFlow: '95 MW · 44 MVAR (Sloshing)', optFlow: '82 MW · 4 MVAR' },
    { id: 'L_BANG_BUTA', from: 'BANG', to: 'BUTA', name: '132kV Bangsar - Bandar Utama Tie', km: 11, baseLoss: 0.86, optLoss: 0.52, baseFlow: '78 MW · 26 MVAR', optFlow: '72 MW · 6 MVAR' },
    { id: 'L_BUTA_SHAH', from: 'BUTA', to: 'SHAH', name: '132kV PJ - Shah Alam Industrial Link', km: 14, baseLoss: 0.98, optLoss: 0.62, baseFlow: '84 MW · 38 MVAR', optFlow: '76 MW · 8 MVAR' },
    { id: 'L_BANG_PUTR', from: 'BANG', to: 'PUTR', name: '275kV Bangsar - Putrajaya Southern Corridor', km: 26, baseLoss: 1.25, optLoss: 0.84, baseFlow: '140 MW · 42 MVAR', optFlow: '128 MW · 14 MVAR' },
    { id: 'L_SHAH_PUTR', from: 'SHAH', to: 'PUTR', name: '275kV Shah Alam - Putrajaya Outer Ring Tie', km: 22, baseLoss: 0.95, optLoss: 0.56, baseFlow: '110 MW · 34 MVAR', optFlow: '98 MW · 10 MVAR' }
  ];

  // Scenario Aggregate KPI Benchmarks
  const SCENARIO_KPIS = {
    heatwave: {
      title: 'Afternoon Air-Con Peak (38°C Tropical Heatwave)',
      baseLoss: 8.42, optLoss: 5.16, savingsM: 1.48,
      baseWorstV: 0.932, optWorstV: 0.996, worstBus: 'PMU Shah Alam East',
      baseSloshing: 46.8, optSloshing: 5.2,
      baseTaps: 38, optTaps: 16
    },
    solar_peak: {
      title: 'Midday Solar Peak (High DER Backfeed)',
      baseLoss: 7.92, optLoss: 4.88, savingsM: 1.38,
      baseWorstV: 1.058, optWorstV: 1.006, worstBus: 'PMU Bandar Utama',
      baseSloshing: 38.4, optSloshing: 4.6,
      baseTaps: 32, optTaps: 12
    },
    nocturnal: {
      title: 'Nocturnal Light Load (Cable Ferranti Effect)',
      baseLoss: 5.60, optLoss: 3.42, savingsM: 0.98,
      baseWorstV: 1.052, optWorstV: 1.002, worstBus: 'PMU Putrajaya',
      baseSloshing: 24.2, optSloshing: 3.1,
      baseTaps: 24, optTaps: 8
    },
    storm_squall: {
      title: 'Monsoon Cloud Squall (Sudden PV Drop)',
      baseLoss: 8.95, optLoss: 5.48, savingsM: 1.56,
      baseWorstV: 0.938, optWorstV: 0.995, worstBus: 'PMU Shah Alam East',
      baseSloshing: 52.0, optSloshing: 6.4,
      baseTaps: 42, optTaps: 18
    }
  };

  // Bayesian Trial History (Gaussian Process Surrogate Trajectory)
  const BAYESIAN_TRIALS = [
    { trial: 1,  loss: 8.42, mu: 8.42, sigma: 1.85, ei: 0.00, best: 8.42, note: 'Initial local autonomous baseline' },
    { trial: 2,  loss: 8.15, mu: 8.28, sigma: 1.62, ei: 0.14, best: 8.15, note: 'Random exploration: Bangsar tap +1' },
    { trial: 3,  loss: 7.82, mu: 8.05, sigma: 1.45, ei: 0.22, best: 7.82, note: 'Exploration: Shah Alam capacitor 50 MVAR' },
    { trial: 4,  loss: 7.95, mu: 7.92, sigma: 1.31, ei: 0.18, best: 7.82, note: 'Suboptimal: Putrajaya tap +2 rejected' },
    { trial: 5,  loss: 7.35, mu: 7.64, sigma: 1.15, ei: 0.35, best: 7.35, note: 'GP correlation: Coordinated Bangsar-Shah Alam taps' },
    { trial: 6,  loss: 7.10, mu: 7.38, sigma: 1.02, ei: 0.41, best: 7.10, note: 'Exploration: KLCC STATCOM +30 MVAR' },
    { trial: 7,  loss: 6.84, mu: 7.12, sigma: 0.90, ei: 0.48, best: 6.84, note: 'GP-EI optimum: Bandar Utama inverter absorption' },
    { trial: 8,  loss: 7.22, mu: 6.95, sigma: 0.78, ei: 0.29, best: 6.84, note: 'High uncertainty exploration in northern corridor' },
    { trial: 9,  loss: 6.42, mu: 6.68, sigma: 0.65, ei: 0.58, best: 6.42, note: 'Major improvement: Sloshing loop decoupled' },
    { trial: 10, loss: 6.18, mu: 6.41, sigma: 0.54, ei: 0.62, best: 6.18, note: 'Exploitation: Fine-tuning Q(V) deadbands' },
    { trial: 11, loss: 5.92, mu: 6.15, sigma: 0.44, ei: 0.55, best: 5.92, note: 'Bukit Badong 500kV tap adjusted to +1' },
    { trial: 12, loss: 6.05, mu: 5.98, sigma: 0.36, ei: 0.38, best: 5.92, note: 'Border boundary sample: 100 MVAR capacitor test' },
    { trial: 13, loss: 5.48, mu: 5.65, sigma: 0.28, ei: 0.68, best: 5.48, note: 'Significant breakthrough: 100% ANSI compliance achieved' },
    { trial: 14, loss: 5.24, mu: 5.40, sigma: 0.19, ei: 0.45, best: 5.24, note: 'Near-optimal: Joint inverter-OLTC co-optimization' },
    { trial: 15, loss: 5.16, mu: 5.22, sigma: 0.12, ei: 0.15, best: 5.16, note: 'GLOBAL OPTIMUM CONVERGED (-38.7% Loss Reduction)' }
  ];

  // Studio State
  let currentScenario = 'heatwave';
  let isOptimized = true;
  let currentTrialIdx = 14; // Default to trial 15 (0-indexed 14)
  let selectedSubstationId = 'BANG';
  let isRunningAuto = false;
  let animTimer = null;
  let flowDashOffset = 0;

  // Safe DOM Log Appender
  function appendLogEntry(logBox, entry) {
    if (!logBox) return;
    if (logBox.firstChild) {
      logBox.insertBefore(entry, logBox.firstChild);
    } else {
      logBox.appendChild(entry);
    }
  }

  // Initialize Studio
  function initVizierMultiSubstationStudio() {
    renderKpiTiles();
    renderNetworkDiagram();
    renderVoltageProfileBars();
    renderBayesianConvergenceChart();
    renderSubstationInspector();
    startFlowParticleAnimation();
  }

  // Animation loop for power flow particles along transmission corridors
  function startFlowParticleAnimation() {
    if (animTimer) cancelAnimationFrame(animTimer);
    function tick() {
      flowDashOffset = (flowDashOffset - 0.7) % 24;
      const linesG = document.getElementById('vvoLinesGroup');
      if (linesG) {
        linesG.querySelectorAll('.vvo-flow-line').forEach(line => {
          line.setAttribute('stroke-dashoffset', flowDashOffset);
        });
      }
      animTimer = requestAnimationFrame(tick);
    }
    animTimer = requestAnimationFrame(tick);
  }

  // Render KPI Tiles
  function renderKpiTiles() {
    const kpi = SCENARIO_KPIS[currentScenario];
    const loss = isOptimized ? kpi.optLoss : kpi.baseLoss;
    const diffPct = (((kpi.baseLoss - loss) / kpi.baseLoss) * 100).toFixed(1);
    const worstV = isOptimized ? kpi.optWorstV : kpi.baseWorstV;
    const sloshing = isOptimized ? kpi.optSloshing : kpi.baseSloshing;
    const taps = isOptimized ? kpi.optTaps : kpi.baseTaps;

    const elLoss = document.getElementById('vvoValLoss');
    const elBadgeLoss = document.getElementById('vvoBadgeLoss');
    const elSubLoss = document.getElementById('vvoSubLoss');
    const elSavings = document.getElementById('vvoValSavings');
    const elWorstV = document.getElementById('vvoValWorstV');
    const elBadgeV = document.getElementById('vvoBadgeV');
    const elSubWorstV = document.getElementById('vvoSubWorstV');
    const elSloshing = document.getElementById('vvoValSloshing');
    const elBadgeSloshing = document.getElementById('vvoBadgeSloshing');
    const elSubSloshing = document.getElementById('vvoSubSloshing');
    const elTaps = document.getElementById('vvoValTaps');
    const elBadgeTaps = document.getElementById('vvoBadgeTaps');

    if (elLoss) elLoss.textContent = loss.toFixed(2);
    if (elBadgeLoss) {
      if (isOptimized) {
        elBadgeLoss.textContent = `-${diffPct}%`;
        elBadgeLoss.style.background = 'rgba(13, 144, 79, 0.18)';
        elBadgeLoss.style.color = '#34d399';
      } else {
        elBadgeLoss.textContent = 'Baseline';
        elBadgeLoss.style.background = 'rgba(239, 68, 68, 0.18)';
        elBadgeLoss.style.color = '#f87171';
      }
    }
    if (elSubLoss) {
      elSubLoss.textContent = isOptimized
        ? `Baseline: ${kpi.baseLoss} MW (Saved ${(kpi.baseLoss - loss).toFixed(2)} MW)`
        : `Uncoordinated local control (${kpi.baseLoss} MW losses)`;
    }

    if (elSavings) {
      const sav = isOptimized ? kpi.savingsM : 0.00;
      elSavings.textContent = sav.toFixed(2);
    }

    if (elWorstV) elWorstV.textContent = `${worstV.toFixed(3)}`;
    if (elBadgeV) {
      if (isOptimized) {
        elBadgeV.textContent = '100% Valid';
        elBadgeV.style.background = 'rgba(13, 144, 79, 0.2)';
        elBadgeV.style.color = '#34d399';
      } else {
        elBadgeV.textContent = worstV < 0.95 ? 'UNDERVOLTAGE' : 'OVERVOLTAGE';
        elBadgeV.style.background = 'rgba(239, 68, 68, 0.2)';
        elBadgeV.style.color = '#f87171';
      }
    }
    if (elSubWorstV) {
      elSubWorstV.textContent = isOptimized
        ? `Worst node at ${kpi.worstBus} strictly in target band`
        : `Violation at ${kpi.worstBus} (TNB code limit exceeded)`;
    }

    if (elSloshing) elSloshing.textContent = sloshing.toFixed(1);
    if (elBadgeSloshing) {
      elBadgeSloshing.textContent = isOptimized ? '-88.9%' : 'High';
      elBadgeSloshing.style.color = isOptimized ? '#34d399' : '#fbbf24';
    }
    if (elSubSloshing) {
      elSubSloshing.textContent = isOptimized ? 'Circulating VAR loops eliminated' : 'High reactive circulation between Bangsar & KLCC';
    }

    if (elTaps) elTaps.textContent = `${taps}`;
    if (elBadgeTaps) {
      elBadgeTaps.textContent = isOptimized ? '-58%' : 'Frequent';
      elBadgeTaps.style.color = isOptimized ? '#34d399' : '#f87171';
    }

    // Engine badge
    const engineBadge = document.getElementById('vvoEngineModeBadge');
    if (engineBadge) {
      if (isOptimized) {
        engineBadge.textContent = 'Mode: Vertex AI Vizier GP-EI (Optimized)';
        engineBadge.style.color = '#34d399';
        engineBadge.style.borderColor = 'rgba(13, 144, 79, 0.3)';
        engineBadge.style.background = 'rgba(13, 144, 79, 0.12)';
      } else {
        engineBadge.textContent = 'Mode: Local Autonomous Baseline (Unoptimized)';
        engineBadge.style.color = '#f87171';
        engineBadge.style.borderColor = 'rgba(239, 68, 68, 0.3)';
        engineBadge.style.background = 'rgba(239, 68, 68, 0.12)';
      }
    }
  }

  // Render SVG Network Topology
  function renderNetworkDiagram() {
    const linesG = document.getElementById('vvoLinesGroup');
    const labelsG = document.getElementById('vvoLineLabelsGroup');
    const nodesG = document.getElementById('vvoNodesGroup');

    if (!linesG || !nodesG) return;
    linesG.innerHTML = '';
    if (labelsG) labelsG.innerHTML = '';
    nodesG.innerHTML = '';

    const kpi = SCENARIO_KPIS[currentScenario];

    // 1. Draw Transmission Corridors
    LINES.forEach(line => {
      const fromNode = SUBSTATIONS[line.from];
      const toNode = SUBSTATIONS[line.to];
      if (!fromNode || !toNode) return;

      const loss = isOptimized ? line.optLoss : line.baseLoss;
      const flow = isOptimized ? line.optFlow : line.baseFlow;

      // Color based on loss severity
      const isHighLoss = loss > 1.2 && !isOptimized;
      const strokeColor = isOptimized ? '#0284c7' : (isHighLoss ? '#f43f5e' : '#eab308');
      const strokeWidth = isOptimized ? 2.5 : (isHighLoss ? 4.0 : 3.0);

      // Base background line
      const bgLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      bgLine.setAttribute('x1', fromNode.x);
      bgLine.setAttribute('y1', fromNode.y);
      bgLine.setAttribute('x2', toNode.x);
      bgLine.setAttribute('y2', toNode.y);
      bgLine.setAttribute('stroke', strokeColor);
      bgLine.setAttribute('stroke-width', strokeWidth);
      bgLine.setAttribute('stroke-opacity', isOptimized ? '0.7' : '0.9');
      bgLine.setAttribute('stroke-linecap', 'round');
      linesG.appendChild(bgLine);

      // Animated dashed flow particle overlay
      const flowLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      flowLine.setAttribute('class', 'vvo-flow-line');
      flowLine.setAttribute('x1', fromNode.x);
      flowLine.setAttribute('y1', fromNode.y);
      flowLine.setAttribute('x2', toNode.x);
      flowLine.setAttribute('y2', toNode.y);
      flowLine.setAttribute('stroke', isOptimized ? '#38bdf8' : '#fbbf24');
      flowLine.setAttribute('stroke-width', Math.max(1.5, strokeWidth - 1));
      flowLine.setAttribute('stroke-dasharray', isOptimized ? '6 12' : '4 8');
      flowLine.setAttribute('stroke-linecap', 'round');
      linesG.appendChild(flowLine);

      // Midpoint for loss badge label
      if (labelsG) {
        const mx = (fromNode.x + toNode.x) / 2;
        const my = (fromNode.y + toNode.y) / 2;

        const gTag = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        gTag.setAttribute('transform', `translate(${mx}, ${my})`);
        gTag.style.cursor = 'pointer';

        const title = document.createElementNS('http://www.w3.org/2000/svg', 'title');
        title.textContent = `${line.name}\nFlow: ${flow}\nLine Loss: ${loss.toFixed(2)} MW (${line.km} km)`;
        gTag.appendChild(title);

        const pill = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        pill.setAttribute('x', -32);
        pill.setAttribute('y', -9);
        pill.setAttribute('width', 64);
        pill.setAttribute('height', 18);
        pill.setAttribute('rx', 9);
        pill.setAttribute('fill', isOptimized ? 'rgba(11, 17, 32, 0.85)' : (isHighLoss ? 'rgba(244, 63, 94, 0.25)' : 'rgba(234, 179, 8, 0.2)'));
        pill.setAttribute('stroke', isOptimized ? 'rgba(56, 189, 248, 0.3)' : (isHighLoss ? '#f43f5e' : '#eab308'));
        pill.setAttribute('stroke-width', '1');
        gTag.appendChild(pill);

        const txt = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        txt.setAttribute('x', 0);
        txt.setAttribute('y', 3.5);
        txt.setAttribute('text-anchor', 'middle');
        txt.setAttribute('fill', isOptimized ? '#94a3b8' : (isHighLoss ? '#fda4af' : '#fef08a'));
        txt.setAttribute('font-size', '8.5');
        txt.setAttribute('font-family', "'Roboto Mono', monospace");
        txt.setAttribute('font-weight', '600');
        txt.textContent = `${loss.toFixed(2)} MW`;
        gTag.appendChild(txt);

        labelsG.appendChild(gTag);
      }
    });

    // 2. Draw Substation Nodes
    Object.values(SUBSTATIONS).forEach(sub => {
      const sc = sub.scenarios[currentScenario];
      const v = isOptimized ? sc.optV : sc.baseV;
      const tap = isOptimized ? sc.optTap : sc.baseTap;
      const cap = isOptimized ? sc.optCap : sc.baseCap;
      const isSelected = sub.id === selectedSubstationId;

      // Determine voltage health status
      let statusColor = '#34d399'; // Normal
      let statusBg = 'rgba(13, 144, 79, 0.25)';
      let statusLabel = 'HEALTHY';
      if (v < 0.95 || v > 1.05) {
        statusColor = '#f43f5e'; // Violation
        statusBg = 'rgba(244, 63, 94, 0.3)';
        statusLabel = v < 0.95 ? 'UNDERVOLT' : 'OVERVOLT';
      } else if (v < 0.98 || v > 1.02) {
        statusColor = '#fbbf24'; // Marginal
        statusBg = 'rgba(251, 191, 36, 0.25)';
        statusLabel = 'MARGINAL';
      }

      const nodeG = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      nodeG.setAttribute('transform', `translate(${sub.x}, ${sub.y})`);
      nodeG.style.cursor = 'pointer';
      nodeG.onclick = () => selectVvoSubstation(sub.id);

      // Tooltip
      const title = document.createElementNS('http://www.w3.org/2000/svg', 'title');
      title.textContent = `${sub.fullName}\nVoltage: ${v.toFixed(3)} p.u. (${(v * sub.kv).toFixed(1)} kV)\nTransformer Tap: ${tap > 0 ? '+' : ''}${tap}\nCapacitor: ${cap} MVAR\nLocal Load: ${sub.p} MW / ${sub.q} MVAR`;
      nodeG.appendChild(title);

      // Selection Halo
      if (isSelected) {
        const halo = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        halo.setAttribute('x', -66);
        halo.setAttribute('y', -36);
        halo.setAttribute('width', 132);
        halo.setAttribute('height', 72);
        halo.setAttribute('rx', 12);
        halo.setAttribute('fill', 'none');
        halo.setAttribute('stroke', '#a855f7');
        halo.setAttribute('stroke-width', '2.5');
        halo.setAttribute('stroke-dasharray', '4 4');
        nodeG.appendChild(halo);
      }

      // Card Background Box
      const box = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      box.setAttribute('x', -60);
      box.setAttribute('y', -30);
      box.setAttribute('width', 120);
      box.setAttribute('height', 60);
      box.setAttribute('rx', 8);
      box.setAttribute('fill', isSelected ? '#1e1b4b' : '#0f172a');
      box.setAttribute('stroke', isSelected ? '#a855f7' : statusColor);
      box.setAttribute('stroke-width', isSelected ? '2' : '1.5');
      box.setAttribute('filter', statusColor === '#f43f5e' ? 'url(#glowRed)' : 'url(#glowGreen)');
      nodeG.appendChild(box);

      // Substation Code & Voltage Class
      const headerTxt = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      headerTxt.setAttribute('x', -52);
      headerTxt.setAttribute('y', -14);
      headerTxt.setAttribute('fill', '#94a3b8');
      headerTxt.setAttribute('font-size', '9');
      headerTxt.setAttribute('font-family', "'Roboto Mono', monospace");
      headerTxt.setAttribute('font-weight', '700');
      headerTxt.textContent = `${sub.code} · ${sub.kv}kV`;
      nodeG.appendChild(headerTxt);

      // Substation Short Name
      const nameTxt = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      nameTxt.setAttribute('x', -52);
      nameTxt.setAttribute('y', -1);
      nameTxt.setAttribute('fill', '#f8fafc');
      nameTxt.setAttribute('font-size', '10.5');
      nameTxt.setAttribute('font-weight', '700');
      const sName = sub.shortName || sub.name || sub.code;
      nameTxt.textContent = sName.length > 15 ? sName.slice(0, 14) + '…' : sName;
      nodeG.appendChild(nameTxt);

      // Voltage Metric Readout
      const vTxt = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      vTxt.setAttribute('x', -52);
      vTxt.setAttribute('y', 17);
      vTxt.setAttribute('fill', statusColor);
      vTxt.setAttribute('font-size', '13.5');
      vTxt.setAttribute('font-family', "'Roboto Mono', monospace");
      vTxt.setAttribute('font-weight', '700');
      vTxt.textContent = `${v.toFixed(3)} pu`;
      nodeG.appendChild(vTxt);

      // Sub-pills: Tap and Cap
      const tapPill = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      tapPill.setAttribute('x', 52);
      tapPill.setAttribute('y', 17);
      tapPill.setAttribute('text-anchor', 'end');
      tapPill.setAttribute('fill', '#38bdf8');
      tapPill.setAttribute('font-size', '8.5');
      tapPill.setAttribute('font-family', "'Roboto Mono', monospace");
      tapPill.setAttribute('font-weight', '600');
      tapPill.textContent = `Tap ${tap > 0 ? '+' : ''}${tap}`;
      nodeG.appendChild(tapPill);

      nodesG.appendChild(nodeG);
    });
  }

  // Render Substation Bus Voltage Profile Bars
  function renderVoltageProfileBars() {
    const container = document.getElementById('vvoVoltageBarsContainer');
    if (!container) return;

    const list = Object.values(SUBSTATIONS);
    const html = `
      <div style="display: flex; flex-direction: column; gap: 8px;">
        <div style="display: flex; justify-content: space-between; font-size: 0.68rem; font-family: 'Roboto Mono', monospace; color: var(--text-muted); border-bottom: 1px solid var(--border-color); padding-bottom: 4px;">
          <span>SUBSTATION</span>
          <div style="display: flex; gap: 40px; margin-right: 20px;">
            <span style="color: #f43f5e;">0.95 MIN</span>
            <span style="color: #34d399; font-weight: 700;">1.00 NOMINAL</span>
            <span style="color: #f43f5e;">1.05 MAX</span>
          </div>
          <span>STATUS</span>
        </div>
        ${list.map(sub => {
          const sc = sub.scenarios[currentScenario];
          const vBase = sc.baseV;
          const vOpt = sc.optV;
          const vCur = isOptimized ? vOpt : vBase;

          // Mapping: 0.90 pu = 0%, 1.00 pu = 50%, 1.10 pu = 100%
          const pctBase = Math.max(0, Math.min(100, ((vBase - 0.90) / 0.20) * 100));
          const pctOpt = Math.max(0, Math.min(100, ((vOpt - 0.90) / 0.20) * 100));
          const pctCur = Math.max(0, Math.min(100, ((vCur - 0.90) / 0.20) * 100));

          const isViolation = vCur < 0.95 || vCur > 1.05;
          const isMarginal = !isViolation && (vCur < 0.98 || vCur > 1.02);
          const statusColor = isViolation ? '#f43f5e' : (isMarginal ? '#fbbf24' : '#34d399');

          return `
            <div style="display: flex; align-items: center; gap: 12px; font-size: 0.74rem;">
              <div style="width: 130px; font-weight: 600; color: var(--text-primary); cursor: pointer;" onclick="selectVvoSubstation('${sub.id}')">
                ${sub.shortName} <span style="font-size: 0.65rem; color: var(--text-muted);">(${sub.kv}kV)</span>
              </div>
              <div style="flex: 1; height: 22px; background: var(--bg-primary); border-radius: 4px; position: relative; border: 1px solid var(--border-color); overflow: hidden;">
                <!-- ANSI green band (0.95 to 1.05 -> 25% to 75%) -->
                <div style="position: absolute; left: 25%; width: 50%; height: 100%; background: rgba(13, 144, 79, 0.08);"></div>
                <!-- Strict green target band (0.98 to 1.02 -> 40% to 60%) -->
                <div style="position: absolute; left: 40%; width: 20%; height: 100%; background: rgba(13, 144, 79, 0.16); border-left: 1px dashed rgba(52, 211, 153, 0.3); border-right: 1px dashed rgba(52, 211, 153, 0.3);"></div>
                <!-- 1.00 Nominal Center Line -->
                <div style="position: absolute; left: 50%; top: 0; bottom: 0; width: 1.5px; background: rgba(255,255,255,0.25);"></div>
                
                <!-- Baseline Ghost Marker -->
                <div style="position: absolute; left: ${pctBase}%; top: 2px; bottom: 2px; width: 2px; background: #64748b; opacity: 0.6;" title="Baseline: ${vBase.toFixed(3)} pu"></div>

                <!-- Current Active Marker Bar -->
                <div style="position: absolute; left: ${Math.min(50, pctCur)}%; width: ${Math.abs(pctCur - 50)}%; top: 4px; bottom: 4px; background: ${statusColor}; border-radius: 2px; transition: all 0.3s ease;"></div>
                <div style="position: absolute; left: calc(${pctCur}% - 4px); top: 2px; width: 8px; height: 16px; background: #fff; border-radius: 2px; border: 2px solid ${statusColor}; box-shadow: 0 0 6px ${statusColor}; transition: left 0.3s ease;"></div>
              </div>
              <div style="width: 80px; text-align: right; font-family: 'Roboto Mono', monospace; font-weight: 700; color: ${statusColor};">
                ${vCur.toFixed(3)} pu
              </div>
            </div>
          `;
        }).join('')}
      </div>
    `;

    container.innerHTML = html;
  }

  // Render Bayesian Convergence Chart (SVG)
  function renderBayesianConvergenceChart() {
    const svg = document.getElementById('vvoConvergenceSvg');
    if (!svg) return;

    const trials = BAYESIAN_TRIALS.slice(0, currentTrialIdx + 1);
    const W = 420;
    const H = 180;
    const padL = 40;
    const padR = 20;
    const padT = 15;
    const padB = 25;

    const chartW = W - padL - padR;
    const chartH = H - padT - padB;

    const minLoss = 4.5;
    const maxLoss = 9.5;

    function x(trialNum) { return padL + ((trialNum - 1) / 14) * chartW; }
    function y(lossVal) { return padT + ((maxLoss - lossVal) / (maxLoss - minLoss)) * chartH; }

    let svgHtml = `
      <!-- Grid lines -->
      <line x1="${padL}" y1="${y(5.0)}" x2="${W - padR}" y2="${y(5.0)}" stroke="var(--border-color)" stroke-width="1" stroke-dasharray="3 3"/>
      <line x1="${padL}" y1="${y(6.0)}" x2="${W - padR}" y2="${y(6.0)}" stroke="var(--border-color)" stroke-width="1" stroke-dasharray="3 3"/>
      <line x1="${padL}" y1="${y(7.0)}" x2="${W - padR}" y2="${y(7.0)}" stroke="var(--border-color)" stroke-width="1" stroke-dasharray="3 3"/>
      <line x1="${padL}" y1="${y(8.0)}" x2="${W - padR}" y2="${y(8.0)}" stroke="var(--border-color)" stroke-width="1" stroke-dasharray="3 3"/>

      <!-- Axes Labels -->
      <text x="${padL - 6}" y="${y(5.0) + 3}" fill="var(--text-muted)" font-size="8.5" font-family="'Roboto Mono', monospace" text-anchor="end">5.0</text>
      <text x="${padL - 6}" y="${y(6.0) + 3}" fill="var(--text-muted)" font-size="8.5" font-family="'Roboto Mono', monospace" text-anchor="end">6.0</text>
      <text x="${padL - 6}" y="${y(7.0) + 3}" fill="var(--text-muted)" font-size="8.5" font-family="'Roboto Mono', monospace" text-anchor="end">7.0</text>
      <text x="${padL - 6}" y="${y(8.0) + 3}" fill="var(--text-muted)" font-size="8.5" font-family="'Roboto Mono', monospace" text-anchor="end">8.0</text>
      <text x="${padL - 6}" y="${y(9.0) + 3}" fill="var(--text-muted)" font-size="8.5" font-family="'Roboto Mono', monospace" text-anchor="end">9.0 MW</text>

      <!-- Bottom X Axis Trial Ticks -->
      <text x="${x(1)}" y="${H - 8}" fill="var(--text-muted)" font-size="8.5" font-family="'Roboto Mono', monospace" text-anchor="middle">#1</text>
      <text x="${x(5)}" y="${H - 8}" fill="var(--text-muted)" font-size="8.5" font-family="'Roboto Mono', monospace" text-anchor="middle">#5</text>
      <text x="${x(10)}" y="${H - 8}" fill="var(--text-muted)" font-size="8.5" font-family="'Roboto Mono', monospace" text-anchor="middle">#10</text>
      <text x="${x(15)}" y="${H - 8}" fill="var(--text-muted)" font-size="8.5" font-family="'Roboto Mono', monospace" text-anchor="middle">#15</text>
    `;

    // 1. GP Uncertainty Envelope (mu + 2sigma down to mu - 2sigma)
    if (trials.length > 1) {
      let upperPath = `M ${x(trials[0].trial)} ${y(Math.min(maxLoss, trials[0].mu + trials[0].sigma * 2))}`;
      let lowerPath = '';
      for (let i = 1; i < trials.length; i++) {
        const t = trials[i];
        upperPath += ` L ${x(t.trial)} ${y(Math.min(maxLoss, t.mu + t.sigma * 2))}`;
      }
      for (let i = trials.length - 1; i >= 0; i--) {
        const t = trials[i];
        lowerPath += ` L ${x(t.trial)} ${y(Math.max(minLoss, t.mu - t.sigma * 2))}`;
      }
      svgHtml += `<path d="${upperPath} ${lowerPath} Z" fill="rgba(56, 189, 248, 0.12)" stroke="rgba(56, 189, 248, 0.25)" stroke-width="1" />`;
    }

    // 2. GP Posterior Mean Line
    if (trials.length > 1) {
      let meanPath = `M ${x(trials[0].trial)} ${y(trials[0].mu)}`;
      for (let i = 1; i < trials.length; i++) {
        meanPath += ` L ${x(trials[i].trial)} ${y(trials[i].mu)}`;
      }
      svgHtml += `<path d="${meanPath}" fill="none" stroke="#a855f7" stroke-width="2" stroke-dasharray="2 2" />`;
    }

    // 3. Best-So-Far Pareto Step Line
    if (trials.length > 0) {
      let stepPath = `M ${x(trials[0].trial)} ${y(trials[0].best)}`;
      for (let i = 1; i < trials.length; i++) {
        stepPath += ` H ${x(trials[i].trial)} V ${y(trials[i].best)}`;
      }
      svgHtml += `<path d="${stepPath}" fill="none" stroke="#34d399" stroke-width="2.5" />`;
    }

    // 4. Scatter Points for Evaluated Trials
    trials.forEach((t, i) => {
      const cx = x(t.trial);
      const cy = y(t.loss);
      const isBest = t.loss === t.best;
      const isLatest = i === trials.length - 1;

      if (isLatest) {
        svgHtml += `<circle cx="${cx}" cy="${cy}" r="8" fill="none" stroke="#a855f7" stroke-width="2" opacity="0.8" />`;
      }

      svgHtml += `
        <circle cx="${cx}" cy="${cy}" r="${isBest ? 4.5 : 3}" fill="${isBest ? '#34d399' : '#38bdf8'}" stroke="#0b1120" stroke-width="1.5">
          <title>Trial #${t.trial}: Loss = ${t.loss.toFixed(2)} MW\n${t.note}</title>
        </circle>
      `;
    });

    svg.innerHTML = svgHtml;

    // Update Trial Badge
    const badge = document.getElementById('vvoTrialCounterBadge');
    if (badge) {
      badge.textContent = `Trial ${currentTrialIdx + 1} / 15`;
    }
  }

  // Render Substation Parameter Inspector & Q(V) Dynamic Curve
  function renderSubstationInspector() {
    const sub = SUBSTATIONS[selectedSubstationId];
    if (!sub) return;

    const nameEl = document.getElementById('vvoSelectedNodeName');
    if (nameEl) nameEl.textContent = sub.fullName;

    const sc = sub.scenarios[currentScenario];
    const tap = isOptimized ? sc.optTap : sc.baseTap;
    const cap = isOptimized ? sc.optCap : sc.baseCap;
    const invQ = isOptimized ? sc.inverterQ : 0;

    // Update Tap Slider & Readout
    const sliderTap = document.getElementById('vvoSliderTap');
    const readoutTap = document.getElementById('vvoReadoutTap');
    if (sliderTap) sliderTap.value = tap;
    if (readoutTap) readoutTap.textContent = `Tap ${tap > 0 ? '+' : ''}${tap}`;

    // Update Cap buttons
    const capGroup = document.getElementById('vvoCapButtonGroup');
    if (capGroup) {
      capGroup.querySelectorAll('button').forEach(btn => {
        const val = parseInt(btn.textContent);
        if (val === cap) {
          btn.classList.add('active');
        } else {
          btn.classList.remove('active');
        }
      });
    }

    const capHint = document.getElementById('vvoCapHint');
    if (capHint) {
      capHint.textContent = sub.hasReactor && cap > 0
        ? `${cap} MVAR Shunt Reactor (Absorbs cable charging VARs)`
        : `${cap} MVAR Switched Capacitor Banks`;
    }

    // Inverter Q Readout
    const inQEl = document.getElementById('vvoInverterQVal');
    if (inQEl) {
      if (invQ > 0) {
        inQEl.textContent = `Dispatch: +${invQ.toFixed(1)} MVAR (Inject)`;
        inQEl.style.color = '#38bdf8';
      } else if (invQ < 0) {
        inQEl.textContent = `Dispatch: ${invQ.toFixed(1)} MVAR (Absorb)`;
        inQEl.style.color = '#fbbf24';
      } else {
        inQEl.textContent = `Dispatch: 0.0 MVAR (Deadband)`;
        inQEl.style.color = 'var(--text-muted)';
      }
    }

    // Redraw Dynamic IEEE 1547 Q(V) Piecewise Curve
    renderVoltVarCurve(sub);
  }

  // Draw Piecewise Smart Inverter Q(V) Curve in SVG
  function renderVoltVarCurve(sub) {
    const svg = document.getElementById('vvoCurveSvg');
    if (!svg) return;

    const curve = sub.vCurve || { v1: 0.92, v2: 0.97, v3: 1.03, v4: 1.08 };
    const sc = sub.scenarios[currentScenario];
    const curV = isOptimized ? sc.optV : sc.baseV;

    // SVG coordinates: W=380, H=130
    const W = 380;
    const H = 130;
    const padL = 40;
    const padR = 20;
    const midY = 65;

    function puToX(pu) {
      return padL + ((pu - 0.90) / 0.20) * (W - padL - padR);
    }

    const x1 = Math.round(puToX(curve.v1));
    const x2 = Math.round(puToX(curve.v2));
    const x3 = Math.round(puToX(curve.v3));
    const x4 = Math.round(puToX(curve.v4));
    const curX = Math.round(puToX(curV));

    // Current Q(V) operating position on curve
    let curY = midY;
    if (curV <= curve.v1) curY = 25;
    else if (curV < curve.v2) curY = 25 + ((curV - curve.v1) / (curve.v2 - curve.v1)) * (midY - 25);
    else if (curV <= curve.v3) curY = midY;
    else if (curV < curve.v4) curY = midY + ((curV - curve.v3) / (curve.v4 - curve.v3)) * (105 - midY);
    else curY = 105;

    svg.innerHTML = `
      <!-- Grid Reference Lines -->
      <line x1="${padL}" y1="25" x2="${W - padR}" y2="25" stroke="var(--border-color)" stroke-width="1" stroke-dasharray="3 3"/>
      <line x1="${padL}" y1="${midY}" x2="${W - padR}" y2="${midY}" stroke="var(--border-color)" stroke-width="1.5"/>
      <line x1="${padL}" y1="105" x2="${W - padR}" y2="105" stroke="var(--border-color)" stroke-width="1" stroke-dasharray="3 3"/>

      <!-- ANSI Safe Zone Envelope (0.95 to 1.05) -->
      <rect x="${puToX(0.95)}" y="15" width="${puToX(1.05) - puToX(0.95)}" height="100" fill="rgba(13, 144, 79, 0.08)" />

      <!-- Y Axis Labels -->
      <text x="${padL - 4}" y="29" fill="var(--text-muted)" font-size="8" font-family="'Roboto Mono', monospace" text-anchor="end">+Q (Inject)</text>
      <text x="${padL - 4}" y="${midY + 3}" fill="var(--text-muted)" font-size="8" font-family="'Roboto Mono', monospace" text-anchor="end">0 VAR</text>
      <text x="${padL - 4}" y="108" fill="var(--text-muted)" font-size="8" font-family="'Roboto Mono', monospace" text-anchor="end">-Q (Absorb)</text>

      <!-- X Axis Voltage Ticks -->
      <text x="${puToX(0.92)}" y="125" fill="var(--text-muted)" font-size="8" font-family="'Roboto Mono', monospace" text-anchor="middle">0.92</text>
      <text x="${puToX(0.95)}" y="125" fill="#f43f5e" font-size="8" font-family="'Roboto Mono', monospace" text-anchor="middle">0.95</text>
      <text x="${puToX(1.00)}" y="125" fill="#34d399" font-size="8" font-family="'Roboto Mono', monospace" text-anchor="middle">1.00</text>
      <text x="${puToX(1.05)}" y="125" fill="#f43f5e" font-size="8" font-family="'Roboto Mono', monospace" text-anchor="middle">1.05</text>
      <text x="${puToX(1.08)}" y="125" fill="var(--text-muted)" font-size="8" font-family="'Roboto Mono', monospace" text-anchor="middle">1.08</text>

      <!-- Piecewise Q(V) Line -->
      <polyline points="${padL},25 ${x1},25 ${x2},${midY} ${x3},${midY} ${x4},105 ${W - padR},105" fill="none" stroke="#a855f7" stroke-width="2.5" />

      <!-- Knee Points -->
      <circle cx="${x1}" cy="25" r="3.5" fill="#c084fc" />
      <circle cx="${x2}" cy="${midY}" r="3.5" fill="#c084fc" />
      <circle cx="${x3}" cy="${midY}" r="3.5" fill="#c084fc" />
      <circle cx="${x4}" cy="105" r="3.5" fill="#c084fc" />

      <!-- Current Operating Voltage Indicator Point -->
      <line x1="${curX}" y1="15" x2="${curX}" y2="115" stroke="${curV < 0.95 || curV > 1.05 ? '#f43f5e' : '#34d399'}" stroke-width="1.5" stroke-dasharray="2 2"/>
      <circle cx="${curX}" cy="${curY}" r="5" fill="#fff" stroke="#a855f7" stroke-width="2" />
    `;

    // Knee Readouts
    const r1 = document.getElementById('valV1Readout');
    const r2 = document.getElementById('valV2Readout');
    const r3 = document.getElementById('valV3Readout');
    const r4 = document.getElementById('valV4Readout');
    if (r1) r1.textContent = curve.v1.toFixed(3);
    if (r2) r2.textContent = curve.v2.toFixed(3);
    if (r3) r3.textContent = curve.v3.toFixed(3);
    if (r4) r4.textContent = curve.v4.toFixed(3);
  }

  // Select Substation Action
  function selectVvoSubstation(subId, btnElem) {
    selectedSubstationId = subId;
    if (btnElem) {
      document.querySelectorAll('.vvo-node-picker-strip .vvo-node-btn').forEach(b => b.classList.remove('active'));
      btnElem.classList.add('active');
    } else {
      document.querySelectorAll('.vvo-node-picker-strip .vvo-node-btn').forEach(b => {
        if (b.textContent.toLowerCase().includes(SUBSTATIONS[subId]?.shortName.toLowerCase() || '')) {
          b.classList.add('active');
        } else {
          b.classList.remove('active');
        }
      });
    }

    renderNetworkDiagram();
    renderSubstationInspector();
  }

  // On Grid Scenario Change
  function onVvoScenarioChange(scenarioKey) {
    currentScenario = scenarioKey;
    isOptimized = true;
    currentTrialIdx = 14;

    const logBox = document.getElementById('vvoStreamLogBox');
    if (logBox) {
      const timeStr = new Date().toLocaleTimeString('en-GB', { hour12: false });
      const entry = document.createElement('div');
      entry.innerHTML = `<span style="color: #64748b;">[${timeStr} MYT]</span> <span style="color: #f59e0b;">[SCADA]</span> Injected scenario: <strong>${SCENARIO_KPIS[scenarioKey].title}</strong>. Loading corresponding network constraints.`;
      appendLogEntry(logBox, entry);
    }

    renderKpiTiles();
    renderNetworkDiagram();
    renderVoltageProfileBars();
    renderBayesianConvergenceChart();
    renderSubstationInspector();
  }

  // Run Automated Vizier Study (Animated 15 trials)
  function runVizierAutoStudy() {
    if (isRunningAuto) return;
    isRunningAuto = true;

    const btn = document.getElementById('btnRunVizierAuto');
    const spinner = document.getElementById('vvoAutoSpinner');
    const label = document.getElementById('vvoAutoLabel');

    if (btn) btn.classList.add('is-loading');
    if (spinner) spinner.style.display = 'inline-block';
    if (label) label.textContent = 'Running GP-EI Trials (15)…';

    // Start from Trial 1
    currentTrialIdx = 0;
    isOptimized = false;
    renderKpiTiles();
    renderNetworkDiagram();
    renderVoltageProfileBars();
    renderBayesianConvergenceChart();

    let step = 0;
    const interval = setInterval(() => {
      step++;
      currentTrialIdx = step;

      if (step >= 10) isOptimized = true;

      renderKpiTiles();
      renderNetworkDiagram();
      renderVoltageProfileBars();
      renderBayesianConvergenceChart();
      renderSubstationInspector();

      // Log progress
      const logBox = document.getElementById('vvoStreamLogBox');
      if (logBox && step < BAYESIAN_TRIALS.length) {
        const t = BAYESIAN_TRIALS[step];
        const timeStr = new Date().toLocaleTimeString('en-GB', { hour12: false });
        const entry = document.createElement('div');
        entry.innerHTML = `<span style="color: #64748b;">[${timeStr} MYT]</span> <span style="color: #c084fc;">[GP-EI Trial #${t.trial}]</span> Evaluated candidate: Loss = <strong>${t.loss.toFixed(2)} MW</strong> (Best: ${t.best.toFixed(2)} MW). ${t.note}`;
        appendLogEntry(logBox, entry);
      }

      if (step >= 14) {
        clearInterval(interval);
        isRunningAuto = false;
        isOptimized = true;
        if (btn) btn.classList.remove('is-loading');
        if (spinner) spinner.style.display = 'none';
        if (label) label.textContent = '▶ Run Live Vizier Study (15 Trials)';

        // Flash tiles
        const tiles = document.getElementById('vvoKpiTiles');
        if (tiles) {
          tiles.style.transform = 'scale(1.01)';
          setTimeout(() => { tiles.style.transform = 'none'; }, 200);
        }
      }
    }, 220);
  }

  // Single Step Trial
  function runVizierSingleStep() {
    if (currentTrialIdx < BAYESIAN_TRIALS.length - 1) {
      currentTrialIdx++;
    } else {
      currentTrialIdx = 0;
    }
    isOptimized = currentTrialIdx >= 8;

    renderKpiTiles();
    renderNetworkDiagram();
    renderVoltageProfileBars();
    renderBayesianConvergenceChart();
    renderSubstationInspector();

    const t = BAYESIAN_TRIALS[currentTrialIdx];
    const logBox = document.getElementById('vvoStreamLogBox');
    if (logBox) {
      const timeStr = new Date().toLocaleTimeString('en-GB', { hour12: false });
      const entry = document.createElement('div');
      entry.innerHTML = `<span style="color: #64748b;">[${timeStr} MYT]</span> <span style="color: #c084fc;">[GP-EI Trial #${t.trial}]</span> Stepped candidate: Loss = <strong>${t.loss.toFixed(2)} MW</strong>. ${t.note}`;
      appendLogEntry(logBox, entry);
    }
  }

  // Reset to Baseline
  function resetVvoToBaseline() {
    isOptimized = false;
    currentTrialIdx = 0;

    renderKpiTiles();
    renderNetworkDiagram();
    renderVoltageProfileBars();
    renderBayesianConvergenceChart();
    renderSubstationInspector();

    const logBox = document.getElementById('vvoStreamLogBox');
    if (logBox) {
      const timeStr = new Date().toLocaleTimeString('en-GB', { hour12: false });
      const entry = document.createElement('div');
      entry.innerHTML = `<span style="color: #64748b;">[${timeStr} MYT]</span> <span style="color: #f43f5e;">[Vizier]</span> Reset grid to uncoordinated local autonomous baseline. Active losses 8.42 MW.`;
      appendLogEntry(logBox, entry);
    }
  }

  // Manual Overrides
  function onManualTapChange(val) {
    const readout = document.getElementById('vvoReadoutTap');
    if (readout) readout.textContent = `Tap ${val > 0 ? '+' : ''}${val}`;

    const sub = SUBSTATIONS[selectedSubstationId];
    if (sub) {
      const sc = sub.scenarios[currentScenario];
      if (isOptimized) sc.optTap = parseInt(val);
      else sc.baseTap = parseInt(val);
      renderNetworkDiagram();
      renderVoltageProfileBars();
    }
  }

  function setVvoCapacitor(mvar) {
    const sub = SUBSTATIONS[selectedSubstationId];
    if (sub) {
      const sc = sub.scenarios[currentScenario];
      if (isOptimized) sc.optCap = mvar;
      else sc.baseCap = mvar;
      renderSubstationInspector();
      renderNetworkDiagram();
      renderVoltageProfileBars();
    }
  }

  // Submode Switcher inside Vizier Tab
  function switchVvoSubmode(mode, btnElem) {
    if (btnElem) {
      document.querySelectorAll('#tab-vizier .card-header .wx-pill-btn').forEach(b => b.classList.remove('active'));
      btnElem.classList.add('active');
    }

    const cardNet = document.getElementById('cardVvoNetwork');
    const cardBayes = document.getElementById('cardVvoBayesian');
    const cardVolt = document.getElementById('cardVvoVoltageProfile');

    if (mode === 'grid' && cardNet) {
      cardNet.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } else if (mode === 'bayesian' && cardBayes) {
      cardBayes.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } else if (mode === 'voltages' && cardVolt) {
      cardVolt.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  // Backwards Compatibility Aliases
  function updateVizierSim() {
    renderSubstationInspector();
  }

  function runVizierBayesianTrial() {
    runVizierSingleStep();
  }

  // Expose global methods on window
  window.initVizierMultiSubstationStudio = initVizierMultiSubstationStudio;
  window.updateVizierSim = updateVizierSim;
  window.runVizierBayesianTrial = runVizierBayesianTrial;
  window.runVizierAutoStudy = runVizierAutoStudy;
  window.runVizierSingleStep = runVizierSingleStep;
  window.resetVvoToBaseline = resetVvoToBaseline;
  window.onVvoScenarioChange = onVvoScenarioChange;
  window.selectVvoSubstation = selectVvoSubstation;
  window.onManualTapChange = onManualTapChange;
  window.setVvoCapacitor = setVvoCapacitor;
  window.switchVvoSubmode = switchVvoSubmode;

})(window);
