/*! For license information please see chunk.786f1aef13ef43a57230.js.LICENSE */
(self.webpackJsonp=self.webpackJsonp||[]).push([[140],{110:function(t,e,r){"use strict";r(3),r(111),r(43);var i=r(57),n=r(5),a=r(4);Object(n.a)({is:"paper-icon-button",_template:a.a`
    <style>
      :host {
        display: inline-block;
        position: relative;
        padding: 8px;
        outline: none;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
        cursor: pointer;
        z-index: 0;
        line-height: 1;

        width: 40px;
        height: 40px;

        /*
          NOTE: Both values are needed, since some phones require the value to
          be \`transparent\`.
        */
        -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
        -webkit-tap-highlight-color: transparent;

        /* Because of polymer/2558, this style has lower specificity than * */
        box-sizing: border-box !important;

        @apply --paper-icon-button;
      }

      :host #ink {
        color: var(--paper-icon-button-ink-color, var(--primary-text-color));
        opacity: 0.6;
      }

      :host([disabled]) {
        color: var(--paper-icon-button-disabled-text, var(--disabled-text-color));
        pointer-events: none;
        cursor: auto;

        @apply --paper-icon-button-disabled;
      }

      :host([hidden]) {
        display: none !important;
      }

      :host(:hover) {
        @apply --paper-icon-button-hover;
      }

      iron-icon {
        --iron-icon-width: 100%;
        --iron-icon-height: 100%;
      }
    </style>

    <iron-icon id="icon" src="[[src]]" icon="[[icon]]"
               alt$="[[alt]]"></iron-icon>
  `,hostAttributes:{role:"button",tabindex:"0"},behaviors:[i.a],registered:function(){this._template.setAttribute("strip-whitespace","")},properties:{src:{type:String},icon:{type:String},alt:{type:String,observer:"_altChanged"}},_altChanged:function(t,e){var r=this.getAttribute("aria-label");r&&e!=r||this.setAttribute("aria-label",t)}})},154:function(t,e){t.exports=function(t,e){var r=0,i={};t.addEventListener("message",function(e){var r=e.data;if("RPC"===r.type)if(r.id){var n=i[r.id];n&&(delete i[r.id],r.error?n[1](Object.assign(Error(r.error.message),r.error)):n[0](r.result))}else{var a=document.createEvent("Event");a.initEvent(r.method,!1,!1),a.data=r.params,t.dispatchEvent(a)}}),e.forEach(function(e){t[e]=function(){for(var n=[],a=arguments.length;a--;)n[a]=arguments[a];return new Promise(function(a,o){var s=++r;i[s]=[a,o],t.postMessage({type:"RPC",id:s,method:e,params:n})})}})}},189:function(t,e,r){"use strict";var i=r(0);const n=t=>(e,r)=>{if(e.constructor._observers){if(!e.constructor.hasOwnProperty("_observers")){const t=e.constructor._observers;e.constructor._observers=new Map,t.forEach((t,r)=>e.constructor._observers.set(r,t))}}else{e.constructor._observers=new Map;const t=e.updated;e.updated=function(e){t.call(this,e),e.forEach((t,e)=>{const r=this.constructor._observers.get(e);void 0!==r&&r.call(this,this[e],t)})}}e.constructor._observers.set(r,t)};r(76);function a(t){return{addClass:e=>{t.classList.add(e)},removeClass:e=>{t.classList.remove(e)},hasClass:e=>t.classList.contains(e)}}let o=!1;const s=()=>{},l={get passive(){return o=!0,!1}};document.addEventListener("x",s,l),document.removeEventListener("x",s);r.d(e,"a",function(){return c}),r.d(e,"c",function(){return n}),r.d(e,"b",function(){return a});class c extends i.a{createFoundation(){void 0!==this.mdcFoundation&&this.mdcFoundation.destroy(),this.mdcFoundation=new this.mdcFoundationClass(this.createAdapter()),this.mdcFoundation.init()}firstUpdated(){this.createFoundation()}}},191:function(t,e,r){"use strict";r(3),r(68),r(153);var i=r(5),n=r(4),a=r(131);const o=n.a`
  <style include="paper-spinner-styles"></style>

  <div id="spinnerContainer" class-name="[[__computeContainerClasses(active, __coolingDown)]]" on-animationend="__reset" on-webkit-animation-end="__reset">
    <div class="spinner-layer layer-1">
      <div class="circle-clipper left">
        <div class="circle"></div>
      </div>
      <div class="circle-clipper right">
        <div class="circle"></div>
      </div>
    </div>

    <div class="spinner-layer layer-2">
      <div class="circle-clipper left">
        <div class="circle"></div>
      </div>
      <div class="circle-clipper right">
        <div class="circle"></div>
      </div>
    </div>

    <div class="spinner-layer layer-3">
      <div class="circle-clipper left">
        <div class="circle"></div>
      </div>
      <div class="circle-clipper right">
        <div class="circle"></div>
      </div>
    </div>

    <div class="spinner-layer layer-4">
      <div class="circle-clipper left">
        <div class="circle"></div>
      </div>
      <div class="circle-clipper right">
        <div class="circle"></div>
      </div>
    </div>
  </div>
`;o.setAttribute("strip-whitespace",""),Object(i.a)({_template:o,is:"paper-spinner",behaviors:[a.a]})},193:function(t,e,r){"use strict";r.d(e,"b",function(){return a}),r.d(e,"a",function(){return o});r(3);var i=r(88),n=r(1);const a={hostAttributes:{role:"dialog",tabindex:"-1"},properties:{modal:{type:Boolean,value:!1},__readied:{type:Boolean,value:!1}},observers:["_modalChanged(modal, __readied)"],listeners:{tap:"_onDialogClick"},ready:function(){this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick,this.__prevNoCancelOnEscKey=this.noCancelOnEscKey,this.__prevWithBackdrop=this.withBackdrop,this.__readied=!0},_modalChanged:function(t,e){e&&(t?(this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick,this.__prevNoCancelOnEscKey=this.noCancelOnEscKey,this.__prevWithBackdrop=this.withBackdrop,this.noCancelOnOutsideClick=!0,this.noCancelOnEscKey=!0,this.withBackdrop=!0):(this.noCancelOnOutsideClick=this.noCancelOnOutsideClick&&this.__prevNoCancelOnOutsideClick,this.noCancelOnEscKey=this.noCancelOnEscKey&&this.__prevNoCancelOnEscKey,this.withBackdrop=this.withBackdrop&&this.__prevWithBackdrop))},_updateClosingReasonConfirmed:function(t){this.closingReason=this.closingReason||{},this.closingReason.confirmed=t},_onDialogClick:function(t){for(var e=Object(n.a)(t).path,r=0,i=e.indexOf(this);r<i;r++){var a=e[r];if(a.hasAttribute&&(a.hasAttribute("dialog-dismiss")||a.hasAttribute("dialog-confirm"))){this._updateClosingReasonConfirmed(a.hasAttribute("dialog-confirm")),this.close(),t.stopPropagation();break}}}},o=[i.a,a]},200:function(t,e,r){"use strict";r(3),r(47),r(43),r(48),r(87);const i=document.createElement("template");i.setAttribute("style","display: none;"),i.innerHTML='<dom-module id="paper-dialog-shared-styles">\n  <template>\n    <style>\n      :host {\n        display: block;\n        margin: 24px 40px;\n\n        background: var(--paper-dialog-background-color, var(--primary-background-color));\n        color: var(--paper-dialog-color, var(--primary-text-color));\n\n        @apply --paper-font-body1;\n        @apply --shadow-elevation-16dp;\n        @apply --paper-dialog;\n      }\n\n      :host > ::slotted(*) {\n        margin-top: 20px;\n        padding: 0 24px;\n      }\n\n      :host > ::slotted(.no-padding) {\n        padding: 0;\n      }\n\n      \n      :host > ::slotted(*:first-child) {\n        margin-top: 24px;\n      }\n\n      :host > ::slotted(*:last-child) {\n        margin-bottom: 24px;\n      }\n\n      /* In 1.x, this selector was `:host > ::content h2`. In 2.x <slot> allows\n      to select direct children only, which increases the weight of this\n      selector, so we have to re-define first-child/last-child margins below. */\n      :host > ::slotted(h2) {\n        position: relative;\n        margin: 0;\n\n        @apply --paper-font-title;\n        @apply --paper-dialog-title;\n      }\n\n      /* Apply mixin again, in case it sets margin-top. */\n      :host > ::slotted(h2:first-child) {\n        margin-top: 24px;\n        @apply --paper-dialog-title;\n      }\n\n      /* Apply mixin again, in case it sets margin-bottom. */\n      :host > ::slotted(h2:last-child) {\n        margin-bottom: 24px;\n        @apply --paper-dialog-title;\n      }\n\n      :host > ::slotted(.paper-dialog-buttons),\n      :host > ::slotted(.buttons) {\n        position: relative;\n        padding: 8px 8px 8px 24px;\n        margin: 0;\n\n        color: var(--paper-dialog-button-color, var(--primary-color));\n\n        @apply --layout-horizontal;\n        @apply --layout-end-justified;\n      }\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(i.content)},202:function(t,e,r){"use strict";r(3),r(200);var i=r(126),n=r(193),a=r(5),o=r(4);Object(a.a)({_template:o.a`
    <style include="paper-dialog-shared-styles"></style>
    <slot></slot>
`,is:"paper-dialog",behaviors:[n.a,i.a],listeners:{"neon-animation-finish":"_onNeonAnimationFinish"},_renderOpened:function(){this.cancelAnimation(),this.playAnimation("entry")},_renderClosed:function(){this.cancelAnimation(),this.playAnimation("exit")},_onNeonAnimationFinish:function(){this.opened?this._finishRenderOpened():this._finishRenderClosed()}})},206:function(t,e,r){"use strict";var i=r(17),n=r(0),a=r(65),o=r(73);class s extends n.a{constructor(){super(...arguments),this.primary=!1,this.accent=!1,this.unbounded=!1,this.disabled=!1,this.interactionNode=this}connectedCallback(){if(this.interactionNode===this){const t=this.parentNode;t instanceof HTMLElement?this.interactionNode=t:t instanceof ShadowRoot&&t.host instanceof HTMLElement&&(this.interactionNode=t.host)}super.connectedCallback()}render(){const t={"mdc-ripple-surface--primary":this.primary,"mdc-ripple-surface--accent":this.accent},{disabled:e,unbounded:r,active:i,interactionNode:s}=this,l={disabled:e,unbounded:r,interactionNode:s};return void 0!==i&&(l.active=i),n.f`
      <div .ripple="${Object(o.a)(l)}"
          class="mdc-ripple-surface ${Object(a.a)(t)}"></div>`}}Object(i.b)([Object(n.g)({type:Boolean})],s.prototype,"primary",void 0),Object(i.b)([Object(n.g)({type:Boolean})],s.prototype,"active",void 0),Object(i.b)([Object(n.g)({type:Boolean})],s.prototype,"accent",void 0),Object(i.b)([Object(n.g)({type:Boolean})],s.prototype,"unbounded",void 0),Object(i.b)([Object(n.g)({type:Boolean})],s.prototype,"disabled",void 0),Object(i.b)([Object(n.g)({attribute:!1})],s.prototype,"interactionNode",void 0);const l=n.c`@keyframes mdc-ripple-fg-radius-in{from{animation-timing-function:cubic-bezier(0.4, 0, 0.2, 1);transform:translate(var(--mdc-ripple-fg-translate-start, 0)) scale(1)}to{transform:translate(var(--mdc-ripple-fg-translate-end, 0)) scale(var(--mdc-ripple-fg-scale, 1))}}@keyframes mdc-ripple-fg-opacity-in{from{animation-timing-function:linear;opacity:0}to{opacity:var(--mdc-ripple-fg-opacity, 0)}}@keyframes mdc-ripple-fg-opacity-out{from{animation-timing-function:linear;opacity:var(--mdc-ripple-fg-opacity, 0)}to{opacity:0}}.mdc-ripple-surface{--mdc-ripple-fg-size: 0;--mdc-ripple-left: 0;--mdc-ripple-top: 0;--mdc-ripple-fg-scale: 1;--mdc-ripple-fg-translate-end: 0;--mdc-ripple-fg-translate-start: 0;-webkit-tap-highlight-color:rgba(0,0,0,0);position:relative;outline:none;overflow:hidden}.mdc-ripple-surface::before,.mdc-ripple-surface::after{position:absolute;border-radius:50%;opacity:0;pointer-events:none;content:""}.mdc-ripple-surface::before{transition:opacity 15ms linear,background-color 15ms linear;z-index:1}.mdc-ripple-surface.mdc-ripple-upgraded::before{transform:scale(var(--mdc-ripple-fg-scale, 1))}.mdc-ripple-surface.mdc-ripple-upgraded::after{top:0;left:0;transform:scale(0);transform-origin:center center}.mdc-ripple-surface.mdc-ripple-upgraded--unbounded::after{top:var(--mdc-ripple-top, 0);left:var(--mdc-ripple-left, 0)}.mdc-ripple-surface.mdc-ripple-upgraded--foreground-activation::after{animation:mdc-ripple-fg-radius-in 225ms forwards,mdc-ripple-fg-opacity-in 75ms forwards}.mdc-ripple-surface.mdc-ripple-upgraded--foreground-deactivation::after{animation:mdc-ripple-fg-opacity-out 150ms;transform:translate(var(--mdc-ripple-fg-translate-end, 0)) scale(var(--mdc-ripple-fg-scale, 1))}.mdc-ripple-surface::before,.mdc-ripple-surface::after{background-color:#000}.mdc-ripple-surface:hover::before{opacity:.04}.mdc-ripple-surface.mdc-ripple-upgraded--background-focused::before,.mdc-ripple-surface:not(.mdc-ripple-upgraded):focus::before{transition-duration:75ms;opacity:.12}.mdc-ripple-surface:not(.mdc-ripple-upgraded)::after{transition:opacity 150ms linear}.mdc-ripple-surface:not(.mdc-ripple-upgraded):active::after{transition-duration:75ms;opacity:.12}.mdc-ripple-surface.mdc-ripple-upgraded{--mdc-ripple-fg-opacity: 0.12}.mdc-ripple-surface::before,.mdc-ripple-surface::after{top:calc(50% - 100%);left:calc(50% - 100%);width:200%;height:200%}.mdc-ripple-surface.mdc-ripple-upgraded::after{width:var(--mdc-ripple-fg-size, 100%);height:var(--mdc-ripple-fg-size, 100%)}.mdc-ripple-surface[data-mdc-ripple-is-unbounded]{overflow:visible}.mdc-ripple-surface[data-mdc-ripple-is-unbounded]::before,.mdc-ripple-surface[data-mdc-ripple-is-unbounded]::after{top:calc(50% - 50%);left:calc(50% - 50%);width:100%;height:100%}.mdc-ripple-surface[data-mdc-ripple-is-unbounded].mdc-ripple-upgraded::before,.mdc-ripple-surface[data-mdc-ripple-is-unbounded].mdc-ripple-upgraded::after{top:var(--mdc-ripple-top, calc(50% - 50%));left:var(--mdc-ripple-left, calc(50% - 50%));width:var(--mdc-ripple-fg-size, 100%);height:var(--mdc-ripple-fg-size, 100%)}.mdc-ripple-surface[data-mdc-ripple-is-unbounded].mdc-ripple-upgraded::after{width:var(--mdc-ripple-fg-size, 100%);height:var(--mdc-ripple-fg-size, 100%)}.mdc-ripple-surface--primary::before,.mdc-ripple-surface--primary::after{background-color:#6200ee;background-color:var(--mdc-theme-primary, #6200ee)}.mdc-ripple-surface--primary:hover::before{opacity:.04}.mdc-ripple-surface--primary.mdc-ripple-upgraded--background-focused::before,.mdc-ripple-surface--primary:not(.mdc-ripple-upgraded):focus::before{transition-duration:75ms;opacity:.12}.mdc-ripple-surface--primary:not(.mdc-ripple-upgraded)::after{transition:opacity 150ms linear}.mdc-ripple-surface--primary:not(.mdc-ripple-upgraded):active::after{transition-duration:75ms;opacity:.12}.mdc-ripple-surface--primary.mdc-ripple-upgraded{--mdc-ripple-fg-opacity: 0.12}.mdc-ripple-surface--accent::before,.mdc-ripple-surface--accent::after{background-color:#018786;background-color:var(--mdc-theme-secondary, #018786)}.mdc-ripple-surface--accent:hover::before{opacity:.04}.mdc-ripple-surface--accent.mdc-ripple-upgraded--background-focused::before,.mdc-ripple-surface--accent:not(.mdc-ripple-upgraded):focus::before{transition-duration:75ms;opacity:.12}.mdc-ripple-surface--accent:not(.mdc-ripple-upgraded)::after{transition:opacity 150ms linear}.mdc-ripple-surface--accent:not(.mdc-ripple-upgraded):active::after{transition-duration:75ms;opacity:.12}.mdc-ripple-surface--accent.mdc-ripple-upgraded{--mdc-ripple-fg-opacity: 0.12}.mdc-ripple-surface{pointer-events:none;position:absolute;top:0;right:0;bottom:0;left:0}`;let c=class extends s{};c.styles=l,c=Object(i.b)([Object(n.d)("mwc-ripple")],c)},208:function(t,e,r){"use strict";r(3);const i=r(4).a`
/* Most common used flex styles*/
<dom-module id="iron-flex">
  <template>
    <style>
      .layout.horizontal,
      .layout.vertical {
        display: -ms-flexbox;
        display: -webkit-flex;
        display: flex;
      }

      .layout.inline {
        display: -ms-inline-flexbox;
        display: -webkit-inline-flex;
        display: inline-flex;
      }

      .layout.horizontal {
        -ms-flex-direction: row;
        -webkit-flex-direction: row;
        flex-direction: row;
      }

      .layout.vertical {
        -ms-flex-direction: column;
        -webkit-flex-direction: column;
        flex-direction: column;
      }

      .layout.wrap {
        -ms-flex-wrap: wrap;
        -webkit-flex-wrap: wrap;
        flex-wrap: wrap;
      }

      .layout.no-wrap {
        -ms-flex-wrap: nowrap;
        -webkit-flex-wrap: nowrap;
        flex-wrap: nowrap;
      }

      .layout.center,
      .layout.center-center {
        -ms-flex-align: center;
        -webkit-align-items: center;
        align-items: center;
      }

      .layout.center-justified,
      .layout.center-center {
        -ms-flex-pack: center;
        -webkit-justify-content: center;
        justify-content: center;
      }

      .flex {
        -ms-flex: 1 1 0.000000001px;
        -webkit-flex: 1;
        flex: 1;
        -webkit-flex-basis: 0.000000001px;
        flex-basis: 0.000000001px;
      }

      .flex-auto {
        -ms-flex: 1 1 auto;
        -webkit-flex: 1 1 auto;
        flex: 1 1 auto;
      }

      .flex-none {
        -ms-flex: none;
        -webkit-flex: none;
        flex: none;
      }
    </style>
  </template>
</dom-module>
/* Basic flexbox reverse styles */
<dom-module id="iron-flex-reverse">
  <template>
    <style>
      .layout.horizontal-reverse,
      .layout.vertical-reverse {
        display: -ms-flexbox;
        display: -webkit-flex;
        display: flex;
      }

      .layout.horizontal-reverse {
        -ms-flex-direction: row-reverse;
        -webkit-flex-direction: row-reverse;
        flex-direction: row-reverse;
      }

      .layout.vertical-reverse {
        -ms-flex-direction: column-reverse;
        -webkit-flex-direction: column-reverse;
        flex-direction: column-reverse;
      }

      .layout.wrap-reverse {
        -ms-flex-wrap: wrap-reverse;
        -webkit-flex-wrap: wrap-reverse;
        flex-wrap: wrap-reverse;
      }
    </style>
  </template>
</dom-module>
/* Flexbox alignment */
<dom-module id="iron-flex-alignment">
  <template>
    <style>
      /**
       * Alignment in cross axis.
       */
      .layout.start {
        -ms-flex-align: start;
        -webkit-align-items: flex-start;
        align-items: flex-start;
      }

      .layout.center,
      .layout.center-center {
        -ms-flex-align: center;
        -webkit-align-items: center;
        align-items: center;
      }

      .layout.end {
        -ms-flex-align: end;
        -webkit-align-items: flex-end;
        align-items: flex-end;
      }

      .layout.baseline {
        -ms-flex-align: baseline;
        -webkit-align-items: baseline;
        align-items: baseline;
      }

      /**
       * Alignment in main axis.
       */
      .layout.start-justified {
        -ms-flex-pack: start;
        -webkit-justify-content: flex-start;
        justify-content: flex-start;
      }

      .layout.center-justified,
      .layout.center-center {
        -ms-flex-pack: center;
        -webkit-justify-content: center;
        justify-content: center;
      }

      .layout.end-justified {
        -ms-flex-pack: end;
        -webkit-justify-content: flex-end;
        justify-content: flex-end;
      }

      .layout.around-justified {
        -ms-flex-pack: distribute;
        -webkit-justify-content: space-around;
        justify-content: space-around;
      }

      .layout.justified {
        -ms-flex-pack: justify;
        -webkit-justify-content: space-between;
        justify-content: space-between;
      }

      /**
       * Self alignment.
       */
      .self-start {
        -ms-align-self: flex-start;
        -webkit-align-self: flex-start;
        align-self: flex-start;
      }

      .self-center {
        -ms-align-self: center;
        -webkit-align-self: center;
        align-self: center;
      }

      .self-end {
        -ms-align-self: flex-end;
        -webkit-align-self: flex-end;
        align-self: flex-end;
      }

      .self-stretch {
        -ms-align-self: stretch;
        -webkit-align-self: stretch;
        align-self: stretch;
      }

      .self-baseline {
        -ms-align-self: baseline;
        -webkit-align-self: baseline;
        align-self: baseline;
      }

      /**
       * multi-line alignment in main axis.
       */
      .layout.start-aligned {
        -ms-flex-line-pack: start;  /* IE10 */
        -ms-align-content: flex-start;
        -webkit-align-content: flex-start;
        align-content: flex-start;
      }

      .layout.end-aligned {
        -ms-flex-line-pack: end;  /* IE10 */
        -ms-align-content: flex-end;
        -webkit-align-content: flex-end;
        align-content: flex-end;
      }

      .layout.center-aligned {
        -ms-flex-line-pack: center;  /* IE10 */
        -ms-align-content: center;
        -webkit-align-content: center;
        align-content: center;
      }

      .layout.between-aligned {
        -ms-flex-line-pack: justify;  /* IE10 */
        -ms-align-content: space-between;
        -webkit-align-content: space-between;
        align-content: space-between;
      }

      .layout.around-aligned {
        -ms-flex-line-pack: distribute;  /* IE10 */
        -ms-align-content: space-around;
        -webkit-align-content: space-around;
        align-content: space-around;
      }
    </style>
  </template>
</dom-module>
/* Non-flexbox positioning helper styles */
<dom-module id="iron-flex-factors">
  <template>
    <style>
      .flex,
      .flex-1 {
        -ms-flex: 1 1 0.000000001px;
        -webkit-flex: 1;
        flex: 1;
        -webkit-flex-basis: 0.000000001px;
        flex-basis: 0.000000001px;
      }

      .flex-2 {
        -ms-flex: 2;
        -webkit-flex: 2;
        flex: 2;
      }

      .flex-3 {
        -ms-flex: 3;
        -webkit-flex: 3;
        flex: 3;
      }

      .flex-4 {
        -ms-flex: 4;
        -webkit-flex: 4;
        flex: 4;
      }

      .flex-5 {
        -ms-flex: 5;
        -webkit-flex: 5;
        flex: 5;
      }

      .flex-6 {
        -ms-flex: 6;
        -webkit-flex: 6;
        flex: 6;
      }

      .flex-7 {
        -ms-flex: 7;
        -webkit-flex: 7;
        flex: 7;
      }

      .flex-8 {
        -ms-flex: 8;
        -webkit-flex: 8;
        flex: 8;
      }

      .flex-9 {
        -ms-flex: 9;
        -webkit-flex: 9;
        flex: 9;
      }

      .flex-10 {
        -ms-flex: 10;
        -webkit-flex: 10;
        flex: 10;
      }

      .flex-11 {
        -ms-flex: 11;
        -webkit-flex: 11;
        flex: 11;
      }

      .flex-12 {
        -ms-flex: 12;
        -webkit-flex: 12;
        flex: 12;
      }
    </style>
  </template>
</dom-module>
<dom-module id="iron-positioning">
  <template>
    <style>
      .block {
        display: block;
      }

      [hidden] {
        display: none !important;
      }

      .invisible {
        visibility: hidden !important;
      }

      .relative {
        position: relative;
      }

      .fit {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
      }

      body.fullbleed {
        margin: 0;
        height: 100vh;
      }

      .scroll {
        -webkit-overflow-scrolling: touch;
        overflow: auto;
      }

      /* fixed position */
      .fixed-bottom,
      .fixed-left,
      .fixed-right,
      .fixed-top {
        position: fixed;
      }

      .fixed-top {
        top: 0;
        left: 0;
        right: 0;
      }

      .fixed-right {
        top: 0;
        right: 0;
        bottom: 0;
      }

      .fixed-bottom {
        right: 0;
        bottom: 0;
        left: 0;
      }

      .fixed-left {
        top: 0;
        bottom: 0;
        left: 0;
      }
    </style>
  </template>
</dom-module>
`;i.setAttribute("style","display: none;"),document.head.appendChild(i.content)},209:function(t,e,r){"use strict";var i={},n=/d{1,4}|M{1,4}|YY(?:YY)?|S{1,3}|Do|ZZ|([HhMsDm])\1?|[aA]|"[^"]*"|'[^']*'/g,a="[^\\s]+",o=/\[([^]*?)\]/gm,s=function(){};function l(t,e){for(var r=[],i=0,n=t.length;i<n;i++)r.push(t[i].substr(0,e));return r}function c(t){return function(e,r,i){var n=i[t].indexOf(r.charAt(0).toUpperCase()+r.substr(1).toLowerCase());~n&&(e.month=n)}}function u(t,e){for(t=String(t),e=e||2;t.length<e;)t="0"+t;return t}var d=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],h=["January","February","March","April","May","June","July","August","September","October","November","December"],p=l(h,3),f=l(d,3);i.i18n={dayNamesShort:f,dayNames:d,monthNamesShort:p,monthNames:h,amPm:["am","pm"],DoFn:function(t){return t+["th","st","nd","rd"][t%10>3?0:(t-t%10!=10)*t%10]}};var m={D:function(t){return t.getDate()},DD:function(t){return u(t.getDate())},Do:function(t,e){return e.DoFn(t.getDate())},d:function(t){return t.getDay()},dd:function(t){return u(t.getDay())},ddd:function(t,e){return e.dayNamesShort[t.getDay()]},dddd:function(t,e){return e.dayNames[t.getDay()]},M:function(t){return t.getMonth()+1},MM:function(t){return u(t.getMonth()+1)},MMM:function(t,e){return e.monthNamesShort[t.getMonth()]},MMMM:function(t,e){return e.monthNames[t.getMonth()]},YY:function(t){return u(String(t.getFullYear()),4).substr(2)},YYYY:function(t){return u(t.getFullYear(),4)},h:function(t){return t.getHours()%12||12},hh:function(t){return u(t.getHours()%12||12)},H:function(t){return t.getHours()},HH:function(t){return u(t.getHours())},m:function(t){return t.getMinutes()},mm:function(t){return u(t.getMinutes())},s:function(t){return t.getSeconds()},ss:function(t){return u(t.getSeconds())},S:function(t){return Math.round(t.getMilliseconds()/100)},SS:function(t){return u(Math.round(t.getMilliseconds()/10),2)},SSS:function(t){return u(t.getMilliseconds(),3)},a:function(t,e){return t.getHours()<12?e.amPm[0]:e.amPm[1]},A:function(t,e){return t.getHours()<12?e.amPm[0].toUpperCase():e.amPm[1].toUpperCase()},ZZ:function(t){var e=t.getTimezoneOffset();return(e>0?"-":"+")+u(100*Math.floor(Math.abs(e)/60)+Math.abs(e)%60,4)}},g={D:["\\d\\d?",function(t,e){t.day=e}],Do:["\\d\\d?"+a,function(t,e){t.day=parseInt(e,10)}],M:["\\d\\d?",function(t,e){t.month=e-1}],YY:["\\d\\d?",function(t,e){var r=+(""+(new Date).getFullYear()).substr(0,2);t.year=""+(e>68?r-1:r)+e}],h:["\\d\\d?",function(t,e){t.hour=e}],m:["\\d\\d?",function(t,e){t.minute=e}],s:["\\d\\d?",function(t,e){t.second=e}],YYYY:["\\d{4}",function(t,e){t.year=e}],S:["\\d",function(t,e){t.millisecond=100*e}],SS:["\\d{2}",function(t,e){t.millisecond=10*e}],SSS:["\\d{3}",function(t,e){t.millisecond=e}],d:["\\d\\d?",s],ddd:[a,s],MMM:[a,c("monthNamesShort")],MMMM:[a,c("monthNames")],a:[a,function(t,e,r){var i=e.toLowerCase();i===r.amPm[0]?t.isPm=!1:i===r.amPm[1]&&(t.isPm=!0)}],ZZ:["[^\\s]*?[\\+\\-]\\d\\d:?\\d\\d|[^\\s]*?Z",function(t,e){var r,i=(e+"").match(/([+-]|\d\d)/gi);i&&(r=60*i[1]+parseInt(i[2],10),t.timezoneOffset="+"===i[0]?r:-r)}]};g.dd=g.d,g.dddd=g.ddd,g.DD=g.D,g.mm=g.m,g.hh=g.H=g.HH=g.h,g.MM=g.M,g.ss=g.s,g.A=g.a,i.masks={default:"ddd MMM DD YYYY HH:mm:ss",shortDate:"M/D/YY",mediumDate:"MMM D, YYYY",longDate:"MMMM D, YYYY",fullDate:"dddd, MMMM D, YYYY",shortTime:"HH:mm",mediumTime:"HH:mm:ss",longTime:"HH:mm:ss.SSS"},i.format=function(t,e,r){var a=r||i.i18n;if("number"==typeof t&&(t=new Date(t)),"[object Date]"!==Object.prototype.toString.call(t)||isNaN(t.getTime()))throw new Error("Invalid Date in fecha.format");e=i.masks[e]||e||i.masks.default;var s=[];return(e=(e=e.replace(o,function(t,e){return s.push(e),"??"})).replace(n,function(e){return e in m?m[e](t,a):e.slice(1,e.length-1)})).replace(/\?\?/g,function(){return s.shift()})},i.parse=function(t,e,r){var a=r||i.i18n;if("string"!=typeof e)throw new Error("Invalid format in fecha.parse");if(e=i.masks[e]||e,t.length>1e3)return null;var o,s={},l=[],c=(o=e,o.replace(/[|\\{()[^$+*?.-]/g,"\\$&")).replace(n,function(t){if(g[t]){var e=g[t];return l.push(e[1]),"("+e[0]+")"}return t}),u=t.match(new RegExp(c,"i"));if(!u)return null;for(var d=1;d<u.length;d++)l[d-1](s,u[d],a);var h,p=new Date;return!0===s.isPm&&null!=s.hour&&12!=+s.hour?s.hour=+s.hour+12:!1===s.isPm&&12==+s.hour&&(s.hour=0),null!=s.timezoneOffset?(s.minute=+(s.minute||0)-+s.timezoneOffset,h=new Date(Date.UTC(s.year||p.getFullYear(),s.month||0,s.day||1,s.hour||0,s.minute||0,s.second||0,s.millisecond||0))):h=new Date(s.year||p.getFullYear(),s.month||0,s.day||1,s.hour||0,s.minute||0,s.second||0,s.millisecond||0),h},e.a=i},213:function(t,e,r){"use strict";r.d(e,"a",function(){return i});const i=r(0).c`.mdc-switch__thumb-underlay{left:-18px;right:initial;top:-17px;width:48px;height:48px}[dir=rtl] .mdc-switch__thumb-underlay,.mdc-switch__thumb-underlay[dir=rtl]{left:initial;right:-18px}.mdc-switch__native-control{width:68px;height:48px}.mdc-switch{display:inline-block;position:relative;outline:none;user-select:none}.mdc-switch.mdc-switch--checked .mdc-switch__track{background-color:#018786;background-color:var(--mdc-theme-secondary, #018786)}.mdc-switch.mdc-switch--checked .mdc-switch__thumb{background-color:#018786;background-color:var(--mdc-theme-secondary, #018786);border-color:#018786;border-color:var(--mdc-theme-secondary, #018786)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__track{background-color:#000}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb{background-color:#fff;border-color:#fff}.mdc-switch__native-control{left:0;right:initial;position:absolute;top:0;margin:0;opacity:0;cursor:pointer;pointer-events:auto}[dir=rtl] .mdc-switch__native-control,.mdc-switch__native-control[dir=rtl]{left:initial;right:0}.mdc-switch__track{box-sizing:border-box;width:32px;height:14px;border:1px solid;border-radius:7px;opacity:.38;transition:opacity 90ms cubic-bezier(0.4, 0, 0.2, 1),background-color 90ms cubic-bezier(0.4, 0, 0.2, 1),border-color 90ms cubic-bezier(0.4, 0, 0.2, 1);border-color:transparent}.mdc-switch__thumb-underlay{display:flex;position:absolute;align-items:center;justify-content:center;transform:translateX(0);transition:transform 90ms cubic-bezier(0.4, 0, 0.2, 1),background-color 90ms cubic-bezier(0.4, 0, 0.2, 1),border-color 90ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-switch__thumb{box-shadow:0px 3px 1px -2px rgba(0, 0, 0, 0.2),0px 2px 2px 0px rgba(0, 0, 0, 0.14),0px 1px 5px 0px rgba(0,0,0,.12);box-sizing:border-box;width:20px;height:20px;border:10px solid;border-radius:50%;pointer-events:none;z-index:1}.mdc-switch--checked .mdc-switch__track{opacity:.54}.mdc-switch--checked .mdc-switch__thumb-underlay{transform:translateX(20px)}[dir=rtl] .mdc-switch--checked .mdc-switch__thumb-underlay,.mdc-switch--checked .mdc-switch__thumb-underlay[dir=rtl]{transform:translateX(-20px)}.mdc-switch--checked .mdc-switch__native-control{transform:translateX(-20px)}[dir=rtl] .mdc-switch--checked .mdc-switch__native-control,.mdc-switch--checked .mdc-switch__native-control[dir=rtl]{transform:translateX(20px)}.mdc-switch--disabled{opacity:.38;pointer-events:none}.mdc-switch--disabled .mdc-switch__thumb{border-width:1px}.mdc-switch--disabled .mdc-switch__native-control{cursor:default;pointer-events:none}@keyframes mdc-ripple-fg-radius-in{from{animation-timing-function:cubic-bezier(0.4, 0, 0.2, 1);transform:translate(var(--mdc-ripple-fg-translate-start, 0)) scale(1)}to{transform:translate(var(--mdc-ripple-fg-translate-end, 0)) scale(var(--mdc-ripple-fg-scale, 1))}}@keyframes mdc-ripple-fg-opacity-in{from{animation-timing-function:linear;opacity:0}to{opacity:var(--mdc-ripple-fg-opacity, 0)}}@keyframes mdc-ripple-fg-opacity-out{from{animation-timing-function:linear;opacity:var(--mdc-ripple-fg-opacity, 0)}to{opacity:0}}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb-underlay::before,.mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb-underlay::after{background-color:#9e9e9e}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb-underlay:hover::before{opacity:.08}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb-underlay.mdc-ripple-upgraded--background-focused::before,.mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb-underlay:not(.mdc-ripple-upgraded):focus::before{transition-duration:75ms;opacity:.24}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb-underlay:not(.mdc-ripple-upgraded)::after{transition:opacity 150ms linear}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb-underlay:not(.mdc-ripple-upgraded):active::after{transition-duration:75ms;opacity:.24}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb-underlay.mdc-ripple-upgraded{--mdc-ripple-fg-opacity: 0.24}.mdc-switch__thumb-underlay{--mdc-ripple-fg-size: 0;--mdc-ripple-left: 0;--mdc-ripple-top: 0;--mdc-ripple-fg-scale: 1;--mdc-ripple-fg-translate-end: 0;--mdc-ripple-fg-translate-start: 0;-webkit-tap-highlight-color:rgba(0,0,0,0)}.mdc-switch__thumb-underlay::before,.mdc-switch__thumb-underlay::after{position:absolute;border-radius:50%;opacity:0;pointer-events:none;content:""}.mdc-switch__thumb-underlay::before{transition:opacity 15ms linear,background-color 15ms linear;z-index:1}.mdc-switch__thumb-underlay.mdc-ripple-upgraded::before{transform:scale(var(--mdc-ripple-fg-scale, 1))}.mdc-switch__thumb-underlay.mdc-ripple-upgraded::after{top:0;left:0;transform:scale(0);transform-origin:center center}.mdc-switch__thumb-underlay.mdc-ripple-upgraded--unbounded::after{top:var(--mdc-ripple-top, 0);left:var(--mdc-ripple-left, 0)}.mdc-switch__thumb-underlay.mdc-ripple-upgraded--foreground-activation::after{animation:mdc-ripple-fg-radius-in 225ms forwards,mdc-ripple-fg-opacity-in 75ms forwards}.mdc-switch__thumb-underlay.mdc-ripple-upgraded--foreground-deactivation::after{animation:mdc-ripple-fg-opacity-out 150ms;transform:translate(var(--mdc-ripple-fg-translate-end, 0)) scale(var(--mdc-ripple-fg-scale, 1))}.mdc-switch__thumb-underlay::before,.mdc-switch__thumb-underlay::after{top:calc(50% - 50%);left:calc(50% - 50%);width:100%;height:100%}.mdc-switch__thumb-underlay.mdc-ripple-upgraded::before,.mdc-switch__thumb-underlay.mdc-ripple-upgraded::after{top:var(--mdc-ripple-top, calc(50% - 50%));left:var(--mdc-ripple-left, calc(50% - 50%));width:var(--mdc-ripple-fg-size, 100%);height:var(--mdc-ripple-fg-size, 100%)}.mdc-switch__thumb-underlay.mdc-ripple-upgraded::after{width:var(--mdc-ripple-fg-size, 100%);height:var(--mdc-ripple-fg-size, 100%)}.mdc-switch__thumb-underlay::before,.mdc-switch__thumb-underlay::after{background-color:#018786;background-color:var(--mdc-theme-secondary, #018786)}.mdc-switch__thumb-underlay:hover::before{opacity:.04}.mdc-switch__thumb-underlay.mdc-ripple-upgraded--background-focused::before,.mdc-switch__thumb-underlay:not(.mdc-ripple-upgraded):focus::before{transition-duration:75ms;opacity:.12}.mdc-switch__thumb-underlay:not(.mdc-ripple-upgraded)::after{transition:opacity 150ms linear}.mdc-switch__thumb-underlay:not(.mdc-ripple-upgraded):active::after{transition-duration:75ms;opacity:.12}.mdc-switch__thumb-underlay.mdc-ripple-upgraded{--mdc-ripple-fg-opacity: 0.12}:host{outline:none}`},215:function(t,e,r){"use strict";r.d(e,"a",function(){return n});var i=r(189);r.d(e,"b",function(){return i.b}),r.d(e,"c",function(){return i.c});class n extends i.a{createRenderRoot(){return this.attachShadow({mode:"open",delegatesFocus:!0})}click(){this.formElement&&(this.formElement.focus(),this.formElement.click())}setAriaLabel(t){this.formElement&&this.formElement.setAttribute("aria-label",t)}firstUpdated(){super.firstUpdated(),this.mdcRoot.addEventListener("change",t=>{this.dispatchEvent(new Event("change",t))})}}},225:function(t,e,r){"use strict";r.d(e,"a",function(){return a});var i=r(9);const n=new WeakMap,a=Object(i.f)(t=>e=>{if(!(e instanceof i.a)||e instanceof i.c||"style"!==e.committer.name||e.committer.parts.length>1)throw new Error("The `styleMap` directive must be used in the style attribute and must be the only part in the attribute.");const{committer:r}=e,{style:a}=r.element;n.has(e)||(a.cssText=r.strings.join(" "));const o=n.get(e);for(const i in o)i in t||(-1===i.indexOf("-")?a[i]=null:a.removeProperty(i));for(const i in t)-1===i.indexOf("-")?a[i]=t[i]:a.setProperty(i,t[i]);n.set(e,t)})},250:function(t,e,r){"use strict";var i=r(17),n=r(0),a=r(215),o=r(73),s=r(75),l={CHECKED:"mdc-switch--checked",DISABLED:"mdc-switch--disabled"},c={ARIA_CHECKED_ATTR:"aria-checked",NATIVE_CONTROL_SELECTOR:".mdc-switch__native-control",RIPPLE_SURFACE_SELECTOR:".mdc-switch__thumb-underlay"},u=function(t){function e(r){return t.call(this,i.a({},e.defaultAdapter,r))||this}return i.c(e,t),Object.defineProperty(e,"strings",{get:function(){return c},enumerable:!0,configurable:!0}),Object.defineProperty(e,"cssClasses",{get:function(){return l},enumerable:!0,configurable:!0}),Object.defineProperty(e,"defaultAdapter",{get:function(){return{addClass:function(){},removeClass:function(){},setNativeControlChecked:function(){},setNativeControlDisabled:function(){},setNativeControlAttr:function(){}}},enumerable:!0,configurable:!0}),e.prototype.setChecked=function(t){this.adapter_.setNativeControlChecked(t),this.updateAriaChecked_(t),this.updateCheckedStyling_(t)},e.prototype.setDisabled=function(t){this.adapter_.setNativeControlDisabled(t),t?this.adapter_.addClass(l.DISABLED):this.adapter_.removeClass(l.DISABLED)},e.prototype.handleChange=function(t){var e=t.target;this.updateAriaChecked_(e.checked),this.updateCheckedStyling_(e.checked)},e.prototype.updateCheckedStyling_=function(t){t?this.adapter_.addClass(l.CHECKED):this.adapter_.removeClass(l.CHECKED)},e.prototype.updateAriaChecked_=function(t){this.adapter_.setNativeControlAttr(c.ARIA_CHECKED_ATTR,""+!!t)},e}(s.a);class d extends a.a{constructor(){super(...arguments),this.checked=!1,this.disabled=!1,this.mdcFoundationClass=u}_changeHandler(t){this.mdcFoundation.handleChange(t),this.checked=this.formElement.checked}createAdapter(){return Object.assign(Object.assign({},Object(a.b)(this.mdcRoot)),{setNativeControlChecked:t=>{this.formElement.checked=t},setNativeControlDisabled:t=>{this.formElement.disabled=t},setNativeControlAttr:(t,e)=>{this.formElement.setAttribute(t,e)}})}get ripple(){return this.rippleNode.ripple}render(){return n.f`
      <div class="mdc-switch">
        <div class="mdc-switch__track"></div>
        <div class="mdc-switch__thumb-underlay" .ripple="${Object(o.a)({interactionNode:this})}">
          <div class="mdc-switch__thumb">
            <input
              type="checkbox"
              id="basic-switch"
              class="mdc-switch__native-control"
              role="switch"
              @change="${this._changeHandler}">
          </div>
        </div>
      </div>
      <slot></slot>`}}Object(i.b)([Object(n.g)({type:Boolean}),Object(a.c)(function(t){this.mdcFoundation.setChecked(t)})],d.prototype,"checked",void 0),Object(i.b)([Object(n.g)({type:Boolean}),Object(a.c)(function(t){this.mdcFoundation.setDisabled(t)})],d.prototype,"disabled",void 0),Object(i.b)([Object(n.h)(".mdc-switch")],d.prototype,"mdcRoot",void 0),Object(i.b)([Object(n.h)("input")],d.prototype,"formElement",void 0),Object(i.b)([Object(n.h)(".mdc-switch__thumb-underlay")],d.prototype,"rippleNode",void 0);var h=r(213);let p=class extends d{};p.styles=h.a,p=Object(i.b)([Object(n.d)("mwc-switch")],p)},260:function(t,e,r){"use strict";r(3),r(47);var i=r(34),n=r(61),a=r(5),o=r(1),s=r(4);Object(a.a)({_template:s.a`
    <style>
      :host {
        display: inline-block;
        position: relative;
        width: 400px;
        border: 1px solid;
        padding: 2px;
        -moz-appearance: textarea;
        -webkit-appearance: textarea;
        overflow: hidden;
      }

      .mirror-text {
        visibility: hidden;
        word-wrap: break-word;
        @apply --iron-autogrow-textarea;
      }

      .fit {
        @apply --layout-fit;
      }

      textarea {
        position: relative;
        outline: none;
        border: none;
        resize: none;
        background: inherit;
        color: inherit;
        /* see comments in template */
        width: 100%;
        height: 100%;
        font-size: inherit;
        font-family: inherit;
        line-height: inherit;
        text-align: inherit;
        @apply --iron-autogrow-textarea;
      }

      textarea::-webkit-input-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea:-moz-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea::-moz-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea:-ms-input-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }
    </style>

    <!-- the mirror sizes the input/textarea so it grows with typing -->
    <!-- use &#160; instead &nbsp; of to allow this element to be used in XHTML -->
    <div id="mirror" class="mirror-text" aria-hidden="true">&nbsp;</div>

    <!-- size the input/textarea with a div, because the textarea has intrinsic size in ff -->
    <div class="textarea-container fit">
      <textarea id="textarea" name\$="[[name]]" aria-label\$="[[label]]" autocomplete\$="[[autocomplete]]" autofocus\$="[[autofocus]]" inputmode\$="[[inputmode]]" placeholder\$="[[placeholder]]" readonly\$="[[readonly]]" required\$="[[required]]" disabled\$="[[disabled]]" rows\$="[[rows]]" minlength\$="[[minlength]]" maxlength\$="[[maxlength]]"></textarea>
    </div>
`,is:"iron-autogrow-textarea",behaviors:[n.a,i.a],properties:{value:{observer:"_valueChanged",type:String,notify:!0},bindValue:{observer:"_bindValueChanged",type:String,notify:!0},rows:{type:Number,value:1,observer:"_updateCached"},maxRows:{type:Number,value:0,observer:"_updateCached"},autocomplete:{type:String,value:"off"},autofocus:{type:Boolean,value:!1},inputmode:{type:String},placeholder:{type:String},readonly:{type:String},required:{type:Boolean},minlength:{type:Number},maxlength:{type:Number},label:{type:String}},listeners:{input:"_onInput"},get textarea(){return this.$.textarea},get selectionStart(){return this.$.textarea.selectionStart},get selectionEnd(){return this.$.textarea.selectionEnd},set selectionStart(t){this.$.textarea.selectionStart=t},set selectionEnd(t){this.$.textarea.selectionEnd=t},attached:function(){navigator.userAgent.match(/iP(?:[oa]d|hone)/)&&(this.$.textarea.style.marginLeft="-3px")},validate:function(){var t=this.$.textarea.validity.valid;return t&&(this.required&&""===this.value?t=!1:this.hasValidator()&&(t=n.a.validate.call(this,this.value))),this.invalid=!t,this.fire("iron-input-validate"),t},_bindValueChanged:function(t){this.value=t},_valueChanged:function(t){var e=this.textarea;e&&(e.value!==t&&(e.value=t||0===t?t:""),this.bindValue=t,this.$.mirror.innerHTML=this._valueForMirror(),this.fire("bind-value-changed",{value:this.bindValue}))},_onInput:function(t){var e=Object(o.a)(t).path;this.value=e?e[0].value:t.target.value},_constrain:function(t){var e;for(t=t||[""],e=this.maxRows>0&&t.length>this.maxRows?t.slice(0,this.maxRows):t.slice(0);this.rows>0&&e.length<this.rows;)e.push("");return e.join("<br/>")+"&#160;"},_valueForMirror:function(){var t=this.textarea;if(t)return this.tokens=t&&t.value?t.value.replace(/&/gm,"&amp;").replace(/"/gm,"&quot;").replace(/'/gm,"&#39;").replace(/</gm,"&lt;").replace(/>/gm,"&gt;").split("\n"):[""],this._constrain(this.tokens)},_updateCached:function(){this.$.mirror.innerHTML=this._constrain(this.tokens)}});r(115),r(116),r(117);var l=r(60),c=r(96);Object(a.a)({_template:s.a`
    <style>
      :host {
        display: block;
      }

      :host([hidden]) {
        display: none !important;
      }

      label {
        pointer-events: none;
      }
    </style>

    <paper-input-container no-label-float$="[[noLabelFloat]]" always-float-label="[[_computeAlwaysFloatLabel(alwaysFloatLabel,placeholder)]]" auto-validate$="[[autoValidate]]" disabled$="[[disabled]]" invalid="[[invalid]]">

      <label hidden$="[[!label]]" aria-hidden="true" for$="[[_inputId]]" slot="label">[[label]]</label>

      <iron-autogrow-textarea class="paper-input-input" slot="input" id$="[[_inputId]]" aria-labelledby$="[[_ariaLabelledBy]]" aria-describedby$="[[_ariaDescribedBy]]" bind-value="{{value}}" invalid="{{invalid}}" validator$="[[validator]]" disabled$="[[disabled]]" autocomplete$="[[autocomplete]]" autofocus$="[[autofocus]]" inputmode$="[[inputmode]]" name$="[[name]]" placeholder$="[[placeholder]]" readonly$="[[readonly]]" required$="[[required]]" minlength$="[[minlength]]" maxlength$="[[maxlength]]" autocapitalize$="[[autocapitalize]]" rows$="[[rows]]" max-rows$="[[maxRows]]" on-change="_onChange"></iron-autogrow-textarea>

      <template is="dom-if" if="[[errorMessage]]">
        <paper-input-error aria-live="assertive" slot="add-on">[[errorMessage]]</paper-input-error>
      </template>

      <template is="dom-if" if="[[charCounter]]">
        <paper-input-char-counter slot="add-on"></paper-input-char-counter>
      </template>

    </paper-input-container>
`,is:"paper-textarea",behaviors:[c.a,l.a],properties:{_ariaLabelledBy:{observer:"_ariaLabelledByChanged",type:String},_ariaDescribedBy:{observer:"_ariaDescribedByChanged",type:String},value:{type:String},rows:{type:Number,value:1},maxRows:{type:Number,value:0}},get selectionStart(){return this.$.input.textarea.selectionStart},set selectionStart(t){this.$.input.textarea.selectionStart=t},get selectionEnd(){return this.$.input.textarea.selectionEnd},set selectionEnd(t){this.$.input.textarea.selectionEnd=t},_ariaLabelledByChanged:function(t){this._focusableElement.setAttribute("aria-labelledby",t)},_ariaDescribedByChanged:function(t){this._focusableElement.setAttribute("aria-describedby",t)},get _focusableElement(){return this.inputElement.textarea}})},326:function(t,e,r){"use strict";r(3);var i=r(5),n=r(4),a=r(19);Object(i.a)({_template:n.a`
    <style>
      :host {
        display: inline-block;
        overflow: hidden;
        position: relative;
      }

      #baseURIAnchor {
        display: none;
      }

      #sizedImgDiv {
        position: absolute;
        top: 0px;
        right: 0px;
        bottom: 0px;
        left: 0px;

        display: none;
      }

      #img {
        display: block;
        width: var(--iron-image-width, auto);
        height: var(--iron-image-height, auto);
      }

      :host([sizing]) #sizedImgDiv {
        display: block;
      }

      :host([sizing]) #img {
        display: none;
      }

      #placeholder {
        position: absolute;
        top: 0px;
        right: 0px;
        bottom: 0px;
        left: 0px;

        background-color: inherit;
        opacity: 1;

        @apply --iron-image-placeholder;
      }

      #placeholder.faded-out {
        transition: opacity 0.5s linear;
        opacity: 0;
      }
    </style>

    <a id="baseURIAnchor" href="#"></a>
    <div id="sizedImgDiv" role="img" hidden$="[[_computeImgDivHidden(sizing)]]" aria-hidden$="[[_computeImgDivARIAHidden(alt)]]" aria-label$="[[_computeImgDivARIALabel(alt, src)]]"></div>
    <img id="img" alt$="[[alt]]" hidden$="[[_computeImgHidden(sizing)]]" crossorigin$="[[crossorigin]]" on-load="_imgOnLoad" on-error="_imgOnError">
    <div id="placeholder" hidden$="[[_computePlaceholderHidden(preload, fade, loading, loaded)]]" class$="[[_computePlaceholderClassName(preload, fade, loading, loaded)]]"></div>
