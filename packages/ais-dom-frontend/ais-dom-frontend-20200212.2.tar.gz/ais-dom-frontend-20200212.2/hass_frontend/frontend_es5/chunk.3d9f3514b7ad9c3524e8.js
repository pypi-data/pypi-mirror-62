(self.webpackJsonp=self.webpackJsonp||[]).push([[30],{178:function(e,t,n){"use strict";n.d(t,"a",function(){return s});var r=n(192),s=function(e){return void 0===e.attributes.friendly_name?Object(r.a)(e.entity_id).replace(/_/g," "):e.attributes.friendly_name||""}},183:function(e,t,n){"use strict";n.d(t,"a",function(){return i});var r=n(118),s={alert:"hass:alert",alexa:"hass:amazon-alexa",automation:"hass:robot",calendar:"hass:calendar",camera:"hass:video",climate:"hass:thermostat",configurator:"hass:settings",conversation:"hass:text-to-speech",counter:"hass:counter",device_tracker:"hass:account",fan:"hass:fan",google_assistant:"hass:google-assistant",group:"hass:google-circles-communities",history_graph:"hass:chart-line",homeassistant:"hass:home-assistant",homekit:"hass:home-automation",image_processing:"hass:image-filter-frames",input_boolean:"hass:drawing",input_datetime:"hass:calendar-clock",input_number:"hass:ray-vertex",input_select:"hass:format-list-bulleted",input_text:"hass:textbox",light:"hass:lightbulb",mailbox:"hass:mailbox",notify:"hass:comment-alert",persistent_notification:"hass:bell",person:"hass:account",plant:"hass:flower",proximity:"hass:apple-safari",remote:"hass:remote",scene:"hass:palette",script:"hass:script-text",sensor:"hass:eye",simple_alarm:"hass:bell",sun:"hass:white-balance-sunny",switch:"hass:flash",timer:"hass:timer",updater:"hass:cloud-upload",vacuum:"hass:robot-vacuum",water_heater:"hass:thermometer",weather:"hass:weather-cloudy",weblink:"hass:open-in-new",zone:"hass:map-marker-radius"},i=function(e,t){if(e in s)return s[e];switch(e){case"alarm_control_panel":switch(t){case"armed_home":return"hass:bell-plus";case"armed_night":return"hass:bell-sleep";case"disarmed":return"hass:bell-outline";case"triggered":return"hass:bell-ring";default:return"hass:bell"}case"binary_sensor":return t&&"off"===t?"hass:radiobox-blank":"hass:checkbox-marked-circle";case"cover":return"closed"===t?"hass:window-closed":"hass:window-open";case"lock":return t&&"unlocked"===t?"hass:lock-open":"hass:lock";case"media_player":return t&&"off"!==t&&"idle"!==t?"hass:cast-connected":"hass:cast";case"zwave":switch(t){case"dead":return"hass:emoticon-dead";case"sleeping":return"hass:sleep";case"initializing":return"hass:timer-sand";default:return"hass:z-wave"}default:return console.warn("Unable to find icon for domain "+e+" ("+t+")"),r.a}}},192:function(e,t,n){"use strict";n.d(t,"a",function(){return r});var r=function(e){return e.substr(e.indexOf(".")+1)}},193:function(e,t,n){"use strict";var r=n(118),s=n(119),i=n(183),a={humidity:"hass:water-percent",illuminance:"hass:brightness-5",temperature:"hass:thermometer",pressure:"hass:gauge",power:"hass:flash",signal_strength:"hass:wifi"};n.d(t,"a",function(){return c});var o={binary_sensor:function(e){var t=e.state&&"off"===e.state;switch(e.attributes.device_class){case"battery":return t?"hass:battery":"hass:battery-outline";case"cold":return t?"hass:thermometer":"hass:snowflake";case"connectivity":return t?"hass:server-network-off":"hass:server-network";case"door":return t?"hass:door-closed":"hass:door-open";case"garage_door":return t?"hass:garage":"hass:garage-open";case"gas":case"power":case"problem":case"safety":case"smoke":return t?"hass:shield-check":"hass:alert";case"heat":return t?"hass:thermometer":"hass:fire";case"light":return t?"hass:brightness-5":"hass:brightness-7";case"lock":return t?"hass:lock":"hass:lock-open";case"moisture":return t?"hass:water-off":"hass:water";case"motion":return t?"hass:walk":"hass:run";case"occupancy":return t?"hass:home-outline":"hass:home";case"opening":return t?"hass:square":"hass:square-outline";case"plug":return t?"hass:power-plug-off":"hass:power-plug";case"presence":return t?"hass:home-outline":"hass:home";case"sound":return t?"hass:music-note-off":"hass:music-note";case"vibration":return t?"hass:crop-portrait":"hass:vibrate";case"window":return t?"hass:window-closed":"hass:window-open";default:return t?"hass:radiobox-blank":"hass:checkbox-marked-circle"}},cover:function(e){var t="closed"!==e.state;switch(e.attributes.device_class){case"garage":return t?"hass:garage-open":"hass:garage";case"door":return t?"hass:door-open":"hass:door-closed";case"shutter":return t?"hass:window-shutter-open":"hass:window-shutter";case"blind":return t?"hass:blinds-open":"hass:blinds";case"window":return t?"hass:window-open":"hass:window-closed";default:return Object(i.a)("cover",e.state)}},sensor:function(e){var t=e.attributes.device_class;if(t&&t in a)return a[t];if("battery"===t){var n=Number(e.state);if(isNaN(n))return"hass:battery-unknown";var s=10*Math.round(n/10);return s>=100?"hass:battery":s<=0?"hass:battery-alert":"hass".concat(":battery-",s)}var o=e.attributes.unit_of_measurement;return o===r.j||o===r.k?"hass:thermometer":Object(i.a)("sensor")},input_datetime:function(e){return e.attributes.has_date?e.attributes.has_time?Object(i.a)("input_datetime"):"hass:calendar":"hass:clock"}},c=function(e){if(!e)return r.a;if(e.attributes.icon)return e.attributes.icon;var t=Object(s.a)(e.entity_id);return t in o?o[t](e):Object(i.a)(t,e.state)}},205:function(e,t,n){"use strict";n.d(t,"b",function(){return r}),n.d(t,"a",function(){return s});var r=function(e,t){return e<t?-1:e>t?1:0},s=function(e,t){return r(e.toLowerCase(),t.toLowerCase())}},520:function(e,t,n){"use strict";n.d(t,"b",function(){return s}),n.d(t,"a",function(){return i});var r=n(119),s=function(e){return e.include_domains.length+e.include_entities.length+e.exclude_domains.length+e.exclude_entities.length===0},i=function(e,t,n,s){var i=new Set(e),a=new Set(t),o=new Set(n),c=new Set(s),u=i.size>0||a.size>0,l=o.size>0||c.size>0;return u||l?u&&!l?function(e){return a.has(e)||i.has(Object(r.a)(e))}:!u&&l?function(e){return!c.has(e)&&!o.has(Object(r.a)(e))}:i.size?function(e){return i.has(Object(r.a)(e))?!c.has(e):a.has(e)}:o.size?function(e){return o.has(Object(r.a)(e))?a.has(e):!c.has(e)}:function(e){return a.has(e)}:function(){return!0}}},521:function(e,t,n){"use strict";n.d(t,"a",function(){return i});var r=n(14),s=function(){return Promise.all([n.e(1),n.e(45)]).then(n.bind(null,572))},i=function(e,t){Object(r.a)(e,"show-dialog",{dialogTag:"dialog-domain-toggler",dialogImport:s,dialogParams:t})}},853:function(e,t,n){"use strict";n.r(t);var r=n(0),s=n(122),i=(n(107),n(157),n(161),n(179),n(185),n(200),n(356)),a=n(520),o=n(205),c=n(14),u=n(48),l=n(521),d=n(178),h=n(119);function f(e){return(f="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function p(){var e=O(["\n      .banner {\n        color: var(--primary-text-color);\n        background-color: var(\n          --ha-card-background,\n          var(--paper-card-background-color, white)\n        );\n        padding: 16px 8px;\n        text-align: center;\n      }\n      h1 {\n        color: var(--primary-text-color);\n        font-size: 24px;\n        letter-spacing: -0.012em;\n        margin-bottom: 0;\n        padding: 0 8px;\n      }\n      .content {\n        display: grid;\n        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));\n        grid-gap: 8px 8px;\n        padding: 8px;\n      }\n      .card-content {\n        padding-bottom: 12px;\n      }\n      state-info {\n        cursor: pointer;\n      }\n      ha-switch {\n        padding: 8px 0;\n      }\n\n      @media all and (max-width: 450px) {\n        ha-card {\n          max-width: 100%;\n        }\n      }\n    "]);return p=function(){return e},e}function m(){var e=O(["\n                  <h1>\n                    ",'\n                  </h1>\n                  <div class="content">',"</div>\n                "]);return m=function(){return e},e}function g(){var e=O(["\n                  <h1>\n                    ",'\n                  </h1>\n                  <div class="content">',"</div>\n                "]);return g=function(){return e},e}function b(){var e=O(['\n                <div class="banner">\n                  ',"\n                </div>\n              "]);return b=function(){return e},e}function y(){var e=O(['\n                <paper-icon-button\n                  slot="toolbar-icon"\n                  icon="hass:tune"\n                  @click=',"\n                ></paper-icon-button>\n              "]);return y=function(){return e},e}function v(){var e=O(["\n            selected\n          "]);return v=function(){return e},e}function w(){var e=O(['\n      <hass-subpage header="','">\n        <span slot="toolbar-icon">\n          ',"","\n        </span>\n        ","\n        ","\n          ","\n          ","\n        </div>\n      </hass-subpage>\n    "]);return w=function(){return e},e}function _(){var e=O(["\n                  <ha-switch\n                    .entityId=","\n                    .checked=","\n                    @change=","\n                  >\n                    ","\n                  </ha-switch>\n                "]);return _=function(){return e},e}function k(){var e=O(['\n        <ha-card>\n          <div class="card-content">\n            <state-info\n              .hass=',"\n              .stateObj=","\n              secondary-line\n              @click=","\n            >\n              ","\n            </state-info>\n            <ha-switch\n              .entityId=","\n              .disabled=","\n              .checked=","\n              @change=","\n            >\n              ","\n            </ha-switch>\n            ","\n          </div>\n        </ha-card>\n      "]);return k=function(){return e},e}function x(){var e=O(["\n        <hass-loading-screen></hass-loading-screen>\n      "]);return x=function(){return e},e}function O(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function j(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function E(e,t){return(E=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function S(e){var t,n=D(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:n,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function z(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function C(e){return e.decorators&&e.decorators.length}function P(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function A(e,t){var n=e[t];if(void 0!==n&&"function"!=typeof n)throw new TypeError("Expected '"+t+"' to be a function");return n}function D(e){var t=function(e,t){if("object"!==f(e)||null===e)return e;var n=e[Symbol.toPrimitive];if(void 0!==n){var r=n.call(e,t||"default");if("object"!==f(r))return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===f(t)?t:String(t)}function T(e,t,n){return(T="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,n){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=R(e)););return e}(e,t);if(r){var s=Object.getOwnPropertyDescriptor(r,t);return s.get?s.get.call(n):s.value}})(e,t,n||e)}function R(e){return(R=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}var I=function(e){return void 0===e.should_expose||e.should_expose};!function(e,t,n,r){var s=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(n){t.forEach(function(t){t.kind===n&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var n=e.prototype;["method","field"].forEach(function(r){t.forEach(function(t){var s=t.placement;if(t.kind===r&&("static"===s||"prototype"===s)){var i="static"===s?e:n;this.defineClassElement(i,t)}},this)},this)},defineClassElement:function(e,t){var n=t.descriptor;if("field"===t.kind){var r=t.initializer;n={enumerable:n.enumerable,writable:n.writable,configurable:n.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,n)},decorateClass:function(e,t){var n=[],r=[],s={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,s)},this),e.forEach(function(e){if(!C(e))return n.push(e);var t=this.decorateElement(e,s);n.push(t.element),n.push.apply(n,t.extras),r.push.apply(r,t.finishers)},this),!t)return{elements:n,finishers:r};var i=this.decorateConstructor(n,t);return r.push.apply(r,i.finishers),i.finishers=r,i},addElementPlacement:function(e,t,n){var r=t[e.placement];if(!n&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var n=[],r=[],s=e.decorators,i=s.length-1;i>=0;i--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var o=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,s[i])(o)||o);e=c.element,this.addElementPlacement(e,t),c.finisher&&r.push(c.finisher);var u=c.extras;if(u){for(var l=0;l<u.length;l++)this.addElementPlacement(u[l],t);n.push.apply(n,u)}}return{element:e,finishers:r,extras:n}},decorateConstructor:function(e,t){for(var n=[],r=t.length-1;r>=0;r--){var s=this.fromClassDescriptor(e),i=this.toClassDescriptor((0,t[r])(s)||s);if(void 0!==i.finisher&&n.push(i.finisher),void 0!==i.elements){e=i.elements;for(var a=0;a<e.length-1;a++)for(var o=a+1;o<e.length;o++)if(e[a].key===e[o].key&&e[a].placement===e[o].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:n}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var n=D(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var s=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var i={kind:t,key:n,placement:r,descriptor:Object.assign({},s)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(s,"get","The property descriptor of a field descriptor"),this.disallowProperty(s,"set","The property descriptor of a field descriptor"),this.disallowProperty(s,"value","The property descriptor of a field descriptor"),i.initializer=e.initializer),i},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),n=A(e,"finisher"),r=this.toElementDescriptors(e.extras);return{element:t,finisher:n,extras:r}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var n=A(e,"finisher"),r=this.toElementDescriptors(e.elements);return{elements:r,finisher:n}},runClassFinishers:function(e,t){for(var n=0;n<t.length;n++){var r=(0,t[n])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,n){if(void 0!==e[t])throw new TypeError(n+" can't have a ."+t+" property.")}};return e}();if(r)for(var i=0;i<r.length;i++)s=r[i](s);var a=t(function(e){s.initializeInstanceElements(e,o.elements)},n),o=s.decorateClass(function(e){for(var t=[],n=function(e){return"method"===e.kind&&e.key===i.key&&e.placement===i.placement},r=0;r<e.length;r++){var s,i=e[r];if("method"===i.kind&&(s=t.find(n)))if(P(i.descriptor)||P(s.descriptor)){if(C(i)||C(s))throw new ReferenceError("Duplicated methods ("+i.key+") can't be decorated.");s.descriptor=i.descriptor}else{if(C(i)){if(C(s))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+i.key+").");s.decorators=i.decorators}z(i,s)}else t.push(i)}return t}(a.d.map(S)),e);s.initializeClassElements(a.F,o.elements),s.runClassFinishers(a.F,o.finishers)}([Object(r.d)("cloud-google-assistant")],function(e,t){var n=function(n){function r(){var t,n,s,i;!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,r);for(var a=arguments.length,o=new Array(a),c=0;c<a;c++)o[c]=arguments[c];return s=this,n=!(i=(t=R(r)).call.apply(t,[this].concat(o)))||"object"!==f(i)&&"function"!=typeof i?j(s):i,e(j(n)),n}return function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&E(e,t)}(r,t),r}();return{F:n,d:[{kind:"field",decorators:[Object(r.g)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"cloudStatus",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"narrow",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"_entities",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"_entityConfigs",value:function(){return{}}},{kind:"field",key:"_popstateSyncAttached",value:function(){return!1}},{kind:"field",key:"_popstateReloadStatusAttached",value:function(){return!1}},{kind:"field",key:"_isInitialExposed",value:void 0},{kind:"field",key:"_getEntityFilterFunc",value:function(){return Object(s.a)(function(e){return Object(a.a)(e.include_domains,e.include_entities,e.exclude_domains,e.exclude_entities)})}},{kind:"method",key:"render",value:function(){var e=this;if(void 0===this._entities)return Object(r.f)(x());var t=Object(a.b)(this.cloudStatus.google_entities),n=this._getEntityFilterFunc(this.cloudStatus.google_entities),s=this._isInitialExposed||new Set,i=void 0===this._isInitialExposed,o=0,c=[],u=[];return this._entities.forEach(function(a){var l=e.hass.states[a.entity_id],d=e._entityConfigs[a.entity_id]||{},h=t?I(d):n(a.entity_id);h&&(o++,i&&s.add(a.entity_id)),(s.has(a.entity_id)?c:u).push(Object(r.f)(k(),e.hass,l,e._showMoreInfo,a.traits.map(function(e){return e.substr(e.lastIndexOf(".")+1)}).join(", "),a.entity_id,!t,h,e._exposeChanged,e.hass.localize("ui.panel.config.cloud.google.expose"),a.might_2fa?Object(r.f)(_(),a.entity_id,Boolean(d.disable_2fa),e._disable2FAChanged,e.hass.localize("ui.panel.config.cloud.google.disable_2FA")):""))}),i&&(this._isInitialExposed=s),Object(r.f)(w(),this.hass.localize("ui.panel.config.cloud.google.title"),o,this.narrow?"":Object(r.f)(v()),t?Object(r.f)(y(),this._openDomainToggler):"",t?"":Object(r.f)(b(),this.hass.localize("ui.panel.config.cloud.google.banner")),c.length>0?Object(r.f)(g(),this.hass.localize("ui.panel.config.cloud.google.exposed_entities"),c):"",u.length>0?Object(r.f)(m(),this.hass.localize("ui.panel.config.cloud.google.not_exposed_entities"),u):"")}},{kind:"method",key:"firstUpdated",value:function(e){T(R(n.prototype),"firstUpdated",this).call(this,e),this._fetchData()}},{kind:"method",key:"updated",value:function(e){T(R(n.prototype),"updated",this).call(this,e),e.has("cloudStatus")&&(this._entityConfigs=this.cloudStatus.prefs.google_entity_configs)}},{kind:"method",key:"_fetchData",value:function(){var e,t=this;return regeneratorRuntime.async(function(n){for(;;)switch(n.prev=n.next){case 0:return n.next=2,regeneratorRuntime.awrap(this.hass.callWS({type:"cloud/google_assistant/entities"}));case 2:(e=n.sent).sort(function(e,n){var r=t.hass.states[e.entity_id],s=t.hass.states[n.entity_id];return Object(o.b)(r?Object(d.a)(r):e.entity_id,s?Object(d.a)(s):n.entity_id)}),this._entities=e;case 5:case"end":return n.stop()}},null,this)}},{kind:"method",key:"_showMoreInfo",value:function(e){var t=e.currentTarget.stateObj.entity_id;Object(c.a)(this,"hass-more-info",{entityId:t})}},{kind:"method",key:"_exposeChanged",value:function(e){var t,n;return regeneratorRuntime.async(function(r){for(;;)switch(r.prev=r.next){case 0:return t=e.currentTarget.entityId,n=e.target.checked,r.next=4,regeneratorRuntime.awrap(this._updateExposed(t,n));case 4:case"end":return r.stop()}},null,this)}},{kind:"method",key:"_updateExposed",value:function(e,t){var n;return regeneratorRuntime.async(function(r){for(;;)switch(r.prev=r.next){case 0:if(n=I(this._entityConfigs[e]||{}),t!==n){r.next=3;break}return r.abrupt("return");case 3:return r.next=5,regeneratorRuntime.awrap(this._updateConfig(e,{should_expose:t}));case 5:this._ensureEntitySync();case 6:case"end":return r.stop()}},null,this)}},{kind:"method",key:"_disable2FAChanged",value:function(e){var t,n,r;return regeneratorRuntime.async(function(s){for(;;)switch(s.prev=s.next){case 0:if(t=e.currentTarget.entityId,n=e.target.checked,r=Boolean((this._entityConfigs[t]||{}).disable_2fa),n!==r){s.next=5;break}return s.abrupt("return");case 5:return s.next=7,regeneratorRuntime.awrap(this._updateConfig(t,{disable_2fa:n}));case 7:case"end":return s.stop()}},null,this)}},{kind:"method",key:"_updateConfig",value:function(e,t){var n;return regeneratorRuntime.async(function(r){for(;;)switch(r.prev=r.next){case 0:return r.next=2,regeneratorRuntime.awrap(Object(i.j)(this.hass,e,t));case 2:n=r.sent,this._entityConfigs=Object.assign({},this._entityConfigs,(o=n,(a=e)in(s={})?Object.defineProperty(s,a,{value:o,enumerable:!0,configurable:!0,writable:!0}):s[a]=o,s)),this._ensureStatusReload();case 5:case"end":return r.stop()}var s,a,o},null,this)}},{kind:"method",key:"_openDomainToggler",value:function(){var e=this;Object(l.a)(this,{domains:this._entities.map(function(e){return Object(h.a)(e.entity_id)}).filter(function(e,t,n){return n.indexOf(e)===t}),toggleDomain:function(t,n){e._entities.forEach(function(r){Object(h.a)(r.entity_id)===t&&e._updateExposed(r.entity_id,n)})}})}},{kind:"method",key:"_ensureStatusReload",value:function(){if(!this._popstateReloadStatusAttached){this._popstateReloadStatusAttached=!0;var e=this.parentElement;window.addEventListener("popstate",function(){return Object(c.a)(e,"ha-refresh-cloud-status")},{once:!0})}}},{kind:"method",key:"_ensureEntitySync",value:function(){var e=this;if(!this._popstateSyncAttached){this._popstateSyncAttached=!0;var t=this.parentElement;window.addEventListener("popstate",function(){Object(u.a)(t,{message:e.hass.localize("ui.panel.config.cloud.google.sync_to_google")}),Object(i.a)(e.hass)},{once:!0})}}},{kind:"get",static:!0,key:"styles",value:function(){return Object(r.c)(p())}}]}},r.a)}}]);
//# sourceMappingURL=chunk.3d9f3514b7ad9c3524e8.js.map