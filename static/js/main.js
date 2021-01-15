var cartBtn = document.getElementsByClassName('cart-btn')

var wishBtn = document.getElementsByClassName('addToWish')

//add product to cart
for(var i = 0; i < cartBtn.length; i++){
    cartBtn[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action)

        
		if (user == 'AnonymousUser'){
            alert("Please!! Login to add item to Cart")
            // window.location.href = "{% url 'login' %}"
		}else{
            updateCart(productId, action)
            //alert("product added to cart successfull")
            
		}
        
    })
}

for(var i = 0; i < wishBtn.length; i++){
    wishBtn[i].addEventListener('click', function(){
        console.log("button clicked")
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action)

		if (user == 'AnonymousUser'){
            alert("Please!! Login to add item you wish")
            // window.location.href = "{% url 'login' %}"
		}else{
            updateWishList(productId, action)
		}
        
    })
}


function updateCart(productId, action){
    var url = '/add_Cart/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body:JSON.stringify({'productId': productId, 'action': action})
    })
    .then((response)=>{
        return response.json()
    })
    .then((data)=>{
        console.log('data:', data)
        location.reload()
    })
}

//wishlist function
function updateWishList(productId, action){
    var url = '/add_wishlist/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body:JSON.stringify({'productId': productId, 'action': action})
    })
    .then((response)=>{
        return response.json()
    })
    .then((data)=>{
        console.log('data:', data)
        //alert("product added to wish list ")
        location.reload()
    })
}

/*searchBtn.addEventListener('click', function(){
    var action = this.dataset.action

    console.log("btn clicked")
    searchBy(action)
})*/

