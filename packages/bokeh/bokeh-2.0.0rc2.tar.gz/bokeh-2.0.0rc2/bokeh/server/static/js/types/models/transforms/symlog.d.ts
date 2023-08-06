import { Transform } from "./transform";
import { Range } from "../ranges/range";
import * as p from "../../core/properties";
import { Arrayable } from "../../core/types";
export declare namespace SymLog {
    type Attrs = p.AttrsOf<Props>;
    type Props = Transform.Props & {
        value: p.Property<number>;
        range: p.Property<Range>;
    };
}
export interface SymLog extends SymLog.Attrs {
}
export declare class SymLog extends Transform {
    properties: SymLog.Props;
    constructor(attrs?: Partial<SymLog.Attrs>);
    static init_SymLog(): void;
    v_compute(xs: Arrayable<number>): Arrayable<number>;
    compute(x: number): number;
}
