import { HiPlotProps, HiPlot } from "./hiplot";
import React from "react";
interface TesterState {
    testNum: number;
    testDone: boolean;
    renderNum: number;
    width: number;
    keepCount: number;
}
export declare class HiPlotTester extends React.Component<{
    hiplotProps: HiPlotProps;
}, TesterState> {
    root: React.RefObject<HTMLDivElement>;
    hiplot: React.RefObject<HiPlot>;
    timeout: ReturnType<typeof setTimeout>;
    state: {
        testNum: number;
        testDone: boolean;
        renderNum: number;
        keepCount: number;
        width: number;
    };
    testSelection: {
        name: string;
        test: () => void;
    }[];
    testFn: {
        name: string;
        test: () => void;
    }[];
    testSelect(): void;
    testSelectNone(): void;
    testSelectAll(): void;
    testHighlightAllSelected(): void;
    testButton(text: string): void;
    checkStartTesting(): void;
    componentDidMount(): void;
    componentDidUpdate(): void;
    componentWillUnmount(): void;
    render(): JSX.Element;
}
export declare function hiplot_setup(element: HTMLElement, extra?: object): void;
export {};
