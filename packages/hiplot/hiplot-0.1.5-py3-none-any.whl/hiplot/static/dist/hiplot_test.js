/*
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
import $ from "jquery";
import { HiPlot, defaultPlugins } from "./hiplot";
import { PersistentStateInURL } from "./lib/savedstate";
import React from "react";
import ReactDOM from "react-dom";
import assert from "assert";
;
export class HiPlotTester extends React.Component {
    constructor() {
        super(...arguments);
        this.root = React.createRef();
        this.hiplot = React.createRef();
        this.timeout = null;
        this.state = {
            testNum: -1,
            testDone: false,
            renderNum: 0,
            keepCount: 10,
            width: 1024,
        };
        this.testSelection = [
            { name: "testSelect", test: this.testSelect },
            { name: "keepBtn", test: function () { this.testButton("Keep"); } },
            { name: "kept", test: function () { assert(this.hiplot.current.data.rows.all.get().length == this.state.keepCount); } },
            { name: "restoreBtn", test: function () { this.testButton("Restore"); } },
            { name: "restored", test: function () { assert(this.hiplot.current.data.rows.all.get().length != this.state.keepCount); } },
            { name: "testSelect", test: this.testSelect },
            { name: "excludeBtn", test: function () { this.testButton("Exclude"); } },
            { name: "restoreBtn", test: function () { this.testButton("Restore"); } },
        ];
        this.testFn = [
            { name: "responsiveWidth", test: function () { assert(this.root.current.scrollWidth == this.state.width); } },
            { name: "testSelect", test: this.testSelect },
            { name: "testSelectNone", test: this.testSelectNone },
            { name: "testSelectAll", test: this.testSelectAll },
            ...this.testSelection,
            { name: "testResize", test: function () { this.setState({ width: 800 }); } },
            { name: "testResize2", test: function () { $(window).trigger('resize'); } },
            { name: "responsiveWidth", test: function () { assert(this.root.current.scrollWidth == this.state.width); } },
            { name: "testResize", test: function () { this.setState({ width: 1024 }); } },
            { name: "testResize2", test: function () { $(window).trigger('resize'); } },
        ];
    }
    // Selection/highlights
    testSelect() {
        const allRows = this.hiplot.current.data.rows.all.get();
        this.hiplot.current.data.rows.selected.set(allRows.slice(0, this.state.keepCount));
    }
    testSelectNone() {
        this.hiplot.current.data.rows.selected.set([]);
    }
    testSelectAll() {
        this.hiplot.current.data.rows.selected.set(this.hiplot.current.data.rows.all.get());
    }
    testHighlightAllSelected() {
        this.hiplot.current.data.rows.highlighted.set(this.hiplot.current.data.rows.selected.get());
    }
    // Keep/restore/exclude buttons
    testButton(text) {
        $(this.root.current).find(`button:contains(${text})`)[0].click();
    }
    checkStartTesting() {
        console.log("Waiting for user to load an experiment...");
        if (this.hiplot.current.state.experiment) {
            clearInterval(this.timeout);
            this.setState({
                testNum: 0,
                keepCount: Math.floor(this.hiplot.current.state.experiment.datapoints.length / 2),
            });
        }
    }
    componentDidMount() {
        this.timeout = setInterval(this.checkStartTesting.bind(this), 500);
    }
    componentDidUpdate() {
        if (this.state.testDone) {
            return;
        }
        if (this.state.testNum >= this.testFn.length) {
            console.log("Tests done!");
            return;
        }
        this.setState({ testDone: true });
        const testDef = this.testFn[this.state.testNum];
        console.log(`## TEST ${this.state.testNum}: ${testDef.name}`);
        testDef.test.bind(this)();
        this.timeout = setTimeout(this.setState.bind(this, { testNum: this.state.testNum + 1, testDone: false }), 500);
    }
    componentWillUnmount() {
        if (this.timeout !== null) {
            clearTimeout(this.timeout);
        }
    }
    render() {
        return React.createElement("div", { ref: this.root, style: { width: this.state.width } },
            React.createElement(HiPlot, Object.assign({ ref: this.hiplot, key: this.state.renderNum }, this.props.hiplotProps)));
    }
}
;
export function hiplot_setup(element, extra) {
    var props = {
        experiment: null,
        is_webserver: true,
        persistent_state: new PersistentStateInURL("hip"),
        plugins: defaultPlugins,
    };
    if (extra !== undefined) {
        Object.assign(props, extra);
    }
    return ReactDOM.render(React.createElement(HiPlotTester, { hiplotProps: props }), element);
}
Object.assign(window, {
    'hiplot_setup': hiplot_setup,
});
