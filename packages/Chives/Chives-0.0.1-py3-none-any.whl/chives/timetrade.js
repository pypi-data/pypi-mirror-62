/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./jssrc/timetrade.ts");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./jssrc/timetrade.ts":
/*!****************************!*\
  !*** ./jssrc/timetrade.ts ***!
  \****************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/**
 * 分时成交JS
 */
function GetQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.toLowerCase().substr(1).match(reg);
    if (r != null)
        return unescape(r[2]);
    return null;
}
window['stockEnity'] = {
    "stockCode": GetQueryString("code") || "",
    "stockmarket": GetQueryString("market") || "",
    "stockId": GetQueryString("id") || GetQueryString("code") + GetQueryString("market")
};
__webpack_require__(/*! ../src/modules/old_f1 */ "./src/modules/old_f1/index.js");
setTimeout(function () {
    qphf.getIndexQuote(15);
}, 500);
var HV = new HistoryViews("historyest", {
    def: "",
    set: "",
    lns: 11
});
var _cpyno = "c1";


/***/ }),

/***/ "./src/modules/ie_sse_polyfill/index.js":
/*!**********************************************!*\
  !*** ./src/modules/ie_sse_polyfill/index.js ***!
  \**********************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/*
   * EventSource polyfill version 0.9.7
   * Supported by sc AmvTek srl
   * :email: devel@amvtek.com
 */
