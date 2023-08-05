import { ParamDefMap } from "./infertypes";
import { HiPlotPluginData } from "./plugin";
import React from "react";
export interface PlotXYDisplayData {
    axis_x: string | null;
    axis_y: string | null;
    lines_thickness: number;
    lines_opacity: number;
    dots_thickness: number;
    dots_opacity: number;
    height?: number;
}
interface PlotXYProps extends HiPlotPluginData, PlotXYDisplayData {
}
interface PlotXYState extends PlotXYDisplayData {
    width: number;
    height: number;
    enabled: boolean;
}
export declare class PlotXY extends React.Component<PlotXYProps, PlotXYState> {
    on_resize: () => void;
    params_def: ParamDefMap;
    svg: any;
    clear_canvas: () => void;
    update_axis: () => void;
    root_ref: React.RefObject<HTMLDivElement>;
    container_ref: React.RefObject<HTMLDivElement>;
    canvas_lines_ref: React.RefObject<HTMLCanvasElement>;
    canvas_highlighted_ref: React.RefObject<HTMLCanvasElement>;
    constructor(props: PlotXYProps);
    static defaultProps: {
        axis_x: any;
        axis_y: any;
        lines_thickness: number;
        lines_opacity: any;
        dots_thickness: number;
        dots_opacity: any;
        data: {};
    };
    componentDidMount(): void;
    mountPlotXY(): void;
    onResize(height: number, width: number): void;
    render(): any[] | JSX.Element;
    componentWillUnmount(): void;
    componentDidUpdate(prevProps: any, prevState: any): void;
}
export {};
