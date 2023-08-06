import React from "react";
import './global';
import { Datapoint, HiPlotExperiment, HiPlotLoadStatus } from "./types";
import { RowsDisplayTable } from "./rowsdisplaytable";
import { PersistentState } from "./lib/savedstate";
import { HiPlotPluginData } from "./plugin";
export { PlotXY } from "./plotxy";
export { ParallelPlot } from "./parallel/parallel";
export { RowsDisplayTable } from "./rowsdisplaytable";
export { HiPlotPluginData } from "./plugin";
export { Datapoint, HiPlotExperiment, AllDatasets, HiPlotLoadStatus } from "./types";
interface PluginInfo {
    name: string;
    render: (plugin_data: HiPlotPluginData) => JSX.Element;
}
export interface HiPlotProps {
    experiment: HiPlotExperiment | null;
    is_webserver: boolean;
    plugins: Array<PluginInfo>;
    persistent_state?: PersistentState;
}
interface HiPlotState {
    experiment: HiPlotExperiment | null;
    version: number;
    loadStatus: HiPlotLoadStatus;
    error: string;
}
export declare class HiPlot extends React.Component<HiPlotProps, HiPlotState> {
    domRoot: React.RefObject<HTMLDivElement>;
    comm: any;
    comm_selection_id: number;
    table: RowsDisplayTable;
    data: HiPlotPluginData;
    plugins_window_state: {
        [plugin: string]: any;
    };
    constructor(props: HiPlotProps);
    static defaultProps: {
        is_webserver: boolean;
    };
    onSelectedChange(selection: Array<Datapoint>): void;
    recomputeParamsDef(all_data: Array<Datapoint>): void;
    _loadExperiment(experiment: HiPlotExperiment): void;
    loadWithPromise(prom: Promise<any>): void;
    setup_comm(comm_: any): void;
    componentWillUnmount(): void;
    componentDidMount(): void;
    componentDidUpdate(): void;
    columnContextMenu(column: string, cm: HTMLDivElement): void;
    onRefreshDataBtn(): void;
    loadURI(uri: string): void;
    onRunsTextareaSubmitted(uri: string): void;
    render(): JSX.Element;
}
export declare const defaultPlugins: {
    name: string;
    render: (plugin_data: HiPlotPluginData) => JSX.Element;
}[];
export declare function hiplot_setup(element: HTMLElement, extra?: object): void;