;(function (global) {

    if (global.EventSource && !global._eventSourceImportPrefix){
        return;
    }

    var evsImportName = (global._eventSourceImportPrefix||'')+"EventSource";

    var EventSource = function (url, options) {

        if (!url || typeof url != 'string') {
            throw new SyntaxError('Not enough arguments');
        }

        this.URL = url;
        this.setOptions(options);
        var evs = this;
        setTimeout(function(){evs.poll()}, 0);
    };

    EventSource.prototype = {

        CONNECTING: 0,

        OPEN: 1,

        CLOSED: 2,

        defaultOptions: {

            loggingEnabled: false,

            loggingPrefix: "eventsource",

            interval: 500, // milliseconds

            bufferSizeLimit: 256*1024, // bytes

            silentTimeout: 300000, // milliseconds

            getArgs:{
                'evs_buffer_size_limit': 256*1024
            },

            xhrHeaders:{
                'Accept': 'text/event-stream',
                'Cache-Control': 'no-cache',
                'X-Requested-With': 'XMLHttpRequest'
            }
        },

        setOptions: function(options){

            var defaults = this.defaultOptions;
            var option;

            // set all default options...
            for (option in defaults){

                if ( defaults.hasOwnProperty(option) ){
                    this[option] = defaults[option];
                }
            }

            // override with what is in options
            for (option in options){

                if (option in defaults && options.hasOwnProperty(option)){
                    this[option] = options[option];
                }
            }

            // if getArgs option is enabled
            // ensure evs_buffer_size_limit corresponds to bufferSizeLimit
            if (this.getArgs && this.bufferSizeLimit) {

                this.getArgs['evs_buffer_size_limit'] = this.bufferSizeLimit;
            }

            // if console is not available, force loggingEnabled to false
            if (typeof console === "undefined" || typeof console.log === "undefined") {

                this.loggingEnabled = false;
            }
        },

        log: function(message) {

            if (this.loggingEnabled) {

                console.log("[" + this.loggingPrefix +"]:" + message)
            }
        },

        poll: function() {

            try {

                if (this.readyState == this.CLOSED) {
                    return;
                }

                this.cleanup();
                this.readyState = this.CONNECTING;
                this.cursor = 0;
                this.cache = '';
                this._xhr = new this.XHR(this);
                this.resetNoActivityTimer();

            }
            catch (e) {

                // in an attempt to silence the errors
                this.log('There were errors inside the pool try-catch');
                this.dispatchEvent('error', { type: 'error', data: e.message });
            }
        },

        pollAgain: function (interval) {

            // schedule poll to be called after interval milliseconds
            var evs = this;
            evs.readyState = evs.CONNECTING;
            evs.dispatchEvent('error', {
                type: 'error',
                data: "Reconnecting "
            });
            this._pollTimer = setTimeout(function(){evs.poll()}, interval||0);
        },


        cleanup: function() {

            this.log('evs cleaning up')

            if (this._pollTimer){
                clearInterval(this._pollTimer);
                this._pollTimer = null;
            }

            if (this._noActivityTimer){
                clearInterval(this._noActivityTimer);
                this._noActivityTimer = null;
            }

            if (this._xhr){
                this._xhr.abort();
                this._xhr = null;
            }
        },

        resetNoActivityTimer: function(){

            if (this.silentTimeout){

                if (this._noActivityTimer){
                    clearInterval(this._noActivityTimer);
                }
                var evs = this;
                this._noActivityTimer = setTimeout(
                        function(){ evs.log('Timeout! silentTImeout:'+evs.silentTimeout); evs.pollAgain(); },
                        this.silentTimeout
                        );
            }
        },

        close: function () {

            this.readyState = this.CLOSED;
            this.log('Closing connection. readyState: '+this.readyState);
            this.cleanup();
        },

        _onxhrdata: function() {

            var request = this._xhr;

            if (request.isReady() && !request.hasError() ) {
                // reset the timer, as we have activity
                this.resetNoActivityTimer();

                // move this EventSource to OPEN state...
                if (this.readyState == this.CONNECTING) {
                    this.readyState = this.OPEN;
                    this.dispatchEvent('open', { type: 'open' });
                }

                var buffer = request.getBuffer();

                if (buffer.length > this.bufferSizeLimit) {
                    this.log('buffer.length > this.bufferSizeLimit');
                    this.pollAgain();
                }

                if (this.cursor == 0 && buffer.length > 0){

                    // skip byte order mark \uFEFF character if it starts the stream
                    if (buffer.substring(0,1) == '\uFEFF'){
                        this.cursor = 1;
                    }
                }

                var lastMessageIndex = this.lastMessageIndex(buffer);
                if (lastMessageIndex[0] >= this.cursor){

                    var newcursor = lastMessageIndex[1];
                    var toparse = buffer.substring(this.cursor, newcursor);
                    this.parseStream(toparse);
                    this.cursor = newcursor;
                }

                // if request is finished, reopen the connection
                if (request.isDone()) {
                    this.log('request.isDone(). reopening the connection');
                    this.pollAgain(this.interval);
                }
            }
            else if (this.readyState !== this.CLOSED) {

                this.log('this.readyState !== this.CLOSED');
                this.pollAgain(this.interval);

                //MV: Unsure why an error was previously dispatched
            }
        },

        parseStream: function(chunk) {

            // normalize line separators (\r\n,\r,\n) to \n
            // remove white spaces that may precede \n
            chunk = this.cache + this.normalizeToLF(chunk);

            var events = chunk.split('\n\n');

            var i, j, eventType, datas, line, retry;

            for (i=0; i < (events.length - 1); i++) {

                eventType = 'message';
                datas = [];
                parts = events[i].split('\n');

                for (j=0; j < parts.length; j++) {

                    line = this.trimWhiteSpace(parts[j]);

                    if (line.indexOf('event') == 0) {

                        eventType = line.replace(/event:?\s*/, '');
                    }
                    else if (line.indexOf('retry') == 0) {

                        retry = parseInt(line.replace(/retry:?\s*/, ''));
                        if(!isNaN(retry)) {
                            this.interval = retry;
                        }
                    }
                    else if (line.indexOf('data') == 0) {

                        datas.push(line.replace(/data:?\s*/, ''));
                    }
                    else if (line.indexOf('id:') == 0) {

                        this.lastEventId = line.replace(/id:?\s*/, '');
                    }
                    else if (line.indexOf('id') == 0) { // this resets the id

                        this.lastEventId = null;
                    }
                }

                if (datas.length) {
                    // dispatch a new event
                    var event = new MessageEvent(eventType, datas.join('\n'), window.location.origin, this.lastEventId);
                    this.dispatchEvent(eventType, event);
                }
            }

            this.cache = events[events.length - 1];
        },

        dispatchEvent: function (type, event) {
            var handlers = this['_' + type + 'Handlers'];

            if (handlers) {

                for (var i = 0; i < handlers.length; i++) {
                    handlers[i].call(this, event);
                }
            }

            if (this['on' + type]) {
                this['on' + type].call(this, event);
            }

        },

        addEventListener: function (type, handler) {
            if (!this['_' + type + 'Handlers']) {
                this['_' + type + 'Handlers'] = [];
            }

            this['_' + type + 'Handlers'].push(handler);
        },

        removeEventListener: function (type, handler) {
            var handlers = this['_' + type + 'Handlers'];
            if (!handlers) {
                return;
            }
            for (var i = handlers.length - 1; i >= 0; --i) {
                if (handlers[i] === handler) {
                    handlers.splice(i, 1);
                    break;
                }
            }
        },

        _pollTimer: null,

        _noactivityTimer: null,

        _xhr: null,

        lastEventId: null,

        cache: '',

        cursor: 0,

        onerror: null,

        onmessage: null,

        onopen: null,

        readyState: 0,

        // ===================================================================
        // helpers functions
        // those are attached to prototype to ease reuse and testing...

        urlWithParams: function (baseURL, params) {

            var encodedArgs = [];

            if (params){

                var key, urlarg;
                var urlize = encodeURIComponent;

                for (key in params){
                    if (params.hasOwnProperty(key)) {
                        urlarg = urlize(key)+'='+urlize(params[key]);
                        encodedArgs.push(urlarg);
                    }
                }
            }

            if (encodedArgs.length > 0){

                if (baseURL.indexOf('?') == -1)
                    return baseURL + '?' + encodedArgs.join('&');
                return baseURL + '&' + encodedArgs.join('&');
            }
            return baseURL;
        },

        lastMessageIndex: function(text) {

            var ln2 =text.lastIndexOf('\n\n');
            var lr2 = text.lastIndexOf('\r\r');
            var lrln2 = text.lastIndexOf('\r\n\r\n');

            if (lrln2 > Math.max(ln2, lr2)) {
                return [lrln2, lrln2+4];
            }
            return [Math.max(ln2, lr2), Math.max(ln2, lr2) + 2]
        },

        trimWhiteSpace: function(str) {
            // to remove whitespaces left and right of string

            var reTrim = /^(\s|\u00A0)+|(\s|\u00A0)+$/g;
            return str.replace(reTrim, '');
        },

        normalizeToLF: function(str) {

            // replace \r and \r\n with \n
            return str.replace(/\r\n|\r/g, '\n');
        }

    };

    if (!isOldIE()){

        EventSource.isPolyfill = "XHR";

        // EventSource will send request using XMLHttpRequest
        EventSource.prototype.XHR = function(evs) {

            request = new XMLHttpRequest();
            this._request = request;
            evs._xhr = this;

            // set handlers
            request.onreadystatechange = function(){
                if (request.readyState > 1 && evs.readyState != evs.CLOSED) {
                    if (request.status == 200 || (request.status>=300 && request.status<400)){
                        evs._onxhrdata();
                    }
                    else {
                        request._failed = true;
                        evs.readyState = evs.CLOSED;
                        evs.dispatchEvent('error', {
                            type: 'error',
                            data: "The server responded with "+request.status
                        });
                        evs.close();
                    }
                }
            };

            request.onprogress = function () {
            };

            request.open('GET', evs.urlWithParams(evs.URL, evs.getArgs), true);

            var headers = evs.xhrHeaders; // maybe null
            for (var header in headers) {
                if (headers.hasOwnProperty(header)){
                    request.setRequestHeader(header, headers[header]);
                }
            }
            if (evs.lastEventId) {
                request.setRequestHeader('Last-Event-Id', evs.lastEventId);
            }

            request.send();
        };

        EventSource.prototype.XHR.prototype = {

            useXDomainRequest: false,

            _request: null,

            _failed: false, // true if we have had errors...

            isReady: function() {


                return this._request.readyState >= 2;
            },

            isDone: function() {

                return (this._request.readyState == 4);
            },

            hasError: function() {

                return (this._failed || (this._request.status >= 400));
            },

            getBuffer: function() {

                var rv = '';
                try {
                    rv = this._request.responseText || '';
                }
                catch (e){}
                return rv;
            },

            abort: function() {

                if ( this._request ) {
                    this._request.abort();
                }
            }
        };
    }
    else {

	EventSource.isPolyfill = "IE_8-9";

        // patch EventSource defaultOptions
        var defaults = EventSource.prototype.defaultOptions;
        defaults.xhrHeaders = null; // no headers will be sent
        defaults.getArgs['evs_preamble'] = 2048 + 8;

        // EventSource will send request using Internet Explorer XDomainRequest
        EventSource.prototype.XHR = function(evs) {

            request = new XDomainRequest();
            this._request = request;

            // set handlers
            request.onprogress = function(){
                request._ready = true;
                evs._onxhrdata();
            };

            request.onload = function(){
                this._loaded = true;
                evs._onxhrdata();
            };

            request.onerror = function(){
                this._failed = true;
                evs.readyState = evs.CLOSED;
                evs.dispatchEvent('error', {
                    type: 'error',
                    data: "XDomainRequest error"
                });
            };

            request.ontimeout = function(){
                this._failed = true;
                evs.readyState = evs.CLOSED;
                evs.dispatchEvent('error', {
                    type: 'error',
                    data: "XDomainRequest timed out"
                });
            };

            // XDomainRequest does not allow setting custom headers
            // If EventSource has enabled the use of GET arguments
            // we add parameters to URL so that server can adapt the stream...
            var reqGetArgs = {};
            if (evs.getArgs) {

                // copy evs.getArgs in reqGetArgs
                var defaultArgs = evs.getArgs;
                    for (var key in defaultArgs) {
                        if (defaultArgs.hasOwnProperty(key)){
                            reqGetArgs[key] = defaultArgs[key];
                        }
                    }
                if (evs.lastEventId){
                    reqGetArgs['evs_last_event_id'] = evs.lastEventId;
                }
            }
            // send the request

            request.open('GET', evs.urlWithParams(evs.URL,reqGetArgs));
            request.send();
        };

        EventSource.prototype.XHR.prototype = {

            useXDomainRequest: true,

            _request: null,

            _ready: false, // true when progress events are dispatched

            _loaded: false, // true when request has been loaded

            _failed: false, // true if when request is in error

            isReady: function() {

                return this._request._ready;
            },

            isDone: function() {

                return this._request._loaded;
            },

            hasError: function() {

                return this._request._failed;
            },

            getBuffer: function() {

                var rv = '';
                try {
                    rv = this._request.responseText || '';
                }
                catch (e){}
                return rv;
            },

            abort: function() {

                if ( this._request){
                    this._request.abort();
                }
            }
        };
    }

    function MessageEvent(type, data, origin, lastEventId) {

        this.bubbles = false;
        this.cancelBubble = false;
        this.cancelable = false;
        this.data = data || null;
        this.origin = origin || '';
        this.lastEventId = lastEventId || '';
        this.type = type || 'message';
    }

    function isOldIE () {

        //return true if we are in IE8 or IE9
        return (window.XDomainRequest && (window.XMLHttpRequest && new XMLHttpRequest().responseType === undefined)) ? true : false;
    }

    global[evsImportName] = EventSource;
})(window);

