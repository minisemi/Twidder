window.onload = function () {
    displayView()
}

function displayView() {
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
    displayView()
}

function login() {
    var error = document.getElementById("error")
    var serverMessage = serverstub.signIn(document.getElementById("loginemail").value, document.getElementById("loginpassword").value)
        if (serverMessage.success == true) {
            checkForToken(serverMessage.data, document.getElementById("loginemail").value)
        } else {
            error.innerHTML = serverMessage.message
        }
}

function signUp() {

    var proceed = true
    var error = document.getElementById("error")


    if(document.getElementById("password").value!=document.getElementById("repeatpsw").value){
        error.innerHTML = "Repeat password failed"
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
        // TODO: Useful in lab 3
        // data = FormData();
        // data.append("email", email)
        var serverMessage = serverstub.signUp(user)
        if (serverMessage.success == true) {
            error.innerHTML = serverMessage.message
        } else {
            error.innerHTML = serverMessage.message
        }
    }
}

function checkForToken(token, email){
    if (typeof(Storage) !== "undefined") {
        sessionStorage.setItem("token", token)
        sessionStorage.setItem("email", email)
        displayView()
    } else {
      //  alert("Browser doesn't support web storage")
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
    var pwText = document.getElementById("passwordText")
    var oldpw =document.getElementById("changePasswordOld").value
    var newpw1=document.getElementById("changePasswordNew1").value
    var newpw2=document.getElementById("changePasswordNew2").value
    if(newpw1!=newpw2){
        pwText.innerHTML = "Repeat password failed"
        return false
    }

    if (newpw1!=oldpw){
        var serverMessage = serverstub.changePassword(sessionStorage.token,oldpw,newpw1)
        if(serverMessage.success==true){
        pwText.innerHTML="Password successfully changed"
        } else{
            pwText.innerHTML="Wrong password"
        }
    } else {
        pwText.innerHTML="New password same as old"
    }
    return false
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
    textArea.setAttribute("readonly","readonly")

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
            textArea.setAttribute("readonly","readonly")

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
        refreshMessages(searchEmail,"searchmessageBoard")

    } else {
      //  alert(serverMessage.message)
    }
}

function xmlHttpRequest(method, url, data, callback){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var response = JSON.parse(this.responseText)
            callback(response);
        }
    };
    xhttp.open(method, "http://localhost:5000/" + url, true);
    if (data==null){
        xhttp.send();
    }
    else
        xhttp.send(data);
}