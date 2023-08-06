import React from "react";
import * as d3 from "d3";
import { HiPlotPluginData } from "../plugin";
interface StringMapping<V> {
    [key: string]: V;
}
interface ParallelPlotState {
    height: number;
    width: number;
    order: Array<string>;
    hide: Set<string>;
    invert: Set<string>;
    dimensions: Array<string>;
    brush_count: number;
    dragging: {
        col: string;
        pos: number;
        origin: number;
        dragging: boolean;
    };
}
interface ParallelPlotDisplayData {
    order?: Array<string>;
    hide?: Array<string>;
    invert?: Array<string>;
    categoricalMaximumValues: number;
}
interface ParallelPlotData extends HiPlotPluginData, ParallelPlotDisplayData {
}
export declare class ParallelPlot extends React.Component<ParallelPlotData, ParallelPlotState> {
    on_resize: () => void;
    m: number[];
    w: number;
    h: number;
    dimensions_dom: any;
    render_speed: number;
    animloop: d3.Timer;
    xscale: any;
    debounced_brush: any;
    root_ref: React.RefObject<HTMLDivElement>;
    foreground_ref: React.RefObject<HTMLCanvasElement>;
    foreground: CanvasRenderingContext2D;
    highlighted_ref: React.RefObject<HTMLCanvasElement>;
    highlighted: CanvasRenderingContext2D;
    svg_ref: React.RefObject<SVGSVGElement>;
    svgg_ref: React.RefObject<SVGGElement>;
    div: any;
    yscale: StringMapping<any>;
    axis: d3.Axis<number>;
    d3brush: d3.BrushBehavior<unknown>;
    constructor(props: ParallelPlotData);
    static defaultProps: {
        categoricalMaximumValues: number;
        data: {};
    };
    componentWillUnmount(): void;
    componentDidUpdate(prevProps: any, prevState: any): void;
    onResize(height: number, width: number): void;
    render(): JSX.Element;
    componentDidMount(): void;
    position: any;
    initParallelPlot(): void;
    setScaleRange(k: string): void;
    createScale(k: string): any;
    compute_dimensions(): void;
    update_ticks: any;
    paths: any;
    path: any;
}
export {};
