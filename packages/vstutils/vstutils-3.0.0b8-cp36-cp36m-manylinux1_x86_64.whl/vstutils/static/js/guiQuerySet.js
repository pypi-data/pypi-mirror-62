let guiQuerySets={};guiQuerySets.QuerySet=class QuerySet{constructor(model,url,query={}){this.model=model;this.url=url;this.query=query;this.use_prefetch=false;}
makeQueryString(query=this.query){let filters=[];for(let key in query){if(query.hasOwnProperty(key)){filters.push([key,query[key]].join('='));}}
return filters.join("&");}
getDataType(){return this.url.replace(/^\/|\/$/g,"").split("/");}
formBulkQuery(method,data){let query={method:method,data_type:this.getDataType(),};if(data){query.data=data;}
let filters=this.makeQueryString();if(filters.length>0){query.filters=filters;}
return query;}
formQueryAndSend(method,data){return this.sendQuery(this.formBulkQuery(method,data));}
sendQuery(bulk){return app.api.bulkQuery(bulk);}
clone(props={},save_cache=false){let clone=$.extend(true,{},this);clone.__proto__=this.__proto__;for(let key in props){if(props.hasOwnProperty(key)){clone[key]=props[key];}}
if(!save_cache){clone.clearCache();}
return clone;}
copy(props={}){return this.clone(props,true);}
all(){return this.clone();}
filter(filters){return this.clone({query:$.extend(true,{},this.query,filters),});}
exclude(filters){let ecd_filters={};for(let key in filters){if(filters.hasOwnProperty(key)){let ecd_key=key.indexOf("__not")==-1?key+"__not":key;ecd_filters[ecd_key]=filters[key];}}
return this.clone({query:$.extend(true,{},this.query,ecd_filters)});}
prefetch(instances=true){let qs=this.clone();if(instances){qs.use_prefetch=instances;}else{qs.use_prefetch=false;}
return qs;}
items(){if(this.cache){return Promise.resolve(this.cache);}
return this.formQueryAndSend('get').then(response=>{let instances=[];let data=response.data.results;let prefetch_fields=this._getPrefetchFields();for(let index=0;index<data.length;index++){instances.push(this.model.getInstance(data[index],this.clone()));}
if(prefetch_fields&&prefetch_fields.length>0){return this._loadPrefetchData(prefetch_fields,instances).then(()=>{this.api_count=response.data.count;this.cache=instances;return instances;});}
this.api_count=response.data.count;this.cache=instances;return instances;}).catch(error=>{debugger;throw error;});}
create(data){return this.formQueryAndSend('post',data).then(response=>{return this.model.getInstance(response.data,this.clone());}).catch(error=>{debugger;throw error;});}
delete(){this.items().then(instances=>{instances.forEach(instance=>{instance.delete();});}).catch(error=>{debugger;throw error;});}
get(){if(this.cache){return Promise.resolve(this.cache);}
return this.formQueryAndSend('get').then(response=>{let instance=this.model.getInstance(response.data,this);let prefetch_fields=this._getPrefetchFields();if(prefetch_fields&&prefetch_fields.length>0){return this._loadPrefetchData(prefetch_fields,[instance]).then(()=>{this.cache=instance;return instance;});}
this.cache=instance;return instance;}).catch(error=>{debugger;throw error;});}
clearCache(){delete this.cache;delete this.api_count;}
_getPrefetchFields(){if(Array.isArray(this.use_prefetch)){return this.use_prefetch;}else if(this.use_prefetch){return this.model.getPrefetchFields();}}
_getBulkDataForPrefetch(prefetch_fields,instances){let bulk_data={};for(let index=0;index<instances.length;index++){let instance=instances[index];this._getBulkDataForPrefetchForInstance(prefetch_fields,instance,bulk_data);}
return bulk_data;}
_getBulkDataForPrefetchForInstance(prefetch_fields,instance,bulk_data){for(let key in prefetch_fields){if(prefetch_fields.hasOwnProperty(key)){let field_name=prefetch_fields[key];let field=this.model.fields[field_name];let value=instance.data[field_name];if(value==null||value==undefined){continue;}
if(!field.prefetchDataOrNot(instance.data)){continue;}
let obj=field.getObjectBulk(instance.data,this.url);if(obj==undefined||typeof obj=='string'){continue;}
if(!bulk_data[field_name]){bulk_data[field_name]=[];}
let pushed=false;for(let item in bulk_data[field_name]){if(deepEqual(bulk_data[field_name][item].data_type,obj.data_type)){if(!bulk_data[field_name][item].filter_values.includes(obj.id)){bulk_data[field_name][item].filter_values.push(obj.id);}
if(!bulk_data[field_name][item].instances_ids.includes(instance.getPkValue())){bulk_data[field_name][item].instances_ids.push(instance.getPkValue());}
pushed=true;}}
if(!pushed){bulk_data[field_name].push({instances_ids:[instance.getPkValue()],data_type:obj.data_type,filter_name:field.getPrefetchFilterName(instance.data),filter_values:[obj.id],});}}}
return bulk_data;}
_loadPrefetchData(prefetch_fields,instances){let promises=[];let bulk_data=this._getBulkDataForPrefetch(prefetch_fields,instances);for(let key in bulk_data){if(bulk_data.hasOwnProperty(key)){for(let index=0;index<bulk_data[key].length;index++){let item=bulk_data[key][index];let filters={};filters[item.filter_name]=item.filter_values;let bulk={method:'get',data_type:item.data_type,filters:this.makeQueryString(filters),};promises.push(this.sendQuery(bulk).then(res=>{this._setPrefetchValue(res,item,instances,key);}).catch(error=>{debugger;}));}}}
return Promise.all(promises);}
_setPrefetchValue(res,bulk_data_item,instances,field_name){if(res.status!="200"){return;}
let prefetch_data=res.data.results;let field=this.model.fields[field_name];for(let index=0;index<instances.length;index++){let instance=instances[index];if(!bulk_data_item.instances_ids.includes(instance.getPkValue())){continue;}
for(let num=0;num<prefetch_data.length;num++){if(field.isPrefetchDataForMe(instance.data,prefetch_data[num])){instance.data[field_name]=field.getPrefetchValue(instance.data,prefetch_data[num]);}}}}};