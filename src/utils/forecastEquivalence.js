/**
 * Map the forecaster-calibrated AI scenarios onto the shift-sweep axis.
 *
 * The sweep moves k% of positive labor income into capital with output held
 * fixed. A scenario tilts factor shares while output grows. The dimension the
 * two share is the fraction of labor income relocated relative to a
 * shares-fixed world at the same output:
 *
 *   k = 1 - (1 + g_L) / (1 + g_Y)
 *
 * which equals (theta0_L - theta1_L) / theta0_L, the proportional fall in the
 * labor share. Derived from fields already in the scenario payload; nothing
 * here re-models anything.
 */

/** Equivalent sweep-shift fraction for one scenario row (0..1), or null. */
export function equivalentShift(scenario) {
  const gY = scenario?.gdpGrowth;
  const gL = scenario?.laborGrowth;
  if (!Number.isFinite(gY) || !Number.isFinite(gL) || 1 + gY === 0) {
    return null;
  }
  return 1 - (1 + gL) / (1 + gY);
}

/**
 * Markers for the sweep axis: one per named scenario, from the proportional
 * variant (the tilt itself, before any inequality overlay). Sorted ascending.
 */
export function forecastMarkers(aiScenariosData) {
  const rows = aiScenariosData?.scenarios ?? [];
  const markers = [];
  for (const row of rows) {
    if (row.inequality !== "proportional" || row.holdSharesFixed) continue;
    if ((row.realizationRate ?? 1) !== 1) continue;
    const shift = equivalentShift(row);
    if (shift == null || shift <= 0) continue;
    markers.push({ name: row.name, shiftPct: shift * 100 });
  }
  return markers.sort((a, b) => a.shiftPct - b.shiftPct);
}

/** The band from 0 to the largest forecast-equivalent shift, or null. */
export function forecastBand(aiScenariosData) {
  const markers = forecastMarkers(aiScenariosData);
  if (markers.length === 0) return null;
  return { markers, maxPct: markers[markers.length - 1].shiftPct };
}
