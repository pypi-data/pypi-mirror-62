import React from "react";
import { HiPlotPluginData } from "../plugin";
import { HistogramData } from "./plot";
export interface HiPlotDistributionPluginState {
    height: number;
    width: number;
    axis?: string;
    histData: HistogramData;
}
interface DistributionDisplayData {
    nbins: number;
    animateMs: number;
    axis?: string;
}
interface DistributionPluginProps extends HiPlotPluginData, DistributionDisplayData {
}
export declare class HiPlotDistributionPlugin extends React.Component<DistributionPluginProps, HiPlotDistributionPluginState> {
    container_ref: React.RefObject<HTMLDivElement>;
    constructor(props: DistributionPluginProps);
    static defaultProps: {
        nbins: number;
        animateMs: number;
    };
    componentDidMount(): void;
    componentDidUpdate(prevProps: HiPlotPluginData, prevState: HiPlotDistributionPluginState): void;
    componentWillUnmount(): void;
    onResize(height: number, width: number): void;
    render(): any[] | JSX.Element;
}
export {};
