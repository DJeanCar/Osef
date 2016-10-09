var $notification = $('.dropdown__notification');
$notification.on('click', function (e) {
  // e.preventDefault();
  $.ajax({
  		url: '/notification/' + this.dataset.id + '/',
  		type: "GET",
      success: function (data) {
      	console.log(data);
        console.log('success');
      }
  	});
});
