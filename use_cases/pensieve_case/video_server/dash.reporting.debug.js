(function(f){if(typeof exports==="object"&&typeof module!=="undefined"){module.exports=f()}else if(typeof define==="function"&&define.amd){define([],f)}else{var g;if(typeof window!=="undefined"){g=window}else if(typeof global!=="undefined"){g=global}else if(typeof self!=="undefined"){g=self}else{g=this}(g.dashjs || (g.dashjs = {})).MetricsReporting = f()}})(function(){var define,module,exports;return (function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(_dereq_,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

/**
 * The copyright in this software is being made available under the BSD License,
 * included below. This software may be subject to other third party and contributor
 * rights, including patent rights, and no such rights are granted under this license.
 *
 * Copyright (c) 2013, Dash Industry Forum.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *  * Redistributions of source code must retain the above copyright notice, this
 *  list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright notice,
 *  this list of conditions and the following disclaimer in the documentation and/or
 *  other materials provided with the distribution.
 *  * Neither the name of Dash Industry Forum nor the names of its
 *  contributors may be used to endorse or promote products derived from this software
 *  without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS AS IS AND ANY
 *  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 *  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 *  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 *  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 *  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 *  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 *  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 */

/**
 * @module FactoryMaker
 */
var FactoryMaker = function () {
  var instance;
  var extensions = [];
  var singletonContexts = [];

  function extend(name, childInstance, override, context) {
    var extensionContext = getExtensionContext(context);

    if (!extensionContext[name] && childInstance) {
      extensionContext[name] = {
        instance: childInstance,
        override: override
      };
    }
  }
  /**
   * Use this method from your extended object.  this.factory is injected into your object.
   * this.factory.getSingletonInstance(this.context, 'VideoModel')
   * will return the video model for use in the extended object.
   *
   * @param {Object} context - injected into extended object as this.context
   * @param {string} className - string name found in all dash.js objects
   * with name __dashjs_factory_name Will be at the bottom. Will be the same as the object's name.
   * @returns {*} Context aware instance of specified singleton name.
   * @memberof module:FactoryMaker
   * @instance
   */


  function getSingletonInstance(context, className) {
    for (var i in singletonContexts) {
      var obj = singletonContexts[i];

      if (obj.context === context && obj.name === className) {
        return obj.instance;
      }
    }

    return null;
  }
  /**
   * Use this method to add an singleton instance to the system.  Useful for unit testing to mock objects etc.
   *
   * @param {Object} context
   * @param {string} className
   * @param {Object} instance
   * @memberof module:FactoryMaker
   * @instance
   */


  function setSingletonInstance(context, className, instance) {
    for (var i in singletonContexts) {
      var obj = singletonContexts[i];

      if (obj.context === context && obj.name === className) {
        singletonContexts[i].instance = instance;
        return;
      }
    }

    singletonContexts.push({
      name: className,
      context: context,
      instance: instance
    });
  }

  function getClassFactory(classConstructor) {
    return function (context) {
      if (context === undefined) {
        context = {};
      }

      return {
        create: function create() {
          return merge(classConstructor.__dashjs_factory_name, classConstructor.apply({
            context: context
          }, arguments), context, arguments);
        }
      };
    };
  }

  function getSingletonFactory(classConstructor) {
    return function (context) {
      var instance;

      if (context === undefined) {
        context = {};
      }

      return {
        getInstance: function getInstance() {
          // If we don't have an instance yet check for one on the context
          if (!instance) {
            instance = getSingletonInstance(context, classConstructor.__dashjs_factory_name);
          } // If there's no instance on the context then create one


          if (!instance) {
            instance = merge(classConstructor.__dashjs_factory_name, classConstructor.apply({
              context: context
            }, arguments), context, arguments);
            singletonContexts.push({
              name: classConstructor.__dashjs_factory_name,
              context: context,
              instance: instance
            });
          }

          return instance;
        }
      };
    };
  }

  function merge(name, classConstructor, context, args) {
    var extensionContext = getExtensionContext(context);
    var extensionObject = extensionContext[name];

    if (extensionObject) {
      var extension = extensionObject.instance;

      if (extensionObject.override) {
        //Override public methods in parent but keep parent.
        extension = extension.apply({
          context: context,
          factory: instance,
          parent: classConstructor
        }, args);

        for (var prop in extension) {
          if (classConstructor.hasOwnProperty(prop)) {
            classConstructor[prop] = extension[prop];
          }
        }
      } else {
        //replace parent object completely with new object. Same as dijon.
        return extension.apply({
          context: context,
          factory: instance
        }, args);
      }
    }

    return classConstructor;
  }

  function getExtensionContext(context) {
    var extensionContext;
    extensions.forEach(function (obj) {
      if (obj === context) {
        extensionContext = obj;
      }
    });

    if (!extensionContext) {
      extensionContext = extensions.push(context);
    }

    return extensionContext;
  }

  instance = {
    extend: extend,
    getSingletonInstance: getSingletonInstance,
    setSingletonInstance: setSingletonInstance,
    getSingletonFactory: getSingletonFactory,
    getClassFactory: getClassFactory
  };
  return instance;
}();

var _default = FactoryMaker;
exports.default = _default;

},{}],2:[function(_dereq_,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _EventsBase2 = _interopRequireDefault(_dereq_(4));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }

/**
 * @class
 * @ignore
 */
var CoreEvents =
/*#__PURE__*/
function (_EventsBase) {
  _inherits(CoreEvents, _EventsBase);

  function CoreEvents() {
    var _this;

    _classCallCheck(this, CoreEvents);

    _this = _possibleConstructorReturn(this, _getPrototypeOf(CoreEvents).call(this));
    _this.AST_IN_FUTURE = 'astinfuture';
    _this.BUFFERING_COMPLETED = 'bufferingCompleted';
    _this.BUFFER_CLEARED = 'bufferCleared';
    _this.BUFFER_LEVEL_UPDATED = 'bufferLevelUpdated';
    _this.BYTES_APPENDED = 'bytesAppended';
    _this.CHECK_FOR_EXISTENCE_COMPLETED = 'checkForExistenceCompleted';
    _this.CHUNK_APPENDED = 'chunkAppended';
    _this.CURRENT_TRACK_CHANGED = 'currenttrackchanged';
    _this.DATA_UPDATE_COMPLETED = 'dataUpdateCompleted';
    _this.DATA_UPDATE_STARTED = 'dataUpdateStarted';
    _this.FRAGMENT_LOADING_COMPLETED = 'fragmentLoadingCompleted';
    _this.FRAGMENT_LOADING_STARTED = 'fragmentLoadingStarted';
    _this.FRAGMENT_LOADING_ABANDONED = 'fragmentLoadingAbandoned';
    _this.INITIALIZATION_LOADED = 'initializationLoaded';
    _this.INIT_FRAGMENT_LOADED = 'initFragmentLoaded';
    _this.INIT_REQUESTED = 'initRequested';
    _this.INTERNAL_MANIFEST_LOADED = 'internalManifestLoaded';
    _this.LIVE_EDGE_SEARCH_COMPLETED = 'liveEdgeSearchCompleted';
    _this.LOADING_COMPLETED = 'loadingCompleted';
    _this.LOADING_PROGRESS = 'loadingProgress';
    _this.MANIFEST_UPDATED = 'manifestUpdated';
    _this.MEDIA_FRAGMENT_LOADED = 'mediaFragmentLoaded';
    _this.QUOTA_EXCEEDED = 'quotaExceeded';
    _this.REPRESENTATION_UPDATED = 'representationUpdated';
    _this.SEGMENTS_LOADED = 'segmentsLoaded';
    _this.SERVICE_LOCATION_BLACKLIST_CHANGED = 'serviceLocationBlacklistChanged';
    _this.SOURCEBUFFER_APPEND_COMPLETED = 'sourceBufferAppendCompleted';
    _this.SOURCEBUFFER_REMOVE_COMPLETED = 'sourceBufferRemoveCompleted';
    _this.STREAMS_COMPOSED = 'streamsComposed';
    _this.STREAM_BUFFERING_COMPLETED = 'streamBufferingCompleted';
    _this.STREAM_COMPLETED = 'streamCompleted';
    _this.STREAM_INITIALIZED = 'streaminitialized';
    _this.STREAM_TEARDOWN_COMPLETE = 'streamTeardownComplete';
    _this.TIMED_TEXT_REQUESTED = 'timedTextRequested';
    _this.TIME_SYNCHRONIZATION_COMPLETED = 'timeSynchronizationComplete';
    _this.URL_RESOLUTION_FAILED = 'urlResolutionFailed';
    _this.WALLCLOCK_TIME_UPDATED = 'wallclockTimeUpdated';
    _this.XLINK_ALL_ELEMENTS_LOADED = 'xlinkAllElementsLoaded';
    _this.XLINK_ELEMENT_LOADED = 'xlinkElementLoaded';
    _this.XLINK_READY = 'xlinkReady';
    return _this;
  }

  return CoreEvents;
}(_EventsBase2.default);

var _default = CoreEvents;
exports.default = _default;

},{"4":4}],3:[function(_dereq_,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _CoreEvents2 = _interopRequireDefault(_dereq_(2));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }

var Events =
/*#__PURE__*/
function (_CoreEvents) {
  _inherits(Events, _CoreEvents);

  function Events() {
    _classCallCheck(this, Events);

    return _possibleConstructorReturn(this, _getPrototypeOf(Events).apply(this, arguments));
  }

  return Events;
}(_CoreEvents2.default);

var events = new Events();
var _default = events;
exports.default = _default;

},{"2":2}],4:[function(_dereq_,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

/**
 * The copyright in this software is being made available under the BSD License,
 * included below. This software may be subject to other third party and contributor
 * rights, including patent rights, and no such rights are granted under this license.
 *
 * Copyright (c) 2013, Dash Industry Forum.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *  * Redistributions of source code must retain the above copyright notice, this
 *  list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright notice,
 *  this list of conditions and the following disclaimer in the documentation and/or
 *  other materials provided with the distribution.
 *  * Neither the name of Dash Industry Forum nor the names of its
 *  contributors may be used to endorse or promote products derived from this software
 *  without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS AS IS AND ANY
 *  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 *  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 *  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 *  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 *  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 *  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 *  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 */

/**
 * @class
 * @ignore
 */
var EventsBase =
/*#__PURE__*/
function () {
  function EventsBase() {
    _classCallCheck(this, EventsBase);
  }

  _createClass(EventsBase, [{
    key: "extend",
    value: function extend(events, config) {
      if (!events) return;
      var override = config ? config.override : false;
      var publicOnly = config ? config.publicOnly : false;

      for (var evt in events) {
        if (!events.hasOwnProperty(evt) || this[evt] && !override) continue;
        if (publicOnly && events[evt].indexOf('public_') === -1) continue;
        this[evt] = events[evt];
      }
    }
  }]);

  return EventsBase;
}();

var _default = EventsBase;
exports.default = _default;

},{}],5:[function(_dereq_,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _EventsBase2 = _interopRequireDefault(_dereq_(4));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }

/**
 * @class
 *
 */
var MediaPlayerEvents =
/*#__PURE__*/
function (_EventsBase) {
  _inherits(MediaPlayerEvents, _EventsBase);

  /**
   * @description Public facing external events to be used when developing a player that implements dash.js.
   */
  function MediaPlayerEvents() {
    var _this;

    _classCallCheck(this, MediaPlayerEvents);

    _this = _possibleConstructorReturn(this, _getPrototypeOf(MediaPlayerEvents).call(this));
    /**
     * Triggered when the video element's buffer state changes to stalled.
     * Check mediaType in payload to determine type (Video, Audio, FragmentedText).
     * @event MediaPlayerEvents#BUFFER_EMPTY
     */

    _this.BUFFER_EMPTY = 'bufferstalled';
    /**
     * Triggered when the video element's buffer state changes to loaded.
     * Check mediaType in payload to determine type (Video, Audio, FragmentedText).
     * @event MediaPlayerEvents#BUFFER_LOADED
     */

    _this.BUFFER_LOADED = 'bufferloaded';
    /**
     * Triggered when the video element's buffer state changes, either stalled or loaded. Check payload for state.
     * @event MediaPlayerEvents#BUFFER_LEVEL_STATE_CHANGED
     */

    _this.BUFFER_LEVEL_STATE_CHANGED = 'bufferStateChanged';
    /**
     * Triggered when
     * @event MediaPlayerEvents#ERROR
     */

    _this.ERROR = 'error';
    /**
     * Triggered when {@link module:Debug} log method is called.
     * @event MediaPlayerEvents#LOG
     */

    _this.LOG = 'log'; //TODO refactor with internal event

    /**
     * Triggered when the manifest load is complete
     * @event MediaPlayerEvents#MANIFEST_LOADED
     */

    _this.MANIFEST_LOADED = 'manifestloaded';
    /**
     * Triggered anytime there is a change to the overall metrics.
     * @event MediaPlayerEvents#METRICS_CHANGED
     */

    _this.METRICS_CHANGED = 'metricschanged';
    /**
     * Triggered when an individual metric is added, updated or cleared.
     * @event MediaPlayerEvents#METRIC_CHANGED
     */

    _this.METRIC_CHANGED = 'metricchanged';
    /**
     * Triggered every time a new metric is added.
     * @event MediaPlayerEvents#METRIC_ADDED
     */

    _this.METRIC_ADDED = 'metricadded';
    /**
     * Triggered every time a metric is updated.
     * @event MediaPlayerEvents#METRIC_UPDATED
     */

    _this.METRIC_UPDATED = 'metricupdated';
    /**
     * Triggered at the stream end of a period.
     * @event MediaPlayerEvents#PERIOD_SWITCH_COMPLETED
     */

    _this.PERIOD_SWITCH_COMPLETED = 'streamswitchcompleted';
    /**
     * Triggered when a new period starts.
     * @event MediaPlayerEvents#PERIOD_SWITCH_STARTED
     */

    _this.PERIOD_SWITCH_STARTED = 'streamswitchstarted';
    /**
     * Triggered when an ABR up /down switch is initialed; either by user in manual mode or auto mode via ABR rules.
     * @event MediaPlayerEvents#QUALITY_CHANGE_REQUESTED
     */

    _this.QUALITY_CHANGE_REQUESTED = 'qualityChangeRequested';
    /**
     * Triggered when the new ABR quality is being rendered on-screen.
     * @event MediaPlayerEvents#QUALITY_CHANGE_RENDERED
     */

    _this.QUALITY_CHANGE_RENDERED = 'qualityChangeRendered';
    /**
     * Triggered when the stream is setup and ready.
     * @event MediaPlayerEvents#STREAM_INITIALIZED
     */

    _this.STREAM_INITIALIZED = 'streaminitialized';
    /**
     * Triggered once all text tracks detected in the MPD are added to the video element.
     * @event MediaPlayerEvents#TEXT_TRACKS_ADDED
     */

    _this.TEXT_TRACKS_ADDED = 'alltexttracksadded';
    /**
     * Triggered when a text track is added to the video element's TextTrackList
     * @event MediaPlayerEvents#TEXT_TRACK_ADDED
     */

    _this.TEXT_TRACK_ADDED = 'texttrackadded';
    /**
     * Sent when enough data is available that the media can be played,
     * at least for a couple of frames.  This corresponds to the
     * HAVE_ENOUGH_DATA readyState.
     * @event MediaPlayerEvents#CAN_PLAY
     */

    _this.CAN_PLAY = 'canPlay';
    /**
     * Sent when playback completes.
     * @event MediaPlayerEvents#PLAYBACK_ENDED
     */

    _this.PLAYBACK_ENDED = 'playbackEnded';
    /**
     * Sent when an error occurs.  The element's error
     * attribute contains more information.
     * @event MediaPlayerEvents#PLAYBACK_ERROR
     */

    _this.PLAYBACK_ERROR = 'playbackError';
    /**
     * Sent when playback is not allowed (for example if user gesture is needed).
     * @event MediaPlayerEvents#PLAYBACK_NOT_ALLOWED
     */

    _this.PLAYBACK_NOT_ALLOWED = 'playbackNotAllowed';
    /**
     * The media's metadata has finished loading; all attributes now
     * contain as much useful information as they're going to.
     * @event MediaPlayerEvents#PLAYBACK_METADATA_LOADED
     */

    _this.PLAYBACK_METADATA_LOADED = 'playbackMetaDataLoaded';
    /**
     * Sent when playback is paused.
     * @event MediaPlayerEvents#PLAYBACK_PAUSED
     */

    _this.PLAYBACK_PAUSED = 'playbackPaused';
    /**
     * Sent when the media begins to play (either for the first time, after having been paused,
     * or after ending and then restarting).
     *
     * @event MediaPlayerEvents#PLAYBACK_PLAYING
     */

    _this.PLAYBACK_PLAYING = 'playbackPlaying';
    /**
     * Sent periodically to inform interested parties of progress downloading
     * the media. Information about the current amount of the media that has
     * been downloaded is available in the media element's buffered attribute.
     * @event MediaPlayerEvents#PLAYBACK_PROGRESS
     */

    _this.PLAYBACK_PROGRESS = 'playbackProgress';
    /**
     * Sent when the playback speed changes.
     * @event MediaPlayerEvents#PLAYBACK_RATE_CHANGED
     */

    _this.PLAYBACK_RATE_CHANGED = 'playbackRateChanged';
    /**
     * Sent when a seek operation completes.
     * @event MediaPlayerEvents#PLAYBACK_SEEKED
     */

    _this.PLAYBACK_SEEKED = 'playbackSeeked';
    /**
     * Sent when a seek operation begins.
     * @event MediaPlayerEvents#PLAYBACK_SEEKING
     */

    _this.PLAYBACK_SEEKING = 'playbackSeeking';
    /**
     * Sent when playback of the media starts after having been paused;
     * that is, when playback is resumed after a prior pause event.
     *
     * @event MediaPlayerEvents#PLAYBACK_STARTED
     */

    _this.PLAYBACK_STARTED = 'playbackStarted';
    /**
     * The time indicated by the element's currentTime attribute has changed.
     * @event MediaPlayerEvents#PLAYBACK_TIME_UPDATED
     */

    _this.PLAYBACK_TIME_UPDATED = 'playbackTimeUpdated';
    return _this;
  }

  return MediaPlayerEvents;
}(_EventsBase2.default);

var mediaPlayerEvents = new MediaPlayerEvents();
var _default = mediaPlayerEvents;
exports.default = _default;

},{"4":4}],6:[function(_dereq_,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _DVBErrorsTranslator = _interopRequireDefault(_dereq_(20));

var _MetricsReportingEvents = _interopRequireDefault(_dereq_(7));

var _MetricsCollectionController = _interopRequireDefault(_dereq_(8));

var _MetricsHandlerFactory = _interopRequireDefault(_dereq_(13));

var _ReportingFactory = _interopRequireDefault(_dereq_(18));

var _FactoryMaker = _interopRequireDefault(_dereq_(1));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

/**
 * The copyright in this software is being made available under the BSD License,
 * included below. This software may be subject to other third party and contributor
 * rights, including patent rights, and no such rights are granted under this license.
 *
 * Copyright (c) 2013, Dash Industry Forum.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *  * Redistributions of source code must retain the above copyright notice, this
 *  list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright notice,
 *  this list of conditions and the following disclaimer in the documentation and/or
 *  other materials provided with the distribution.
 *  * Neither the name of Dash Industry Forum nor the names of its
 *  contributors may be used to endorse or promote products derived from this software
 *  without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS AS IS AND ANY
 *  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 *  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 *  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 *  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 *  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 *  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 *  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 */
function MetricsReporting() {
  var context = this.context;
  var instance;
  var dvbErrorsTranslator;
  /**
   * Create a MetricsCollectionController, and a DVBErrorsTranslator
   * @param {Object} config - dependancies from owner
   * @return {MetricsCollectionController} Metrics Collection Controller
   */

  function createMetricsReporting(config) {
    dvbErrorsTranslator = (0, _DVBErrorsTranslator.default)(context).getInstance({
      eventBus: config.eventBus,
      metricsModel: config.metricsModel
    });
    return (0, _MetricsCollectionController.default)(context).create(config);
  }
  /**
   * Get the ReportingFactory to allow new reporters to be registered
   * @return {ReportingFactory} Reporting Factory
   */


  function getReportingFactory() {
    return (0, _ReportingFactory.default)(context).getInstance();
  }
  /**
   * Get the MetricsHandlerFactory to allow new handlers to be registered
   * @return {MetricsHandlerFactory} Metrics Handler Factory
   */


  function getMetricsHandlerFactory() {
    return (0, _MetricsHandlerFactory.default)(context).getInstance();
  }

  instance = {
    createMetricsReporting: createMetricsReporting,
    getReportingFactory: getReportingFactory,
    getMetricsHandlerFactory: getMetricsHandlerFactory
  };
  return instance;
}

MetricsReporting.__dashjs_factory_name = 'MetricsReporting';

var factory = _FactoryMaker.default.getClassFactory(MetricsReporting);

factory.events = _MetricsReportingEvents.default;
var _default = factory;
exports.default = _default;

},{"1":1,"13":13,"18":18,"20":20,"7":7,"8":8}],7:[function(_dereq_,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _EventsBase2 = _interopRequireDefault(_dereq_(4));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }

var MetricsReportingEvents =
/*#__PURE__*/
function (_EventsBase) {
  _inherits(MetricsReportingEvents, _EventsBase);

  function MetricsReportingEvents() {
    var _this;

    _classCallCheck(this, MetricsReportingEvents);

    _this = _possibleConstructorReturn(this, _getPrototypeOf(MetricsReportingEvents).call(this));
    _this.METRICS_INITIALISATION_COMPLETE = 'internal_metricsReportingInitialized';
    _this.BECAME_REPORTING_PLAYER = 'internal_becameReportingPlayer';
    return _this;
  }

  return MetricsReportingEvents;
}(_EventsBase2.default);

var metricsReportingEvents = new MetricsReportingEvents();
var _default = metricsReportingEvents;
exports.default = _default;

},{"4":4}],8:[function(_dereq_,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _MetricsController = _interopRequireDefault(_dereq_(9));

var _ManifestParsing = _interopRequireDefault(_dereq_(22));

var _FactoryMaker = _interopRequireDefault(_dereq_(1));

var _MetricsReportingEvents = _interopRequireDefault(_dereq_(7));

var _Events = _interopRequireDefault(_dereq_(3));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

/**
 * The copyright in this software is being made available under the BSD License,
 * included below. This software may be subject to other third party and contributor
 * rights, including patent rights, and no such rights are granted under this license.
 *
 * Copyright (c) 2013, Dash Industry Forum.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *  * Redistributions of source code must retain the above copyright notice, this
 *  list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright notice,
 *  this list of conditions and the following disclaimer in the documentation and/or
 *  other materials provided with the distribution.
 *  * Neither the name of Dash Industry Forum nor the names of its
 *  contributors may be used to endorse or promote products derived from this software
 *  without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS AS IS AND ANY
 *  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 *  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 *  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 *  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 *  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 *  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 *  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 */
function MetricsCollectionController(config) {
  var metricsControllers = {};
  var context = this.context;
  var eventBus = config.eventBus;

  function update(e) {
    if (e.error) {
      return;
    } // start by assuming all existing controllers need removing


    var controllersToRemove = Object.keys(metricsControllers);
    var metrics = (0, _ManifestParsing.default)(context).getInstance({
      dashManifestModel: config.dashManifestModel
    }).getMetrics(e.manifest);
    metrics.forEach(function (m) {
      var key = JSON.stringify(m);

      if (!metricsControllers.hasOwnProperty(key)) {
        try {
          var controller = (0, _MetricsController.default)(context).create(config);
          controller.initialize(m);
          metricsControllers[key] = controller;
        } catch (e) {// fail quietly
        }
      } else {
        // we still need this controller - delete from removal list
        controllersToRemove.splice(key, 1);
      }
    }); // now remove the unwanted controllers

    controllersToRemove.forEach(function (c) {
      metricsControllers[c].reset();
      delete metricsControllers[c];
    });
    eventBus.trigger(_MetricsReportingEvents.default.METRICS_INITIALISATION_COMPLETE);
  }

  function reset() {
    Object.keys(metricsControllers).forEach(function (key) {
      metricsControllers[key].reset();
    });
    metricsControllers = {};
  }

  function setup() {
    eventBus.on(_Events.default.MANIFEST_UPDATED, update);
    eventBus.on(_Events.default.STREAM_TEARDOWN_COMPLETE, reset);
  }

  setup(); // don't export any actual methods

  return {};
}

MetricsCollectionController.__dashjs_factory_name = 'MetricsCollectionController';

var _default = _FactoryMaker.default.getClassFactory(MetricsCollectionController);

exports.default = _default;

},{"1":1,"22":22,"3":3,"7":7,"9":9}],9:[function(_dereq_,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _FactoryMaker = _interopRequireDefault(_dereq_(1));

var _RangeController = _interopRequireDefault(_dereq_(11));

var _ReportingController = _interopRequireDefault(_dereq_(12));

var _MetricsHandlersController = _interopRequireDefault(_dereq_(10));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

/**
 * The copyright in this software is being made available under the BSD License,
 * included below. This software may be subject to other third party and contributor
 * rights, including patent rights, and no such rights are granted under this license.
 *
 * Copyright (c) 2013, Dash Industry Forum.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *  * Redistributions of source code must retain the above copyright notice, this
 *  list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright notice,
 *  this list of conditions and the following disclaimer in the documentation and/or
 *  other materials provided with the distribution.
 *  * Neither the name of Dash Industry Forum nor the names of its
 *  contributors may be used to endorse or promote products derived from this software
 *  without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS AS IS AND ANY
 *  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 *  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 *  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 *  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 *  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 *  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 *  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 */
function MetricsController(config) {
  var metricsHandlersController, reportingController, rangeController, instance;
  var context = this.context;

  function initialize(metricsEntry) {
    try {
      rangeController = (0, _RangeController.default)(context).create({
        mediaElement: config.mediaElement
      });
      rangeController.initialize(metricsEntry.Range);
      reportingController = (0, _ReportingController.default)(context).create({
        log: config.log
      });
      reportingController.initialize(metricsEntry.Reporting, rangeController);
      metricsHandlersController = (0, _MetricsHandlersController.default)(context).create({
        log: config.log,
        eventBus: config.eventBus
      });
      metricsHandlersController.initialize(metricsEntry.metrics, reportingController);
    } catch (e) {
      reset();
      throw e;
    }
  }

  function reset() {
    if (metricsHandlersController) {
      metricsHandlersController.reset();
    }

    if (reportingController) {
      reportingController.reset();
    }

    if (rangeController) {
      rangeController.reset();
    }
  }

  instance = {
    initialize: initialize,
    reset: reset
  };
  return instance;
}

MetricsController.__dashjs_factory_name = 'MetricsController';

var _default = _FactoryMaker.default.getClassFactory(MetricsController);

exports.default = _default;

},{"1":1,"10":10,"11":11,"12":12}],10:[function(_dereq_,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _MetricsHandlerFactory = _interopRequireDefault(_dereq_(13));

var _FactoryMaker = _interopRequireDefault(_dereq_(1));

var _MediaPlayerEvents = _interopRequireDefault(_dereq_(5));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

/**
 * The copyright in this software is being made available under the BSD License,
 * included below. This software may be subject to other third party and contributor
 * rights, including patent rights, and no such rights are granted under this license.
 *
 * Copyright (c) 2013, Dash Industry Forum.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *  * Redistributions of source code must retain the above copyright notice, this
 *  list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright notice,
 *  this list of conditions and the following disclaimer in the documentation and/or
 *  other materials provided with the distribution.
 *  * Neither the name of Dash Industry Forum nor the names of its
 *  contributors may be used to endorse or promote products derived from this software
 *  without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS AS IS AND ANY
 *  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 *  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 *  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 *  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 *  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 *  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 *  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 */
function MetricsHandlersController(config) {
  var handlers = [];
  var instance;
  var context = this.context;
  var eventBus = config.eventBus;
  var metricsHandlerFactory = (0, _MetricsHandlerFactory.default)(context).getInstance({
    log: config.log,
    eventBus: config.eventBus
  });

  function handle(e) {
    handlers.forEach(function (handler) {
      handler.handleNewMetric(e.metric, e.value, e.mediaType);
    });
  }

  function initialize(metrics, reportingController) {
    metrics.split(',').forEach(function (m, midx, ms) {
      var handler; // there is a bug in ISO23009-1 where the metrics attribute
      // is a comma-separated list but HttpList key can contain a
      // comma enclosed by ().

      if (m.indexOf('(') !== -1 && m.indexOf(')') === -1) {
        var nextm = ms[midx + 1];

        if (nextm && nextm.indexOf('(') === -1 && nextm.indexOf(')') !== -1) {
          m += ',' + nextm; // delete the next metric so forEach does not visit.

          delete ms[midx + 1];
        }
      }

      handler = metricsHandlerFactory.create(m, reportingController);

      if (handler) {
        handlers.push(handler);
      }
    });
    eventBus.on(_MediaPlayerEvents.default.METRIC_ADDED, handle, instance);
    eventBus.on(_MediaPlayerEvents.default.METRIC_UPDATED, handle, instance);
  }

  function reset() {
    eventBus.off(_MediaPlayerEvents.default.METRIC_ADDED, handle, instance);
    eventBus.off(_MediaPlayerEvents.default.METRIC_UPDATED, handle, instance);
    handlers.forEach(function (handler) {
      return handler.reset();
    });
    handlers = [];
  }

  instance = {
    initialize: initialize,
    reset: reset
  };
  return instance;
}

MetricsHandlersController.__dashjs_factory_name = 'MetricsHandlersController';

var _default = _FactoryMaker.default.getClassFactory(MetricsHandlersController);

exports.default = _default;

},{"1":1,"13":13,"5":5}],11:[function(_dereq_,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _FactoryMaker = _interopRequireDefault(_dereq_(1));

var _CustomTimeRanges = _interopRequireDefault(_dereq_(29));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

/**
 * The copyright in this software is being made available under the BSD License,
 * included below. This software may be subject to other third party and contributor
 * rights, including patent rights, and no such rights are granted under this license.
 *
 * Copyright (c) 2013, Dash Industry Forum.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *  * Redistributions of source code must retain the above copyright notice, this
 *  list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright notice,
 *  this list of conditions and the following disclaimer in the documentation and/or
 *  other materials provided with the distribution.
 *  * Neither the name of Dash Industry Forum nor the names of its
 *  contributors may be used to endorse or promote products derived from this software
 *  without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS AS IS AND ANY
 *  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 *  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 *  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 *  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 *  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 *  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 *  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 */
function RangeController(config) {
  var useWallClockTime = false;
  var context = this.context;
  var instance, ranges;
  var mediaElement = config.mediaElement;

  function initialize(rs) {
    if (rs && rs.length) {
      rs.forEach(function (r) {
        var start = r.starttime;
        var end = start + r.duration;
        ranges.add(start, end);
      });
      useWallClockTime = !!rs[0]._useWallClockTime;
    }
  }

  function reset() {
    ranges.clear();
  }

  function setup() {
    ranges = (0, _CustomTimeRanges.default)(context).create();
  }

  function isEnabled() {
    var numRanges = ranges.length;
    var time;

    if (!numRanges) {
      return true;
    } // When not present, DASH Metrics reporting is requested
    // for the whole duration of the content.


    time = useWallClockTime ? new Date().getTime() / 1000 : mediaElement.currentTime;

    for (var i = 0; i < numRanges; i += 1) {
      var start = ranges.start(i);
      var end = ranges.end(i);

      if (start <= time && time < end) {
        return true;
      }
    }

    return false;
  }

  instance = {
    initialize: initialize,
    reset: reset,
    isEnabled: isEnabled
  };
  setup();
  return instance;
}

RangeController.__dashjs_factory_name = 'RangeController';

var _default = _FactoryMaker.default.getClassFactory(RangeController);

exports.default = _default;

},{"1":1,"29":29}],12:[function(_dereq_,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _FactoryMaker = _interopRequireDefault(_dereq_(1));

var _ReportingFactory = _interopRequireDefault(_dereq_(18));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

/**
 * The copyright in this software is being made available under the BSD License,
 * included below. This software may be subject to other third party and contributor
 * rights, including patent rights, and no such rights are granted under this license.
 *
 * Copyright (c) 2013, Dash Industry Forum.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *  * Redistributions of source code must retain the above copyright notice, this
 *  list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright notice,
 *  this list of conditions and the following disclaimer in the documentation and/or
 *  other materials provided with the distribution.
 *  * Neither the name of Dash Industry Forum nor the names of its
 *  contributors may be used to endorse or promote products derived from this software
 *  without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS AS IS AND ANY
 *  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 *  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 *  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 *  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 *  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 *  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 *  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 */
function ReportingController(config) {
  var reporters = [];
  var instance;
  var reportingFactory = (0, _ReportingFactory.default)(this.context).getInstance({
    log: config.log
  });

  function initialize(reporting, rangeController) {
    // "if multiple Reporting elements are present, it is expected that
    // the client processes one of the recognized reporting schemes."
    // to ignore this, and support multiple Reporting per Metric,
    // simply change the 'some' below to 'forEach'
    reporting.some(function (r) {
      var reporter = reportingFactory.create(r, rangeController);

      if (reporter) {
        reporters.push(reporter);
        return true;
      }
    });
  }

  function reset() {
    reporters.forEach(function (r) {
      return r.reset();
    });
    reporters = [];
  }

  function report(type, vos) {
    reporters.forEach(function (r) {
      return r.report(type, vos);
    });
  }

  instance = {
    initialize: initialize,
    reset: reset,
    report: report
  };
  return instance;
}

ReportingController.__dashjs_factory_name = 'ReportingController';

var _default = _FactoryMaker.default.getClassFactory(ReportingController);

exports.default = _default;

},{"1":1,"18":18}],13:[function(_dereq_,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _FactoryMaker = _interopRequireDefault(_dereq_(1));

var _BufferLevelHandler = _interopRequireDefault(_dereq_(14));

var _DVBErrorsHandler = _interopRequireDefault(_dereq_(15));

var _HttpListHandler = _interopRequireDefault(_dereq_(17));

var _GenericMetricHandler = _interopRequireDefault(_dereq_(16));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

/**
 * The copyright in this software is being made available under the BSD License,
 * included below. This software may be subject to other third party and contributor
 * rights, including patent rights, and no such rights are granted under this license.
 *
 * Copyright (c) 2013, Dash Industry Forum.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *  * Redistributions of source code must retain the above copyright notice, this
 *  list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright notice,
 *  this list of conditions and the following disclaimer in the documentation and/or
 *  other materials provided with the distribution.
 *  * Neither the name of Dash Industry Forum nor the names of its
 *  contributors may be used to endorse or promote products derived from this software
 *  without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS AS IS AND ANY
 *  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 *  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 *  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 *  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 *  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 *  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 *  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 */
function MetricsHandlerFactory(config) {
  var instance;
  var log = config.log; // group 1: key, [group 3: n [, group 5: type]]

  var keyRegex = /([a-zA-Z]*)(\(([0-9]*)(\,\s*([a-zA-Z]*))?\))?/;
  var context = this.context;
  var knownFactoryProducts = {
    BufferLevel: _BufferLevelHandler.default,
    DVBErrors: _DVBErrorsHandler.default,
    HttpList: _HttpListHandler.default,
    PlayList: _GenericMetricHandler.default,
    RepSwitchList: _GenericMetricHandler.default,
    TcpList: _GenericMetricHandler.default
  };

  function create(listType, reportingController) {
    var matches = listType.match(keyRegex);
    var handler;

    if (!matches) {
      return;
    }

    try {
      handler = knownFactoryProducts[matches[1]](context).create({
        eventBus: config.eventBus
      });
      handler.initialize(matches[1], reportingController, matches[3], matches[5]);
    } catch (e) {
      handler = null;
      log("MetricsHandlerFactory: Could not create handler for type ".concat(matches[1], " with args ").concat(matches[3], ", ").concat(matches[5], " (").concat(e.message, ")"));
    }

    return handler;
  }

  function register(key, handler) {
    knownFactoryProducts[key] = handler;
  }

  function unregister(key) {
    delete knownFactoryProducts[key];
  }

  instance = {
    create: create,
    register: register,
    unregister: unregister
  };
  return instance;
}

MetricsHandlerFactory.__dashjs_factory_name = 'MetricsHandlerFactory';

var _default = _FactoryMaker.default.getSingletonFactory(MetricsHandlerFactory);

exports.default = _default;

},{"1":1,"14":14,"15":15,"16":16,"17":17}],14:[function(_dereq_,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _FactoryMaker = _interopRequireDefault(_dereq_(1));

var _HandlerHelpers = _interopRequireDefault(_dereq_(21));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

/**
 * The copyright in this software is being made available under the BSD License,
 * included below. This software may be subject to other third party and contributor
 * rights, including patent rights, and no such rights are granted under this license.
 *
 * Copyright (c) 2013, Dash Industry Forum.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *  * Redistributions of source code must retain the above copyright notice, this
 *  list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright notice,
 *  this list of conditions and the following disclaimer in the documentation and/or
 *  other materials provided with the distribution.
 *  * Neither the name of Dash Industry Forum nor the names of its
 *  contributors may be used to endorse or promote products derived from this software
 *  without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS AS IS AND ANY
 *  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 *  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 *  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 *  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 *  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 *  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 *  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 */
function BufferLevelHandler() {
  var instance, reportingController, n, name, interval, lastReportedTime;
  var context = this.context;
  var handlerHelpers = (0, _HandlerHelpers.default)(context).getInstance();
  var storedVOs = [];

  function getLowestBufferLevelVO() {
    try {
      return Object.keys(storedVOs).map(function (key) {
        return storedVOs[key];
      }).reduce(function (a, b) {
        return a.level < b.level ? a : b;
      });
    } catch (e) {
      return;
    }
  }

  function intervalCallback() {
    var vo = getLowestBufferLevelVO();

    if (vo) {
      if (lastReportedTime !== vo.t) {
        lastReportedTime = vo.t;
        reportingController.report(name, vo);
      }
    }
  }

  function initialize(basename, rc, n_ms) {
    if (rc) {
      // this will throw if n is invalid, to be
      // caught by the initialize caller.
      n = handlerHelpers.validateN(n_ms);
      reportingController = rc;
      name = handlerHelpers.reconstructFullMetricName(basename, n_ms);
      interval = setInterval(intervalCallback, n);
    }
  }

  function reset() {
    clearInterval(interval);
    interval = null;
    n = 0;
    reportingController = null;
    lastReportedTime = null;
  }

  function handleNewMetric(metric, vo, type) {
    if (metric === 'BufferLevel') {
      storedVOs[type] = vo;
    }
  }

  instance = {
    initialize: initialize,
    reset: reset,
    handleNewMetric: handleNewMetric
  };
  return instance;
}

BufferLevelHandler.__dashjs_factory_name = 'BufferLevelHandler';

var _default = _FactoryMaker.default.getClassFactory(BufferLevelHandler);

exports.default = _default;

},{"1":1,"21":21}],15:[function(_dereq_,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _FactoryMaker = _interopRequireDefault(_dereq_(1));

var _MetricsReportingEvents = _interopRequireDefault(_dereq_(7));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

/**
 * The copyright in this software is being made available under the BSD License,
 * included below. This software may be subject to other third party and contributor
 * rights, including patent rights, and no such rights are granted under this license.
 *
 * Copyright (c) 2013, Dash Industry Forum.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *  * Redistributions of source code must retain the above copyright notice, this
 *  list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright notice,
 *  this list of conditions and the following disclaimer in the documentation and/or
 *  other materials provided with the distribution.
 *  * Neither the name of Dash Industry Forum nor the names of its
 *  contributors may be used to endorse or promote products derived from this software
 *  without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS AS IS AND ANY
 *  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 *  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 *  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 *  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 *  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 *  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 *  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 */
function DVBErrorsHandler(config) {
  var instance, reportingController;
  var eventBus = config.eventBus;

  function onInitialisationComplete() {
    // we only want to report this once per call to initialize
    eventBus.off(_MetricsReportingEvents.default.METRICS_INITIALISATION_COMPLETE, onInitialisationComplete, this); // Note: A Player becoming a reporting Player is itself
    // something which is recorded by the DVBErrors metric.

    eventBus.trigger(_MetricsReportingEvents.default.BECAME_REPORTING_PLAYER);
  }

  function initialize(unused, rc) {
    if (rc) {
      reportingController = rc;
      eventBus.on(_MetricsReportingEvents.default.METRICS_INITIALISATION_COMPLETE, onInitialisationComplete, this);
    }
  }

  function reset() {
    reportingController = null;
  }

  function handleNewMetric(metric, vo) {
    // simply pass metric straight through
    if (metric === 'DVBErrors') {
      if (reportingController) {
        reportingController.report(metric, vo);
      }
    }
  }

  instance = {
    initialize: initialize,
    reset: reset,
    handleNewMetric: handleNewMetric
  };
  return instance;
}

var _default = _FactoryMaker.default.getClassFactory(DVBErrorsHandler);

exports.default = _default;

},{"1":1,"7":7}],16:[function(_dereq_,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _FactoryMaker = _interopRequireDefault(_dereq_(1));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

/**
 * The copyright in this software is being made available under the BSD License,
 * included below. This software may be subject to other third party and contributor
 * rights, including patent rights, and no such rights are granted under this license.
 *
 * Copyright (c) 2013, Dash Industry Forum.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *  * Redistributions of source code must retain the above copyright notice, this
 *  list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright notice,
 *  this list of conditions and the following disclaimer in the documentation and/or
 *  other materials provided with the distribution.
 *  * Neither the name of Dash Industry Forum nor the names of its
 *  contributors may be used to endorse or promote products derived from this software
 *  without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS AS IS AND ANY
 *  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 *  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 *  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 *  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 *  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 *  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 *  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 */
function GenericMetricHandler() {
  var instance, metricName, reportingController;

  function initialize(name, rc) {
    metricName = name;
    reportingController = rc;
  }

  function reset() {
    reportingController = null;
    metricName = undefined;
  }

  function handleNewMetric(metric, vo) {
    // simply pass metric straight through
    if (metric === metricName) {
      if (reportingController) {
        reportingController.report(metricName, vo);
      }
    }
  }

  instance = {
    initialize: initialize,
    reset: reset,
    handleNewMetric: handleNewMetric
  };
  return instance;
}

GenericMetricHandler.__dashjs_factory_name = 'GenericMetricHandler';

var _default = _FactoryMaker.default.getClassFactory(GenericMetricHandler);

exports.default = _default;

},{"1":1}],17:[function(_dereq_,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _FactoryMaker = _interopRequireDefault(_dereq_(1));

var _HandlerHelpers = _interopRequireDefault(_dereq_(21));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

/**
 * The copyright in this software is being made available under the BSD License,
 * included below. This software may be subject to other third party and contributor
 * rights, including patent rights, and no such rights are granted under this license.
 *
 * Copyright (c) 2013, Dash Industry Forum.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *  * Redistributions of source code must retain the above copyright notice, this
 *  list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright notice,
 *  this list of conditions and the following disclaimer in the documentation and/or
 *  other materials provided with the distribution.
 *  * Neither the name of Dash Industry Forum nor the names of its
 *  contributors may be used to endorse or promote products derived from this software
 *  without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS AS IS AND ANY
 *  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 *  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 *  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 *  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 *  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 *  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 *  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 */
function HttpListHandler() {
  var instance, reportingController, n, type, name, interval;
  var storedVos = [];
  var handlerHelpers = (0, _HandlerHelpers.default)(this.context).getInstance();

  function intervalCallback() {
    var vos = storedVos;

    if (vos.length) {
      if (reportingController) {
        reportingController.report(name, vos);
      }
    }

    storedVos = [];
  }

  function initialize(basename, rc, n_ms, requestType) {
    if (rc) {
      // this will throw if n is invalid, to be
      // caught by the initialize caller.
      n = handlerHelpers.validateN(n_ms);
      reportingController = rc;

      if (requestType && requestType.length) {
        type = requestType;
      }

      name = handlerHelpers.reconstructFullMetricName(basename, n_ms, requestType);
      interval = setInterval(intervalCallback, n);
    }
  }

  function reset() {
    clearInterval(interval);
    interval = null;
    n = null;
    type = null;
    storedVos = [];
    reportingController = null;
  }

  function handleNewMetric(metric, vo) {
    if (metric === 'HttpList') {
      if (!type || type === vo.type) {
        storedVos.push(vo);
      }
    }
  }

  instance = {
    initialize: initialize,
    reset: reset,
    handleNewMetric: handleNewMetric
  };
  return instance;
}

HttpListHandler.__dashjs_factory_name = 'HttpListHandler';

var _default = _FactoryMaker.default.getClassFactory(HttpListHandler);

exports.default = _default;

},{"1":1,"21":21}],18:[function(_dereq_,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _FactoryMaker = _interopRequireDefault(_dereq_(1));

var _DVBReporting = _interopRequireDefault(_dereq_(19));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

/**
 * The copyright in this software is being made available under the BSD License,
 * included below. This software may be subject to other third party and contributor
 * rights, including patent rights, and no such rights are granted under this license.
 *
 * Copyright (c) 2013, Dash Industry Forum.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *  * Redistributions of source code must retain the above copyright notice, this
 *  list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright notice,
 *  this list of conditions and the following disclaimer in the documentation and/or
 *  other materials provided with the distribution.
 *  * Neither the name of Dash Industry Forum nor the names of its
 *  contributors may be used to endorse or promote products derived from this software
 *  without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS AS IS AND ANY
 *  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 *  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 *  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 *  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 *  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 *  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 *  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 */
function ReportingFactory(config) {
  var knownReportingSchemeIdUris = {
    'urn:dvb:dash:reporting:2014': _DVBReporting.default
  };
  var context = this.context;
  var log = config.log;
  var instance;

  function create(entry, rangeController) {
    var reporting;

    try {
      reporting = knownReportingSchemeIdUris[entry.schemeIdUri](context).create();
      reporting.initialize(entry, rangeController);
    } catch (e) {
      reporting = null;
      log("ReportingFactory: could not create Reporting with schemeIdUri ".concat(entry.schemeIdUri, " (").concat(e.message, ")"));
    }

    return reporting;
  }

  function register(schemeIdUri, moduleName) {
    knownReportingSchemeIdUris[schemeIdUri] = moduleName;
  }

  function unregister(schemeIdUri) {
    delete knownReportingSchemeIdUris[schemeIdUri];
  }

  instance = {
    create: create,
    register: register,
    unregister: unregister
  };
  return instance;
}

ReportingFactory.__dashjs_factory_name = 'ReportingFactory';

var _default = _FactoryMaker.default.getSingletonFactory(ReportingFactory);

exports.default = _default;

},{"1":1,"19":19}],19:[function(_dereq_,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _FactoryMaker = _interopRequireDefault(_dereq_(1));

var _MetricSerialiser = _interopRequireDefault(_dereq_(23));

var _RNG = _interopRequireDefault(_dereq_(24));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

/**
 * The copyright in this software is being made available under the BSD License,
 * included below. This software may be subject to other third party and contributor
 * rights, including patent rights, and no such rights are granted under this license.
 *
 * Copyright (c) 2013, Dash Industry Forum.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *  * Redistributions of source code must retain the above copyright notice, this
 *  list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright notice,
 *  this list of conditions and the following disclaimer in the documentation and/or
 *  other materials provided with the distribution.
 *  * Neither the name of Dash Industry Forum nor the names of its
 *  contributors may be used to endorse or promote products derived from this software
 *  without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS AS IS AND ANY
 *  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 *  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 *  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 *  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 *  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 *  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 *  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 */
function DVBReporting() {
  var instance;
  var context = this.context;
  var metricSerialiser = (0, _MetricSerialiser.default)(context).getInstance();
  var randomNumberGenerator = (0, _RNG.default)(context).getInstance();
  var USE_DRAFT_DVB_SPEC = true;
  var isReportingPlayer = false;
  var reportingPlayerStatusDecided = false;
  var reportingUrl = null;
  var rangeController = null;
  var allowPendingRequestsToCompleteOnReset = true;
  var pendingRequests = [];

  function doGetRequest(url, successCB, failureCB) {
    var req = new XMLHttpRequest();

    var oncomplete = function oncomplete() {
      var reqIndex = pendingRequests.indexOf(req);

      if (reqIndex === -1) {
        return;
      } else {
        pendingRequests.splice(reqIndex, 1);
      }

      if (req.status >= 200 && req.status < 300) {
        if (successCB) {
          successCB();
        }
      } else {
        if (failureCB) {
          failureCB();
        }
      }
    };

    pendingRequests.push(req);

    try {
      req.open('GET', url);
      req.onloadend = oncomplete;
      req.onerror = oncomplete;
      req.send();
    } catch (e) {
      req.onerror();
    }
  }

  function report(type, vos) {
    if (!Array.isArray(vos)) {
      vos = [vos];
    } // If the Player is not a reporting Player, then the Player shall
    // not report any errors.
    // ... In addition to any time restrictions specified by a Range
    // element within the Metrics element.


    if (isReportingPlayer && rangeController.isEnabled()) {
      // This reporting mechanism operates by creating one HTTP GET
      // request for every entry in the top level list of the metric.
      vos.forEach(function (vo) {
        var url = metricSerialiser.serialise(vo); // this has been proposed for errata

        if (USE_DRAFT_DVB_SPEC && type !== 'DVBErrors') {
          url = "metricname=".concat(type, "&").concat(url);
        } // Take the value of the @reportingUrl attribute, append a
        // question mark ('?') character and then append the string
        // created in the previous step.


        url = "".concat(reportingUrl, "?").concat(url); // Make an HTTP GET request to the URL contained within the
        // string created in the previous step.

        doGetRequest(url, null, function () {
          // If the Player is unable to make the report, for
          // example because the @reportingUrl is invalid, the
          // host cannot be reached, or an HTTP status code other
          // than one in the 200 series is received, the Player
          // shall cease being a reporting Player for the
          // duration of the MPD.
          isReportingPlayer = false;
        });
      });
    }
  }

  function initialize(entry, rc) {
    var probability;
    rangeController = rc;
    reportingUrl = entry['dvb:reportingUrl']; // If a required attribute is missing, the Reporting descriptor may
    // be ignored by the Player

    if (!reportingUrl) {
      throw new Error('required parameter missing (dvb:reportingUrl)');
    } // A Player's status, as a reporting Player or not, shall remain
    // static for the duration of the MPD, regardless of MPD updates.
    // (i.e. only calling reset (or failure) changes this state)


    if (!reportingPlayerStatusDecided) {
      // NOTE: DVB spec has a typo where it incorrectly references the
      // priority attribute, which should be probability
      probability = entry['dvb:probability'] || entry['dvb:priority'] || 0; // If the @priority attribute is set to 1000, it shall be a reporting Player.
      // If the @priority attribute is missing, the Player shall not be a reporting Player.
      // For any other value of the @probability attribute, it shall decide at random whether to be a
      // reporting Player, such that the probability of being one is @probability/1000.

      if (probability && (probability === 1000 || probability / 1000 >= randomNumberGenerator.random())) {
        isReportingPlayer = true;
      }

      reportingPlayerStatusDecided = true;
    }
  }

  function reset() {
    if (!allowPendingRequestsToCompleteOnReset) {
      pendingRequests.forEach(function (req) {
        return req.abort();
      });
      pendingRequests = [];
    }

    reportingPlayerStatusDecided = false;
    isReportingPlayer = false;
    reportingUrl = null;
    rangeController = null;
  }

  instance = {
    report: report,
    initialize: initialize,
    reset: reset
  };
  return instance;
}

DVBReporting.__dashjs_factory_name = 'DVBReporting';

var _default = _FactoryMaker.default.getClassFactory(DVBReporting);

exports.default = _default;

},{"1":1,"23":23,"24":24}],20:[function(_dereq_,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _DVBErrors = _interopRequireDefault(_dereq_(25));

var _Events = _interopRequireDefault(_dereq_(3));

var _MediaPlayerEvents = _interopRequireDefault(_dereq_(5));

var _MetricsReportingEvents = _interopRequireDefault(_dereq_(7));

var _FactoryMaker = _interopRequireDefault(_dereq_(1));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

/**
 * The copyright in this software is being made available under the BSD License,
 * included below. This software may be subject to other third party and contributor
 * rights, including patent rights, and no such rights are granted under this license.
 *
 * Copyright (c) 2013, Dash Industry Forum.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *  * Redistributions of source code must retain the above copyright notice, this
 *  list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright notice,
 *  this list of conditions and the following disclaimer in the documentation and/or
 *  other materials provided with the distribution.
 *  * Neither the name of Dash Industry Forum nor the names of its
 *  contributors may be used to endorse or promote products derived from this software
 *  without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS AS IS AND ANY
 *  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 *  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 *  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 *  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 *  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 *  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 *  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 */
function DVBErrorsTranslator(config) {
  var instance;
  var eventBus = config.eventBus;
  var metricModel = config.metricsModel;
  var mpd;

  function report(vo) {
    var o = new _DVBErrors.default();

    if (!mpd) {
      return;
    }

    for (var key in vo) {
      if (vo.hasOwnProperty(key)) {
        o[key] = vo[key];
      }
    }

    if (!o.mpdurl) {
      o.mpdurl = mpd.originalUrl || mpd.url;
    }

    if (!o.terror) {
      o.terror = new Date();
    }

    metricModel.addDVBErrors(o);
  }

  function onManifestUpdate(e) {
    if (e.error) {
      return;
    }

    mpd = e.manifest;
  }

  function onServiceLocationChanged(e) {
    report({
      errorcode: _DVBErrors.default.BASE_URL_CHANGED,
      servicelocation: e.entry
    });
  }

  function onBecameReporter() {
    report({
      errorcode: _DVBErrors.default.BECAME_REPORTER
    });
  }

  function handleHttpMetric(vo) {
    if (vo.responsecode === 0 || // connection failure - unknown
    vo.responsecode >= 400 || // HTTP error status code
    vo.responsecode < 100 || // unknown status codes
    vo.responsecode >= 600) {
      // unknown status codes
      report({
        errorcode: vo.responsecode || _DVBErrors.default.CONNECTION_ERROR,
        url: vo.url,
        terror: vo.tresponse,
        servicelocation: vo._serviceLocation
      });
    }
  }

  function onMetricEvent(e) {
    switch (e.metric) {
      case 'HttpList':
        handleHttpMetric(e.value);
        break;

      default:
        break;
    }
  }

  function onPlaybackError(e) {
    var reason = e.error ? e.error.code : 0;
    var errorcode;

    switch (reason) {
      case MediaError.MEDIA_ERR_NETWORK:
        errorcode = _DVBErrors.default.CONNECTION_ERROR;
        break;

      case MediaError.MEDIA_ERR_DECODE:
        errorcode = _DVBErrors.default.CORRUPT_MEDIA_OTHER;
        break;

      default:
        return;
    }

    report({
      errorcode: errorcode
    });
  }

  function initialise() {
    eventBus.on(_Events.default.MANIFEST_UPDATED, onManifestUpdate, instance);
    eventBus.on(_Events.default.SERVICE_LOCATION_BLACKLIST_CHANGED, onServiceLocationChanged, instance);
    eventBus.on(_MediaPlayerEvents.default.METRIC_ADDED, onMetricEvent, instance);
    eventBus.on(_MediaPlayerEvents.default.METRIC_UPDATED, onMetricEvent, instance);
    eventBus.on(_MediaPlayerEvents.default.PLAYBACK_ERROR, onPlaybackError, instance);
    eventBus.on(_MetricsReportingEvents.default.BECAME_REPORTING_PLAYER, onBecameReporter, instance);
  }

  function reset() {
    eventBus.off(_Events.default.MANIFEST_UPDATED, onManifestUpdate, instance);
    eventBus.off(_Events.default.SERVICE_LOCATION_BLACKLIST_CHANGED, onServiceLocationChanged, instance);
    eventBus.off(_MediaPlayerEvents.default.METRIC_ADDED, onMetricEvent, instance);
    eventBus.off(_MediaPlayerEvents.default.METRIC_UPDATED, onMetricEvent, instance);
    eventBus.off(_MediaPlayerEvents.default.PLAYBACK_ERROR, onPlaybackError, instance);
    eventBus.off(_MetricsReportingEvents.default.BECAME_REPORTING_PLAYER, onBecameReporter, instance);
  }

  instance = {
    initialise: initialise,
    reset: reset
  };
  initialise();
  return instance;
}

DVBErrorsTranslator.__dashjs_factory_name = 'DVBErrorsTranslator';

var _default = _FactoryMaker.default.getSingletonFactory(DVBErrorsTranslator);

exports.default = _default;

},{"1":1,"25":25,"3":3,"5":5,"7":7}],21:[function(_dereq_,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _FactoryMaker = _interopRequireDefault(_dereq_(1));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

/**
 * The copyright in this software is being made available under the BSD License,
 * included below. This software may be subject to other third party and contributor
 * rights, including patent rights, and no such rights are granted under this license.
 *
 * Copyright (c) 2013, Dash Industry Forum.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *  * Redistributions of source code must retain the above copyright notice, this
 *  list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright notice,
 *  this list of conditions and the following disclaimer in the documentation and/or
 *  other materials provided with the distribution.
 *  * Neither the name of Dash Industry Forum nor the names of its
 *  contributors may be used to endorse or promote products derived from this software
 *  without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS AS IS AND ANY
 *  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 *  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 *  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 *  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 *  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 *  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 *  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 */
function HandlerHelpers() {
  return {
    reconstructFullMetricName: function reconstructFullMetricName(key, n, type) {
      var mn = key;

      if (n) {
        mn += '(' + n;

        if (type && type.length) {
          mn += ',' + type;
        }

        mn += ')';
      }

      return mn;
    },
    validateN: function validateN(n_ms) {
      if (!n_ms) {
        throw new Error('missing n');
      }

      if (isNaN(n_ms)) {
        throw new Error('n is NaN');
      } // n is a positive integer is defined to refer to the metric
      // in which the buffer level is recorded every n ms.


      if (n_ms < 0) {
        throw new Error('n must be positive');
      }

      return n_ms;
    }
  };
}

HandlerHelpers.__dashjs_factory_name = 'HandlerHelpers';

var _default = _FactoryMaker.default.getSingletonFactory(HandlerHelpers);

exports.default = _default;

},{"1":1}],22:[function(_dereq_,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _Metrics = _interopRequireDefault(_dereq_(26));

var _Range = _interopRequireDefault(_dereq_(27));

var _Reporting = _interopRequireDefault(_dereq_(28));

var _FactoryMaker = _interopRequireDefault(_dereq_(1));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function ManifestParsing(config) {
  var instance;
  var dashManifestModel = config.dashManifestModel;

  function getMetricsRangeStartTime(manifest, dynamic, range) {
    var mpd = dashManifestModel.getMpd(manifest);
    var periods;
    var presentationStartTime = 0;
    var reportingStartTime;

    if (dynamic) {
      // For services with MPD@type='dynamic', the start time is
      // indicated in wall clock time by adding the value of this
      // attribute to the value of the MPD@availabilityStartTime
      // attribute.
      presentationStartTime = mpd.availabilityStartTime.getTime() / 1000;
    } else {
      // For services with MPD@type='static', the start time is indicated
      // in Media Presentation time and is relative to the PeriodStart
      // time of the first Period in this MPD.
      periods = this.getRegularPeriods(manifest, mpd);

      if (periods.length) {
        presentationStartTime = periods[0].start;
      }
    } // When not present, DASH Metrics collection is
    // requested from the beginning of content
    // consumption.


    reportingStartTime = presentationStartTime;

    if (range && range.hasOwnProperty('starttime')) {
      reportingStartTime += range.starttime;
    }

    return reportingStartTime;
  }

  function getMetrics(manifest) {
    var metrics = [];

    if (manifest.Metrics_asArray) {
      manifest.Metrics_asArray.forEach(function (metric) {
        var metricEntry = new _Metrics.default();
        var isDynamic = dashManifestModel.getIsDynamic(manifest);

        if (metric.hasOwnProperty('metrics')) {
          metricEntry.metrics = metric.metrics;
        } else {
          //console.log("Invalid Metrics. metrics must be set. Ignoring.");
          return;
        }

        if (metric.Range_asArray) {
          metric.Range_asArray.forEach(function (range) {
            var rangeEntry = new _Range.default();
            rangeEntry.starttime = getMetricsRangeStartTime(manifest, isDynamic, range);

            if (range.hasOwnProperty('duration')) {
              rangeEntry.duration = range.duration;
            } else {
              // if not present, the value is identical to the
              // Media Presentation duration.
              rangeEntry.duration = dashManifestModel.getDuration(manifest);
            }

            rangeEntry._useWallClockTime = isDynamic;
            metricEntry.Range.push(rangeEntry);
          });
        }

        if (metric.Reporting_asArray) {
          metric.Reporting_asArray.forEach(function (reporting) {
            var reportingEntry = new _Reporting.default();

            if (reporting.hasOwnProperty('schemeIdUri')) {
              reportingEntry.schemeIdUri = reporting.schemeIdUri;
            } else {
              // Invalid Reporting. schemeIdUri must be set. Ignore.
              return;
            }

            for (var prop in reporting) {
              if (reporting.hasOwnProperty(prop)) {
                reportingEntry[prop] = reporting[prop];
              }
            }

            metricEntry.Reporting.push(reportingEntry);
          });
        } else {
          // Invalid Metrics. At least one reporting must be present. Ignore
          return;
        }

        metrics.push(metricEntry);
      });
    }

    return metrics;
  }

  instance = {
    getMetrics: getMetrics
  };
  return instance;
}

ManifestParsing.__dashjs_factory_name = 'ManifestParsing';

var _default = _FactoryMaker.default.getSingletonFactory(ManifestParsing);

exports.default = _default;

},{"1":1,"26":26,"27":27,"28":28}],23:[function(_dereq_,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _FactoryMaker = _interopRequireDefault(_dereq_(1));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

/**
 * The copyright in this software is being made available under the BSD License,
 * included below. This software may be subject to other third party and contributor
 * rights, including patent rights, and no such rights are granted under this license.
 *
 * Copyright (c) 2013, Dash Industry Forum.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *  * Redistributions of source code must retain the above copyright notice, this
 *  list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright notice,
 *  this list of conditions and the following disclaimer in the documentation and/or
 *  other materials provided with the distribution.
 *  * Neither the name of Dash Industry Forum nor the names of its
 *  contributors may be used to endorse or promote products derived from this software
 *  without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS AS IS AND ANY
 *  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 *  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 *  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 *  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 *  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 *  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 *  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 */
function MetricSerialiser() {
  // For each entry in the top level list within the metric (in the case
  // of the DVBErrors metric each entry corresponds to an "error event"
  // described in clause 10.8.4) the Player shall:
  function serialise(metric) {
    var pairs = [];
    var obj = [];
    var key, value; // Take each (key, value) pair from the metric entry and create a
    // string consisting of the name of the key, followed by an equals
    // ('=') character, followed by the string representation of the
    // value. The string representation of the value is created based
    // on the type of the value following the instructions in Table 22.

    for (key in metric) {
      if (metric.hasOwnProperty(key) && key.indexOf('_') !== 0) {
        value = metric[key]; // we want to ensure that keys still end up in the report
        // even if there is no value

        if (value === undefined || value === null) {
          value = '';
        } // DVB A168 10.12.4 Table 22


        if (Array.isArray(value)) {
          // if trace or similar is null, do not include in output
          if (!value.length) {
            continue;
          }

          obj = [];
          value.forEach(function (v) {
            var isBuiltIn = Object.prototype.toString.call(v).slice(8, -1) !== 'Object';
            obj.push(isBuiltIn ? v : serialise(v));
          });
          value = encodeURIComponent(obj.join(','));
        } else if (typeof value === 'string') {
          value = encodeURIComponent(value);
        } else if (value instanceof Date) {
          value = value.toISOString();
        } else if (typeof value === 'number') {
          value = Math.round(value);
        }

        pairs.push(key + '=' + value);
      }
    } // Concatenate the strings created in the previous step with an
    // ampersand ('&') character between each one.


    return pairs.join('&');
  }

  return {
    serialise: serialise
  };
}

MetricSerialiser.__dashjs_factory_name = 'MetricSerialiser';

var _default = _FactoryMaker.default.getSingletonFactory(MetricSerialiser);

exports.default = _default;

},{"1":1}],24:[function(_dereq_,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _FactoryMaker = _interopRequireDefault(_dereq_(1));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

/**
 * The copyright in this software is being made available under the BSD License,
 * included below. This software may be subject to other third party and contributor
 * rights, including patent rights, and no such rights are granted under this license.
 *
 * Copyright (c) 2013, Dash Industry Forum.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *  * Redistributions of source code must retain the above copyright notice, this
 *  list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright notice,
 *  this list of conditions and the following disclaimer in the documentation and/or
 *  other materials provided with the distribution.
 *  * Neither the name of Dash Industry Forum nor the names of its
 *  contributors may be used to endorse or promote products derived from this software
 *  without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS AS IS AND ANY
 *  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 *  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 *  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 *  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 *  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 *  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 *  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 */
function RNG() {
  // check whether secure random numbers are available. if not, revert to
  // using Math.random
  var crypto = window.crypto || window.msCrypto; // could just as easily use any other array type by changing line below

  var ArrayType = Uint32Array;
  var MAX_VALUE = Math.pow(2, ArrayType.BYTES_PER_ELEMENT * 8) - 1; // currently there is only one client for this code, and that only uses
  // a single random number per initialisation. may want to increase this
  // number if more consumers in the future

  var NUM_RANDOM_NUMBERS = 10;
  var randomNumbers, index, instance;

  function initialise() {
    if (crypto) {
      if (!randomNumbers) {
        randomNumbers = new ArrayType(NUM_RANDOM_NUMBERS);
      }

      crypto.getRandomValues(randomNumbers);
      index = 0;
    }
  }

  function rand(min, max) {
    var r;

    if (!min) {
      min = 0;
    }

    if (!max) {
      max = 1;
    }

    if (crypto) {
      if (index === randomNumbers.length) {
        initialise();
      }

      r = randomNumbers[index] / MAX_VALUE;
      index += 1;
    } else {
      r = Math.random();
    }

    return r * (max - min) + min;
  }

  instance = {
    random: rand
  };
  initialise();
  return instance;
}

RNG.__dashjs_factory_name = 'RNG';

var _default = _FactoryMaker.default.getSingletonFactory(RNG);

exports.default = _default;

},{"1":1}],25:[function(_dereq_,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * The copyright in this software is being made available under the BSD License,
 * included below. This software may be subject to other third party and contributor
 * rights, including patent rights, and no such rights are granted under this license.
 *
 * Copyright (c) 2013, Dash Industry Forum.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *  * Redistributions of source code must retain the above copyright notice, this
 *  list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright notice,
 *  this list of conditions and the following disclaimer in the documentation and/or
 *  other materials provided with the distribution.
 *  * Neither the name of Dash Industry Forum nor the names of its
 *  contributors may be used to endorse or promote products derived from this software
 *  without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS AS IS AND ANY
 *  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 *  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 *  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 *  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 *  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 *  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 *  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 */

/**
 * @class
 * @ignore
 */
var DVBErrors = function DVBErrors() {
  _classCallCheck(this, DVBErrors);

  this.mpdurl = null; // String - Absolute URL from which the MPD was originally
  // retrieved (MPD updates will not change this value).

  this.errorcode = null; // String - The value of errorcode depends upon the type
  // of error being reported. For an error listed in the
  // ErrorType column below the value is as described in the
  // Value column.
  //
  // ErrorType                                            Value
  // ---------                                            -----
  // HTTP error status code                               HTTP status code
  // Unknown HTTP status code                             HTTP status code
  // SSL connection failed                                "SSL" followed by SSL alert value
  // DNS resolution failed                                "C00"
  // Host unreachable                                     "C01"
  // Connection refused                                   "C02"
  // Connection error – Not otherwise specified           "C03"
  // Corrupt media – ISO BMFF container cannot be parsed  "M00"
  // Corrupt media – Not otherwise specified              "M01"
  // Changing Base URL in use due to errors               "F00"
  // Becoming an error reporting Player                   "S00"

  this.terror = null; // Real-Time - Date and time at which error occurred in UTC,
  // formatted as a combined date and time according to ISO 8601.

  this.url = null; // String - Absolute URL from which data was being requested
  // when this error occurred. If the error report is in relation
  // to corrupt media or changing BaseURL, this may be a null
  // string if the URL from which the media was obtained or
  // which led to the change of BaseURL is no longer known.

  this.ipaddress = null; // String - IP Address which the host name in "url" resolved to.
  // If the error report is in relation to corrupt media or
  // changing BaseURL, this may be a null string if the URL
  // from which the media was obtained or which led to the
  // change of BaseURL is no longer known.

  this.servicelocation = null; // String - The value of the serviceLocation field in the
  // BaseURL being used. In the event of this report indicating
  // a change of BaseURL this is the value from the BaseURL
  // being moved from.
};

DVBErrors.SSL_CONNECTION_FAILED_PREFIX = 'SSL';
DVBErrors.DNS_RESOLUTION_FAILED = 'C00';
DVBErrors.HOST_UNREACHABLE = 'C01';
DVBErrors.CONNECTION_REFUSED = 'C02';
DVBErrors.CONNECTION_ERROR = 'C03';
DVBErrors.CORRUPT_MEDIA_ISOBMFF = 'M00';
DVBErrors.CORRUPT_MEDIA_OTHER = 'M01';
DVBErrors.BASE_URL_CHANGED = 'F00';
DVBErrors.BECAME_REPORTER = 'S00';
var _default = DVBErrors;
exports.default = _default;

},{}],26:[function(_dereq_,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * The copyright in this software is being made available under the BSD License,
 * included below. This software may be subject to other third party and contributor
 * rights, including patent rights, and no such rights are granted under this license.
 *
 * Copyright (c) 2013, Dash Industry Forum.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *  * Redistributions of source code must retain the above copyright notice, this
 *  list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright notice,
 *  this list of conditions and the following disclaimer in the documentation and/or
 *  other materials provided with the distribution.
 *  * Neither the name of Dash Industry Forum nor the names of its
 *  contributors may be used to endorse or promote products derived from this software
 *  without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS AS IS AND ANY
 *  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 *  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 *  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 *  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 *  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 *  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 *  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 */

/**
 * @class
 * @ignore
 */
var Metrics = function Metrics() {
  _classCallCheck(this, Metrics);

  this.metrics = '';
  this.Range = [];
  this.Reporting = [];
};

var _default = Metrics;
exports.default = _default;

},{}],27:[function(_dereq_,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * The copyright in this software is being made available under the BSD License,
 * included below. This software may be subject to other third party and contributor
 * rights, including patent rights, and no such rights are granted under this license.
 *
 * Copyright (c) 2013, Dash Industry Forum.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *  * Redistributions of source code must retain the above copyright notice, this
 *  list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright notice,
 *  this list of conditions and the following disclaimer in the documentation and/or
 *  other materials provided with the distribution.
 *  * Neither the name of Dash Industry Forum nor the names of its
 *  contributors may be used to endorse or promote products derived from this software
 *  without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS AS IS AND ANY
 *  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 *  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 *  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 *  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 *  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 *  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 *  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 */

/**
 * @class
 * @ignore
 */
var Range = function Range() {
  _classCallCheck(this, Range);

  // as defined in ISO23009-1
  this.starttime = 0;
  this.duration = Infinity; // for internal use

  this._useWallClockTime = false;
};

var _default = Range;
exports.default = _default;

},{}],28:[function(_dereq_,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * The copyright in this software is being made available under the BSD License,
 * included below. This software may be subject to other third party and contributor
 * rights, including patent rights, and no such rights are granted under this license.
 *
 * Copyright (c) 2013, Dash Industry Forum.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *  * Redistributions of source code must retain the above copyright notice, this
 *  list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright notice,
 *  this list of conditions and the following disclaimer in the documentation and/or
 *  other materials provided with the distribution.
 *  * Neither the name of Dash Industry Forum nor the names of its
 *  contributors may be used to endorse or promote products derived from this software
 *  without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS AS IS AND ANY
 *  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 *  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 *  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 *  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 *  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 *  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 *  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 */

/**
 * @class
 * @ignore
 */
var Reporting = function Reporting() {
  _classCallCheck(this, Reporting);

  // Reporting is a DescriptorType and doesn't have any additional fields
  this.schemeIdUri = '';
  this.value = '';
};

var _default = Reporting;
exports.default = _default;

},{}],29:[function(_dereq_,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _FactoryMaker = _interopRequireDefault(_dereq_(1));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

/**
* The copyright in this software is being made available under the BSD License,
* included below. This software may be subject to other third party and contributor
* rights, including patent rights, and no such rights are granted under this license.
*
* Copyright (c) 2013, Dash Industry Forum.
* All rights reserved.
*
* Redistribution and use in source and binary forms, with or without modification,
* are permitted provided that the following conditions are met:
*  * Redistributions of source code must retain the above copyright notice, this
*  list of conditions and the following disclaimer.
*  * Redistributions in binary form must reproduce the above copyright notice,
*  this list of conditions and the following disclaimer in the documentation and/or
*  other materials provided with the distribution.
*  * Neither the name of Dash Industry Forum nor the names of its
*  contributors may be used to endorse or promote products derived from this software
*  without specific prior written permission.
*
*  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS AS IS AND ANY
*  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
*  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
*  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
*  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
*  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
*  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
*  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
*  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
*  POSSIBILITY OF SUCH DAMAGE.
*/
function CustomTimeRanges()
/*config*/
{
  var customTimeRangeArray = [];
  var length = 0;

  function add(start, end) {
    var i = 0;

    for (i = 0; i < this.customTimeRangeArray.length && start > this.customTimeRangeArray[i].start; i++) {
      ;
    }

    this.customTimeRangeArray.splice(i, 0, {
      start: start,
      end: end
    });

    for (i = 0; i < this.customTimeRangeArray.length - 1; i++) {
      if (this.mergeRanges(i, i + 1)) {
        i--;
      }
    }

    this.length = this.customTimeRangeArray.length;
  }

  function clear() {
    this.customTimeRangeArray = [];
    this.length = 0;
  }

  function remove(start, end) {
    for (var i = 0; i < this.customTimeRangeArray.length; i++) {
      if (start <= this.customTimeRangeArray[i].start && end >= this.customTimeRangeArray[i].end) {
        //      |--------------Range i-------|
        //|---------------Range to remove ---------------|
        //    or
        //|--------------Range i-------|
        //|--------------Range to remove ---------------|
        //    or
        //                 |--------------Range i-------|
        //|--------------Range to remove ---------------|
        this.customTimeRangeArray.splice(i, 1);
        i--;
      } else if (start > this.customTimeRangeArray[i].start && end < this.customTimeRangeArray[i].end) {
        //|-----------------Range i----------------|
        //        |-------Range to remove -----|
        this.customTimeRangeArray.splice(i + 1, 0, {
          start: end,
          end: this.customTimeRangeArray[i].end
        });
        this.customTimeRangeArray[i].end = start;
        break;
      } else if (start > this.customTimeRangeArray[i].start && start < this.customTimeRangeArray[i].end) {
        //|-----------Range i----------|
        //                    |---------Range to remove --------|
        //    or
        //|-----------------Range i----------------|
        //            |-------Range to remove -----|
        this.customTimeRangeArray[i].end = start;
      } else if (end > this.customTimeRangeArray[i].start && end < this.customTimeRangeArray[i].end) {
        //                     |-----------Range i----------|
        //|---------Range to remove --------|
        //            or
        //|-----------------Range i----------------|
        //|-------Range to remove -----|
        this.customTimeRangeArray[i].start = end;
      }
    }

    this.length = this.customTimeRangeArray.length;
  }

  function mergeRanges(rangeIndex1, rangeIndex2) {
    var range1 = this.customTimeRangeArray[rangeIndex1];
    var range2 = this.customTimeRangeArray[rangeIndex2];

    if (range1.start <= range2.start && range2.start <= range1.end && range1.end <= range2.end) {
      //|-----------Range1----------|
      //                    |-----------Range2----------|
      range1.end = range2.end;
      this.customTimeRangeArray.splice(rangeIndex2, 1);
      return true;
    } else if (range2.start <= range1.start && range1.start <= range2.end && range2.end <= range1.end) {
      //                |-----------Range1----------|
      //|-----------Range2----------|
      range1.start = range2.start;
      this.customTimeRangeArray.splice(rangeIndex2, 1);
      return true;
    } else if (range2.start <= range1.start && range1.start <= range2.end && range1.end <= range2.end) {
      //      |--------Range1-------|
      //|---------------Range2--------------|
      this.customTimeRangeArray.splice(rangeIndex1, 1);
      return true;
    } else if (range1.start <= range2.start && range2.start <= range1.end && range2.end <= range1.end) {
      //|-----------------Range1--------------|
      //        |-----------Range2----------|
      this.customTimeRangeArray.splice(rangeIndex2, 1);
      return true;
    }

    return false;
  }

  function start(index) {
    return this.customTimeRangeArray[index].start;
  }

  function end(index) {
    return this.customTimeRangeArray[index].end;
  }

  return {
    customTimeRangeArray: customTimeRangeArray,
    length: length,
    add: add,
    clear: clear,
    remove: remove,
    mergeRanges: mergeRanges,
    start: start,
    end: end
  };
}

CustomTimeRanges.__dashjs_factory_name = 'CustomTimeRanges';

var _default = _FactoryMaker.default.getClassFactory(CustomTimeRanges);

exports.default = _default;

},{"1":1}]},{},[6])(6)
});
//# sourceMappingURL=dash.reporting.debug.js.map
