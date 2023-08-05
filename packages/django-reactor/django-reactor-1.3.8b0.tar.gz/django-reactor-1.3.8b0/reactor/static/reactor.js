(function(){var FOCUSABLE_INPUTS,ReactorChannel,TRANSPILER_CACHE,_timeouts,debounce,declare_components,load_page,merge_objects,origin,reactor,reactor_channel,transpile,indexOf=[].indexOf;origin=new Date();FOCUSABLE_INPUTS=['text','textarea','number','email','password','search','tel','url'];ReactorChannel=class ReactorChannel{constructor(url1='/reactor',retry_interval=100){this.on=this.on.bind(this);this.url=url1;this.retry_interval=retry_interval;this.online=false;this.callbacks={};this.original_retry_interval=this.retry_interval;}
on(event_name,callback){return this.callbacks[event_name]=callback;}
trigger(event_name,...args){var base;return typeof(base=this.callbacks)[event_name]==="function"?base[event_name](...args):void 0;}
open(){var protocol,ref;if(this.retry_interval<10000){this.retry_interval+=1000;}
if(navigator.onLine){if((ref=this.websocket)!=null){ref.close();}
if(window.location.protocol==='https:'){protocol='wss://';}else{protocol='ws://';}
this.websocket=new WebSocket(`${protocol}${window.location.host}${this.url}`);this.websocket.onopen=(event)=>{this.online=true;this.trigger('open',event);return this.retry_interval=this.original_retry_interval;};this.websocket.onclose=(event)=>{this.online=false;this.trigger('close',event);return setTimeout((()=>{return this.open();}),this.retry_interval||0);};return this.websocket.onmessage=(event)=>{var data;data=JSON.parse(event.data);return this.trigger('message',data);};}else{return setTimeout((()=>{return this.open();}),this.retry_interval);}}
send(command,payload){var data;data={command:command,payload:payload};if(this.online){try{return this.websocket.send(JSON.stringify(data));}catch(error){return console.log('Failed sending');}}}
reconnect(){var ref;this.retry_interval=0;return(ref=this.websocket)!=null?ref.close():void 0;}
close(){var ref;console.log('CLOSE');return(ref=this.websocket)!=null?ref.close():void 0;}};reactor_channel=new ReactorChannel();reactor_channel.on('open',function(){var el,i,len,ref,results;console.log('ON-LINE');ref=document.querySelectorAll('[is]');results=[];for(i=0,len=ref.length;i<len;i++){el=ref[i];el.classList.remove('reactor-disconnected');results.push(typeof el.connect==="function"?el.connect():void 0);}
return results;});reactor_channel.on('close',function(){var el,i,len,ref,results;console.log('OFF-LINE');ref=document.querySelectorAll('[is]');results=[];for(i=0,len=ref.length;i<len;i++){el=ref[i];results.push(el.classList.add('reactor-disconnected'));}
return results;});reactor_channel.on('message',function({type,id,html_diff,url,component_types}){var el;console.log('<<<',type.toUpperCase(),id||url||component_types);if(type==='components'){return declare_components(component_types);}else if(type==='redirect'){return window.location.assign(url);}else if(type==='push_state'){return reactor.push_state(url);}else{el=document.getElementById(id);if(el!=null){if(type==='render'){return el.apply_diff(html_diff);}else if(type==='remove'){return window.requestAnimationFrame(function(){return el.remove();});}}}});TRANSPILER_CACHE={};transpile=function(el){var attr,cache_key,code,i,j,l,len,len1,len2,method_args,method_name,modifier,modifiers,name,nu_attr,old_name,ref,ref1,replacements,results,start;if(el.attributes===void 0){return;}
replacements=[];ref=el.attributes;for(i=0,len=ref.length;i<len;i++){attr=ref[i];if(attr.name===':load'){replacements.push({nane:'onclick',code:'event.preventDefault(); reactor.push_state(this.href);'});}else if(attr.name.startsWith('@')){[name,...modifiers]=attr.name.split('.');start=attr.value.indexOf(' ');if(start!==-1){method_name=attr.value.slice(0,start);method_args=attr.value.slice(start+1);}else{method_name=attr.value;method_args='null';}
cache_key=`${modifiers}.${method_name}.${method_args}`;code=TRANSPILER_CACHE[cache_key];if(!code){if(method_name===''){code='';}else{code=`reactor.send(this, '${method_name}', ${method_args});`;}
ref1=modifiers.reverse();for(j=0,len1=ref1.length;j<len1;j++){modifier=ref1[j];modifier=modifier==='space'?' ':modifier;switch(modifier){case"prevent":code="event.preventDefault(); "+code;break;case"ctrl":code=`if (event.ctrlKey) { ${code} }`;break;case"alt":code=`if (event.altKey) { ${code} }`;break;default:code=`if (event.key.toLowerCase() == '${modifier}') { ${code} }; `;}}
TRANSPILER_CACHE[cache_key]=code;}
replacements.push({old_name:attr.name,name:'on'+name.slice(1),code:code});}}
results=[];for(l=0,len2=replacements.length;l<len2;l++){({old_name,name,code}=replacements[l]);if(old_name){el.attributes.removeNamedItem(old_name);}
nu_attr=document.createAttribute(name);nu_attr.value=code;results.push(el.attributes.setNamedItem(nu_attr));}
return results;};declare_components=function(component_types){var Component,base_element,base_html_element,component_name,results;results=[];for(component_name in component_types){base_html_element=component_types[component_name];if(customElements.get(component_name)){continue;}
base_element=document.createElement(base_html_element);Component=class Component extends base_element.constructor{constructor(...args){super(...args);this.tag_name=this.getAttribute('is');this._last_received_html='';}
connectedCallback(){return this.connect();}
disconnectedCallback(){return reactor_channel.send('leave',{id:this.id});}
is_root(){return!this.parent_component();}
parent_component(){var component;component=this.parentElement;while(component){if(component.getAttribute('is')){return component;}
component=component.parentElement;}}
connect(){var state;if(this.is_root()){console.log('>>> JOIN',this.tag_name);state=JSON.parse(this.getAttribute('state'));return reactor_channel.send('join',{tag_name:this.tag_name,state:state});}}
apply_diff(html_diff){var cursor,diff,html,i,len;console.log(`${new Date() - origin}ms`);html=[];cursor=0;for(i=0,len=html_diff.length;i<len;i++){diff=html_diff[i];if(typeof diff==='string'){html.push(diff);}else if(diff<0){cursor-=diff;}else{html.push(this._last_received_html.slice(cursor,cursor+diff));cursor+=diff;}}
html=html.join('');if(this._last_received_html!==html){this._last_received_html=html;return window.requestAnimationFrame(()=>{var ref;morphdom(this,html,{onNodeAdded:transpile,onBeforeElUpdated:function(from_el,to_el){var ref;if(from_el.hasAttribute('reactor-once')){return false;}
if((ref=from_el.type,indexOf.call(FOCUSABLE_INPUTS,ref)>=0)&&from_el===document.activeElement&&indexOf.call(to_el.getAttributeNames(),'reactor-override-value')<0){transpile(to_el);to_el.getAttributeNames().forEach(function(name){return from_el.setAttribute(name,to_el.getAttribute(name));});from_el.readOnly=to_el.readOnly;return false;}
transpile(to_el);return true;}});return(ref=this.querySelector('[reactor-focus]:not([disabled])'))!=null?ref.focus():void 0;});}}
dispatch(name,form,args){var state;if(args){state=args;}else{state=this.serialize(form||this);}
state['id']=this.id;console.log('>>> USER_EVENT',this.tag_name,name,state);origin=new Date();return reactor_channel.send('user_event',{name:name,state:state});}
serialize(form){var checked,i,j,len,len1,name,obj,part,ref,ref1,state,type,value;state={id:this.id};ref=form.querySelectorAll('[name]');for(i=0,len=ref.length;i<len;i++){({type,name,value,checked}=ref[i]);value=type==='checkbox'?checked:value;ref1=name.split('.').reverse();for(j=0,len1=ref1.length;j<len1;j++){part=ref1[j];obj={};if(part.endsWith('[]')){obj[part.slice(0,-2)]=[value];}else{obj[part]=value;}
value=obj;}
state=merge_objects(state,value);}
return state;}};results.push(customElements.define(component_name,Component,{extends:base_html_element}));}
return results;};merge_objects=function(target,source){var k,target_value,v;for(k in source){v=source[k];target_value=target[k];if(Array.isArray(target_value)){target_value.push(...v);}else if(typeof target_value==='object'){merge_objects(target_value,v);}else{target[k]=v;}}
return target;};window.reactor=reactor={};reactor.send=function(element,name,args){var first_form_found;first_form_found=null;while(element){if(first_form_found===null&&element.tagName==='FORM'){first_form_found=element;}
if(element.dispatch!=null){return element.dispatch(name,first_form_found,args);}
element=element.parentElement;}};_timeouts={};debounce=function(delay_name,delay){return function(...args){clearTimeout(_timeouts[delay_name]);return _timeouts[delay_name]=setTimeout((()=>{return window.send(...args);}),delay);};};reactor.push_state=function(url){if(history.pushState!=null){return load_page(url,true);}else{return window.location.assign(url);}};window.addEventListener('popstate',function(){return load_page(window.location.href);});load_page=function(url,push=true){var utf8_decoder;console.log('GOTO',url);utf8_decoder=new TextDecoder("utf-8");return fetch(url).then(async function(response){var done,html,reader,result,value;if(response.redirected){return load_page(response.url);}else{history.pushState({},'',url);reader=(await response.body.getReader());done=false;result=[];while(!done){({done,value}=(await reader.read()));value=value?utf8_decoder.decode(value):'';result.push(value);}
html=result.join('').trim();return window.requestAnimationFrame(function(){var ref;morphdom(document.documentElement,html);return(ref=document.querySelector('[autofocus]:not([disabled])'))!=null?ref.focus():void 0;});}});};reactor_channel.open();}).call(this);