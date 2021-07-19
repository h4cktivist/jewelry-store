const openButton = document.querySelector('#open');
const popupWrapper = document.querySelector('.popup');
const closeButton = document.querySelector('.close');

openButton.addEventListener('click', function(){
	openPopup();
});

closeButton.addEventListener('click', function(){
	closePopup();
});

popupWrapper.addEventListener('click', function(e){
	if(e.target !== this) return;
	closePopup();
});


function openPopup() {
	popupWrapper.classList.add('active');
}
function closePopup() {
	popupWrapper.classList.remove('active');
}

