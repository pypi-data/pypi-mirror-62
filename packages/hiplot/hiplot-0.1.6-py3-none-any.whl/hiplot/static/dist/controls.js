/*
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
import $ from "jquery";
import * as d3 from "d3";
import * as _ from 'underscore';
import React from "react";
import style from "./hiplot.css";
;
export class KeepDataBtn extends React.Component {
    constructor(props) {
        super(props);
        this.btnRef = React.createRef();
        this.state = {
            btnEnabled: false
        };
    }
    componentDidMount() {
        var me = this;
        var rows = this.props.rows;
        var btn = this.btnRef.current;
        rows['selected'].on_change(function (cb) {
            me.setState({ btnEnabled: 0 < cb.length && cb.length < rows['all'].get().length });
        }, this);
        $(btn).click(function (ev) {
            rows['all'].set(rows['selected'].get());
        });
    }
    componentWillUnmount() {
        this.props.rows.off(this);
    }
    render() {
        return (React.createElement("button", { title: "Zoom in on selected data", ref: this.btnRef, className: style.keepData, disabled: !this.state.btnEnabled }, "Keep"));
    }
}
;
export class ExcludeDataBtn extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            btnEnabled: false
        };
    }
    componentDidMount() {
        var me = this;
        var rows = this.props.rows;
        rows['selected'].on_change(function (cb) {
            me.setState({ btnEnabled: 0 < cb.length && cb.length < rows['all'].get().length });
        }, this);
    }
    onClick() {
        var new_data = _.difference(this.props.rows['all'].get(), this.props.rows['selected'].get());
        this.props.rows['all'].set(new_data);
    }
    componentWillUnmount() {
        this.props.rows.off(this);
    }
    render() {
        return (React.createElement("button", { title: "Remove selected data", className: style.excludeData, disabled: !this.state.btnEnabled, onClick: this.onClick.bind(this) }, "Exclude"));
    }
}
;
function downloadURL(url, filename) {
    var element = document.createElement('a');
    element.setAttribute('href', url);
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}
export class ExportDataCSVBtn extends React.Component {
    onClick() {
        var all_selected = this.props.rows['selected'].get();
        var csv = d3.csvFormat(all_selected);
        var blob = new Blob([csv], { type: "text/csv" });
        var url = window.URL.createObjectURL(blob);
        downloadURL(url, `hiplot-selected-${all_selected.length}.csv`);
    }
    render() {
        return (React.createElement("button", { title: "Export data as CSV", onClick: this.onClick.bind(this) }, "Export"));
    }
}
;
export class RestoreDataBtn extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            btnEnabled: false
        };
    }
    componentDidMount() {
        var me = this;
        var rows = this.props.rows;
        function update() {
            me.setState({ btnEnabled: rows['all'].get().length != rows['experiment_all'].get().length });
        }
        rows['all'].on_change(update, this);
        rows['experiment_all'].on_change(update, this);
    }
    componentWillUnmount() {
        this.props.rows.off(this);
    }
    onClick() {
        this.props.rows['all'].set(this.props.rows['experiment_all'].get());
    }
    render() {
        return (React.createElement("button", { title: "Remove all applied filters", className: style.restoreData, disabled: !this.state.btnEnabled, onClick: this.onClick.bind(this) }, "Restore"));
    }
}
;
export class SelectedCountProgressBar extends React.Component {
    constructor() {
        super(...arguments);
        this.selectedBar = React.createRef();
        this.renderedBar = React.createRef();
    }
    componentDidMount() {
        var rows = this.props.rows;
        var selectedBar = this.selectedBar.current;
        var renderedBar = this.renderedBar.current;
        rows.selected.on_change(function (selected) {
            var total = rows.all.get().length;
            selectedBar.style.width = (100 * selected.length / total) + "%";
        }, this);
        rows.rendered.on_change(function (rendered) {
            var total = rows.selected.get().length;
            renderedBar.style.width = (100 * rendered.length / total) + "%";
        }, this);
    }
    componentWillUnmount() {
        this.props.rows.off(this);
    }
    render() {
        return (React.createElement("div", { className: style.fillbar },
            React.createElement("div", { ref: this.selectedBar, className: style.selectedBar },
                React.createElement("div", { ref: this.renderedBar, className: style.renderedBar }, "\u00A0"))));
    }
}
;
;
export class ThemeToggle extends React.Component {
    constructor(props) {
        super(props);
        this.btnRef = React.createRef();
        this.state = { 'dark': false };
    }
    onClick() {
        this.setState(function (s, p) { return { dark: !s.dark }; });
    }
    componentDidUpdate() {
        if (this.props.root.current === null) {
            return;
        }
        if (this.state.dark) {
            this.props.root.current.classList.add(style.dark);
        }
        else {
            this.props.root.current.classList.remove(style.dark);
        }
    }
    render() {
        return (React.createElement("button", { title: "Toggle dark/light theme", ref: this.btnRef, onClick: this.onClick.bind(this) }, this.state.dark ? "Light" : "Dark"));
    }
}
;
