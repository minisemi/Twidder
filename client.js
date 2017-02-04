window.onload = function () {
    if (sessionStorage.token == undefined){
        return document.getElementById("currentView").innerHTML = document.getElementById("welcome").innerHTML
    } else {
       // var currentView = document.getElementById("currentView").innerHTML

        //document.getElementById("Home").innerHTML
        //currentView = document.getElementById("profile").innerHTML

        return document.getElementById("currentView").innerHTML= document.getElementById("profile").innerHTML
    }
}

function logout(){
    serverstub.signOut(sessionStorage.token)
    sessionStorage.removeItem("token")
    sessionStorage.removeItem("email")
    sessionStorage.removeItem("currentTab")
    location.reload()
}

function login() {

    var serverMessage = serverstub.signIn(document.getElementById("loginemail").value, document.getElementById("loginpassword").value)
        if (serverMessage.success == true) {
            alert(serverMessage.message)
            checkForToken(serverMessage.data, document.getElementById("loginemail").value)
        } else {
            alert(serverMessage.message)
        }

}

function signUp() {

    var proceed = true

    if(document.getElementById("password").value!=document.getElementById("repeatpsw").value){
        alert("Not matching password")
        proceed = false
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

function checkForToken(token, email){
    if (typeof(Storage) !== "undefined") {
        sessionStorage.setItem("token", token)
        sessionStorage.setItem("email", email)
        sessionStorage.setItem("currentTab", "Home")
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

function changePassword() {
    var oldpw =document.getElementById("changePasswordOld").value
    var newpw=document.getElementById("changePasswordNew").value
    if (newpw!=oldpw){
        var serverMessage = serverstub.changePassword(sessionStorage.token,oldpw,newpw)
        alert(serverMessage.message)
    } else {
        alert("Not a new password")
    }
    //openTab("Account")
}

function displayUserData(){
    var serverMessage=serverstub.getUserDataByToken(sessionStorage.token)
    document.getElementById("userfirstname").innerHTML=serverMessage.data.firstname
    document.getElementById("userfamilyname").innerHTML=serverMessage.data.familyname
    document.getElementById("useremail").innerHTML=serverMessage.data.email
    document.getElementById("usergender").innerHTML=serverMessage.data.gender
    document.getElementById("usercountry").innerHTML=serverMessage.data.country
    document.getElementById("usercity").innerHTML=serverMessage.data.city
}

function postMessage() {
    var message = document.getElementById("message").value
    var serverMessage=serverstub.postMessage(sessionStorage.token,message,sessionStorage.email)
    loadMessages()

}

function loadMessages() {
    var messages = serverstub.getUserMessagesByToken(sessionStorage.token)
    var messageBoard = document.getElementById("messageBoard")

    for(var i=0;i<messages.data.length;i++) {
        var textArea = document.createElement("textarea")
        var text = messages.data[i].content
        var textNode = document.createTextNode(text)
        textArea.appendChild(textNode)
        messageBoard.appendChild(textArea)
    }
}