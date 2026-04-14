/**
 * PlotWrapper — Properly initialize react-plotly.js with the factory pattern.
 * This avoids ESM/CJS interop issues with the default export.
 */
import createPlotlyComponentModule from 'react-plotly.js/factory';
import Plotly from 'plotly.js/dist/plotly';

const createPlotlyComponent = createPlotlyComponentModule.default || createPlotlyComponentModule;
const Plot = createPlotlyComponent(Plotly);

export default Plot;
