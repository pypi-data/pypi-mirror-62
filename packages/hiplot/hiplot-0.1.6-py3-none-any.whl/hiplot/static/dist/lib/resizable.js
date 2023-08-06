/*
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
import style from "./resizable.css";
import $ from "jquery";
import React from "react";
import _ from "underscore";
;
;
export class ResizableH extends React.Component {
    constructor(props) {
        super(props);
        this.div_ref = React.createRef();
        this.m_pos = null;
        this.onMouseMove = function (e) {
            const dy = e.clientY - this.m_pos;
            this.m_pos = e.clientY;
            if (dy != 0) {
                var internalHeight = this.state.internalHeight + dy;
                this.setState({
                    height: Math.max(this.props.minHeight, internalHeight),
                    internalHeight: internalHeight,
                    position: e.clientY,
                });
            }
        }.bind(this);
        this.onMouseUp = function (e) {
            if (this.m_pos == null) {
                return;
            }
            this.m_pos = null;
            document.removeEventListener("mousemove", this.onMouseMove, false);
        }.bind(this);
        this.onWindowResize = function () {
            if (this.div_ref.current) {
                this.setState({ width: this.div_ref.current.offsetWidth });
            }
        }.bind(this);
        this.state = {
            width: 0,
            height: this.props.initialHeight,
            internalHeight: this.props.initialHeight,
        };
        this.onWindowResizeDebounced = _.debounce(this.onWindowResize.bind(this), 100);
    }
    componentDidMount() {
        var div = $(this.div_ref.current);
        div.on("mousedown", function (e) {
            if (e.offsetY > div.height() - this.props.borderSize) {
                this.m_pos = e.clientY;
                document.addEventListener("mousemove", this.onMouseMove, false);
            }
        }.bind(this));
        document.addEventListener("mouseup", this.onMouseUp);
        $(window).on("resize", this.onWindowResizeDebounced);
        this.setState({ width: this.div_ref.current.parentElement.offsetWidth });
    }
    componentDidUpdate(prevProps, prevState) {
        if (prevState.height != this.state.height || prevState.width != this.state.width) {
            this.props.onResize(this.state.height, this.state.width);
        }
    }
    componentWillUnmount() {
        document.removeEventListener("mousemove", this.onMouseMove, false);
        document.removeEventListener("mouseup", this.onMouseUp);
        $(window).off("resize", this.onWindowResizeDebounced);
    }
    render() {
        return (React.createElement("div", { ref: this.div_ref, style: { "height": this.state.height }, className: style.resizableH }, this.props.children));
    }
}
ResizableH.defaultProps = {
    borderSize: 4,
    minHeight: 50,
};
