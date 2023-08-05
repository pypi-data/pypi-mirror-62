import { ContinuousScale } from "./continuous_scale";
import { Arrayable } from "../../core/types";
import * as p from "../../core/properties";
export declare namespace SymLogScale {
    type Attrs = p.AttrsOf<Props>;
    type Props = ContinuousScale.Props;
}
export interface SymLogScale extends SymLogScale.Attrs {
}
export declare class SymLogScale extends ContinuousScale {
    properties: SymLogScale.Props;
    constructor(attrs?: Partial<SymLogScale.Attrs>);
    compute(x: number): number;
    v_compute(xs: Arrayable<number>): Arrayable<number>;
    invert(xprime: number): number;
    v_invert(xprimes: Arrayable<number>): Arrayable<number>;
}
