import { Transform } from "./transform";
const C = 1.0 / Math.LN10;
export class SymLog extends Transform {
    constructor(attrs) {
        super(attrs);
    }
    static init_SymLog() {
        this.define({});
    }
    // XXX: this is repeated in ./jitter.ts
    v_compute(xs) {
        const result = new Float64Array(xs.length);
        for (let i = 0; i < xs.length; i++) {
            const x = xs[i];
            result[i] = Math.sign(x) * Math.log10(1 + Math.abs(x / C));
        }
        return result;
    }
    compute(x) {
        return Math.sign(x) * Math.log10(1 + Math.abs(x / C));
    }
}
SymLog.__name__ = "SymLog";
SymLog.init_SymLog();
//# sourceMappingURL=symlog.js.map