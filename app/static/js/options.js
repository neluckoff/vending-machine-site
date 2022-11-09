let products = `{{ json_products }}`
products = products.replace(/&#39;/g, '"').replace(/&quot;/ig,'"');;
let json = JSON.parse(products);

$( "#select-machine-to-buy" ).change(function(e) {
    let city_id = e.target.value
    
    let products_by_id = json[city_id]

    if (typeof products_by_id.products === "undefined") return
    
    $("#sel-wr").html(`
        <select class="select" id="select-product" name="select-product">
        </select>
    `)

    for (var i = 0; i < products_by_id.products.length; i++) {
        $('<option value="' + products_by_id.products[i].id + '">' + products_by_id.products[i].name + '</option>').appendTo('#select-product');
    }
    
});