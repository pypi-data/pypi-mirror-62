import { PersistentState } from "./lib/savedstate";
import { Datapoint, ParamType, HiPlotValueDef } from "./types";
export interface ParamDef extends HiPlotValueDef {
    optional: boolean;
    numeric: boolean;
    distinct_values: Array<any>;
    special_values: Array<any>;
    type_options: Array<ParamType>;
    __val2color?: {
        [k: string]: any;
    };
}
export declare function create_d3_scale_without_outliers(pd: ParamDef): any;
export declare function create_d3_scale(pd: ParamDef): any;
export declare function colorScheme(pd: ParamDef, value: any, alpha: number): string;
export interface ParamDefMap {
    [key: string]: ParamDef;
}
/**
 * Ideally we want to infer:
 *  - If a variable is categorical
 *  - If a variable is numeric
 *  - If a variable is log-scaled
 */
export declare function infertypes(url_states: PersistentState, table: Array<Datapoint>, hints: {
    [key: string]: HiPlotValueDef;
}): ParamDefMap;
