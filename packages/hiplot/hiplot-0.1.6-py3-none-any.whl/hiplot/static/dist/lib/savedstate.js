/*
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
;
export class PersistentStateInURL {
    constructor(name) {
        this.params = {}; // In case history doesnt work, like when we are embedded in an iframe
        this.prefix = name == '' ? '' : name + '.';
    }
    get(name, def_value) {
        return this._get(this.prefix + name, def_value);
    }
    set(name, value) {
        this._set(this.prefix + name, value);
    }
    _get(name, default_value) {
        if (this.params[name] !== undefined) {
            return this.params[name];
        }
        const searchParams = new URLSearchParams(location.search);
        var value = searchParams.get(name);
        if (value === null) {
            return default_value;
        }
        return JSON.parse(value);
    }
    _set(name, new_value) {
        const searchParams = new URLSearchParams(location.search);
        searchParams.set(name, JSON.stringify(new_value));
        try {
            history.replaceState({}, 'title', '?' + searchParams.toString());
        }
        catch (e) {
            this.params[name] = new_value;
        }
    }
    children(name) {
        return new PersistentStateInURL(this.prefix + name);
    }
}
;
export class PersistentStateInMemory {
    constructor(name, params) {
        this.params = {};
        this.prefix = name == '' ? '' : name + '.';
        this.params = params;
    }
    get(name, def_value) {
        var v = this.params[this.prefix + name];
        return v !== undefined ? v : def_value;
    }
    set(name, value) {
        this.params[this.prefix + name] = value;
    }
    clear() {
        Object.keys(this.params)
            .filter(key => key.startsWith(this.prefix))
            .forEach(key => delete this.params[key]);
    }
    children(name) {
        return new PersistentStateInMemory(this.prefix + name, this.params);
    }
}
;
