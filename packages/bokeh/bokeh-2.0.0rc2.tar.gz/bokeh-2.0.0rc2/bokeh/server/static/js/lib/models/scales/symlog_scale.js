import { ContinuousScale } from "./continuous_scale";
// This model implements "A Bi-Symmetric Log transformation for wide-range data."
// found in https://pdfs.semanticscholar.org/70d5/3d9f448e6f2c10bd87a4a058be64f5af7dbc.pdf
const C = 1.0 / Math.LN10;
export class SymLogScale extends ContinuousScale {
    constructor(attrs) {
        super(attrs);
    }
    compute(x) {
        const value = Math.sign(x) * Math.log10(1 + Math.abs(x / C));
        return this._linear_compute(value);
    }
    v_compute(xs) {
        const result = new Float64Array(xs.length);
        for (let i = 0; i < xs.length; i++) {
            result[i] = Math.sign(xs[i]) * Math.log10(1 + Math.abs(xs[i] / C));
        }
        return this._linear_v_compute(result);
    }
    invert(xprime) {
        const value = this._linear_invert(xprime);
        return Math.sign(value) * C * (10 ** Math.abs(value) - 1);
    }
    v_invert(xprimes) {
        const value = this._linear_v_invert(xprimes);
        const result = new Float64Array(xprimes.length);
        for (let i = 0; i < xprimes.length; i++) {
            result[i] = Math.sign(value[i]) * C * (10 ** Math.abs(value[i]) - 1);
        }
        return result;
    }
}
SymLogScale.__name__ = "SymLogScale";
//# sourceMappingURL=symlog_scale.js.map