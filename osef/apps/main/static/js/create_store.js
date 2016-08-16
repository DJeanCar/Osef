var create_store = (function (){

	var $select_mov = $('#mov');
	var $select_kind_mov = $('#kind-mov');
	var $div_kind_mov = $('#div-kind-mov');
	var $div_rest_input = $('#div-rest-input');
	var $div_shipment = $('#div-shipment');
	var $common_fields = $('#common-fields');
	var $kind_charge = $('#kind-charge');

	// bind events
	$select_mov.on('change', movSelected);
	$select_kind_mov.on('change', kindMovSelect);
	$kind_charge.on('contentChanged', optionsChanged);

	function movSelected() {
		if ($select_mov.val() === 'cargo') {
			$div_kind_mov.show();
		} 
		if ($select_mov.val() === 'abono') {
			$div_kind_mov.hide();
			$div_rest_input.hide();
			$common_fields.show();
			$div_shipment.show();
		}
	}

	function kindMovSelect() {
		if ($select_kind_mov.val() === 'directo') {
			$div_shipment.show();
		} else {
			$div_shipment.hide();
		}
		$div_rest_input.show();
		$common_fields.show();
		get_kind_charges_ajax($select_kind_mov.val());
	}

	function optionsChanged() {
		$(this).material_select();
	}

	function get_kind_charges_ajax(kind_charge) {
		$.ajax({
			data: {kind_charge : kind_charge},
			method: "GET",
			url: '/traer-cargos-ajax/',
			success: function (charges) {
				var html = '<option disabled selected>Selecciona un cargo</option>';
				charges = JSON.parse(charges);
				charges.forEach(function (charge) {
					html += "<option value='"+ charge.pk +"'>"+ charge.fields.name +"</option>";
				});
				$kind_charge.html(html);
				$kind_charge.trigger('contentChanged');
			}
		});
	}

}())

