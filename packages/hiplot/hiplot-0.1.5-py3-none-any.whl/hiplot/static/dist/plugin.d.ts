/// <reference types="react" />
import { ParamDefMap } from "./infertypes";
import { AllDatasets, DatapointLookup, WatchedProperty, Datapoint, HiPlotExperiment } from "./types";
import { ContextMenu } from "./contextmenu";
import { PersistentState } from "./lib/savedstate";
export interface HiPlotPluginData {
    experiment: HiPlotExperiment;
    params_def: ParamDefMap;
    rows: AllDatasets;
    get_color_for_row: (uid: Datapoint, opacity: number) => string;
    render_row_text: (rows: Datapoint) => string;
    dp_lookup: DatapointLookup;
    context_menu_ref?: React.RefObject<ContextMenu>;
    colorby: WatchedProperty;
    name: string;
    window_state: any;
    persistent_state: PersistentState;
}