/***/ }),

/***/ "./src/modules/old_f1/index.js":
/*!*************************************!*\
  !*** ./src/modules/old_f1/index.js ***!
  \*************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {


__webpack_require__(/*! ../ie_sse_polyfill */ "./src/modules/ie_sse_polyfill/index.js");

var template = __webpack_require__(/*! ../template */ "./src/modules/template/index.js")
// var marge = require('lodash/merge');
var marge = _.merge;



    $(function () {
        drawTable();
        setInterval(refresh, 30 * 1000);
        //setInterval(loadQuote, 10*1000);
        loadQuote();
        JuadeIe7();
        

        filterFun();
        clickFun();
        // isRong();
        var suggest =  new suggest2017({
            inputid: "search_box",
            offset: { left: -91, top: 5 }
        });
    });

    function refresh() {
        var option = argFun();
        drawTable(option);
        // loadQuote();
    }

    //区分ie7
    function JuadeIe7() {
         //增加判断浏览器是否为ie7及以下
         if (document.all && !document.querySelector) {
            setInterval(loadQuote, 30 * 1000);
         } else {
            sseHeadData();
         }
    }

    function argFun() {
        var option = {};
        $(".bigOrder dd input[type=radio]").each(function () {
            if ($(this).prop("checked")) {
                // option.gtvolume = $(this).val();
                var gtvolume = $(this).val();
                if(gtvolume == '100') {
                    option.ft = 2
                } else if(gtvolume == '200') {
                    option.ft = 3
                } else if(gtvolume == '500') {
                    option.ft = 4
                } else if(gtvolume == '1000') {
                    option.ft = 5
                } else if(gtvolume == '2000') {
                    option.ft = 6
                } else if(gtvolume == '5000') {
                    option.ft = 7
                } else if(gtvolume == '10000') {
                    option.ft = 8
                } else {
                    option.ft = 1
                }
            }

        });
        option.sort = $("#reverseInput").val();
        option.pageindex = Number($(".curPage").html()) - 1;
        //console.log(option)
        return option;
    }


    //青色=绿色=1=#00ffff，紫色=红色=2=ff00ff 先判断方向再判断大于20万  1是涨 -1是跌 0是没跌没涨
    //增加newflag 倒序无需执行分页
    //分时成交
    function drawTable(option, newflag) {
        var _default = {
            "pageindex": 0, "id": stockEnity.stockId, "sort": 1, "ft": 1
        }
        var _option = $.extend(_default, option);
        _option.code = getCode();
        _option.market = getMarket();


        if (_option.pageindex == -1) { return; }
        // var url = "http://61.152.230.32:1981/getStockFenShi?pagesize=144&ut=7eea3edcaed734bea9cbfc24409ed989&dpt=wzfscj"
        var url = "http://push2ex.eastmoney.com/getStockFenShi?pagesize=144&ut=7eea3edcaed734bea9cbfc24409ed989&dpt=wzfscj"
        $.ajax({
            url: url,
            dataType: "jsonp",
            jsonp: "cb",
            data: _option,
            success: function (json) {
                if (json.data) {
                    // console.log('分时时间')
                    // console.log(json)
                    var count = Math.ceil(json.data.tc / 144);
                    var kcbFlag = json.data.ct;
                    if(count == 0) {
                        count = 1;
                    }
                    // console.log(count)
                    var data = json.data.data, pc = Dealprice(json.data.cp);
                    var list1 = [], list2 = [], list3 = [], list4 = [];
                    var html_1 = "", html_2 = "", html_3 = "", html_4 = "";
                    var dir = "", color = "", otherColor = "", chje = "";
                    if (!data && data.length == 0 && typeof data == "string") { return; }
                    for (var i = 0; i < data.length; i++) {
                        var preItems = data[i-1];
                        var items = data[i];
                        color = Dealprice(items.p) - pc == 0 ? "" : Dealprice(items.p) - pc > 0 ? "red" : Dealprice(items.p) - pc < 0 ? "green" : "";
                        chje = items.v * 100 * Dealprice(items.p);
                        if (items.bs == "1") {
                            otherColor = chje > 200000 ? "blue" : "green";
                        } else if (items.bs == "2") {
                            otherColor = chje > 200000 ? "purple" : "red";
                        } else {
                            otherColor = "";
                        }
                        //箭头
                        if (items.bs != "4") {
                            if(preItems) {
                                if (items.p > preItems.p) {
                                    dir = "red";
                                } else if (items.p < preItems.p) {
                                    dir = "green";
                                } else {
                                    dir = "";
                                }
                            }else {
                                dir = "";
                            }
                           
                        } else {
                            dir = "";
                            items.v = "-";
                            color = "";
                        }

                        //判断是否是科创板 手数做不同处理
                        var new_cjs = items.v;
                        if(kcbFlag == 1) {
                            new_cjs = kcbMyformatNum(new_cjs);
                            // console.log(new_cjs)
                            
                        }else {
                            new_cjs = new_cjs;
                        }
                        

                        if (i < 36) {
                            list1.push({
                                "time": DealTime(items.t),
                                "close": Dealprice(items.p),
                                "coloseColor": color,
                                "num": new_cjs,
                                "fontColor": otherColor,
                                "dir": dir
                            });
                        }
                        if (i > 35 && i < 72) {
                            list2.push({
                                "time": DealTime(items.t),
                                "close": Dealprice(items.p),
                                "coloseColor": color,
                                "num": new_cjs,
                                "fontColor": otherColor,
                                "dir": dir
                            });
                        }
                        if (i > 71 && i < 108) {
                            list3.push({
                                "time": DealTime(items.t),
                                "close": Dealprice(items.p),
                                "coloseColor": color,
                                "num": new_cjs,
                                "fontColor": otherColor,
                                "dir": dir
                            });
                        }
                        if (i > 107 && i < 144) {
                            list4.push({
                                "time": DealTime(items.t),
                                "close": Dealprice(items.p),
                                "coloseColor": color,
                                "num": new_cjs,
                                "fontColor": otherColor,
                                "dir": dir
                            });
                        }
                    }
                    var html_1 = template("tmp", { list: list1 });
                    var html_2 = template("tmp", { list: list2 });
                    var html_3 = template("tmp", { list: list3 });
                    var html_4 = template("tmp", { list: list4 });
                    $("#listTable1 tbody").html(html_1);
                    $("#listTable2 tbody").html(html_2);
                    $("#listTable3 tbody").html(html_3);
                    $("#listTable4 tbody").html(html_4);

                   

                    if(newflag !== false) {
                        pageFun(count, _option.pageindex);
                    }
                    
                }


            }
        })

    }


    //科创板成交量
    function kcbMyformatNum(num) {
        if (num == '-') {
            return '-';
        }

        if (num == undefined  || isNaN(num)) {
            return '';
        }


        var hz = '';
        var num2 = '';
        try {
           if (num >= 0 && num <= 99.999999999) {
                num2 = parseFloat(num).toFixed(2);
            } else if (num >= 100 && num <= 999) {
                num2 = parseFloat(num).toFixed(1);
            } else if (num >= 1000) {
                // num2 = parseFloat(num).toFixed(0);
                if (num > 10000 && num < 100000000) {
                    num2 = (num / 10000).toFixed(2) + "万";
                } else if (num > 100000000) {
                    num2 = (num / 100000000).toFixed(2) + "亿";
                } else if (num == 0) {
                    num2 = '-';
                } else {
                    num2 = num.toFixed(0);
                }
            }


            return num2.toString() + hz;

        } catch (error) {
            return '-';
        }


    }


    //处理价格
    function Dealprice(val) {
        try {
            val = val/1000;
            return val.toFixed(2);
        } catch(e) {
            return '-'
        }

    }

    //处理时间
    function DealTime(val) {
        try {
            val = '' + val;
           if(val.length == 5) {
               val = '0' + val;
           }

           return val.substr(0,2) + ':' + val.substr(2,2) + ':' + val.substr(4,2)

        } catch(e) {
            return '-'
        }

    }

    //翻页的html
    function pageFun(count, page) {
        var count = Number(count);
        var page = Number(page);
        if (count == 0) {
            page = 0;
        }

        var obj = {
            "curPage": page,
            "prev": page == 0 ? 0 : page - 1 ,
            "next": page == count ? count : page + 1,
            "count": count
        };
        var lstxt = obj.curPage + 1;
        //ie7
        $(".prevPage").attr("mypage",  obj.prev);
        // $(".prevPage").attr("value", obj.prev);
        $(".nextPage").attr("mypage", obj.next);
        $(".lastPage").attr("mypage", obj.count-1);
       
        $(".curPage").text(lstxt);
       
       
        $(".count").text(obj.count);

        if (count == page+1) {
            $(".lastPage").removeClass("canClick");
            $(".arrowR").hide();
            $(".nextPage").removeClass("canClick");
        } else {
            $(".lastPage").addClass("canClick");
            $(".nextPage").addClass("canClick");
            $(".arrowR").show();
        }
        if (page+1 == 1) {
            $(".fistPage").removeClass("canClick");
            $(".prevPage").removeClass("canClick");
            $(".arrowL").hide();
        } else {
            $(".fistPage").addClass("canClick");
            $(".prevPage").addClass("canClick");
            $(".arrowL").show();
        }
        if (count == 0) {
            $(".liPage").removeClass("canClick");
            $(".arrowR").hide();
            $(".arrowL").hide();
        }
    }

    //筛选、倒序
    function filterFun() {
        $(".bigOrder input[type=radio]").change(function () {
            var option = {};
            // console.log('筛选大单：',$(this).val())
            // option.gtvolume = $(this).val();
            var gtvolume = $(this).val();
            if(gtvolume == '100') {
                option.ft = 2
            } else if(gtvolume == '200') {
                option.ft = 3
            } else if(gtvolume == '500') {
                option.ft = 4
            } else if(gtvolume == '1000') {
                option.ft = 5
            } else if(gtvolume == '2000') {
                option.ft = 6
            } else if(gtvolume == '5000') {
                option.ft = 7
            } else if(gtvolume == '10000') {
                option.ft = 8
            } else {
                option.ft = 1
            }
           
            option.sort = $("#reverseInput").val();

            drawTable(option);
        });

        $(".reverseDiv input[type=checkbox]").change(function () {
            var option = {};
            if ($(this).prop("checked")) {
                $(this).val("2");
            } else {
                $(this).val("1");
            }
            option.sort = $("#reverseInput").val();
            //option.page = Number($(".curPage").html());
            //argFun()
            var _option = $.extend(argFun(), option);
            drawTable(_option, false);
        });
    }


    //点击事件
    function clickFun() {

        $(".goBtn").click(function () {
            var val = Number($(".go").val());           
            var curPage = Number($(".PageNavBtm .curPage").text());
            var lastPage = Number($(".PageNavBtm .lastPage").attr("mypage"));
            if (val == "" || val > lastPage+1 || val < 1 || isNaN(val) > 0 || val == curPage) { $(".go").val(""); return; }
            var option = {};
            option.pageindex = val-1;
            var _option = $.extend(argFun(), option);           
            drawTable(_option);
            $(".go").val("");

        });
        $(".liPage").click(function () {
            $(".go").val("");
            if ($(this).hasClass("canClick")) {
                var val = $(this).attr("mypage");
                var option = {};
                option.pageindex = val;
                var _option = $.extend(argFun(), option);
                drawTable(_option);
            }
        });
        $(".go").keydown(function (e) {
            var keyCode = e.keyCode ? e.keyCode : e.which ? e.which : e.charCode; //兼容IE 火狐 谷歌  
            if (keyCode == 13) {
                $(".goBtn").trigger("click");
                return false;
            }
        });

        $(".mobile-icon").mouseover(function () {
            $(".QRcode-div").show();
        });
        $(".mobile-icon").mouseout(function () {
            $(".QRcode-div").hide();
        });
    }

    //快速行情
    function loadQuote() {
        var options = {
            "id": stockEnity.stockId
        }

        var secid = getMarket() + '.' + getCode();

        // var _url = "//nuff.eastmoney.com/EM_Finance2015TradeInterface/JS.ashx?token=beb0a0047196124721f56b0f0ff5a27c";
        var url = 'http://push2.eastmoney.com/api/qt/stock/get?ut=fa5fd1943c7b386f172d6893dbfba10b&invt=2&fltt=2&fields=f1,f43,f57,f58,f169,f170,f46,f44,f51,f168,f47,f116,f60,f45,f52,f50,f48,f167,f117,f71,f161,f49,f162,f107,f86,f177,f127,f199,f128,f80,f152,f110,f111,f107,f285,f286,f262,f263,f256,f257,f269,f270&secid=' + secid;
        
        $.ajax({
            url: url,
            // data: options,
            dataType: "jsonp",
            jsonp: "cb",
            success: function (json) {
                // console.log(json)
                var items = json.data;

                if (!items || items.length == 0 || typeof items == "string") { return; }

                if(items) {
                    formatHead(json);
                    renderContent(items);
                    renderRong(items);

                    renderGenming();
                }
                
            }
        });
    }



    //sse
    function sseHeadData() {
        var secid = getMarket() + '.' + getCode();

        //正式地址
        var url = "http://" + (Math.floor(Math.random() * 99) + 1) +".push2.eastmoney.com/api/qt/stock/sse?ut=fa5fd1943c7b386f172d6893dbfba10b&invt=2&fltt=2&fields=f1,f43,f57,f58,f169,f170,f46,f44,f51,f168,f47,f116,f60,f45,f52,f50,f48,f167,f117,f71,f161,f49,f162,f107,f86,f177,f127,f199,f128,f80,f152,f110,f111,f107,f285,f286,f262,f263,f256,f257,f269,f270&secid=" + secid;


        var evtSource = new EventSource(url);
        evtSource.onmessage = function (msg) {
            var obj = JSON.parse(msg.data)
            var items = msg.data;

            if (obj.data) {
                formatHead(obj);

            }
        }
            

    }


    //head format
    var headSourceData;
    function formatHead(data) {
        // console.log(data);

        if(data.full == 1 && data.data){

            headSourceData = data.data;

        }
        else if(data.full == 0 && data.data ){   

            if(headSourceData) {
                
                headSourceData = marge(headSourceData, data.data);

            }
            
        }

        renderHead(headSourceData);
      
    }


    function renderHead(items) {
        var list = [
            { "name": "zxj", "item": items.f43  == "-" ? "-" : (items.f43).toFixed(items.f152), "color": getColor(items.f170) },
            { "name": "zde", "item": items.f169 == "-" ? "-" : (items.f169).toFixed(items.f152), "color": getColor(items.f170) },
            { "name": "zdf", "item": items.f170 == "-" ? "-" : (items.f170).toFixed(items.f152) + "%", "color": getColor(items.f170) },
            { "name": "jk", "item": items.f46 == "-" ? "-" : (items.f46).toFixed(items.f152), "color": getColor(items.f46 - items.f60) },
            { "name": "zs", "item": items.f60 == "-" ? "-" : (items.f60).toFixed(items.f152)},
            { "name": "zg", "item": items.f44 == "-" ? "-" : (items.f44).toFixed(items.f152), "color": getColor(items.f44 - items.f60) },
            { "name": "zd", "item": items.f45 == "-" ? "-" : (items.f45).toFixed(items.f152), "color": getColor(items.f45 - items.f60) },
            { "name": "zt", "item": items.f51 == "-" ? "-" : (items.f51).toFixed(2), "color": getColor(items.f51 - items.f60) },
            { "name": "dt", "item": items.f52 == "-" ? "-" : (items.f52).toFixed(2), "color": getColor(items.f52 - items.f60) },
            { "name": "hs", "item": items.f168 == "-" ? "-" : items.f168 + "%" },
            { "name": "lb", "item": items.f50 == "-" ? "-" : (items.f50).toFixed(2)},
            { "name": "cjl", "item": items.f47 == "-" ? "-" : NumbericFormat(items.f47) },
            { "name": "cje", "item": items.f48 == "-" ? "-" : NumbericFormat(items.f48) },
            { "name": "sy", "item": items.f162 == "-" ? "-" : (items.f162).toFixed(2)},
            { "name": "sj", "item": items.f167 == "-" ? "-" : (items.f167).toFixed(2)},
            { "name": "zsz", "item": items.f116 == "-" ? "-" : NumbericFormat(items.f116) },
            { "name": "ltsz", "item": items.f117 == "-" ? "-" : NumbericFormat(items.f117) }
        ];
        for (var i = 0; i < list.length; i++) {
            var name = $("#" + list[i].name);
            name.text(list[i].item);
            name.removeClass("red").removeClass("green").addClass(list[i].color);
        }

        //箭头颜色
        onChangeDataRender(items.f170);

        //时间
        if(items.f86) {
            var d = new Date(items.f86 * 1000);  //("0" + (d.getMonth() + 1)).slice(-2)    d.getMinutes()  d.getMinutes()  d.getSeconds()
            var whichDay = '';
            if(d.getDay() == 0) {
                whichDay = '星期天';
            } else if(d.getDay() == 1) {
                whichDay = '星期一';
            } else if(d.getDay() == 2) {
                whichDay = '星期二';
            } else if(d.getDay() == 3) {
                whichDay = '星期三';
            } else if(d.getDay() == 4) {
                whichDay = '星期四';
            } else if(d.getDay() == 5) {
                whichDay = '星期五';
            }else if(d.getDay() == 6) {
                whichDay = '星期六';
            }

            youWant = d.getFullYear() + '-' + (("0" + (d.getMonth() + 1)).slice(-2)) + '-' + (("0" + (d.getDate())).slice(-2)) +  ' ' + whichDay + ' ' + ("0" + (d.getHours())).slice(-2) + ':' + ("0" + (d.getMinutes())).slice(-2) + ':' + ("0" + (d.getSeconds())).slice(-2);
            
            $("#day").html('（' + youWant + '）');
        }

        //判断若字数过长  字体变小
        if(items.f43 >= 1000) {
            $("#zxj").css("font-size", "23px")
            
        }

    }


    function renderContent(items) {
        var obj = {
            "market": items.f107,
            "code": items.f57,
            "name": items.f58,
            "id": items.f107 + items.f57,
            "time": '111'
        }
       


        $(".n1").attr("href", "http://data.eastmoney.com/zlsj/detail/" + obj["code"] + "-1.html");

        if(obj["name"]) {
            $(".n2").text("查看" + obj["name"] + "买卖点");
            $(".n3").text(obj["name"] + "股价预警")
            $(".quote_title_0").text(obj["name"]);
        }
        


        $(".quote_title_1").text(obj["code"]);
        var src = "//pifm3.eastmoney.com/EM_Finance2014PictureInterface/RC.ashx?url=http://m.quote.eastmoney.com/stock," + obj["code"] + ".shtml";
        $(".QRcode-div img").attr("src", src);
        
        
        //ie8
        if(obj["code"] && obj["name"]) {
            // $("title").text(obj["name"] + obj["code"] + "股票价格_行情_走势图—东方财富网");
            document.title = obj["name"] + obj["code"] + "股票价格_行情_走势图—东方财富网";
        }
       

    }

    function renderRong(items) {
         //融 和港股通
        // if(items.f177 & 64) {
        //     $(".rongi").show();
        //     $(".rongi a").attr("href", "http://data.eastmoney.com/rzrq/detail/" + items.f57 + ".html");
        // } else {
        //     $(".rongi").hide();
        // }
        // if (items.f177 & 1024) {
        //     $("#sgt_icon").show();
        //     $("#hgt_icon").hide();
        // } else if (items.f177 & 512){
        //     $("#sgt_icon").hide();
        //     $("#hgt_icon").show();
        // }


        if (items.f110 == 1 && items.f111 == 2) {
            $("#jys-box").show().find("b ").text("沪主板");
            $("#jys-box").attr("title", "该股票在沪主板上市");
            $("#jys-box").find("a").attr("href", "//quote.eastmoney.com/center/gridlist.html#sh_a_board")
        }
        if (items.f110 == 0 && items.f111 == 6) {
            $("#jys-box").show().find("b ").text("深主板");
            $("#jys-box").attr("title", "该股票在深主板上市");
            $("#jys-box").find("a").attr("href", "//quote.eastmoney.com/center/gridlist.html#sz_a_board")
        }
        if (items.f107 == 0 && items.f111 == 13) {
            $("#jys-box").show().find("b ").text("中小板");
            $("#jys-box").attr("title", "该股票在中小板上市");
            $("#jys-box").find("a").attr("href", "//quote.eastmoney.com/center/gridlist.html#sme_board")
        }
        if (items.f107 == 0 && items.f111 == 80) {
            $("#jys-box").show().find("b ").text("创业板");
            $("#jys-box").attr("title", "该股票在创业板上市");
            $("#jys-box").find("a").attr("href", "//quote.eastmoney.com/center/gridlist.html#gem_board")
        }
        if ((items.f177) & 512) {
            $("#hgt_icon").show()
        } else {
            if ((items.f177) & 1024) {
                $("#sgt_icon").show()
            }
        }
        if(items.f107 == 1 && items.f111 == 23) {
            $("#kcb").show()
        }else {
            $("#kcb").hide()
        }
        

        if ((items.f177) & 64) {
            $("#rong").show();
            $("#rong a").attr("href", "http://data.eastmoney.com/rzrq/detail/" + items.f57 + ".html");
        } else {
            $("#rong").hide()
        }
        if (items.f177 & 32768) {
            $("#hlt").show().find("b ").text("沪伦通");
            $("#hlt").attr("title", "该股票为沪伦通标的");
            $("#hlt").find("a").attr("href", "http://quote.eastmoney.com/uk/" + items.f286 + "." + items.f285 + ".html");
            $("#GDR").show().find("b ").text("GDR");
            $("#GDR").attr("title", "该股票存在关联的GDR（全球存托凭证）");
            $("#GDR").find("a").attr("href", "http://quote.eastmoney.com/uk/" + items.f286 + "." + items.f285 + ".html")
        }
        var marketzhai = items.f263 == "1" ? "sh" : "sz";
        if (items.f262 && items.f262 != "-") {
            $("#Z-box").show().find("b").text("可转债");
            $("#Z-box").attr("title", "点击查看关联可转债行情");
            $("#Z-box").find("a").attr("href", "http://quote.eastmoney.com/bond/" + marketzhai + items.f262 + ".html")
        } else {
            $("#Z-box").hide()
        }
        var marketH = items.f257;
        if (items.f256 && items.f256 != "-") {
            $("#H-box").show().find("b").text("H股");
            $("#H-box").attr("title", "点击查看关联H股行情");
            $("#H-box").find("a").attr("href", "http://quote.eastmoney.com/unify/r/" + marketH + "." + items.f256)
        } else {
            $("#H-box").hide()
        }
        var marketB = items.f270 == "1" ? "sh" : "sz";
        if (items.f269 && items.f269 != "-") {
            $("#B-box").show().find("b ").text("B股");
            $("#B-box").attr("title", "点击查看关联B股行情");
            $("#B-box").find("a").attr("href", "http://quote.eastmoney.com/" + marketB + items.f269 + ".html")
        } else {
            $("#B-box").hide()
        }


        //


    }

    //更名
    function renderGenming() {
        var _this = this;
        var code = getCode();
        $.ajax({
            url: "http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=ABLS_MB&token=70f12f2f4f091e459a279469fe49eca5&filter=(scode=%27" + code + "%27)&st=changedate",
            dataType: "jsonp",
            scriptCharset: "utf-8",
            accept: "json",
            success: function(json) {
                if (json.length > 1) {
                    $("#stock_change_name").show();
                    $("#stock_change_name .rongi").css("display", "block");
                    var html = "<span class=usedName>" + json[0].sname + "</span> <span class='usedName'>&gt;&gt;&gt;</span>";
                    for (var i = 1; i < json.length - 1; i++) {
                        html += '<span class="usedName">' + json[i].sname + '<span class="hasDate">(' + json[i].changedate.substring(0, 9).replace(/\//g, "-") + ")</span></span><span class='usedName'>&gt;&gt;&gt;</span>"
                    }
                    html += '<span class="usedName">' + json[json.length - 1].sname + '<span class="hasDate">(' + json[json.length - 1].changedate.substring(0, 9).replace(/\//g, "-") + ")</span></span>";
                    $("#stock_change_name .shorthandInfo").html(html)

                    $("#stock_change_name").hover(function() {
                        // console.log('777');
                        $(".comNameExInfo").show();
                        $(".arrowUp").show();
                    }, function() {
                        $(".comNameExInfo").hide();
                    })

                    $(".closeBtn").click(function() {
                        $(".comNameExInfo").hide();
                    })
                }
            }
        })

    }


    function onChangeDataRender(item) {
        
        if (item != 0 && item != "-") {
            if (item > 0) {
                $("#arrow-find").removeClass("down-arrow").addClass("up-arrow");

            } else {
                $("#arrow-find").removeClass("up-arrow").addClass("down-arrow");
            }
        } 

        if(item == 0){
            $("#arrow-find").removeClass("up-arrow").removeClass("down-arrow");
        }

      
        
    }


    function getParam(name) {
        var urlpara = location.search;
        var par = {};
        if (urlpara != "") {
            urlpara = urlpara.substring(1, urlpara.length);
            var para = urlpara.split("&");
            var parname;
            var parvalue;
            for (var i = 0; i < para.length; i++) {
                parname = para[i].substring(0, para[i].indexOf("="));
                parvalue = para[i].substring(para[i].indexOf("=") + 1, para[i].length);
                par[parname] = parvalue;
            }
        }
        if (typeof (par[name]) != "undefined") {
            return par[name];
        } else {
            return null;
        }
    }

    //获取code和market
    function getCode() {
        var code;
        if(getParam('code')) {
            code = getParam('code');
        }else if(getParam('newcode')) {
            code = getParam('newcode').split('.')[1];
        } else if(getParam('id')) {
            code = getParam('id').substr(0,6);
           
        }

        return code;
    }
    function getMarket() {
        var market;
        if(getParam('market')) {
            var newmarket = getParam('market') == 2 ? 0 : 1;
            market = newmarket;
        }else if(getParam('newcode')) {
            market = getParam('newcode').split('.')[0];
        }else if(getParam('id')) {
            market = getParam('id').substr(6);
            var newmarket = market == 2 ? 0 : 1;

            market = newmarket;
            
        }
        return market
    }


    function gw_now(time, id) {
        var str = time.replace(/-/g, "/");
        var _date = new Date(str);
        var year = _date.getFullYear();
        var month = gw_now_addzero(_date.getMonth() + 1);
        var day = gw_now_addzero(_date.getDate());
        var hour = gw_now_addzero(_date.getHours());
        var minute = gw_now_addzero(_date.getMinutes());
        var second = gw_now_addzero(_date.getSeconds());
        var week = "";
        switch (_date.getDay()) {
            case 0: week = "星期天"; break
            case 1: week = "星期一"; break
            case 2: week = "星期二"; break
            case 3: week = "星期三"; break
            case 4: week = "星期四"; break
            case 5: week = "星期五"; break
            case 6: week = "星期六"; break
        }
        var Time = year + "-" + month + "-" + day + " " + week + " " + hour + ":" + minute + ":" + second;
        $(id).html('(' + Time + ')')
    }
    function gw_now_addzero(temp) {
        if (temp < 10) return "0" + temp;
        else return temp;
    }
    function getColor(str) {
        var context = str.toString();
        context = context.replace("%", "");
        if (context == 0 || isNaN(context)) {
            return "";
        } else if (context > 0) {
            return "red";
        } else {
            return "green";
        }
    }

    //融和沪深股通
    function isRong() {
        var _url = "//nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&sty=MCSS&st=z&js=((x))&token=883df69e21fd8fe57ebf53dd71aae25f&cmd=" + stockEnity.stockId
        $.ajax({
            url: _url,
            dataType: "jsonp",
            jsonp: "cb",
            success: function (json) {              
                if (typeof json !== "string") return;
                var data = json.split(",");
                if (data[4] == "深股通") {
                    $("#sgt_icon").show();
                    $("#hgt_icon").hide();
                } else if (data[4] == "沪股通"){
                    $("#sgt_icon").hide();
                    $("#hgt_icon").show();
                }
                if (data[5] == "True") {
                    $(".rongi").show();
                    $(".rongi a").attr("href", "http://data.eastmoney.com/rzrq/detail/" + data[1] + ".html");
                } else {
                    $(".rongi").hide();
                }

            }

        })
    }

    function NumbericFormat(string) {
        var context = Number(string);
        //var fushu = false;
        if (!isNaN(context)) {
            var item = parseInt(string);
            if ((item > 0 && item < 1e4) || (item < 0 && item > -1e4)) {
                return item;
            } else if ((item > 0 && item < 1e6) || (item < 0 && item > -1e6)) {
                item = item / 10000;
                return item.toFixed(2) + "万";
            } else if ((item > 0 && item < 1e7) || (item < 0 && item > -1e7)) {
                item = item / 10000;
                return item.toFixed(1) + "万";
            } else if ((item > 0 && item < 1e8) || (item < 0 && item > -1e8)) {
                item = item / 10000;
                return item.toFixed(0) + "万";
            } else if ((item > 0 && item < 1e10) || (item < 0 && item > -1e10)) {
                item = item / 1e8;
                return item.toFixed(2) + "亿";
            } else if ((item > 0 && item < 1e11) || (item < 0 && item > -1e11)) {
                item = item / 1e8;
                return item.toFixed(1) + "亿";
            } else if ((item > 0 && item < 1e12) || (item < 0 && item > -1e12)) {
                item = item / 1e8;
                return item.toFixed(0) + "亿";
            } else if ((item > 0 && item < 1e14) || (item < 0 && item > -1e14)) {
                item = item / 1e12;
                return item.toFixed(2) + "万亿";
            } else if ((item > 0 && item < 1e15) || (item < 0 && item > -1e15)) {
                item = item / 1e12;
                return item.toFixed(1) + "万亿";
            } else if ((item > 0 && item < 1e16) || (item < 0 && item > -1e16)) {
                item = item / 1e12;
                return item.toFixed(0) + "万亿";
            } else {
                return item;
            }
        }
        return context.toString();
    }

/***/ }),

