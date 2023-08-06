/*
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
import $ from "jquery";
import React from "react";
import * as d3 from "d3";
import _ from "underscore";
import { DistributionPlot } from "./plot";
import { ResizableH } from "../lib/resizable";
;
;
;
export class HiPlotDistributionPlugin extends React.Component {
    constructor(props) {
        super(props);
        this.container_ref = React.createRef();
        var axis = this.props.persistent_state.get('axis');
        if (axis !== undefined && this.props.params_def[axis] === undefined) {
            axis = undefined;
        }
        if (axis === undefined) {
            axis = this.props.axis;
        }
        if (axis && this.props.params_def[axis] === undefined) {
            axis = undefined;
        }
        this.state = {
            height: d3.min([d3.max([document.body.clientHeight - 540, 240]), 500]),
            width: 0,
            histData: { selected: [], all: props.rows.all.get() },
            axis: axis,
        };
    }
    componentDidMount() {
        if (this.props.context_menu_ref && this.props.context_menu_ref.current) {
            const me = this;
            this.props.context_menu_ref.current.addCallback(function (column, cm) {
                var contextmenu = $(cm);
                contextmenu.append($('<div class="dropdown-divider"></div>'));
                var option = $('<a class="dropdown-item" href="#">').text("View distribution");
                if (me.state.axis == column) {
                    option.addClass('disabled').css('pointer-events', 'none');
                }
                option.click(function (event) {
                    me.setState({ axis: column });
                    event.preventDefault();
                });
                contextmenu.append(option);
            }, this);
        }
        this.props.rows.selected.on_change(function (new_dps) {
            this.setState(function (s, p) {
                return {
                    histData: {
                        ...s.histData,
                        selected: new_dps,
                    }
                };
            });
        }.bind(this), this);
        this.props.rows.all.on_change(function (new_dps) {
            this.setState(function (s, p) {
                return {
                    histData: {
                        ...s.histData,
                        all: new_dps,
                    }
                };
            });
        }.bind(this), this);
    }
    componentDidUpdate(prevProps, prevState) {
        if (prevState.axis != this.state.axis) {
            if (this.props.persistent_state) {
                this.props.persistent_state.set('axis', this.state.axis);
            }
        }
    }
    componentWillUnmount() {
        this.props.rows.off(this);
    }
    onResize(height, width) {
        if (height != this.state.height || width != this.state.width) {
            this.setState({ height: height, width: width });
        }
    }
    render() {
        if (this.state.axis === undefined) {
            return [];
        }
        return (React.createElement(ResizableH, { initialHeight: this.state.height, onResize: _.debounce(this.onResize.bind(this), 150) }, this.state.width > 0 && React.createElement(DistributionPlot, { axis: this.state.axis, height: this.state.height, width: this.state.width, histData: this.state.histData, param_def: this.props.params_def[this.state.axis], nbins: this.props.nbins, animateMs: this.props.animateMs })));
    }
}
HiPlotDistributionPlugin.defaultProps = {
    nbins: 10,
    animateMs: 750,
};
;
