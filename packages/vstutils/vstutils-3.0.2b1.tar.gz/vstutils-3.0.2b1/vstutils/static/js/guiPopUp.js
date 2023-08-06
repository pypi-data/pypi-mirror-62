class PopUp{constructor(options){this.options={default:{maxWidth:500,position:"topRight"},info:{title:"Info"},success:{title:"OK"},warning:{title:"Caution"},error:{title:"Error"},question:{timeout:false,close:true,overlay:true,position:'center',displayMode:'once',zindex:2999,title:'Question',},};this.options=Object.assign(this.options,options);}
_getPopUpSettings(key,opt={}){let base=this.options['default']||{};let custom=this.options[key]||{};return Object.assign({},base,custom,opt);}
_showPopUp(type,opt){if(!iziToast[type]){type="show";}
return iziToast[type](opt);}
_generatePopUp(type="show",message="",opt={}){opt.message=message;return this._showPopUp(type,this._getPopUpSettings(type,opt));}
default(message="",opt={}){return this._generatePopUp("show",message,opt);}
info(message="",opt={}){return this._generatePopUp("info",message,opt);}
success(message="",opt={}){return this._generatePopUp("success",message,opt);}
warning(message="",opt={}){return this._generatePopUp("warning",message,opt);}
error(message="",opt={}){return this._generatePopUp("error",message,opt);}
question(message="",answer_buttons=[],opt={}){let buttons=[];let success,fail;let answer=new Promise((resolve,reject)=>{success=resolve;fail=reject;});answer_buttons.forEach(button=>{buttons.push(['<button>'+button+'</button>',(instance,toast)=>{instance.hide({transitionOut:"fadeOut"},toast,button);},]);});let options={buttons:buttons,onClosed:(instance,toast,closedBy)=>{if(answer_buttons.includes(closedBy)){return success(closedBy);}
return fail(closedBy);}};options=Object.assign(options,opt);this._generatePopUp("question",message,options);return answer;}}
let guiPopUp=new PopUp();let pop_up_msg={instance:{success:{add:'Child "<b>{0}</b>" instance was successfully added to parent list.',create:'New "<b>{0}</b>" instance was successfully created.',remove:'<b>{1}</b> "<b>{0}</b>" was successfully removed.',save:'Changes in <b>{1}</b> "<b>{0}</b>" were successfully saved.',execute:'Action "<b>{0}</b>" was successfully executed'+
' on "<b>{1}</b>".',},error:{add:'Some error occurred during adding of child "<b>{0}</b>" instance'+
' to parent list.'+'<br> Error details: {1}',create:'Some error occurred during new "<b>{0}</b>" instance creation.'+
'<br> Error details: {1}',remove:'Some error occurred during remove process of <b>{1}</b>  "<b>{0}</b>".'+
'<br> Error details: {2}',save:'Some error occurred during saving process of <b>{1}</b> "<b>{0}</b>".'+
'<br> Error details: {2}',execute:'Some error occurred during "<b>{0}</b>" action execution on <b>{1}</b>.'+
'<br> Error details: {2}',},},field:{error:{empty:'Field "<b>{0}</b>" is empty.',required:'Field "<b>{0}</b>" is required.',minLength:'Field "<b>{0}</b>" is too short.'+
'<br> Field length should not be shorter, than {1}.',maxLength:'Field "<b>{0}</b>" is too long. '+
'<br> Field length should not be longer, than {1}.',min:'Field "<b>{0}</b>" is too small.'+
'<br> Field should not be smaller, than {1}.',max:'Field "<b>{0}</b>" is too big.'+
'<br> Field should not be bigger, than {1}.',invalid:'<b>{0} </b> value is not valid for <b>{1}</b> field.',},},};class ErrorHandler{constructor(){}
errorDetailHandler(detail){let error_msg="";for(let key in detail){if(detail.hasOwnProperty(key)){let detail_msg=detail[key];if(Array.isArray(detail_msg)){detail_msg=detail_msg.join('<br>');}
error_msg+="<b>{0}</b>:<br>{1}".format(key,detail_msg);}}
return error_msg;}
errorToString(error){let result="Unknown error";debugger;if(!error){return result;}
if(typeof error=='string'){return error;}
if(typeof error=='object'&&error.message){return error.message;}
if(typeof error=='object'&&error.data){if(error.data.detail&&typeof error.data.detail=="string"){return error.data.detail;}else if(error.data.detail&&typeof error.data.detail=='object'){return this.errorDetailHandler(error.data.detail);}else if(typeof error.data=='object'){return this.errorDetailHandler(error.data);}}
return result;}
showError(to_pop_up,to_console){if(!to_console){to_console=to_pop_up;}
guiPopUp.error(to_pop_up);console.error(to_console);}
defineErrorAndShow(error){return this.showError(this.errorToString(error));}}