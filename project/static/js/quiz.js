var count = 1

function add(){


	let p = document.createElement("p");
	let br = document.createElement("br");
	let input = document.createElement("input");
	let yes = document.createElement("input");
	let no = document.createElement("input");
	let label1 = document.createElement("label");
	let label2 = document.createElement("label");
	yes.type = "radio";
    yes.checked = "true";
	no.type = "radio";
    yes.name = "radio"+count;
    yes.value="true"
    no.value="false"
    no.name = "radio"+count;
    yes.id = "radio"+count;
    no.id = "radio"+count;
	input.id = count;
	input.name = count;
	input.placeholder = "Утверждение";

	label1.setAttribute('for', yes.id);
    label1.innerHTML = "Да";

    label2.setAttribute('for', no.id);
    label2.innerHTML = "Нет";


	div.before(p);
	div.before(input);
	div.before(yes);
	div.before(label1);
	div.before(no);
	div.before(label2);
	div.before(br);


	count += 1;

}


function del(){

	count = count -1
	let del = document.getElementById(String(count));
	let del_checkbox = document.getElementById("radio"+String(count));
	del.parentNode.removeChild(del_checkbox);
	del.parentNode.removeChild(del);


}