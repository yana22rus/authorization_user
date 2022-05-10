let pop_up = document.getElementById("cookie_popup");

document.getElementById("accept_cookie").addEventListener("click", () =>{

document.cookie = "my_cookie_name=this_is_my_cookie"
document.getElementById("cookie_popup")
let del = document.getElementById("cookie_popup");
del.parentNode.removeChild(del);

});
const check_cookie = () =>{
let input = document.cookie.split("=");

if (input[0]=="my_cookie_name"){
    cookie_popup.classList.add("hide");
    cookie_popup.classList.remove("show");
}
};

check_cookie()