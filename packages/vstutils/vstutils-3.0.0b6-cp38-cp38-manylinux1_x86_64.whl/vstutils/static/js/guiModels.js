let guiModels={};guiModels.Model=class Model{constructor(name,fields){this.name=name;this.fields=fields;this.non_instance_attr=['non_instance_attr','constructor','getInstance'];if(!isEmptyObject(this.fields)){this.pk_name=Object.keys(this.fields)[0];for(let field in this.fields){if(this.fields[field].options.is_pk){this.pk_name=field;}}
this.view_name='name';}}
toInner(form_data=this.data){let data={};for(let item in form_data){if(this.fields[item]){data[item]=this.fields[item].toInner(form_data);}}
return data;}
toRepresent(api_data=this.data){let data={};for(let item in api_data){if(this.fields[item]){data[item]=this.fields[item].toRepresent(api_data);}}
return data;}
getPkValue(){if(this.fields[this.pk_name]){return this.fields[this.pk_name].toInner(this.data);}}
getViewFieldValue(){if(this.fields[this.view_name]){return this.fields[this.view_name].toRepresent(this.data);}}
delete(){let bulk=this.queryset.formBulkQuery('delete');if(bulk.data_type[bulk.data_type.length-1]!=this.getPkValue()){bulk.data_type.push(this.getPkValue());}
return this.queryset.sendQuery(bulk).then(response=>{return response;}).catch(error=>{debugger;throw error;});}
save(method="patch"){return this.queryset.formQueryAndSend(method,this.toInner(this.data)).then(response=>{return this.queryset.model.getInstance(response.data,this.queryset);}).catch(error=>{debugger;throw error;});}
getInstance(data,queryset){let instance={data:data,queryset:queryset,};for(let key in this){if(this.hasOwnProperty(key)){if(!this.non_instance_attr.includes(key)){instance[key]=this[key];}}}
let methods=obj_prop_retriever.getPrototypeNonenumerables(this,false);for(let index=0;index<methods.length;index++){let key=methods[index];if(!this.non_instance_attr.includes(key)){instance[key]=this[key];}}
return instance;}
getPrefetchFields(){let fields=[];for(let key in this.fields){if(this.fields.hasOwnProperty(key)){let field=this.fields[key];if(field instanceof guiFields.fk){fields.push(key);}}}
return fields;}};class ModelConstructor extends BaseEntityConstructor{constructor(openapi_dictionary,models_classes){super(openapi_dictionary);this.pk_names=['id'];this.classes=models_classes;}
getModelsList(openapi_schema){return openapi_schema[this.dictionary.models.name];}
getModelFieldsList(model){let required_fields=this.getModelRequiredFieldsList(model);let fields=model[this.dictionary.models.fields.name];for(let key in fields){if(required_fields.includes(key)){fields[key].required=true;}}
return fields;}
getModelRequiredFieldsList(model){return model[this.dictionary.models.required_fields.name]||[];}
getModelFieldFormat(field){return this.getFieldFormat(field);}
generateModelFields(model,model_name){let f_obj={};let fields=this.getModelFieldsList(model);tabSignal.emit("models["+model_name+"].fields.beforeInit",fields);for(let field in fields){if(fields.hasOwnProperty(field)){let format=this.getModelFieldFormat(fields[field]);let opt={name:field,format:format,};if(this.pk_names.includes(field)){opt.is_pk=true;}
f_obj[field]=new guiFields[format]($.extend(true,{},fields[field],opt));}}
tabSignal.emit("models["+model_name+"].fields.afterInit",f_obj);return f_obj;}
getModelsConstructor(model){if(this.classes[model+"Model"]){return this.classes[model+"Model"];}
return this.classes.Model;}
generateModels(openapi_schema){let store={};let models=this.getModelsList(openapi_schema);for(let model in models){if(models.hasOwnProperty(model)){let constructor=this.getModelsConstructor(model);store[model]=new constructor(model,this.generateModelFields(models[model],model),);tabSignal.emit("models["+model+"].created",{model:store[model]});}}
tabSignal.emit("allModels.created",{models:store});return store;}}