/***/ "./src/modules/template/index.js":
/*!***************************************!*\
  !*** ./src/modules/template/index.js ***!
  \***************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var __WEBPACK_AMD_DEFINE_RESULT__;/*!art-template - Template Engine | http://aui.github.com/artTemplate/*/
!function(){function a(a){return a.replace(t,"").replace(u,",").replace(v,"").replace(w,"").replace(x,"").split(y)}function b(a){return"'"+a.replace(/('|\\)/g,"\\$1").replace(/\r/g,"\\r").replace(/\n/g,"\\n")+"'"}function c(c,d){function e(a){return m+=a.split(/\n/).length-1,k&&(a=a.replace(/\s+/g," ").replace(/<!--[\w\W]*?-->/g,"")),a&&(a=s[1]+b(a)+s[2]+"\n"),a}function f(b){var c=m;if(j?b=j(b,d):g&&(b=b.replace(/\n/g,function(){return m++,"$line="+m+";"})),0===b.indexOf("=")){var e=l&&!/^=[=#]/.test(b);if(b=b.replace(/^=[=#]?|[\s;]*$/g,""),e){var f=b.replace(/\s*\([^\)]+\)/,"");n[f]||/^(include|print)$/.test(f)||(b="$escape("+b+")")}else b="$string("+b+")";b=s[1]+b+s[2]}return g&&(b="$line="+c+";"+b),r(a(b),function(a){if(a&&!p[a]){var b;b="print"===a?u:"include"===a?v:n[a]?"$utils."+a:o[a]?"$helpers."+a:"$data."+a,w+=a+"="+b+",",p[a]=!0}}),b+"\n"}var g=d.debug,h=d.openTag,i=d.closeTag,j=d.parser,k=d.compress,l=d.escape,m=1,p={$data:1,$filename:1,$utils:1,$helpers:1,$out:1,$line:1},q="".trim,s=q?["$out='';","$out+=",";","$out"]:["$out=[];","$out.push(",");","$out.join('')"],t=q?"$out+=text;return $out;":"$out.push(text);",u="function(){var text=''.concat.apply('',arguments);"+t+"}",v="function(filename,data){data=data||$data;var text=$utils.$include(filename,data,$filename);"+t+"}",w="'use strict';var $utils=this,$helpers=$utils.$helpers,"+(g?"$line=0,":""),x=s[0],y="return new String("+s[3]+");";r(c.split(h),function(a){a=a.split(i);var b=a[0],c=a[1];1===a.length?x+=e(b):(x+=f(b),c&&(x+=e(c)))});var z=w+x+y;g&&(z="try{"+z+"}catch(e){throw {filename:$filename,name:'Render Error',message:e.message,line:$line,source:"+b(c)+".split(/\\n/)[$line-1].replace(/^\\s+/,'')};}");try{var A=new Function("$data","$filename",z);return A.prototype=n,A}catch(B){throw B.temp="function anonymous($data,$filename) {"+z+"}",B}}var d=function(a,b){return"string"==typeof b?q(b,{filename:a}):g(a,b)};d.version="3.0.0",d.config=function(a,b){e[a]=b};var e=d.defaults={openTag:"<%",closeTag:"%>",escape:!0,cache:!0,compress:!1,parser:null},f=d.cache={};d.render=function(a,b){return q(a)(b)};var g=d.renderFile=function(a,b){var c=d.get(a)||p({filename:a,name:"Render Error",message:"Template not found"});return b?c(b):c};d.get=function(a){var b;if(f[a])b=f[a];else if("object"==typeof document){var c=document.getElementById(a);if(c){var d=(c.value||c.innerHTML).replace(/^\s*|\s*$/g,"");b=q(d,{filename:a})}}return b};var h=function(a,b){return"string"!=typeof a&&(b=typeof a,"number"===b?a+="":a="function"===b?h(a.call(a)):""),a},i={"<":"&#60;",">":"&#62;",'"':"&#34;","'":"&#39;","&":"&#38;"},j=function(a){return i[a]},k=function(a){return h(a).replace(/&(?![\w#]+;)|[<>"']/g,j)},l=Array.isArray||function(a){return"[object Array]"==={}.toString.call(a)},m=function(a,b){var c,d;if(l(a))for(c=0,d=a.length;d>c;c++)b.call(a,a[c],c,a);else for(c in a)b.call(a,a[c],c)},n=d.utils={$helpers:{},$include:g,$string:h,$escape:k,$each:m};d.helper=function(a,b){o[a]=b};var o=d.helpers=n.$helpers;d.onerror=function(a){var b="Template Error\n\n";for(var c in a)b+="<"+c+">\n"+a[c]+"\n\n";"object"==typeof console&&console.error(b)};var p=function(a){return d.onerror(a),function(){return"{Template Error}"}},q=d.compile=function(a,b){function d(c){try{return new i(c,h)+""}catch(d){return b.debug?p(d)():(b.debug=!0,q(a,b)(c))}}b=b||{};for(var g in e)void 0===b[g]&&(b[g]=e[g]);var h=b.filename;try{var i=c(a,b)}catch(j){return j.filename=h||"anonymous",j.name="Syntax Error",p(j)}return d.prototype=i.prototype,d.toString=function(){return i.toString()},h&&b.cache&&(f[h]=d),d},r=n.$each,s="break,case,catch,continue,debugger,default,delete,do,else,false,finally,for,function,if,in,instanceof,new,null,return,switch,this,throw,true,try,typeof,var,void,while,with,abstract,boolean,byte,char,class,const,double,enum,export,extends,final,float,goto,implements,import,int,interface,long,native,package,private,protected,public,short,static,super,synchronized,throws,transient,volatile,arguments,let,yield,undefined",t=/\/\*[\w\W]*?\*\/|\/\/[^\n]*\n|\/\/[^\n]*$|"(?:[^"\\]|\\[\w\W])*"|'(?:[^'\\]|\\[\w\W])*'|\s*\.\s*[$\w\.]+/g,u=/[^\w$]+/g,v=new RegExp(["\\b"+s.replace(/,/g,"\\b|\\b")+"\\b"].join("|"),"g"),w=/^\d[^,]*|,\d[^,]*/g,x=/^,+|,+$/g,y=/^$|,+/;e.openTag="{{",e.closeTag="}}";var z=function(a,b){var c=b.split(":"),d=c.shift(),e=c.join(":")||"";return e&&(e=", "+e),"$helpers."+d+"("+a+e+")"};e.parser=function(a){a=a.replace(/^\s/,"");var b=a.split(" "),c=b.shift(),e=b.join(" ");switch(c){case"if":a="if("+e+"){";break;case"else":b="if"===b.shift()?" if("+b.join(" ")+")":"",a="}else"+b+"{";break;case"/if":a="}";break;case"each":var f=b[0]||"$data",g=b[1]||"as",h=b[2]||"$value",i=b[3]||"$index",j=h+","+i;"as"!==g&&(f="[]"),a="$each("+f+",function("+j+"){";break;case"/each":a="});";break;case"echo":a="print("+e+");";break;case"print":case"include":a=c+"("+b.join(",")+");";break;default:if(/^\s*\|\s*[\w\$]/.test(e)){var k=!0;0===a.indexOf("#")&&(a=a.substr(1),k=!1);for(var l=0,m=a.split("|"),n=m.length,o=m[l++];n>l;l++)o=z(o,m[l]);a=(k?"=":"=#")+o}else a=d.helpers[c]?"=#"+c+"("+b.join(",")+");":"="+a}return a}, true?!(__WEBPACK_AMD_DEFINE_RESULT__ = (function(){return d}).call(exports, __webpack_require__, exports, module),
				__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__)):undefined}();

/***/ })

/******/ });
//# sourceMappingURL=timetrade.js.map