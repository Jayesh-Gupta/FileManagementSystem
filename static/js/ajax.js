    console.log('ajax');
   // let register =document.getElementById('registerbtn');
    console.log('ajax1');
    //console.log(register)
//    register.addEventListener("click" ,myFunction());
//    console.log('ajax2');

//  function myFunction()
//  {
//        console.log('ajax2');
//    console.log('func chal gaya');
//    //instantiate xhr object
//    const xhr=new XMLHttpRequest();
//       console.log('ajax3');
//open object
//    xhr.open('POST','register',true);
//       console.log('ajax4');
//    xhr.getResponseHeader('content-type','application/x-www-form-urlencode');
//       console.log('ajax5');
//    xhr.onprogress=function()
//    {
//    console.log('on progress');
//    }

    //when response is ready
//    xhr.onload=function()
//    {
//    console('onload chal gaya');
//    if(this.status==200)
//    {
//    for  message in messages
//    console.log(message);}
//    }
   /* var email=document.getElementById('email').value
    var name=document.getElementById('name').value
    var username=document.getElementById('username').value
    var password=document.getElementById('password').value
    var confrimpassword=document.getElementById('confrimpassword').value
    var user_type=document.getElementById('user_type').value
    var address=document.getElementById('address').value
    var contact=document.getElementById('contact').value

   params='email='+email+'&name='+name+'&username='+username+'&password='+password+'&confrompassword='+confrimpassword+'&user_type='+user_type+'&address='+address+'&contact='+contact+;
   xhr.send(params);*/

//}

$(document).on('submit','#register_form',function(e){
e.preventDefault();
$.ajax({
type:'POST',
url:'/register',
data:
{
email:$('#email').val(),
name:$('#name').val(),
username:$('#username').val(),
password:$('#password').val(),
confrimpassword:$('#confrimpassword').val(),
user_type:$('#user_type').val(),
address:$('#address').val(),
contact:$('#contact').val(),
csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),



},
success:function(response){

   // location.href='/login'

    console.log(typeof(response.msg));
    console.log(user_type);
   //document.getElementById('form-messages').innerHTML="<li>"+response.msg+"</li>";
  $('#list').html("<li  id='list2'>"+response.success+"</li>");
  if(response.msg!='')
  { $('#list').html("<li  id='list1'>"+response.msg+"</li>");}

    alert('helloooooooooooooo');


}
});



});