`,is:"iron-image",properties:{src:{type:String,value:""},alt:{type:String,value:null},crossorigin:{type:String,value:null},preventLoad:{type:Boolean,value:!1},sizing:{type:String,value:null,reflectToAttribute:!0},position:{type:String,value:"center"},preload:{type:Boolean,value:!1},placeholder:{type:String,value:null,observer:"_placeholderChanged"},fade:{type:Boolean,value:!1},loaded:{notify:!0,readOnly:!0,type:Boolean,value:!1},loading:{notify:!0,readOnly:!0,type:Boolean,value:!1},error:{notify:!0,readOnly:!0,type:Boolean,value:!1},width:{observer:"_widthChanged",type:Number,value:null},height:{observer:"_heightChanged",type:Number,value:null}},observers:["_transformChanged(sizing, position)","_loadStateObserver(src, preventLoad)"],created:function(){this._resolvedSrc=""},_imgOnLoad:function(){this.$.img.src===this._resolveSrc(this.src)&&(this._setLoading(!1),this._setLoaded(!0),this._setError(!1))},_imgOnError:function(){this.$.img.src===this._resolveSrc(this.src)&&(this.$.img.removeAttribute("src"),this.$.sizedImgDiv.style.backgroundImage="",this._setLoading(!1),this._setLoaded(!1),this._setError(!0))},_computePlaceholderHidden:function(){return!this.preload||!this.fade&&!this.loading&&this.loaded},_computePlaceholderClassName:function(){return this.preload&&this.fade&&!this.loading&&this.loaded?"faded-out":""},_computeImgDivHidden:function(){return!this.sizing},_computeImgDivARIAHidden:function(){return""===this.alt?"true":void 0},_computeImgDivARIALabel:function(){return null!==this.alt?this.alt:""===this.src?"":this._resolveSrc(this.src).replace(/[?|#].*/g,"").split("/").pop()},_computeImgHidden:function(){return!!this.sizing},_widthChanged:function(){this.style.width=isNaN(this.width)?this.width:this.width+"px"},_heightChanged:function(){this.style.height=isNaN(this.height)?this.height:this.height+"px"},_loadStateObserver:function(t,e){var r=this._resolveSrc(t);r!==this._resolvedSrc&&(this._resolvedSrc="",this.$.img.removeAttribute("src"),this.$.sizedImgDiv.style.backgroundImage="",""===t||e?(this._setLoading(!1),this._setLoaded(!1),this._setError(!1)):(this._resolvedSrc=r,this.$.img.src=this._resolvedSrc,this.$.sizedImgDiv.style.backgroundImage='url("'+this._resolvedSrc+'")',this._setLoading(!0),this._setLoaded(!1),this._setError(!1)))},_placeholderChanged:function(){this.$.placeholder.style.backgroundImage=this.placeholder?'url("'+this.placeholder+'")':""},_transformChanged:function(){var t=this.$.sizedImgDiv.style,e=this.$.placeholder.style;t.backgroundSize=e.backgroundSize=this.sizing,t.backgroundPosition=e.backgroundPosition=this.sizing?this.position:"",t.backgroundRepeat=e.backgroundRepeat=this.sizing?"no-repeat":""},_resolveSrc:function(t){var e=Object(a.c)(t,this.$.baseURIAnchor.href);return e.length>=2&&"/"===e[0]&&"/"!==e[1]&&(e=(location.origin||location.protocol+"//"+location.host)+e),e}})},368:function(t,e,r){"use strict";function i(t){var e=/^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(t);return null===e?null:[e[1],e[2],e[3]].map(function(t){return parseInt(t,16)})}function n(t,e,r){return e/=255,r/=255,t=(t/=255)>.04045?Math.pow((t+.005)/1.055,2.4):t/12.92,e=e>.04045?Math.pow((e+.005)/1.055,2.4):e/12.92,r=r>.04045?Math.pow((r+.005)/1.055,2.4):r/12.92,[.4124*(t*=100)+.3576*(e*=100)+.1805*(r*=100),.2126*t+.7152*e+.0722*r,.0193*t+.1192*e+.9505*r]}function a(t,e,r){return e/=100,r/=108.883,t=(t/=95.047)>.008856?Math.pow(t,1/3):7.787*t+16/116,[116*(e=e>.008856?Math.pow(e,1/3):7.787*e+16/116)-16,500*(t-e),200*(e-(r=r>.008856?Math.pow(r,1/3):7.787*r+16/116))]}function o(t,e,r){var i=n(t,e,r);return a(i[0],i[1],i[2])}function s(t,e){var r=t[0],i=t[1],n=t[2],a=e[0],o=e[1],s=e[2],l=r-a,c=i-o,u=n-s,d=Math.sqrt(i*i+n*n),h=a-r,p=Math.sqrt(o*o+s*s)-d,f=Math.sqrt(l*l+c*c+u*u),m=Math.sqrt(f)>Math.sqrt(Math.abs(h))+Math.sqrt(Math.abs(p))?Math.sqrt(f*f-h*h-p*p):0;return h/=1,p/=1*(1+.045*d),m/=1*(1+.015*d),Math.sqrt(h*h+p*p+m*m)}function l(t,e){return s(o.apply(void 0,t),o.apply(void 0,e))}Object.defineProperty(e,"__esModule",{value:!0}),e.DELTAE94_DIFF_STATUS={NA:0,PERFECT:1,CLOSE:2,GOOD:10,SIMILAR:50},e.SIGBITS=5,e.RSHIFT=8-e.SIGBITS,e.defer=function(){var t,e,r=new Promise(function(r,i){t=r,e=i});return{resolve:t,reject:e,promise:r}},e.hexToRgb=i,e.rgbToHex=function(t,e,r){return"#"+((1<<24)+(t<<16)+(e<<8)+r).toString(16).slice(1,7)},e.rgbToHsl=function(t,e,r){t/=255,e/=255,r/=255;var i,n,a=Math.max(t,e,r),o=Math.min(t,e,r),s=(a+o)/2;if(a===o)i=n=0;else{var l=a-o;switch(n=s>.5?l/(2-a-o):l/(a+o),a){case t:i=(e-r)/l+(e<r?6:0);break;case e:i=(r-t)/l+2;break;case r:i=(t-e)/l+4}i/=6}return[i,n,s]},e.hslToRgb=function(t,e,r){var i,n,a;function o(t,e,r){return r<0&&(r+=1),r>1&&(r-=1),r<1/6?t+6*(e-t)*r:r<.5?e:r<2/3?t+(e-t)*(2/3-r)*6:t}if(0===e)i=n=a=r;else{var s=r<.5?r*(1+e):r+e-r*e,l=2*r-s;i=o(l,s,t+1/3),n=o(l,s,t),a=o(l,s,t-1/3)}return[255*i,255*n,255*a]},e.rgbToXyz=n,e.xyzToCIELab=a,e.rgbToCIELab=o,e.deltaE94=s,e.rgbDiff=l,e.hexDiff=function(t,e){return l(i(t),i(e))},e.getColorDiffStatus=function(t){return t<e.DELTAE94_DIFF_STATUS.NA?"N/A":t<=e.DELTAE94_DIFF_STATUS.PERFECT?"Perfect":t<=e.DELTAE94_DIFF_STATUS.CLOSE?"Close":t<=e.DELTAE94_DIFF_STATUS.GOOD?"Good":t<e.DELTAE94_DIFF_STATUS.SIMILAR?"Similar":"Wrong"},e.getColorIndex=function(t,r,i){return(t<<2*e.SIGBITS)+(r<<e.SIGBITS)+i}},410:function(t,e,r){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var i=r(368),n=r(604),a=function(){function t(t,e){this._rgb=t,this._population=e}return t.applyFilter=function(t,e){return"function"==typeof e?n(t,function(t){var r=t.r,i=t.g,n=t.b;return e(r,i,n,255)}):t},Object.defineProperty(t.prototype,"r",{get:function(){return this._rgb[0]},enumerable:!0,configurable:!0}),Object.defineProperty(t.prototype,"g",{get:function(){return this._rgb[1]},enumerable:!0,configurable:!0}),Object.defineProperty(t.prototype,"b",{get:function(){return this._rgb[2]},enumerable:!0,configurable:!0}),Object.defineProperty(t.prototype,"rgb",{get:function(){return this._rgb},enumerable:!0,configurable:!0}),Object.defineProperty(t.prototype,"hsl",{get:function(){if(!this._hsl){var t=this._rgb,e=t[0],r=t[1],n=t[2];this._hsl=i.rgbToHsl(e,r,n)}return this._hsl},enumerable:!0,configurable:!0}),Object.defineProperty(t.prototype,"hex",{get:function(){if(!this._hex){var t=this._rgb,e=t[0],r=t[1],n=t[2];this._hex=i.rgbToHex(e,r,n)}return this._hex},enumerable:!0,configurable:!0}),Object.defineProperty(t.prototype,"population",{get:function(){return this._population},enumerable:!0,configurable:!0}),t.prototype.toJSON=function(){return{rgb:this.rgb,population:this.population}},t.prototype.getRgb=function(){return this._rgb},t.prototype.getHsl=function(){return this.hsl},t.prototype.getPopulation=function(){return this._population},t.prototype.getHex=function(){return this.hex},t.prototype.getYiq=function(){if(!this._yiq){var t=this._rgb;this._yiq=(299*t[0]+587*t[1]+114*t[2])/1e3}return this._yiq},Object.defineProperty(t.prototype,"titleTextColor",{get:function(){return this._titleTextColor||(this._titleTextColor=this.getYiq()<200?"#fff":"#000"),this._titleTextColor},enumerable:!0,configurable:!0}),Object.defineProperty(t.prototype,"bodyTextColor",{get:function(){return this._bodyTextColor||(this._bodyTextColor=this.getYiq()<150?"#fff":"#000"),this._bodyTextColor},enumerable:!0,configurable:!0}),t.prototype.getTitleTextColor=function(){return this.titleTextColor},t.prototype.getBodyTextColor=function(){return this.bodyTextColor},t}();e.Swatch=a},416:function(t,e,r){"use strict";r.d(e,"a",function(){return o});var i=r(15),n=r(9);const a=new WeakMap,o=Object(n.f)((...t)=>e=>{let r=a.get(e);void 0===r&&(r={lastRenderedIndex:2147483647,values:[]},a.set(e,r));const n=r.values;let o=n.length;r.values=t;for(let a=0;a<t.length&&!(a>r.lastRenderedIndex);a++){const s=t[a];if(Object(i.h)(s)||"function"!=typeof s.then){e.setValue(s),r.lastRenderedIndex=a;break}a<o&&s===n[a]||(r.lastRenderedIndex=2147483647,o=0,Promise.resolve(s).then(t=>{const i=r.values.indexOf(s);i>-1&&i<r.lastRenderedIndex&&(r.lastRenderedIndex=i,e.setValue(t),e.commit())}))}})},468:function(t,e,r){"use strict";var i=r(0);customElements.define("round-slider",class extends i.a{static get properties(){return{value:{type:Number},high:{type:Number},low:{type:Number},min:{type:Number},max:{type:Number},step:{type:Number},startAngle:{type:Number},arcLength:{type:Number},handleSize:{type:Number},handleZoom:{type:Number},disabled:{type:Boolean},dragging:{type:Boolean,reflect:!0},rtl:{type:Boolean},_scale:{type:Number}}}constructor(){super(),this.min=0,this.max=100,this.step=1,this.startAngle=135,this.arcLength=270,this.handleSize=6,this.handleZoom=1.5,this.disabled=!1,this.dragging=!1,this.rtl=!1,this._scale=1}get _start(){return this.startAngle*Math.PI/180}get _len(){return Math.min(this.arcLength*Math.PI/180,2*Math.PI-.01)}get _end(){return this._start+this._len}get _enabled(){return!(this.disabled||null==this.value&&(null==this.high||null==this.low)||null!=this.value&&(this.value>this.max||this.value<this.min)||null!=this.high&&(this.high>this.max||this.high<this.min)||null!=this.low&&(this.low>this.max||this.low<this.min))}_angleInside(t){let e=(this.startAngle+this.arcLength/2-t+180+360)%360-180;return e<this.arcLength/2&&e>-this.arcLength/2}_angle2xy(t){return this.rtl?{x:-Math.cos(t),y:Math.sin(t)}:{x:Math.cos(t),y:Math.sin(t)}}_xy2angle(t,e){return this.rtl&&(t=-t),(Math.atan2(e,t)-this._start+2*Math.PI)%(2*Math.PI)}_value2angle(t){const e=(t-this.min)/(this.max-this.min);return this._start+e*this._len}_angle2value(t){return Math.round((t/this._len*(this.max-this.min)+this.min)/this.step)*this.step}get _boundaries(){const t=this._angle2xy(this._start),e=this._angle2xy(this._end);let r=1;this._angleInside(270)||(r=Math.max(-t.y,-e.y));let i=1;this._angleInside(90)||(i=Math.max(t.y,e.y));let n=1;this._angleInside(180)||(n=Math.max(-t.x,-e.x));let a=1;return this._angleInside(0)||(a=Math.max(t.x,e.x)),{up:r,down:i,left:n,right:a,height:r+i,width:n+a}}dragStart(t){let e=t.target;if(this._rotation&&"focus"!==this._rotation.type)return;if(e.classList.contains("overflow")&&(e=e.nextElementSibling),!e.classList.contains("handle"))return;e.setAttribute("stroke-width",2*this.handleSize*this.handleZoom*this._scale);const r="high"===e.id?this.low:this.min,i="low"===e.id?this.high:this.max;this._rotation={handle:e,min:r,max:i,start:this[e.id],type:t.type},this.dragging=!0}dragEnd(t){if(!this._rotation)return;const e=this._rotation.handle;e.setAttribute("stroke-width",2*this.handleSize*this._scale),this._rotation=!1,this.dragging=!1,e.blur();let r=new CustomEvent("value-changed",{detail:{[e.id]:this[e.id]}});this.dispatchEvent(r),this.low&&this.low>=.99*this.max?this._reverseOrder=!0:this._reverseOrder=!1}drag(t){if(!this._rotation)return;if("focus"===this._rotation.type)return;t.preventDefault();const e="touchmove"===t.type?t.touches[0].clientX:t.clientX,r="touchmove"===t.type?t.touches[0].clientY:t.clientY,i=this.shadowRoot.querySelector("svg").getBoundingClientRect(),n=this._boundaries,a=e-(i.left+n.left*i.width/n.width),o=r-(i.top+n.up*i.height/n.height),s=this._xy2angle(a,o),l=this._angle2value(s);this._dragpos(l)}_dragpos(t){if(t<this._rotation.min||t>this._rotation.max)return;const e=this._rotation.handle;this[e.id]=t;let r=new CustomEvent("value-changing",{detail:{[e.id]:t}});this.dispatchEvent(r)}_keyStep(t){if(!this._rotation)return;const e=this._rotation.handle;"ArrowLeft"===t.key&&(this.rtl?this._dragpos(this[e.id]+this.step):this._dragpos(this[e.id]-this.step)),"ArrowRight"===t.key&&(this.rtl?this._dragpos(this[e.id]-this.step):this._dragpos(this[e.id]+this.step))}firstUpdated(){document.addEventListener("mouseup",this.dragEnd.bind(this)),document.addEventListener("touchend",this.dragEnd.bind(this),{passive:!1}),document.addEventListener("mousemove",this.drag.bind(this)),document.addEventListener("touchmove",this.drag.bind(this),{passive:!1}),document.addEventListener("keydown",this._keyStep.bind(this))}updated(t){if(this.shadowRoot.querySelector("svg")&&void 0!==this.shadowRoot.querySelector("svg").style.vectorEffect)return;t.has("_scale")&&1!=this._scale&&this.shadowRoot.querySelector("svg").querySelectorAll("path").forEach(t=>{if(t.getAttribute("stroke-width"))return;const e=parseFloat(getComputedStyle(t).getPropertyValue("stroke-width"));t.style.strokeWidth=`${e*this._scale}px`});const e=this.shadowRoot.querySelector("svg").getBoundingClientRect(),r=Math.max(e.width,e.height);this._scale=2/r}_renderArc(t,e){const r=e-t;return t=this._angle2xy(t),e=this._angle2xy(e+.001),`\n      M ${t.x} ${t.y}\n      A 1 1,\n        0,\n        ${r>Math.PI?"1":"0"} ${this.rtl?"0":"1"},\n        ${e.x} ${e.y}\n    `}_renderHandle(t){const e=this._value2angle(this[t]),r=this._angle2xy(e);return i.j`
      <g class="${t} handle">
        <path
          id=${t}
          class="overflow"
          d="
          M ${r.x} ${r.y}
          L ${r.x+.001} ${r.y+.001}
          "
          vector-effect="non-scaling-stroke"
          stroke="rgba(0,0,0,0)"
          stroke-width="${4*this.handleSize*this._scale}"
          />
        <path
          id=${t}
          class="handle"
          d="
          M ${r.x} ${r.y}
          L ${r.x+.001} ${r.y+.001}
          "
          vector-effect="non-scaling-stroke"
          stroke-width="${2*this.handleSize*this._scale}"
          tabindex="0"
          @focus=${this.dragStart}
          @blur=${this.dragEnd}
          />
        </g>
      `}render(){const t=this._boundaries;return i.f`
      <svg
        @mousedown=${this.dragStart}
        @touchstart=${this.dragStart}
        xmln="http://www.w3.org/2000/svg"
        viewBox="${-t.left} ${-t.up} ${t.width} ${t.height}"
        style="margin: ${this.handleSize*this.handleZoom}px;"
        focusable="false"
      >
        <g class="slider">
          <path
            class="path"
            d=${this._renderArc(this._start,this._end)}
            vector-effect="non-scaling-stroke"
          />
          ${this._enabled?i.j`
              <path
                class="bar"
                vector-effect="non-scaling-stroke"
                d=${this._renderArc(this._value2angle(null!=this.low?this.low:this.min),this._value2angle(null!=this.high?this.high:this.value))}
              />`:""}
        </g>

        <g class="handles">
        ${this._enabled?null!=this.low?this._reverseOrder?i.f`${this._renderHandle("high")} ${this._renderHandle("low")}`:i.f`${this._renderHandle("low")} ${this._renderHandle("high")}`:i.f`${this._renderHandle("value")}`:""}
        </g>
      </svg>
    `}static get styles(){return i.c`
      :host {
        display: inline-block;
        width: 100%;
      }
      svg {
        overflow: visible;
      }
      .slider {
        fill: none;
        stroke-width: var(--round-slider-path-width, 3);
        stroke-linecap: var(--round-slider-linecap, round);
      }
      .path {
        stroke: var(--round-slider-path-color, lightgray);
      }
      .bar {
        stroke: var(--round-slider-bar-color, deepskyblue);
      }
      g.handles {
        stroke: var(--round-slider-handle-color, var(--round-slider-bar-color, deepskyblue));
        stroke-linecap: round;
      }
      g.low.handle {
        stroke: var(--round-slider-low-handle-color);
      }
      g.high.handle {
        stroke: var(--round-slider-high-handle-color);
      }
      .handle:focus {
        outline: unset;
      }
    `}})},469:function(t,e,r){"use strict";var i=this&&this.__importDefault||function(t){return t&&t.__esModule?t:{default:t}},n=this&&this.__importStar||function(t){if(t&&t.__esModule)return t;var e={};if(null!=t)for(var r in t)Object.hasOwnProperty.call(t,r)&&(e[r]=t[r]);return e.default=t,e};Object.defineProperty(e,"__esModule",{value:!0});var a=r(410),o=i(r(606)),s=n(r(368)),l=n(r(608)),c=n(r(612)),u=n(r(614)),d=r(436),h=function(){function t(e,r){this._src=e,this.opts=d({},r,t.DefaultOpts),this.opts.combinedFilter=u.combineFilters(this.opts.filters)}return t.from=function(t){return new o.default(t)},t.prototype._process=function(t,e){var r=e.quantizer,i=e.generator;return t.scaleDown(e),t.applyFilter(e.combinedFilter).then(function(t){return r(t.data,e)}).then(function(t){return a.Swatch.applyFilter(t,e.combinedFilter)}).then(function(t){return Promise.resolve(i(t))})},t.prototype.palette=function(){return this.swatches()},t.prototype.swatches=function(){return this._palette},t.prototype.getPalette=function(t){var e=this,r=new this.opts.ImageClass,i=r.load(this._src).then(function(t){return e._process(t,e.opts)}).then(function(t){return e._palette=t,r.remove(),t},function(t){throw r.remove(),t});return t&&i.then(function(e){return t(null,e)},function(e){return t(e)}),i},t.Builder=o.default,t.Quantizer=l,t.Generator=c,t.Filter=u,t.Util=s,t.Swatch=a.Swatch,t.DefaultOpts={colorCount:64,quality:5,generator:c.Default,ImageClass:null,quantizer:l.MMCQ,filters:[u.Default]},t}();e.default=h},491:function(t,e){t.exports=function t(e){return Object.freeze(e),Object.getOwnPropertyNames(e).forEach(function(r){!e.hasOwnProperty(r)||null===e[r]||"object"!=typeof e[r]&&"function"!=typeof e[r]||Object.isFrozen(e[r])||t(e[r])}),e}},57:function(t,e,r){"use strict";r.d(e,"b",function(){return o}),r.d(e,"a",function(){return s});r(3);var i=r(56),n=r(34),a=r(69);const o={observers:["_focusedChanged(receivedFocusFromKeyboard)"],_focusedChanged:function(t){t&&this.ensureRipple(),this.hasRipple()&&(this._ripple.holdDown=t)},_createRipple:function(){var t=a.a._createRipple();return t.id="ink",t.setAttribute("center",""),t.classList.add("circle"),t}},s=[i.a,n.a,a.a,o]},603:function(t,e,r){"use strict";var i=this&&this.__importDefault||function(t){return t&&t.__esModule?t:{default:t}},n=i(r(469)),a=i(r(616));n.default.DefaultOpts.ImageClass=a.default,t.exports=n.default},604:function(t,e,r){var i=r(455),n=r(605),a=r(387),o=r(248);t.exports=function(t,e){return(o(t)?i:n)(t,a(e,3))}},605:function(t,e,r){var i=r(483);t.exports=function(t,e){var r=[];return i(t,function(t,i,n){e(t,i,n)&&r.push(t)}),r}},606:function(t,e,r){"use strict";var i=this&&this.__importDefault||function(t){return t&&t.__esModule?t:{default:t}};Object.defineProperty(e,"__esModule",{value:!0});var n=i(r(469)),a=r(607),o=function(){function t(t,e){void 0===e&&(e={}),this._src=t,this._opts=e,this._opts.filters=a(n.default.DefaultOpts.filters)}return t.prototype.maxColorCount=function(t){return this._opts.colorCount=t,this},t.prototype.maxDimension=function(t){return this._opts.maxDimension=t,this},t.prototype.addFilter=function(t){return this._opts.filters.push(t),this},t.prototype.removeFilter=function(t){var e=this._opts.filters.indexOf(t);return e>0&&this._opts.filters.splice(e),this},t.prototype.clearFilters=function(){return this._opts.filters=[],this},t.prototype.quality=function(t){return this._opts.quality=t,this},t.prototype.useImageClass=function(t){return this._opts.ImageClass=t,this},t.prototype.useGenerator=function(t){return this._opts.generator=t,this},t.prototype.useQuantizer=function(t){return this._opts.quantizer=t,this},t.prototype.build=function(){return new n.default(this._src,this._opts)},t.prototype.getPalette=function(t){return this.build().getPalette(t)},t.prototype.getSwatches=function(t){return this.build().getPalette(t)},t}();e.default=o},607:function(t,e,r){var i=r(487),n=4;t.exports=function(t){return i(t,n)}},608:function(t,e,r){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var i=r(609);e.MMCQ=i.default,e.WebWorker=null},609:function(t,e,r){"use strict";var i=this&&this.__importDefault||function(t){return t&&t.__esModule?t:{default:t}};Object.defineProperty(e,"__esModule",{value:!0});var n=r(410),a=i(r(610)),o=i(r(611));function s(t,e){for(var r=t.size();t.size()<e;){var i=t.pop();if(!(i&&i.count()>0))break;var n=i.split(),a=n[0],o=n[1];if(t.push(a),o&&o.count()>0&&t.push(o),t.size()===r)break;r=t.size()}}e.default=function(t,e){if(0===t.length||e.colorCount<2||e.colorCount>256)throw new Error("Wrong MMCQ parameters");var r=a.default.build(t),i=r.hist,l=(Object.keys(i).length,new o.default(function(t,e){return t.count()-e.count()}));l.push(r),s(l,.75*e.colorCount);var c=new o.default(function(t,e){return t.count()*t.volume()-e.count()*e.volume()});return c.contents=l.contents,s(c,e.colorCount-c.size()),function(t){for(var e=[];t.size();){var r=t.pop(),i=r.avg();i[0],i[1],i[2],e.push(new n.Swatch(i,r.count()))}return e}(c)}},610:function(t,e,r){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var i=r(368),n=function(){function t(t,e,r,i,n,a,o){this._volume=-1,this._count=-1,this.dimension={r1:t,r2:e,g1:r,g2:i,b1:n,b2:a},this.hist=o}return t.build=function(e,r){var n,a,o,s,l,c,u,d,h,p=1<<3*i.SIGBITS,f=new Uint32Array(p);n=o=l=0,a=s=c=Number.MAX_VALUE;for(var m=e.length/4,g=0;g<m;){var b=4*g;if(g++,u=e[b+0],d=e[b+1],h=e[b+2],0!==e[b+3])u>>=i.RSHIFT,d>>=i.RSHIFT,h>>=i.RSHIFT,f[i.getColorIndex(u,d,h)]+=1,u>n&&(n=u),u<a&&(a=u),d>o&&(o=d),d<s&&(s=d),h>l&&(l=h),h<c&&(c=h)}return new t(a,n,s,o,c,l,f)},t.prototype.invalidate=function(){this._volume=this._count=-1,this._avg=null},t.prototype.volume=function(){if(this._volume<0){var t=this.dimension,e=t.r1,r=t.r2,i=t.g1,n=t.g2,a=t.b1,o=t.b2;this._volume=(r-e+1)*(n-i+1)*(o-a+1)}return this._volume},t.prototype.count=function(){if(this._count<0){for(var t=this.hist,e=this.dimension,r=e.r1,n=e.r2,a=e.g1,o=e.g2,s=e.b1,l=e.b2,c=0,u=r;u<=n;u++)for(var d=a;d<=o;d++)for(var h=s;h<=l;h++){c+=t[i.getColorIndex(u,d,h)]}this._count=c}return this._count},t.prototype.clone=function(){var e=this.hist,r=this.dimension;return new t(r.r1,r.r2,r.g1,r.g2,r.b1,r.b2,e)},t.prototype.avg=function(){if(!this._avg){var t=this.hist,e=this.dimension,r=e.r1,n=e.r2,a=e.g1,o=e.g2,s=e.b1,l=e.b2,c=0,u=1<<8-i.SIGBITS,d=void 0,h=void 0,p=void 0;d=h=p=0;for(var f=r;f<=n;f++)for(var m=a;m<=o;m++)for(var g=s;g<=l;g++){var b=t[i.getColorIndex(f,m,g)];c+=b,d+=b*(f+.5)*u,h+=b*(m+.5)*u,p+=b*(g+.5)*u}this._avg=c?[~~(d/c),~~(h/c),~~(p/c)]:[~~(u*(r+n+1)/2),~~(u*(a+o+1)/2),~~(u*(s+l+1)/2)]}return this._avg},t.prototype.contains=function(t){var e=t[0],r=t[1],n=t[2],a=this.dimension,o=a.r1,s=a.r2,l=a.g1,c=a.g2,u=a.b1,d=a.b2;return e>>=i.RSHIFT,r>>=i.RSHIFT,n>>=i.RSHIFT,e>=o&&e<=s&&r>=l&&r<=c&&n>=u&&n<=d},t.prototype.split=function(){var t=this.hist,e=this.dimension,r=e.r1,n=e.r2,a=e.g1,o=e.g2,s=e.b1,l=e.b2,c=this.count();if(!c)return[];if(1===c)return[this.clone()];var u,d,h=n-r+1,p=o-a+1,f=l-s+1,m=Math.max(h,p,f),g=null;u=d=0;var b=null;if(m===h){b="r",g=new Uint32Array(n+1);for(var v=r;v<=n;v++){u=0;for(var y=a;y<=o;y++)for(var _=s;_<=l;_++){u+=t[i.getColorIndex(v,y,_)]}d+=u,g[v]=d}}else if(m===p){b="g",g=new Uint32Array(o+1);for(y=a;y<=o;y++){u=0;for(v=r;v<=n;v++)for(_=s;_<=l;_++){u+=t[i.getColorIndex(v,y,_)]}d+=u,g[y]=d}}else{b="b",g=new Uint32Array(l+1);for(_=s;_<=l;_++){u=0;for(v=r;v<=n;v++)for(y=a;y<=o;y++){u+=t[i.getColorIndex(v,y,_)]}d+=u,g[_]=d}}for(var w=-1,x=new Uint32Array(g.length),k=0;k<g.length;k++){var C=g[k];w<0&&C>d/2&&(w=k),x[k]=d-C}var O=this;return function(t){var e=t+"1",r=t+"2",i=O.dimension[e],n=O.dimension[r],a=O.clone(),o=O.clone(),s=w-i,l=n-w;for(s<=l?(n=Math.min(n-1,~~(w+l/2)),n=Math.max(0,n)):(n=Math.max(i,~~(w-1-s/2)),n=Math.min(O.dimension[r],n));!g[n];)n++;for(var c=x[n];!c&&g[n-1];)c=x[--n];return a.dimension[r]=n,o.dimension[e]=n+1,[a,o]}(b)},t}();e.default=n},611:function(t,e,r){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var i=function(){function t(t){this._comparator=t,this.contents=[],this._sorted=!1}return t.prototype._sort=function(){this._sorted||(this.contents.sort(this._comparator),this._sorted=!0)},t.prototype.push=function(t){this.contents.push(t),this._sorted=!1},t.prototype.peek=function(t){return this._sort(),t="number"==typeof t?t:this.contents.length-1,this.contents[t]},t.prototype.pop=function(){return this._sort(),this.contents.pop()},t.prototype.size=function(){return this.contents.length},t.prototype.map=function(t){return this._sort(),this.contents.map(t)},t}();e.default=i},612:function(t,e,r){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var i=r(613);e.Default=i.default},613:function(t,e,r){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var i=r(410),n=r(368),a=r(436),o={targetDarkLuma:.26,maxDarkLuma:.45,minLightLuma:.55,targetLightLuma:.74,minNormalLuma:.3,targetNormalLuma:.5,maxNormalLuma:.7,targetMutesSaturation:.3,maxMutesSaturation:.4,targetVibrantSaturation:1,minVibrantSaturation:.35,weightSaturation:3,weightLuma:6.5,weightPopulation:.5};function s(t,e,r,i,n,a,o,s,l,c){var u=null,d=0;return e.forEach(function(e){var h=e.getHsl(),p=h[1],f=h[2];if(p>=s&&p<=l&&f>=n&&f<=a&&!function(t,e){return t.Vibrant===e||t.DarkVibrant===e||t.LightVibrant===e||t.Muted===e||t.DarkMuted===e||t.LightMuted===e}(t,e)){var m=function(t,e,r,i,n,a,o){function s(t,e){return 1-Math.abs(t-e)}return function(){for(var t=[],e=0;e<arguments.length;e++)t[e]=arguments[e];for(var r=0,i=0,n=0;n<t.length;n+=2){var a=t[n],o=t[n+1];r+=a*o,i+=o}return r/i}(s(t,e),o.weightSaturation,s(r,i),o.weightLuma,n/a,o.weightPopulation)}(p,o,f,i,e.getPopulation(),r,c);(null===u||m>d)&&(u=e,d=m)}}),u}e.default=function(t,e){e=a({},e,o);var r=function(t){var e=0;return t.forEach(function(t){e=Math.max(e,t.getPopulation())}),e}(t),l=function(t,e,r){var i={};return i.Vibrant=s(i,t,e,r.targetNormalLuma,r.minNormalLuma,r.maxNormalLuma,r.targetVibrantSaturation,r.minVibrantSaturation,1,r),i.LightVibrant=s(i,t,e,r.targetLightLuma,r.minLightLuma,1,r.targetVibrantSaturation,r.minVibrantSaturation,1,r),i.DarkVibrant=s(i,t,e,r.targetDarkLuma,0,r.maxDarkLuma,r.targetVibrantSaturation,r.minVibrantSaturation,1,r),i.Muted=s(i,t,e,r.targetNormalLuma,r.minNormalLuma,r.maxNormalLuma,r.targetMutesSaturation,0,r.maxMutesSaturation,r),i.LightMuted=s(i,t,e,r.targetLightLuma,r.minLightLuma,1,r.targetMutesSaturation,0,r.maxMutesSaturation,r),i.DarkMuted=s(i,t,e,r.targetDarkLuma,0,r.maxDarkLuma,r.targetMutesSaturation,0,r.maxMutesSaturation,r),i}(t,r,e);return function(t,e,r){if(null===t.Vibrant&&null===t.DarkVibrant&&null===t.LightVibrant){if(null===t.DarkVibrant&&null!==t.DarkMuted){var a=t.DarkMuted.getHsl(),o=a[0],s=a[1],l=a[2];l=r.targetDarkLuma,t.DarkVibrant=new i.Swatch(n.hslToRgb(o,s,l),0)}if(null===t.LightVibrant&&null!==t.LightMuted){var c=t.LightMuted.getHsl();o=c[0],s=c[1],l=c[2],l=r.targetDarkLuma,t.DarkVibrant=new i.Swatch(n.hslToRgb(o,s,l),0)}}if(null===t.Vibrant&&null!==t.DarkVibrant){var u=t.DarkVibrant.getHsl();o=u[0],s=u[1],l=u[2],l=r.targetNormalLuma,t.Vibrant=new i.Swatch(n.hslToRgb(o,s,l),0)}else if(null===t.Vibrant&&null!==t.LightVibrant){var d=t.LightVibrant.getHsl();o=d[0],s=d[1],l=d[2],l=r.targetNormalLuma,t.Vibrant=new i.Swatch(n.hslToRgb(o,s,l),0)}if(null===t.DarkVibrant&&null!==t.Vibrant){var h=t.Vibrant.getHsl();o=h[0],s=h[1],l=h[2],l=r.targetDarkLuma,t.DarkVibrant=new i.Swatch(n.hslToRgb(o,s,l),0)}if(null===t.LightVibrant&&null!==t.Vibrant){var p=t.Vibrant.getHsl();o=p[0],s=p[1],l=p[2],l=r.targetLightLuma,t.LightVibrant=new i.Swatch(n.hslToRgb(o,s,l),0)}if(null===t.Muted&&null!==t.Vibrant){var f=t.Vibrant.getHsl();o=f[0],s=f[1],l=f[2],l=r.targetMutesSaturation,t.Muted=new i.Swatch(n.hslToRgb(o,s,l),0)}if(null===t.DarkMuted&&null!==t.DarkVibrant){var m=t.DarkVibrant.getHsl();o=m[0],s=m[1],l=m[2],l=r.targetMutesSaturation,t.DarkMuted=new i.Swatch(n.hslToRgb(o,s,l),0)}if(null===t.LightMuted&&null!==t.LightVibrant){var g=t.LightVibrant.getHsl();o=g[0],s=g[1],l=g[2],l=r.targetMutesSaturation,t.LightMuted=new i.Swatch(n.hslToRgb(o,s,l),0)}}(l,0,e),l}},614:function(t,e,r){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var i=r(615);e.Default=i.default,e.combineFilters=function(t){return Array.isArray(t)&&0!==t.length?function(e,r,i,n){if(0===n)return!1;for(var a=0;a<t.length;a++)if(!t[a](e,r,i,n))return!1;return!0}:null}},615:function(t,e,r){"use strict";Object.defineProperty(e,"__esModule",{value:!0}),e.default=function(t,e,r,i){return i>=125&&!(t>250&&e>250&&r>250)}},616:function(t,e,r){"use strict";var i,n=this&&this.__extends||(i=function(t,e){return(i=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(t,e){t.__proto__=e}||function(t,e){for(var r in e)e.hasOwnProperty(r)&&(t[r]=e[r])})(t,e)},function(t,e){function r(){this.constructor=t}i(t,e),t.prototype=null===e?Object.create(e):(r.prototype=e.prototype,new r)}),a=this&&this.__importStar||function(t){if(t&&t.__esModule)return t;var e={};if(null!=t)for(var r in t)Object.hasOwnProperty.call(t,r)&&(e[r]=t[r]);return e.default=t,e};Object.defineProperty(e,"__esModule",{value:!0});var o=r(617),s=a(r(618));var l=function(t){function e(){return null!==t&&t.apply(this,arguments)||this}return n(e,t),e.prototype._initCanvas=function(){var t=this.image,e=this._canvas=document.createElement("canvas"),r=this._context=e.getContext("2d");e.className="vibrant-canvas",e.style.display="none",this._width=e.width=t.width,this._height=e.height=t.height,r.drawImage(t,0,0),document.body.appendChild(e)},e.prototype.load=function(t){var e,r,i,n,a,o,l=this,c=null,u=null;if("string"==typeof t)c=document.createElement("img"),a=t,null===(o=s.parse(a)).protocol&&null===o.host&&null===o.port||(e=window.location.href,r=t,i=s.parse(e),n=s.parse(r),i.protocol===n.protocol&&i.hostname===n.hostname&&i.port===n.port)||(c.crossOrigin="anonymous"),u=c.src=t;else{if(!(t instanceof HTMLImageElement))return Promise.reject(new Error("Cannot load buffer as an image in browser"));c=t,u=t.src}return this.image=c,new Promise(function(t,e){var r=function(){l._initCanvas(),t(l)};c.complete?r():(c.onload=r,c.onerror=function(t){return e(new Error("Fail to load image: "+u))})})},e.prototype.clear=function(){this._context.clearRect(0,0,this._width,this._height)},e.prototype.update=function(t){this._context.putImageData(t,0,0)},e.prototype.getWidth=function(){return this._width},e.prototype.getHeight=function(){return this._height},e.prototype.resize=function(t,e,r){var i=this._canvas,n=this._context,a=this.image;this._width=i.width=t,this._height=i.height=e,n.scale(r,r),n.drawImage(a,0,0)},e.prototype.getPixelCount=function(){return this._width*this._height},e.prototype.getImageData=function(){return this._context.getImageData(0,0,this._width,this._height)},e.prototype.remove=function(){this._canvas&&this._canvas.parentNode&&this._canvas.parentNode.removeChild(this._canvas)},e}(o.ImageBase);e.default=l},617:function(t,e,r){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var i=function(){function t(){}return t.prototype.scaleDown=function(t){var e=this.getWidth(),r=this.getHeight(),i=1;if(t.maxDimension>0){var n=Math.max(e,r);n>t.maxDimension&&(i=t.maxDimension/n)}else i=1/t.quality;i<1&&this.resize(e*i,r*i,i)},t.prototype.applyFilter=function(t){var e=this.getImageData();if("function"==typeof t)for(var r=e.data,i=r.length/4,n=void 0,a=0;a<i;a++)t(r[(n=4*a)+0],r[n+1],r[n+2],r[n+3])||(r[n+3]=0);return Promise.resolve(e)},t}();e.ImageBase=i},618:function(t,e,r){"use strict";var i=r(619),n=r(620);function a(){this.protocol=null,this.slashes=null,this.auth=null,this.host=null,this.port=null,this.hostname=null,this.hash=null,this.search=null,this.query=null,this.pathname=null,this.path=null,this.href=null}e.parse=y,e.resolve=function(t,e){return y(t,!1,!0).resolve(e)},e.resolveObject=function(t,e){return t?y(t,!1,!0).resolveObject(e):e},e.format=function(t){n.isString(t)&&(t=y(t));return t instanceof a?t.format():a.prototype.format.call(t)},e.Url=a;var o=/^([a-z0-9.+-]+:)/i,s=/:[0-9]*$/,l=/^(\/\/?(?!\/)[^\?\s]*)(\?[^\s]*)?$/,c=["{","}","|","\\","^","`"].concat(["<",">",'"',"`"," ","\r","\n","\t"]),u=["'"].concat(c),d=["%","/","?",";","#"].concat(u),h=["/","?","#"],p=/^[+a-z0-9A-Z_-]{0,63}$/,f=/^([+a-z0-9A-Z_-]{0,63})(.*)$/,m={javascript:!0,"javascript:":!0},g={javascript:!0,"javascript:":!0},b={http:!0,https:!0,ftp:!0,gopher:!0,file:!0,"http:":!0,"https:":!0,"ftp:":!0,"gopher:":!0,"file:":!0},v=r(621);function y(t,e,r){if(t&&n.isObject(t)&&t instanceof a)return t;var i=new a;return i.parse(t,e,r),i}a.prototype.parse=function(t,e,r){if(!n.isString(t))throw new TypeError("Parameter 'url' must be a string, not "+typeof t);var a=t.indexOf("?"),s=-1!==a&&a<t.indexOf("#")?"?":"#",c=t.split(s);c[0]=c[0].replace(/\\/g,"/");var y=t=c.join(s);if(y=y.trim(),!r&&1===t.split("#").length){var _=l.exec(y);if(_)return this.path=y,this.href=y,this.pathname=_[1],_[2]?(this.search=_[2],this.query=e?v.parse(this.search.substr(1)):this.search.substr(1)):e&&(this.search="",this.query={}),this}var w=o.exec(y);if(w){var x=(w=w[0]).toLowerCase();this.protocol=x,y=y.substr(w.length)}if(r||w||y.match(/^\/\/[^@\/]+@[^@\/]+/)){var k="//"===y.substr(0,2);!k||w&&g[w]||(y=y.substr(2),this.slashes=!0)}if(!g[w]&&(k||w&&!b[w])){for(var C,O,S=-1,M=0;M<h.length;M++){-1!==(j=y.indexOf(h[M]))&&(-1===S||j<S)&&(S=j)}-1!==(O=-1===S?y.lastIndexOf("@"):y.lastIndexOf("@",S))&&(C=y.slice(0,O),y=y.slice(O+1),this.auth=decodeURIComponent(C)),S=-1;for(M=0;M<d.length;M++){var j;-1!==(j=y.indexOf(d[M]))&&(-1===S||j<S)&&(S=j)}-1===S&&(S=y.length),this.host=y.slice(0,S),y=y.slice(S),this.parseHost(),this.hostname=this.hostname||"";var D="["===this.hostname[0]&&"]"===this.hostname[this.hostname.length-1];if(!D)for(var A=this.hostname.split(/\./),E=(M=0,A.length);M<E;M++){var I=A[M];if(I&&!I.match(p)){for(var L="",$=0,N=I.length;$<N;$++)I.charCodeAt($)>127?L+="x":L+=I[$];if(!L.match(p)){var R=A.slice(0,M),z=A.slice(M+1),T=I.match(f);T&&(R.push(T[1]),z.unshift(T[2])),z.length&&(y="/"+z.join(".")+y),this.hostname=R.join(".");break}}}this.hostname.length>255?this.hostname="":this.hostname=this.hostname.toLowerCase(),D||(this.hostname=i.toASCII(this.hostname));var P=this.port?":"+this.port:"",H=this.hostname||"";this.host=H+P,this.href+=this.host,D&&(this.hostname=this.hostname.substr(1,this.hostname.length-2),"/"!==y[0]&&(y="/"+y))}if(!m[x])for(M=0,E=u.length;M<E;M++){var F=u[M];if(-1!==y.indexOf(F)){var B=encodeURIComponent(F);B===F&&(B=escape(F)),y=y.split(F).join(B)}}var V=y.indexOf("#");-1!==V&&(this.hash=y.substr(V),y=y.slice(0,V));var q=y.indexOf("?");if(-1!==q?(this.search=y.substr(q),this.query=y.substr(q+1),e&&(this.query=v.parse(this.query)),y=y.slice(0,q)):e&&(this.search="",this.query={}),y&&(this.pathname=y),b[x]&&this.hostname&&!this.pathname&&(this.pathname="/"),this.pathname||this.search){P=this.pathname||"";var Y=this.search||"";this.path=P+Y}return this.href=this.format(),this},a.prototype.format=function(){var t=this.auth||"";t&&(t=(t=encodeURIComponent(t)).replace(/%3A/i,":"),t+="@");var e=this.protocol||"",r=this.pathname||"",i=this.hash||"",a=!1,o="";this.host?a=t+this.host:this.hostname&&(a=t+(-1===this.hostname.indexOf(":")?this.hostname:"["+this.hostname+"]"),this.port&&(a+=":"+this.port)),this.query&&n.isObject(this.query)&&Object.keys(this.query).length&&(o=v.stringify(this.query));var s=this.search||o&&"?"+o||"";return e&&":"!==e.substr(-1)&&(e+=":"),this.slashes||(!e||b[e])&&!1!==a?(a="//"+(a||""),r&&"/"!==r.charAt(0)&&(r="/"+r)):a||(a=""),i&&"#"!==i.charAt(0)&&(i="#"+i),s&&"?"!==s.charAt(0)&&(s="?"+s),e+a+(r=r.replace(/[?#]/g,function(t){return encodeURIComponent(t)}))+(s=s.replace("#","%23"))+i},a.prototype.resolve=function(t){return this.resolveObject(y(t,!1,!0)).format()},a.prototype.resolveObject=function(t){if(n.isString(t)){var e=new a;e.parse(t,!1,!0),t=e}for(var r=new a,i=Object.keys(this),o=0;o<i.length;o++){var s=i[o];r[s]=this[s]}if(r.hash=t.hash,""===t.href)return r.href=r.format(),r;if(t.slashes&&!t.protocol){for(var l=Object.keys(t),c=0;c<l.length;c++){var u=l[c];"protocol"!==u&&(r[u]=t[u])}return b[r.protocol]&&r.hostname&&!r.pathname&&(r.path=r.pathname="/"),r.href=r.format(),r}if(t.protocol&&t.protocol!==r.protocol){if(!b[t.protocol]){for(var d=Object.keys(t),h=0;h<d.length;h++){var p=d[h];r[p]=t[p]}return r.href=r.format(),r}if(r.protocol=t.protocol,t.host||g[t.protocol])r.pathname=t.pathname;else{for(var f=(t.pathname||"").split("/");f.length&&!(t.host=f.shift()););t.host||(t.host=""),t.hostname||(t.hostname=""),""!==f[0]&&f.unshift(""),f.length<2&&f.unshift(""),r.pathname=f.join("/")}if(r.search=t.search,r.query=t.query,r.host=t.host||"",r.auth=t.auth,r.hostname=t.hostname||t.host,r.port=t.port,r.pathname||r.search){var m=r.pathname||"",v=r.search||"";r.path=m+v}return r.slashes=r.slashes||t.slashes,r.href=r.format(),r}var y=r.pathname&&"/"===r.pathname.charAt(0),_=t.host||t.pathname&&"/"===t.pathname.charAt(0),w=_||y||r.host&&t.pathname,x=w,k=r.pathname&&r.pathname.split("/")||[],C=(f=t.pathname&&t.pathname.split("/")||[],r.protocol&&!b[r.protocol]);if(C&&(r.hostname="",r.port=null,r.host&&(""===k[0]?k[0]=r.host:k.unshift(r.host)),r.host="",t.protocol&&(t.hostname=null,t.port=null,t.host&&(""===f[0]?f[0]=t.host:f.unshift(t.host)),t.host=null),w=w&&(""===f[0]||""===k[0])),_)r.host=t.host||""===t.host?t.host:r.host,r.hostname=t.hostname||""===t.hostname?t.hostname:r.hostname,r.search=t.search,r.query=t.query,k=f;else if(f.length)k||(k=[]),k.pop(),k=k.concat(f),r.search=t.search,r.query=t.query;else if(!n.isNullOrUndefined(t.search)){if(C)r.hostname=r.host=k.shift(),(D=!!(r.host&&r.host.indexOf("@")>0)&&r.host.split("@"))&&(r.auth=D.shift(),r.host=r.hostname=D.shift());return r.search=t.search,r.query=t.query,n.isNull(r.pathname)&&n.isNull(r.search)||(r.path=(r.pathname?r.pathname:"")+(r.search?r.search:"")),r.href=r.format(),r}if(!k.length)return r.pathname=null,r.search?r.path="/"+r.search:r.path=null,r.href=r.format(),r;for(var O=k.slice(-1)[0],S=(r.host||t.host||k.length>1)&&("."===O||".."===O)||""===O,M=0,j=k.length;j>=0;j--)"."===(O=k[j])?k.splice(j,1):".."===O?(k.splice(j,1),M++):M&&(k.splice(j,1),M--);if(!w&&!x)for(;M--;M)k.unshift("..");!w||""===k[0]||k[0]&&"/"===k[0].charAt(0)||k.unshift(""),S&&"/"!==k.join("/").substr(-1)&&k.push("");var D,A=""===k[0]||k[0]&&"/"===k[0].charAt(0);C&&(r.hostname=r.host=A?"":k.length?k.shift():"",(D=!!(r.host&&r.host.indexOf("@")>0)&&r.host.split("@"))&&(r.auth=D.shift(),r.host=r.hostname=D.shift()));return(w=w||r.host&&k.length)&&!A&&k.unshift(""),k.length?r.pathname=k.join("/"):(r.pathname=null,r.path=null),n.isNull(r.pathname)&&n.isNull(r.search)||(r.path=(r.pathname?r.pathname:"")+(r.search?r.search:"")),r.auth=t.auth||r.auth,r.slashes=r.slashes||t.slashes,r.href=r.format(),r},a.prototype.parseHost=function(){var t=this.host,e=s.exec(t);e&&(":"!==(e=e[0])&&(this.port=e.substr(1)),t=t.substr(0,t.length-e.length)),t&&(this.hostname=t)}},619:function(t,e,r){(function(t,i){var n;!function(a){e&&e.nodeType,t&&t.nodeType;var o="object"==typeof i&&i;o.global!==o&&o.window!==o&&o.self;var s,l=2147483647,c=36,u=1,d=26,h=38,p=700,f=72,m=128,g="-",b=/^xn--/,v=/[^\x20-\x7E]/,y=/[\x2E\u3002\uFF0E\uFF61]/g,_={overflow:"Overflow: input needs wider integers to process","not-basic":"Illegal input >= 0x80 (not a basic code point)","invalid-input":"Invalid input"},w=c-u,x=Math.floor,k=String.fromCharCode;function C(t){throw new RangeError(_[t])}function O(t,e){for(var r=t.length,i=[];r--;)i[r]=e(t[r]);return i}function S(t,e){var r=t.split("@"),i="";return r.length>1&&(i=r[0]+"@",t=r[1]),i+O((t=t.replace(y,".")).split("."),e).join(".")}function M(t){for(var e,r,i=[],n=0,a=t.length;n<a;)(e=t.charCodeAt(n++))>=55296&&e<=56319&&n<a?56320==(64512&(r=t.charCodeAt(n++)))?i.push(((1023&e)<<10)+(1023&r)+65536):(i.push(e),n--):i.push(e);return i}function j(t){return O(t,function(t){var e="";return t>65535&&(e+=k((t-=65536)>>>10&1023|55296),t=56320|1023&t),e+=k(t)}).join("")}function D(t,e){return t+22+75*(t<26)-((0!=e)<<5)}function A(t,e,r){var i=0;for(t=r?x(t/p):t>>1,t+=x(t/e);t>w*d>>1;i+=c)t=x(t/w);return x(i+(w+1)*t/(t+h))}function E(t){var e,r,i,n,a,o,s,h,p,b,v,y=[],_=t.length,w=0,k=m,O=f;for((r=t.lastIndexOf(g))<0&&(r=0),i=0;i<r;++i)t.charCodeAt(i)>=128&&C("not-basic"),y.push(t.charCodeAt(i));for(n=r>0?r+1:0;n<_;){for(a=w,o=1,s=c;n>=_&&C("invalid-input"),((h=(v=t.charCodeAt(n++))-48<10?v-22:v-65<26?v-65:v-97<26?v-97:c)>=c||h>x((l-w)/o))&&C("overflow"),w+=h*o,!(h<(p=s<=O?u:s>=O+d?d:s-O));s+=c)o>x(l/(b=c-p))&&C("overflow"),o*=b;O=A(w-a,e=y.length+1,0==a),x(w/e)>l-k&&C("overflow"),k+=x(w/e),w%=e,y.splice(w++,0,k)}return j(y)}function I(t){var e,r,i,n,a,o,s,h,p,b,v,y,_,w,O,S=[];for(y=(t=M(t)).length,e=m,r=0,a=f,o=0;o<y;++o)(v=t[o])<128&&S.push(k(v));for(i=n=S.length,n&&S.push(g);i<y;){for(s=l,o=0;o<y;++o)(v=t[o])>=e&&v<s&&(s=v);for(s-e>x((l-r)/(_=i+1))&&C("overflow"),r+=(s-e)*_,e=s,o=0;o<y;++o)if((v=t[o])<e&&++r>l&&C("overflow"),v==e){for(h=r,p=c;!(h<(b=p<=a?u:p>=a+d?d:p-a));p+=c)O=h-b,w=c-b,S.push(k(D(b+O%w,0))),h=x(O/w);S.push(k(D(h,0))),a=A(r,_,i==n),r=0,++i}++r,++e}return S.join("")}s={version:"1.4.1",ucs2:{decode:M,encode:j},decode:E,encode:I,toASCII:function(t){return S(t,function(t){return v.test(t)?"xn--"+I(t):t})},toUnicode:function(t){return S(t,function(t){return b.test(t)?E(t.slice(4).toLowerCase()):t})}},void 0===(n=function(){return s}.call(e,r,e,t))||(t.exports=n)}()}).call(this,r(310)(t),r(281))},620:function(t,e,r){"use strict";t.exports={isString:function(t){return"string"==typeof t},isObject:function(t){return"object"==typeof t&&null!==t},isNull:function(t){return null===t},isNullOrUndefined:function(t){return null==t}}},621:function(t,e,r){"use strict";e.decode=e.parse=r(622),e.encode=e.stringify=r(623)},622:function(t,e,r){"use strict";function i(t,e){return Object.prototype.hasOwnProperty.call(t,e)}t.exports=function(t,e,r,a){e=e||"&",r=r||"=";var o={};if("string"!=typeof t||0===t.length)return o;var s=/\+/g;t=t.split(e);var l=1e3;a&&"number"==typeof a.maxKeys&&(l=a.maxKeys);var c=t.length;l>0&&c>l&&(c=l);for(var u=0;u<c;++u){var d,h,p,f,m=t[u].replace(s,"%20"),g=m.indexOf(r);g>=0?(d=m.substr(0,g),h=m.substr(g+1)):(d=m,h=""),p=decodeURIComponent(d),f=decodeURIComponent(h),i(o,p)?n(o[p])?o[p].push(f):o[p]=[o[p],f]:o[p]=f}return o};var n=Array.isArray||function(t){return"[object Array]"===Object.prototype.toString.call(t)}},623:function(t,e,r){"use strict";var i=function(t){switch(typeof t){case"string":return t;case"boolean":return t?"true":"false";case"number":return isFinite(t)?t:"";default:return""}};t.exports=function(t,e,r,s){return e=e||"&",r=r||"=",null===t&&(t=void 0),"object"==typeof t?a(o(t),function(o){var s=encodeURIComponent(i(o))+r;return n(t[o])?a(t[o],function(t){return s+encodeURIComponent(i(t))}).join(e):s+encodeURIComponent(i(t[o]))}).join(e):s?encodeURIComponent(i(s))+r+encodeURIComponent(i(t)):""};var n=Array.isArray||function(t){return"[object Array]"===Object.prototype.toString.call(t)};function a(t,e){if(t.map)return t.map(e);for(var r=[],i=0;i<t.length;i++)r.push(e(t[i],i));return r}var o=Object.keys||function(t){var e=[];for(var r in t)Object.prototype.hasOwnProperty.call(t,r)&&e.push(r);return e}},624:function(t,e,r){"use strict";r.d(e,"a",function(){return d});var i=r(9);const n=(t,e)=>{const r=t.startNode.parentNode,n=void 0===e?t.endNode:e.startNode,a=r.insertBefore(Object(i.e)(),n);r.insertBefore(Object(i.e)(),n);const o=new i.b(t.options);return o.insertAfterNode(a),o},a=(t,e)=>(t.setValue(e),t.commit(),t),o=(t,e,r)=>{const n=t.startNode.parentNode,a=r?r.startNode:t.endNode,o=e.endNode.nextSibling;o!==a&&Object(i.j)(n,e.startNode,o,a)},s=t=>{Object(i.i)(t.startNode.parentNode,t.startNode,t.endNode.nextSibling)},l=(t,e,r)=>{const i=new Map;for(let n=e;n<=r;n++)i.set(t[n],n);return i},c=new WeakMap,u=new WeakMap,d=Object(i.f)((t,e,r)=>{let d;return void 0===r?r=e:void 0!==e&&(d=e),e=>{if(!(e instanceof i.b))throw new Error("repeat can only be used in text bindings");const h=c.get(e)||[],p=u.get(e)||[],f=[],m=[],g=[];let b,v,y=0;for(const i of t)g[y]=d?d(i,y):y,m[y]=r(i,y),y++;let _=0,w=h.length-1,x=0,k=m.length-1;for(;_<=w&&x<=k;)if(null===h[_])_++;else if(null===h[w])w--;else if(p[_]===g[x])f[x]=a(h[_],m[x]),_++,x++;else if(p[w]===g[k])f[k]=a(h[w],m[k]),w--,k--;else if(p[_]===g[k])f[k]=a(h[_],m[k]),o(e,h[_],f[k+1]),_++,k--;else if(p[w]===g[x])f[x]=a(h[w],m[x]),o(e,h[w],h[_]),w--,x++;else if(void 0===b&&(b=l(g,x,k),v=l(p,_,w)),b.has(p[_]))if(b.has(p[w])){const t=v.get(g[x]),r=void 0!==t?h[t]:null;if(null===r){const t=n(e,h[_]);a(t,m[x]),f[x]=t}else f[x]=a(r,m[x]),o(e,r,h[_]),h[t]=null;x++}else s(h[w]),w--;else s(h[_]),_++;for(;x<=k;){const t=n(e,f[k+1]);a(t,m[x]),f[x++]=t}for(;_<=w;){const t=h[_++];null!==t&&s(t)}c.set(e,f),u.set(e,g)}})},69:function(t,e,r){"use strict";r.d(e,"a",function(){return a});r(3),r(100);var i=r(56),n=r(1);const a={properties:{noink:{type:Boolean,observer:"_noinkChanged"},_rippleContainer:{type:Object}},_buttonStateChanged:function(){this.focused&&this.ensureRipple()},_downHandler:function(t){i.b._downHandler.call(this,t),this.pressed&&this.ensureRipple(t)},ensureRipple:function(t){if(!this.hasRipple()){this._ripple=this._createRipple(),this._ripple.noink=this.noink;var e=this._rippleContainer||this.root;if(e&&Object(n.a)(e).appendChild(this._ripple),t){var r=Object(n.a)(this._rippleContainer||this),i=Object(n.a)(t).rootTarget;r.deepContains(i)&&this._ripple.uiDownAction(t)}}},getRipple:function(){return this.ensureRipple(),this._ripple},hasRipple:function(){return Boolean(this._ripple)},_createRipple:function(){return document.createElement("paper-ripple")},_noinkChanged:function(t){this.hasRipple()&&(this._ripple.noink=t)}}}}]);
//# sourceMappingURL=chunk.786f1aef13ef43a57230.js.map