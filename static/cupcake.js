const urlBase = "http://127.0.0.1/:5000/api"

function cupcakeHTML(cupcake) {
    return `<div data-cupcake-id=${cupcake.id}>
    <li>Flavor: ${cupcake.flavor}, Size: ${cupcake.size}, Rating: ${cupcake.rating}</li>
    <img src="${cupcake.img}">
    </div>`;
}

async function showInitialCupcakes() {
    let resp = await axios.get(`${urlBase}/cupcakes`);
    let respData = resp.data;
    for (let cupcake of respData.cupcakes) {
       let cupcakes = cupcakeHTML(cupcake)
       $('ul').append(cupcakes)
    }
}
    

$('button').on('click', async function(event){
    event.preventDefault();
    let flavor = $('#flavor').val();
    let size = $('#size').val();
    let rating = $('#rating').val();
    let image = $('#Image').val();
    const newCupcakeResponse = await axios.post(`${urlBase}/cupcakes`, {
        flavor,
        rating,
        size,
        image
      });
    
    let newCupcake = cupcakeHTML(newCupcakeResponse.data.cupcake);
    $("ul").append(newCupcake);
    $("form").trigger("reset");
    })


$("#cupcakes-list").on("click", ".delete-button", async function (event) {
    event.preventDefault();
    let $cupcake = $(event.target).closest("div");
    let cupcakeId = $cupcake.attr("data-cupcake-id");
    
    await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
    $cupcake.remove();
    });

//?????????????????
// showInitialCupcakes()
$(showInitialCupcakes);