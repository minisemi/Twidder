window.onload = function () {
    if (sessionStorage.token == undefined){
        return document.getElementById("currentView").innerHTML = document.getElementById("welcome").innerHTML
    } else {
        return document.getElementById("currentView").innerHTML = document.getElementById("profile").innerHTML

    }
}

function logout(){
    sessionStorage.removeItem("token")
    location.reload()
}

function login() {

    var serverMessage = serverstub.signIn(document.getElementById("loginemail").value, document.getElementById("loginpassword").value)
        if (serverMessage.success == true) {
            alert(serverMessage.message)
            checkForToken(serverMessage.data)
        } else {
            alert(serverMessage.message)
        }

}

function signUp() {

    var proceed = true

    if(document.getElementById("password").value!=document.getElementById("repeatpsw").value){
        alert("Not matching password")
        proceed = false

        //måste skriva ut att pw inte är lika
    }

    var select = document.getElementById("gender")
    if (proceed) {
        var email = document.getElementById("email").value
        var password = document.getElementById("password").value
        var firstname = document.getElementById("firstname").value
        var familyname = document.getElementById("familyname").value
        var gender = select.options[select.selectedIndex].text
        var city = document.getElementById("city").value
        var country = document.getElementById("country").value
        var user = {
            email: email,
            password: password,
            firstname: firstname,
            familyname: familyname,
            gender: gender,
            city: city,
            country: country
        }
        var serverMessage = serverstub.signUp(user)
        if (serverMessage.success == true) {
            alert(serverMessage.message)
        } else {
            alert(serverMessage.message)
        }
    }
}

function checkForToken(token){
    if (typeof(Storage) !== "undefined") {
        sessionStorage.setItem("token", token)
        location.reload()
    } else {
        alert("Browser doesn't support web storage")
    }
}

function openTab(tabName) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the link that opened the tab
    document.getElementById(tabName).style.display = "block";
    event.currentTarget.className += " active";
}