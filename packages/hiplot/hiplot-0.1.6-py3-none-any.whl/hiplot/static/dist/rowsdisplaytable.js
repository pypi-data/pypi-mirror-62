/*
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
import $ from "jquery";
import React from "react";
//@ts-ignore
import dt from "datatables.net-bs4";
dt(window, $);
//@ts-ignore
import dtReorder from "datatables.net-colreorder-bs4";
dtReorder(window, $);
import style from "./hiplot.css";
import _ from "underscore";
;
export class RowsDisplayTable extends React.Component {
    constructor(props) {
        super(props);
        this.table_ref = React.createRef();
        this.dt = null;
        this.ordered_cols = [];
        this.state = {};
    }
    componentDidMount() {
        this.dom = $(this.table_ref.current);
        this.ordered_cols = ['', 'uid'];
        const me = this;
        $.each(this.props.params_def, function (k, def) {
            if (k == 'uid') {
                return;
            }
            me.ordered_cols.push(k);
        });
        this.dom.empty();
        var columns = this.ordered_cols.map(function (x) {
            return {
                'title': x,
                'defaultContent': 'null',
                'type': x == '' ? 'html' : (me.props.params_def[x].numeric ? "num" : "string"),
            };
        });
        columns[0]['render'] = function (data, type, row, meta) {
            if (!me.dt) {
                return '';
            }
            const individualUidColIdx = me.dt.colReorder.order().indexOf(1);
            const color = me.props.get_color_for_row(me.props.dp_lookup[row[individualUidColIdx]], 1.0);
            return `<span class="${style.colorBlock}" style="background-color: ${color}" />`;
        };
        this.dt = this.dom.DataTable({
            columns: columns,
            data: [],
            deferRender: true,
            headerCallback: function headerCallback(thead, data, start, end, display) {
                Array.from(thead.cells).forEach(function (th, i) {
                    const col = th.innerHTML;
                    if (col != '' && me.dt === null && me.props.context_menu_ref !== undefined) {
                        th.addEventListener('contextmenu', e => {
                            me.props.context_menu_ref.current.show(e.pageX, e.pageY, col);
                            e.preventDefault();
                        });
                    }
                });
            },
            //@ts-ignore
            colReorder: true,
        });
        this.empty = true;
        this.dom.find('tbody')
            .on('mouseenter', 'td', function () {
            if (!me.dt || me.empty) {
                return;
            }
            const rowIdx = me.dt.cell(this).index().row;
            const row = me.dt.row(rowIdx);
            const individualUidColIdx = me.dt.colReorder.order().indexOf(1);
            $(me.dt.cells().nodes()).removeClass(style.highlight);
            $(row.nodes()).addClass(style.highlight);
            me.props.rows['highlighted'].set([me.props.dp_lookup[row.data()[individualUidColIdx]]]);
        })
            .on("mouseout", "td", function () {
            if (!me.dt || me.empty) {
                return;
            }
            const rowIdx = me.dt.cell(this).index().row;
            $(me.dt.row(rowIdx).nodes()).removeClass(style.highlight);
            me.props.rows['highlighted'].set([]);
        });
        me.set_selected(me.props.rows['selected'].get());
        me.props.rows['selected'].on_change(_.debounce(function (selection) {
            me.set_selected(selection);
        }, 150), this);
    }
    set_selected(selected) {
        const dt = this.dt;
        if (!dt) {
            return;
        }
        const ordered_cols = this.ordered_cols;
        dt.clear();
        dt.rows.add(selected.map(function (row) {
            return dt.colReorder.transpose([...Array(ordered_cols.length).keys()]).map(x => x == '' ? '' : row[ordered_cols[x]]);
        }));
        dt.draw();
        this.empty = selected.length == 0;
    }
    render() {
        return (React.createElement("div", { className: `${style.wrap} container-fluid ${style["horizontal-scrollable"]}` },
            React.createElement("div", { className: "row" },
                React.createElement("div", { className: `col-md-12 sample-table-container` },
                    React.createElement("table", { ref: this.table_ref, className: "sample-rows-table display table table-striped table-bordered dataTable" })))));
    }
    componentWillUnmount() {
        if (this.dt) {
            const dt = this.dt;
            this.dt = null;
            dt.destroy();
        }
        this.props.rows.off(this);
    }
}
