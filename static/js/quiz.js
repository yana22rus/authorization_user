var count = 1

function add(){


	let p = document.createElement("p");
	let input = document.createElement("input");

	let checkbox = document.createElement("input");
	checkbox.type = "checkbox";
    checkbox.name = "checkbox"+count;
    checkbox.id = "checkbox"+count;



	input.id = count;
	input.name = count;
	div.before(p);
	div.before(input);
	div.before(checkbox);
	count += 1;

}


function del(){

	count = count -1
	let del = document.getElementById(String(count));
	let del_checkbox = document.getElementById("checkbox"+String(count));
	del.parentNode.removeChild(del_checkbox);
	del.parentNode.removeChild(del);


}