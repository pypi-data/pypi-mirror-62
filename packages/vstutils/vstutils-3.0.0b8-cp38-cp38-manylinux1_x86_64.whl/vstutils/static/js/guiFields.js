let guiFields={};guiFields.base=class BaseField{constructor(options={}){this.options=options;this.mixins=this.constructor.mixins;}
toInner(data={}){return data[this.options.name];}
toRepresent(data={}){return data[this.options.name];}
validateValue(data={}){let value=data[this.options.name];let value_length=0;let samples=pop_up_msg.field.error;let title=(this.options.title||this.options.name).toLowerCase();let $t=_translate;if(value){value_length=value.toString().length;}
if(this.options.maxLength&&value_length>this.options.maxLength){throw{error:'validation',message:$t(samples.maxLength).format([$t(title),this.options.maxLength]),};}
if(this.options.minLength){if(value_length==0){if(!this.options.required){return;}
throw{error:'validation',message:$t(samples.empty).format([$t(title)]),};}
if(value_length<this.options.minLength){throw{error:'validation',message:$t(samples.minLength).format([$t(title),this.options.minLength]),};}}
if(this.options.max&&value>this.options.max){throw{error:'validation',message:$t(samples.max).format([$t(title),this.options.max]),};}
if(this.options.min&&value<this.options.min){throw{error:'validation',message:$t(samples.min).format([$t(title),this.options.min]),};}
if(value===undefined&&this.options.required&&this.options.default!==undefined){return this.options.default;}
if(value===undefined&&this.options.required&&!this.options.default){throw{error:'validation',message:$t(samples.required).format([$t(title)]),};}
if(this.validateValueCustom&&typeof this.validateValueCustom=='function'){return this.validateValueCustom(data);}
return value;}
_insertTestValue(data={}){let value=data[this.options.name];let format=this.options.format||this.options.type;let el=this._insertTestValue_getElement(format);$(el).val(value);this._insertTestValue_imitateEvent(el);}
_insertTestValue_getElement(format){let selector='.guifield-'+format+'-'+this.options.name+' input';return $(selector)[0];}
_insertTestValue_imitateEvent(el){el.dispatchEvent(new Event('input'));}
static get mixins(){return[gui_fields_mixins.base];}};guiFields.string=class StringField extends guiFields.base{};guiFields.textarea=class TextAreaField extends guiFields.base{_insertTestValue_getElement(format){let selector='.guifield-'+format+'-'+this.options.name+' textarea';return $(selector)[0];}
static get mixins(){return super.mixins.concat(gui_fields_mixins.textarea);}};guiFields.integer=class IntegerField extends guiFields.base{toInner(data={}){let value=data[this.options.name];if(value===undefined){return;}
let val=Number(value);if(isNaN(val)){console.error("Error in integer.toInner()");return;}
return val;}
static get mixins(){return super.mixins.concat(gui_fields_mixins.integer);}};guiFields.int32=class Int32Field extends guiFields.integer{};guiFields.int64=class Int64Field extends guiFields.integer{};guiFields.double=class DoubleField extends guiFields.integer{};guiFields.number=class NumberField extends guiFields.integer{};guiFields.float=class FloatField extends guiFields.integer{};guiFields.boolean=class BooleanField extends guiFields.base{_getValue(data={}){let value=data[this.options.name];if(typeof value=='boolean'){return value;}
if(typeof value=='string'){return stringToBoolean(value);}
if(typeof value=='number'){return Boolean(value);}}
toInner(data={}){return this._getValue(data);}
toRepresent(data={}){return this._getValue(data);}
_insertTestValue(data){let value=data[this.options.name];let format=this.options.format||this.options.type;let el=this._insertTestValue_getElement(format);this._insertTestValue_imitateEvent(el);if($(el).hasClass('selected')==value){this._insertTestValue_imitateEvent(el);}}
_insertTestValue_getElement(format){let selector='.guifield-'+format+'-'+this.options.name+' .boolean-select';return $(selector)[0];}
_insertTestValue_imitateEvent(el){$(el).trigger('click');}
static get mixins(){return super.mixins.concat(gui_fields_mixins.boolean);}};guiFields.choices=class ChoicesField extends guiFields.string{_getValue(data={}){let value=data[this.options.name];if(!value){return;}
if(this.options.enum&&this.options.enum.includes(value)){return value;}
console.error("There is no appropriate choice in enum list");}
toInner(data={}){return this._getValue(data);}
toRepresent(data={}){return this._getValue(data);}
_insertTestValue_getElement(format){let selector='.guifield-'+format+'-'+this.options.name+' select';return $(selector)[0];}
_insertTestValue_imitateEvent(el){el.dispatchEvent(new Event('change'));}
static get mixins(){return super.mixins.concat(gui_fields_mixins.choices);}};guiFields.autocomplete=class AutocompleteField extends guiFields.string{_insertTestValue_imitateEvent(el){el.dispatchEvent(new Event('blur'));}
static get mixins(){return super.mixins.concat(gui_fields_mixins.autocomplete);}};guiFields.password=class PasswordField extends guiFields.string{static get mixins(){return super.mixins.concat(gui_fields_mixins.password);}};guiFields.email=class EmailField extends guiFields.string{static get mixins(){return super.mixins.concat(gui_fields_mixins.email);}
static get validation_reg_exp(){return /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;}
validateValue(data={}){let value=super.validateValue(data);if(this.options.required&&!this.constructor.validation_reg_exp.test(String(value))){let title=(this.options.title||this.options.name).toLowerCase();let $t=_translate;let err_msg='<b>"{0}"</b> field should be written in <b>"example@mail.com"</b> format.';throw{error:'validation',message:$t(err_msg).format([$t(title)]),};}
return value;}};guiFields.file=class FileField extends guiFields.textarea{static get mixins(){return super.mixins.concat(gui_fields_mixins.file);}};guiFields.secretfile=class SecretFileField extends guiFields.file{};guiFields.binfile=class BinFileField extends guiFields.file{static get mixins(){return super.mixins.concat(gui_fields_mixins.binfile);}
toBase64(data={}){let value=data[this.options.name];if(value!==undefined){return arrayBufferToBase64(value);}}};guiFields.namedbinfile=class NamedBinFileField extends guiFields.binfile{static get mixins(){return super.mixins.concat(gui_fields_mixins.namedbinfile);}
validateValue(data={}){let value=super.validateValue(data);if(value&&this.options.required&&value.name===null&&value.content===null){let title=(this.options.title||this.options.name).toLowerCase();let $t=_translate;throw{error:'validation',message:$t(pop_up_msg.field.error.empty).format($t(title)),};}
return value;}};guiFields.namedbinimage=class NamedBinImageField extends guiFields.namedbinfile{static get mixins(){return super.mixins.concat(gui_fields_mixins.namedbinimage);}};guiFields.multiplenamedbinfile=class MultipleNamedBinFileField extends guiFields.namedbinfile{static get mixins(){return super.mixins.concat(gui_fields_mixins.multiplenamedbinfile);}
validateValue(data={}){let value=super.validateValue(data);if(value&&this.options.required&&Array.isArray(value)&&value.length===0){let title=(this.options.title||this.options.name).toLowerCase();let $t=_translate;throw{error:'validation',message:$t(pop_up_msg.field.error.empty).format($t(title)),};}
return value;}};guiFields.multiplenamedbinimage=class MultipleNamedBinImageField extends guiFields.multiplenamedbinfile{static get mixins(){return super.mixins.concat(gui_fields_mixins.multiplenamedbinimage);}};guiFields.text_paragraph=class TextParagraphField extends guiFields.base{toRepresent(data={}){let value=data[this.options.name];if(value===undefined){return this.options.default;}
if(typeof value=='object'){if(Array.isArray(value)){return value.join(" ");}
return JSON.stringify(value);}
return value;}
static get mixins(){return super.mixins.concat(gui_fields_mixins.text_paragraph);}};guiFields.plain_text=class PlainTextField extends guiFields.textarea{static get mixins(){return super.mixins.concat(gui_fields_mixins.plain_text);}};guiFields.html=class HtmlField extends guiFields.plain_text{static get mixins(){return super.mixins.concat(gui_fields_mixins.html);}};guiFields.date=class DateField extends guiFields.base{_getValue(data={}){let value=data[this.options.name];if(!value){return;}
return moment(value).format("YYYY-MM-DD");}
toInner(data={}){return this._getValue(data);}
toRepresent(data={}){return this._getValue(data);}
static get mixins(){return super.mixins.concat(gui_fields_mixins.date);}};guiFields.date_time=class DateTimeField extends guiFields.base{toInner(data={}){let value=data[this.options.name];if(!value){return;}
return moment(value).tz(app.api.getTimeZone()).format();}
toRepresent(data={}){let value=data[this.options.name];if(!value){return;}
let m=moment(moment.tz(value,app.api.getTimeZone())).tz(moment.tz.guess());return m.format("YYYY-MM-DD")+'T'+m.format("HH:mm");}
static get mixins(){return super.mixins.concat(gui_fields_mixins.date_time);}};guiFields.uptime=class UptimeField extends guiFields.base{constructor(options={}){super(options);this.reg_exp_arr=[XRegExp(`(?<y>[0-9]+)[y] (?<m>[0-9]+)[m] (?<d>[0-9]+)[d] (?<hh>[0-9]+):(?<mm>[0-9]+):(?<ss>[0-9]+)`),XRegExp(`(?<m>[0-9]+)[m] (?<d>[0-9]+)[d] (?<hh>[0-9]+):(?<mm>[0-9]+):(?<ss>[0-9]+)`),XRegExp(`(?<d>[0-9]+)[d] (?<hh>[0-9]+):(?<mm>[0-9]+):(?<ss>[0-9]+)`),XRegExp(`(?<hh>[0-9]+):(?<mm>[0-9]+):(?<ss>[0-9]+)`),];}
toInner(data={}){let value=data[this.options.name];if(!value){return;}
if(!isNaN(Number(value))){return Number(value);}
let uptime_in_seconds=0;for(let index=0;index<this.reg_exp_arr.length;index++){let time_parts=XRegExp.exec(value,this.reg_exp_arr[index]);if(!time_parts){continue;}
let duration_obj={seconds:Number(time_parts.ss),minutes:Number(time_parts.mm),hours:Number(time_parts.hh),days:Number(time_parts.d||0),months:Number(time_parts.m||0),years:Number(time_parts.y||0),};uptime_in_seconds=moment.duration(duration_obj).asSeconds();return uptime_in_seconds;}
return uptime_in_seconds;}
toRepresent(data={}){return getTimeInUptimeFormat(data[this.options.name]);}
_insertTestValue_imitateEvent(el){el.dispatchEvent(new Event('blur'));}
static get mixins(){return super.mixins.concat(gui_fields_mixins.uptime);}};guiFields.time_interval=class TimeIntervalField extends guiFields.integer{toInner(data={}){let value=data[this.options.name];if(!value){return;}
if(typeof value=='object'&&value.value){return value.value;}
return value;}
_toInner(data={}){let value=data[this.options.name];if(!value){return;}
return value*1000;}
toRepresent(data={}){let value=data[this.options.name];if(!value){return;}
if(typeof value=='object'&&value.represent_value){return value.represent_value;}
return value/1000;}
static get mixins(){return super.mixins.concat(gui_fields_mixins.time_interval);}};guiFields.crontab=class CrontabField extends guiFields.base{_getValue(data={}){let value=data[this.options.name];if(!value){return"* * * * *";}
return value;}
toInner(data={}){return this._getValue(data);}
toRepresent(data={}){return this._getValue(data);}
_insertTestValue_imitateEvent(el){el.dispatchEvent(new Event('blur'));}
static get mixins(){return super.mixins.concat(gui_fields_mixins.crontab);}};guiFields.json=class JsonField extends guiFields.base{generateRealFields(value={}){let realFields={};for(let field in value){if(value.hasOwnProperty(field)){let opt={name:field,readOnly:this.options.readOnly||false,title:field,format:'string',};if(typeof value[field]=='boolean'){opt.format='boolean';}
realFields[field]=new guiFields[opt.format](opt);}}
return realFields;}
static get mixins(){return super.mixins.concat(gui_fields_mixins.json);}};let fk_and_api_object_mixin=(Class_name)=>class extends Class_name{static findQuerySetSecondLevelPaths(model_name){let views=app.views;let paths=Object.keys(views).filter(item=>{if(views[item].schema.level==2){return item;}}).sort((a,b)=>{return b.length-a.length;});for(let index=0;index<paths.length;index++){let p=paths[index];if(views[p].objects.model.name==model_name){return views[p].objects.clone();}}}};guiFields.api_object=class ApiObjectField extends fk_and_api_object_mixin(guiFields.base){static get mixins(){return super.mixins.concat(gui_fields_mixins.api_object);}
static prepareField(field,path){let constructor=new ViewConstructor(openapi_dictionary,app.models);let model=constructor.getViewSchema_model(field.options);if(!model){return field;}
let new_format='api_'+model.name.toLowerCase();if(guiFields[new_format]){let opt=$.extend(true,{},field.options,{format:new_format});let new_field=new guiFields[new_format](opt);if(guiFields[new_format].prepareField){return guiFields[new_format].prepareField(new_field,path);}
return new_field;}
field.options.querysets=[this.findQuerySetSecondLevelPaths(model.name)];return field;}};guiFields.fk=class FkField extends fk_and_api_object_mixin(guiFields.base){prefetchDataOrNot(data){return true;}
makeLinkOrNot(data){return true;}
getObjectBulk(raw_data,qs_url){let dt=this.getQuerySetFormattedUrl(raw_data).replace(/^\/|\/$/g,"").split('/');return{data_type:dt,id:raw_data[this.options.name],};}
getAppropriateQuerySet(data,querysets){let qs=querysets;if(!qs){qs=this.options.additionalProperties.querysets;}
return qs[0];}
getQuerySetFormattedUrl(data,params,queryset){if(!queryset){queryset=this.getAppropriateQuerySet(data);}
let url=queryset.url;url=this.formatQuerySetUrl(url,data,params);return url;}
formatQuerySetUrl(url="",data={},params={}){if(url.indexOf('{')==-1){return url;}
return url.format(this.getUrlParams(url,data,params));}
getUrlParams(url,data,params){if(Object.entries(params).length!==0){return params;}
if(app&&app.application&&app.application.$route){return app.application.$route.params||{};}
return{};}
getValueField(data={}){return this.options.additionalProperties.value_field;}
getViewField(data={}){return this.options.additionalProperties.view_field;}
isPrefetchDataForMe(data={},prefetch_data={}){return data[this.options.name]==prefetch_data[this.getPrefetchFilterName(data)];}
getPrefetchValue(data={},prefetch_data={}){return{value:data[this.options.name],prefetch_value:prefetch_data[this.getViewField()],};}
getAutocompleteValue(data={},autocomplete_data={}){return{value_field:autocomplete_data[this.getValueField(data)],view_field:autocomplete_data[this.getViewField(data)],};}
getPrefetchFilterName(data={}){return this.getValueField(data);}
getAutocompleteFilterName(data={}){return this.getViewField(data);}
toInner(data={}){let value=data[this.options.name];if(value&&typeof value=="object"){return value.value;}
return value;}
toRepresent(data={}){let value=data[this.options.name];if(value&&typeof value=="object"){return value.prefetch_value;}
return value;}
_insertTestValue(data={}){let val=data[this.options.name];let value;let format=this.options.format||this.options.type;let el=this._insertTestValue_getElement(format);if(val&&val.prefetch_value&&val.value){value=val;}else{value={value:value,prefetch_value:value,};}
let newOption=new Option(value.prefetch_value,value.value,false,false);$(el).append(newOption);this._insertTestValue_imitateEvent(el);}
_insertTestValue_getElement(format){let selector='.guifield-'+format+'-'+this.options.name+' select';return $(selector)[0];}
_insertTestValue_imitateEvent(el){el.dispatchEvent(new Event('change'));}
static get mixins(){return super.mixins.concat(gui_fields_mixins.fk);}
static prepareField(field,path){let props=field.options.additionalProperties;if(!props){return field;}
if(props.querysets){return field;}
if(props.list_paths){props.querysets=[];for(let index=0;index<props.list_paths.length;index++){props.querysets.push(this.getQuerySetByPath(props.list_paths[index]));}
return field;}
if(!props.model){return field;}
let constructor=new ViewConstructor(openapi_dictionary,app.models);let model=constructor.getViewSchema_model(props);if(!model){return field;}
props.querysets=[this.findQuerySet(path,model.name)];return field;}
static getQuerySetByPath(path){if(!app.views[path]){return;}
return app.views[path].objects.clone();}
static findQuerySet(path,model_name){let qs=this.findQuerySetInCurrentPath(path,model_name);if(qs){return qs;}
qs=this.findQuerySetInNeighbourPaths(path,model_name);if(qs){return qs;}
return this.findQuerySetSecondLevelPaths(model_name);}
static findQuerySetInCurrentPath(path,model_name){if(app.views[path]&&app.views[path].objects.model.name==model_name){return app.views[path].objects.clone();}}
static findQuerySetInNeighbourPaths(path,model_name){let views=app.views;let num=path.replace(/^\/|\/$/g,"").split("/").length;let level=views[path].schema.level;let path1=path.split("/").slice(0,-2).join("/")+"/";function func(item){if(item.indexOf(path1)!=-1&&views[item].schema.type=="list"&&views[item].schema.level<=level){return item;}}
function func1(item){if(views[item].objects.model.name==model_name){return item;}}
for(num;num>0;num--){path1=path1.split("/").slice(0,-2).join("/")+"/";let paths=Object.keys(views).filter(func).sort((a,b)=>{return b.length-a.length;});let paths_with_model=paths.filter(func1);let closest_path=findClosestPath(paths_with_model,path);if(closest_path){return views[closest_path].objects.clone();}}}};guiFields.multiselect=class MultiSelect extends guiFields.fk{static get mixins(){return super.mixins.concat(gui_fields_mixins.multiselect);}
prefetchDataOrNot(data={}){return false;}
toInner(data={}){let value=data[this.options.name];if(value&&typeof value=="object"&&Array.isArray(value)){return value.map(item=>{return item.value;}).join(this.options.additionalProperties.view_separator);}
return value;}
toRepresent(data={}){let value=data[this.options.name];if(value&&typeof value=="object"&&Array.isArray(value)){return value.map(item=>{return item.prefetch_value;}).join(this.options.additionalProperties.view_separator);}
return value;}};guiFields.fk_autocomplete=class FkAutocompleteField extends guiFields.fk{_insertTestValue(data={}){let value=data[this.options.name];let format=this.options.format||this.options.type;let el=this._insertTestValue_getElement(format);$(el).val(value);this._insertTestValue_imitateEvent(el);}
_insertTestValue_getElement(format){let selector='.guifield-'+format+'-'+this.options.name+' input';return $(selector)[0];}
_insertTestValue_imitateEvent(el){el.dispatchEvent(new Event('blur'));}
static get mixins(){return super.mixins.concat(gui_fields_mixins.fk_autocomplete);}};guiFields.fk_multi_autocomplete=class FkMultiAutocompleteField extends guiFields.fk_autocomplete{static get mixins(){return super.mixins.concat(gui_fields_mixins.fk_multi_autocomplete);}};guiFields.color=class ColorField extends guiFields.base{static get mixins(){return super.mixins.concat(gui_fields_mixins.color);}
_getValue(data={}){let value=data[this.options.name];if(!value){return"#000000";}
return value;}
toInner(data={}){return this._getValue(data);}
toRepresent(data={}){return this._getValue(data);}};guiFields.inner_api_object=class InnerApiObjectField extends guiFields.base{static get mixins(){return super.mixins.concat(gui_fields_mixins.inner_api_object);}
static getModel(field){let constructor=new ViewConstructor(openapi_dictionary,app.models);return constructor.getViewSchema_model(field.options);}
static prepareField(field,path){let model=this.getModel(field);if(!model){console.error("Model was not found in static method 'prepareField'"+
" of guiFields.inner_api_object class");return field;}
let realFields={};for(let key in model.fields){if(model.fields.hasOwnProperty(key)){let inner_field=model.fields[key];let inner_model=this.getModel(inner_field);realFields[key]={};for(let item in inner_model.fields){if(Object.keys(inner_model.fields).length==1){let f=inner_model.fields[item];let opt=$.extend(true,{required:field.options.required},f.options,{title:'{0} - {1}'.format(key,item)},);realFields[key][item]=new guiFields[f.options.format](opt);}else{realFields[key][item]=inner_model.fields[item];realFields[key][item].options=$.extend(true,{required:field.options.required},inner_model.fields[item].options,);}}}}
field.options.realFields=realFields;return field;}
validateValue(data={}){let val=data[this.options.name]||{};let valid={};for(let key in this.options.realFields){if(this.options.realFields.hasOwnProperty(key)){valid[key]={};for(let item in this.options.realFields[key]){if(this.options.realFields[key].hasOwnProperty(item)){valid[key][item]=this.options.realFields[key][item].validateValue(val[key]);}}}}
return valid;}};guiFields.api_data=class ApiDataField extends guiFields.base{};guiFields.dynamic=class DynamicField extends guiFields.base{static get mixins(){return super.mixins.concat(gui_fields_mixins.dynamic);}
toInner(data={}){return this.getRealField(data).toInner(data);}
toRepresent(data={}){return this.getRealField(data).toRepresent(data);}
validateValue(data={}){return this.getRealField(data).validateValue(data);}
_insertTestValue(data={}){let real_field=this.getRealField(data);setTimeout(()=>{real_field._insertTestValue(data);},20);}
_getParentFields(){let p_f=this.options.additionalProperties.field||[];if(Array.isArray(p_f)){return p_f;}
return[p_f];}
_getParentTypes(){return this.options.additionalProperties.types||{};}
_getParentChoices(){return this.options.additionalProperties.choices||{};}
_getParentValues(data={}){let parent_fields=this._getParentFields();let parent_values={};parent_fields.forEach(item=>{parent_values[item]=data[item];});return parent_values;}
getRealField(data={}){let parent_values=this._getParentValues(data);let parent_types=this._getParentTypes();let parent_choices=this._getParentChoices();let opt={format:undefined,};for(let key in parent_values){if(parent_values.hasOwnProperty(key)){let item=parent_types[parent_values[key]];if(item!==undefined){opt.format=item;}}}
for(let key in parent_values){if(parent_values.hasOwnProperty(key)){let item=parent_choices[parent_values[key]];if(item!==undefined&&Array.isArray(item)){let bool_values=item.some((val)=>{if(typeof val=='boolean'){return val;}});if(bool_values){opt.format='boolean';}else{opt.enum=item;opt.format='choices';}}}}
for(let key in this.options){if(this.options.hasOwnProperty(key)){if(['format','additionalProperties'].includes(key)){continue;}
opt[key]=this.options[key];}}
let callback_opt={};if(this.options.additionalProperties.callback){callback_opt=this.options.additionalProperties.callback(parent_values);}
opt=$.extend(true,opt,callback_opt);if(!guiFields[opt.format]){opt.format='string';}
let real_field=new guiFields[opt.format](opt);if(real_field.constructor.prepareField){real_field=real_field.constructor.prepareField(real_field,app.application.$route.name);}
return real_field;}};guiFields.hidden=class HiddenField extends guiFields.base{static get mixins(){return super.mixins.concat(gui_fields_mixins.hidden);}};guiFields.form=class FormField extends guiFields.base{constructor(options={}){super(options);}
_getValue(data,method){let val={};let realFields=this.generateRealFields();for(let key in realFields){if(realFields.hasOwnProperty(key)){let real_value=realFields[key][method](data[this.options.name]);if(real_value!==undefined){val[key]=real_value;}}}
return val;}
toInner(data={}){return this._getValue(data,'toInner');}
toRepresent(data={}){return this._getValue(data,'toInner');}
validateValue(data={}){return this._getValue(data,'validateValue');}
generateRealFields(){let realFields={};if(this.options.form){let constructor=new BaseEntityConstructor(openapi_dictionary);for(let key in this.options.form){if(this.options.form.hasOwnProperty(key)){let field=this.options.form[key];field.name=key;field.format=constructor.getFieldFormat(field);realFields[key]=this.generateRealField(field);}}}
return realFields;}
generateRealField(options){let field=new guiFields[options.format](options);if(field.constructor.prepareField){field=field.constructor.prepareField(field,app.application.$route.name);}
return field;}
static get mixins(){return super.mixins.concat(gui_fields_mixins.form);}};guiFields.button=class ButtonField extends guiFields.base{static get mixins(){return super.mixins.concat(gui_fields_mixins.button);}};guiFields.string_array=class StringArrayField extends guiFields.textarea{static get mixins(){return super.mixins.concat(gui_fields_mixins.string_array);}};guiFields.string_id=class StringIdField extends guiFields.string{validateValueCustom(data={}){let value=data[this.options.name];let samples=pop_up_msg.field.error;let title=(this.options.title||this.options.name).toLowerCase();let exclude_values=['new','edit','remove'];let $t=_translate;if(value&&exclude_values.includes(value)){throw{error:'validation',message:$t(samples.invalid).format([value,$t(title)]),};}
return value;}
_getValue(data={}){let value=data[this.options.name];if(value!==undefined&&value!==null){return String(value).replace(/-/g,'_');}}
toInner(data={}){return this._getValue(data);}
toRepresent(data={}){return this._getValue(data);}};class GuiFieldComponentRegistrator{constructor(fields_classes){this.fields=fields_classes;}
registerFieldComponent(format,mixins){let component='field_'+format;if(Vue.options.components[component]){return;}
Vue.component(component,{mixins:mixins||[],});}
registerAllFieldsComponents(){for(let key in this.fields){if(this.fields.hasOwnProperty(key)){this.registerFieldComponent(key,this.fields[key].mixins);}}}}
let fieldsRegistrator=new GuiFieldComponentRegistrator(guiFields);