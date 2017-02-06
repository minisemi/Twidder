window.onload = function () {
    if (sessionStorage.token == undefined){
        return document.getElementById("currentView").innerHTML = document.getElementById("welcome").innerHTML
    } else {
        return document.getElementById("currentView").innerHTML= document.getElementById("profile").innerHTML
    }
}


function logout(){
    serverstub.signOut(sessionStorage.token)
    sessionStorage.removeItem("token")
    sessionStorage.removeItem("email")
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
        location.reload()
    } else {
        alert("Browser doesn't support web storage")
    }
}

function openTab(tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");

    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");

    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
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

function postMessage(message, email, messageBoard) {
    var message = document.getElementById(message).value
    var serverMessage=serverstub.postMessage(sessionStorage.token,message,email)
    var messageBoard = document.getElementById(messageBoard)
    var textArea = document.createElement("textarea")
    var textNode = document.createTextNode(message)
    textArea.appendChild(textNode)
    messageBoard.insertBefore(textArea, messageBoard.firstChild);
}

function refreshMessages(email, messageBoard) {
    var messages = serverstub.getUserMessagesByEmail(sessionStorage.token, email)
    var messageBoard = document.getElementById(messageBoard)
    if (messages.data.length>messageBoard.childElementCount){
        while (messageBoard.firstChild) {
            messageBoard.removeChild(messageBoard.firstChild);
        }

        for (var i = 0; i < messages.data.length; i++) {
            var textArea = document.createElement("textarea")
            var text = messages.data[i].content
            var textNode = document.createTextNode(text)
            textArea.appendChild(textNode)
            messageBoard.appendChild(textArea)
        }
    }
}

function searchForUser() {

    var searchEmail = document.getElementById("searchEmail").value
    var serverMessage=serverstub.getUserDataByEmail(sessionStorage.token, searchEmail)
    if (serverMessage.success == true) {

        document.getElementById("searchResults").style.visibility="visible"
        document.getElementById("searchfirstname").innerHTML = serverMessage.data.firstname
        document.getElementById("searchfamilyname").innerHTML = serverMessage.data.familyname
        document.getElementById("searchemail").innerHTML = serverMessage.data.email
        document.getElementById("searchgender").innerHTML = serverMessage.data.gender
        document.getElementById("searchcountry").innerHTML = serverMessage.data.country
        document.getElementById("searchcity").innerHTML = serverMessage.data.city

        var messages = serverstub.getUserMessagesByEmail(sessionStorage.token, searchEmail)
        var messageBoard = document.getElementById("searchmessageBoard")

        while (messageBoard.firstChild) {
            messageBoard.removeChild(messageBoard.firstChild);
        }

        for (var i = 0; i < messages.data.length; i++) {
            var textArea = document.createElement("textarea")
            var text = messages.data[i].content
            var textNode = document.createTextNode(text)
            textArea.appendChild(textNode)
            messageBoard.appendChild(textArea)
        }
    } else {
        alert(serverMessage.message)
    }
}