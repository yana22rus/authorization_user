var count = 1

function add(){


	let p = document.createElement("p");
	let input = document.createElement("input");


	input.id = count;
	input.name = count;
	div.before(p);
	div.before(input);
	count += 1;

}


function del(){

	count = count -1
	let del = document.getElementById(String(count));
	del.parentNode.removeChild(del);


}