var create_store = (function (){

  var $select_mov = $('#mov');
  var $select_kind_mov = $('#kind-mov');
  var $select_currency = $('#currency');
  var $div_kind_mov = $('#div-kind-mov');
  var $div_rest_input = $('#div-rest-input');
  var $div_shipment = $('#div-shipment');
  var $common_fields = $('#common-fields');
  var $kind_charge = $('#kind-charge');
  var $div_create_shipment = $('#div-create-shipment');
  var $div_socio = $('#div-socio');
  var $div_kind_abono = $('#div-kind-abono');
  var $div_type_change = $('#div-type-change');
  var $div_account = $('#div-account');

  // bind events
  $select_mov.on('change', movSelected);
  $select_kind_mov.on('change', kindMovSelect);
  $kind_charge.on('contentChanged', optionsChanged);
  $select_currency.on('change', currencyChange);

  function movSelected() {
    if ($select_mov.val().toLowerCase() === 'cargo') {
      $div_kind_mov.show();
      $div_kind_abono.hide();
      $div_socio.hide();
    } 
    if ($select_mov.val().toLowerCase() === 'abono') {
      abonoSelected();
    }
    if ($select_mov.val().toLowerCase() === 'embarque') {
      embarqueSelected();
    }
    if ($select_mov.val().toLowerCase() === 'retiro') {
      retiroSelected();
    }
  }

  function retiroSelected() {
    $div_kind_mov.hide();
    $div_rest_input.hide();
    $common_fields.show();
    $div_account.show();
    $div_shipment.hide();
    $div_create_shipment.hide();
    $div_socio.show();
    $div_kind_abono.hide();
    $div_type_change.hide();
  }

  function embarqueSelected() {
    $div_kind_mov.hide();
    $div_rest_input.hide();
    $common_fields.hide();
    $div_account.hide();
    $div_shipment.hide();
    $div_create_shipment.show();
    $div_kind_abono.hide();
    $div_socio.hide();
    $div_type_change.hide();
  }

  function abonoSelected() {
    $div_kind_abono.show();
    $div_kind_mov.hide();
    $div_rest_input.hide();
    $common_fields.show();
    $div_account.show();
    $div_shipment.hide();
    $div_socio.hide();
    $div_create_shipment.hide();
    $div_type_change.hide();
  }

  function kindMovSelect() {
    if ($select_kind_mov.val().toLowerCase() === 'directo') {
      $div_shipment.show();
    } else {
      $div_shipment.hide();
    }
    $div_rest_input.show();
    $common_fields.show();
    $div_account.show();
    get_kind_charges_ajax($select_kind_mov.val());
  }

  function currencyChange() {
    if ($select_mov.val().toLowerCase() === 'cargo') {
      if ($select_currency.val().toLowerCase() === 'mxn') {
        $div_type_change.show();
      }
      if ($select_currency.val().toLowerCase() === 'usd') {
        $div_type_change.hide();
      }
    }
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

  return {
    abonoSelected: abonoSelected,
    embarqueSelected: embarqueSelected,
    retiroSelected: retiroSelected,
    get_kind_charges_ajax: get_kind_charges_ajax,
    currencyChange: currencyChange,
  }

}())
