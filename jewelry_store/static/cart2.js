var a = document.getElementById('msg');
var b = document.getElementById('else_text');

if (!a) {
	b.style.margin = '250px';
}
else{
	b.style.margin = '200px';
}


function sneak() {
		  document.getElementById('msg').style.opacity = '0';
		}

		setTimeout(sneak, 5000);