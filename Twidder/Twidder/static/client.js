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

    var callback = function () {
        sessionStorage.removeItem("token")
        sessionStorage.removeItem("email")
        displayView()
    }
    xmlHttpRequest("POST", "sign_out", null, "",callback)
}

function login() {
    var error = document.getElementById("error")
    var callback = function (response) {
        if (response.success == true) {
            checkForToken(response.data, document.getElementById("loginemail").value)
        } else {
            error.innerHTML = response.message
        }
    }
    var form = new FormData(document.getElementById("login_form"))
    xmlHttpRequest("POST", "sign_in", form, "",callback)
    //webSocket(sessionStorage.token);
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

        var callback = function (response) {
            if (response.success == true) {
            error.innerHTML = response.message
            } else {
            error.innerHTML = response.message
            }
        }
        var form = new FormData(document.getElementById("signup_form"))
        form.delete("repeatpsw")
        xmlHttpRequest("POST", "sign_up", form, "",callback)
    }
}

function checkForToken(token, email){
    if (typeof(Storage) !== "undefined") {
        sessionStorage.setItem("token", token)
        sessionStorage.setItem("email", email)
        webSocket();
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
    var form = new FormData(document.getElementById("changePwForm"))

    var pwText = document.getElementById("passwordText")
    if(form.get("new_password")!=form.get("repeat_new_password")){
        pwText.innerHTML = "Repeat password failed"
        return
    }

    if (form.get("new_password")!=form.get("old_password")){
        var callback = function (response) {
            if(response.success==true){
            pwText.innerHTML=response.message
            } else{
            pwText.innerHTML=response.message
            }
        }
        form.delete("repeat_new_password")
        xmlHttpRequest("POST", "change_password", form, "",callback)

    } else {
        pwText.innerHTML="New password same as old"
    }
}

function displayUserData(){
    var callback = function (response) {
        document.getElementById("userfirstname").innerHTML=response.data.firstName
        document.getElementById("userfamilyname").innerHTML=response.data.familyName
        document.getElementById("useremail").innerHTML=response.data.email
        document.getElementById("usergender").innerHTML=response.data.gender
        document.getElementById("usercountry").innerHTML=response.data.country
        document.getElementById("usercity").innerHTML=response.data.city
    }
    xmlHttpRequest("GET", "get_user_data_by_token", null, "",callback)
}

function postMessage(message, email, messageBoard) {
    var form = new FormData()
    var message = document.getElementById(message).value
    var messageBoard = document.getElementById(messageBoard)
    var callback = function (response) {
        if (response.success){
            var textArea = document.createElement("textarea")
            textArea.setAttribute("readonly","readonly")
            var senderNode = document.createTextNode(email + ": \n")
            var textNode = document.createTextNode(message)
            textArea.appendChild(senderNode)
            textArea.appendChild(textNode)
            messageBoard.insertBefore(textArea, messageBoard.firstChild)
        }
    }

    form.append("message", message)
    form.append("email", email)
    xmlHttpRequest("POST", "post_message", form, "",callback)
}
//TODO: Fixa så att meddelanden som hämtas från servern läggs in i rätt ordning. Nu kommer äldst längst upp på väggen (kolla på deras datum från databasen)
function refreshMessages(email, messageBoard) {
    var messageBoard = document.getElementById(messageBoard)
    var callback = function (response) {

            while (messageBoard.firstChild) {
                messageBoard.removeChild(messageBoard.firstChild);
            }

            for (var i = 0; i < response.data.length; i++) {
                var textArea = document.createElement("textarea")
                textArea.setAttribute("readonly","readonly")

                var text = response.data[i].message
                var textNode = document.createTextNode(text)
                var senderNode = document.createTextNode(email + ": \n")
                textArea.appendChild(senderNode)
                textArea.appendChild(textNode)
                messageBoard.appendChild(textArea)
            }

    }
    var emailString = email
    var params = "email="+emailString
    xmlHttpRequest("GET", "get_user_messages_by_email", null, params,callback)
}

function searchForUser() {

    var error = document.getElementById("error")

    var searchEmail = document.getElementById("searchEmail").value
    var callback = function (response) {
        if (response.success == true) {

        document.getElementById("searchResults").style.visibility="visible"
        document.getElementById("searchfirstname").innerHTML = response.data.firstName
        document.getElementById("searchfamilyname").innerHTML = response.data.familyName
        document.getElementById("searchemail").innerHTML = response.data.email
        document.getElementById("searchgender").innerHTML = response.data.gender
        document.getElementById("searchcountry").innerHTML = response.data.country
        document.getElementById("searchcity").innerHTML = response.data.city
        refreshMessages(searchEmail,"searchmessageBoard")

        } else {
      //  alert(serverMessage.message)
         }
    }
    var params = "email="+searchEmail
    xmlHttpRequest("GET", "get_user_data_by_email", null, params, callback)

}

function xmlHttpRequest(method, url, data, params, callback){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var response = JSON.parse(this.responseText)
            callback(response);
        }
    };
    //var params = JSON.stringify({ appoverGUID: approverGUID })
    //var params = "somevariable=somevalue&anothervariable=anothervalue";

    xhttp.open(method, "http://localhost:5000/" + url+"?"+params, true);
    xhttp.setRequestHeader("token",sessionStorage.token)
    if (data==null){
        xhttp.send();
    }
    else
        xhttp.send(data);
}
function webSocket() {
    var connection = new WebSocket('ws://http://localhost:5000/echo');
    connection.send('WebSocket connection opened');

    connection.onerror = function (error) {
        console.log('WebSocketError ' + error);
    }

    connection.onmessage = function (message) {
        console.log('WebSocketMessage ' + message.data);
    }

    

}