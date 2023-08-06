define([
    'require',
    'jquery',
    'base/js/namespace',
    'base/js/events',
    'codemirror/lib/codemirror',
], function (requirejs, $, Jupyter, events, CodeMirror) {
    "use strict"

    var markers = []
    var selections = []
    var lastSel = null

    // define default values for config parameters
    var params = {
        nextHotkey : 'Ctrl-m',
        allHotkey : 'Ctrl-Shift-m',
        splitSelectionHotkey : 'Ctrl-Shift-l',
        highlight : true,
        wrapcell : false,
        allcells : false,
    }
    var updateParams = function(cfg) {
        for (var key in params) {
            if (cfg.multiselection.hasOwnProperty(key)) {
                params[key] = cfg.multiselection[key]
            }
        }
    }

    var initExtension = function() {
        $('<link/>').attr({rel: 'stylesheet',
                           type: 'text/css',
                           href: requirejs.toUrl('./multiselection.css')
                          }).appendTo('head')
    }

    var range = function(start, end) {
        var res = []
        for (let i = start; i <= end; i++) {
            res.push(i)
        }
        return res
    }

    var loadExtension = function() {
        // Actionhandler definition
        var actNext = {icon: 'fa-long-arrow-alt-right',
                       help: 'Select next occurence',
                       help_index: 'ms',
                       prefix: 'Multiselection',
                       id: 'msNext',
                       handler: selectNext,}
        var actAll = {icon: 'fa-arrows-alt-h',
                      help: 'Select all occurences',
                      help_index: 'ms',
                      prefix: 'Multiselection',
                      id: 'msAll',
                      handler: selectAll,}

        // Define keyboard shortcuts
        var edit_mode_shortcuts = {}
        edit_mode_shortcuts[params.nextHotkey] = Jupyter.keyboard_manager.actions.register(
            actNext, 'multiselection:select-next-occurence', 'multiselection'
        )
        edit_mode_shortcuts[params.allHotkey] = Jupyter.keyboard_manager.actions.register(
            actAll, 'multiselection:select-all-occurences', 'multiselection'
        )
        Jupyter.notebook.keyboard_manager.edit_shortcuts.add_shortcuts(edit_mode_shortcuts)

        // Register events
        events.on('select.Cell', (e, d) => {
            var cm = IPython.notebook.get_selected_cell().code_mirror
            cm.on('cursorActivity', highlightSelected)
        })

        return Jupyter.notebook.config.loaded
            .then(initExtension)
            .then(() => updateParams(Jupyter.notebook.config.data))
    }

    var highlightSelected = function() {
        $.extend(true, params, Jupyter.notebook.config.multiselection)


        // Remove previous markers
        for (var mark of markers) {
            mark.clear()
        }

        // Get currently selected word
        var cm = IPython.notebook.get_selected_cell().code_mirror
        cm.options.selectionsMayTouch = true

        var sel = cm.doc.sel.ranges[cm.doc.sel.ranges.length-1]

        if (sel.head.line != sel.anchor.line) return

        var mn = Math.min(sel.head.ch, sel.anchor.ch)
        var mx = Math.max(sel.head.ch, sel.anchor.ch)
        var ln = sel.anchor.line
        var len = mx - mn

        if (len <= 0) return

        var sub = cm.doc.getLine(sel.head.line).slice(mn, mx)
        sub = sub.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')

        var re = new RegExp(sub, 'g')

        if (len == 0) return
        markers = []
        selections = []

        // Add new markers for every occurence of the selection
        var i = 0
        for (var l = 0; l < cm.doc.size; l++) {
            var txt = cm.doc.getLine(l)
            while (re.exec(txt)){
                if (params.highlight) {
                    var mark = cm.doc.markText({line: l, ch: re.lastIndex-len},
                                               {line: l, ch: re.lastIndex},
                                               {className: 'multiselectionMarker'})
                    markers.push(mark)
                }
                selections.push({line: l, mn: re.lastIndex-len, mx: re.lastIndex})

                if (l == ln && mn == (re.lastIndex-len) && mx == (re.lastIndex)) {
                    lastSel = i
                }
                i++
            }
        }

    }

    var selectAll = function() {
        var cm = IPython.notebook.get_selected_cell().code_mirror
        for (var s of selections) {
            cm.addSelection({line: s.line, ch: s.mn}, {line: s.line, ch: s.mx})
        }
    }

    var selectNext = function() {
        var cm = IPython.notebook.get_selected_cell().code_mirror
        // Nothing to do
        if (cm.doc.sel.ranges.length == selections.length) return

        var nextSel = lastSel+1
        if (nextSel == selections.length) nextSel = 0
        var sel = selections[nextSel]

        cm.addSelection({line: sel.line, ch: sel.mn}, {line: sel.line, ch: sel.mx})
        lastSel = nextSel
    }

    // return object to export public methods
    return {
        load_ipython_extension : loadExtension
    }
})
