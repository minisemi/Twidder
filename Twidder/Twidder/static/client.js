var myChart;
window.onload = function () {

    displayView()
}



/* Set index page url to '/'
*  Start router
*/
page('/', displayView);
page();

/*
* Function called when tab in frontend is clicked
* Calls on page to route to correct URL,
* Call on open tab
* tabName: string for URL
* tabID: String ID for each tab
 */
function callOnPage(tabName, tabID){
    page('/'+tabName, function(){
        openTab(tabName, tabID)
});
}

/*
* Displays correct view
* If token is undefined; new session -> log in page
* If token is defined, go to tab stored in sessionStorage (last visited tab, handles refresh page-event)
 */
function displayView() {

    if (sessionStorage.token == undefined){
        document.getElementById("currentView").innerHTML = document.getElementById("welcome").innerHTML
    } else {
        document.getElementById("currentView").innerHTML= document.getElementById("profile").innerHTML
        initializePieChart()
        document.getElementById(sessionStorage.currentTab).click();
        webSocket()
    }
}

/*
* Function called when user logs out
* Clears sessionStorage as necessary, call display view (with undefined token)
* and routs back to index page. Send http POST request to update server.
 */
function logout(){
    var callback = function () {
        sessionStorage.removeItem("token")
        sessionStorage.removeItem("email")
        displayView()
        page('/')
    }
    xmlHttpRequest("POST", "sign_out", null, "",callback)
}

/*
* Function called to log in.
* Define callback function to update sessionStorage if server logs in user successfully,
* or send error message if failed.
* Sends data by form in http POST request to server.
 */
function login() {
    var error = document.getElementById("error")
    var callback = function (response) {
        if (response.success == true) {
            updateSessionStorage(response.data, document.getElementById("loginemail").value)
            //webSocket()
        } else {
            error.innerHTML = response.message
        }
    }
    var form = new FormData(document.getElementById("login_form"))
    xmlHttpRequest("POST", "sign_in", form, "",callback)
}

function initializePieChart() {

    var ctx = document.getElementById("myChart");
    myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ["Posts on wall", "Wall visits", "Posts to others"],
            datasets: [{
                data: [0, 0, 0],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)'
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)'
                ],
                borderWidth: 1
            }]

        },
        options: {
            responsive: false,
            maintainAspectRatio:false,
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            },
            legend: {
                display: false
            },
            tooltips: {
                callbacks: {
                    label: function(tooltipItem) {
                        return tooltipItem.yLabel;
                    }
                }
            }
        }
    });
}

function updateChart(data) {

    switch (data.chartType){
        case "posts":
            myChart.data.datasets[0].data[0] = data.chartValue['COUNT(message)'];
            myChart.update()
            break
        case "visits":
            myChart.data.datasets[0].data[1] = data.chartValue['pageViews'];
            myChart.update()
            break
        case "postsToOthers":
            myChart.data.datasets[0].data[2] = data.chartValue['COUNT(message)'];
            myChart.update()
            break
        default:break
    }
}

/*
* Function called when a user signs up.
* First checks password repeat client side
* Define callback function to alert user in error message about success/failure
* Sends data by form in http POST request to server
 */
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

/*
* Called to upate sessionStorage in log in/out event, display view called.
* token: unique login token for user (undefined if not logged in)
* email: email to user (unique, works as user name)
 */
function updateSessionStorage(token, email){
    if (typeof(Storage) !== "undefined") {
        sessionStorage.setItem("token", token)
        sessionStorage.setItem("email", email)
        sessionStorage.setItem("currentTab", "homeTab")
        //webSocket().open()
        //call for websocket connection

        displayView()
    } else {
      //  alert("Browser doesn't support web storage")
    }
}

/*
* Function called when a tab is opened,
* called from onClick in HTML indirectly through callOnPage()
* First closes all tabs by setting its style.display to none
* And replaces classNames from active to "" to not make buttons look like they are pressed
* Then shows correct tab (block) and sets this one to active (button pressed), stores tabID.
* tabName: string for URL
* tabID: String ID for each tab
 */
function openTab(tabName, tabID) {
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
    sessionStorage.currentTab = tabID

}

/*
* Function called when user presses button Change password
* First check client side if new password is repeated correctly,
* Define callback function to display correct response to user.
* Sends data by form in http POST request to server.
* If new password is same as old, dont connect to server
* just alert user.
 */
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

/*
* Define callback function to set all user info to data from server response.
* Sends http GET request to get all data.
 */
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

/*
* Function called when user posts message on own or other users wall.
* First refreshes messages displayed.
* Defines callback function to call on loadMessage for specific message.
* Sends all data by form in POST request to server by calling on xmlHttpRequest
* with data and callback function
*/
function postMessage(message, email, sender, messageBoard) {
    refreshMessages(email, messageBoard)
    var form = new FormData()
    var message = document.getElementById(message).value
    var messageBoard = document.getElementById(messageBoard)
    var callback = function (response) {
        if (response.success){
            loadMessage(message, email, messageBoard, sender)

        }
    }

    form.append("message", message)
    form.append("email", email)
    form.append("sender", sender)
    xmlHttpRequest("POST", "post_message", form, "",callback)
}

/*
* Callback function defined: Refreshes all messages by
* first clearing messageBoard, then calls on loadMessage for each message retrieved from served
* by http GET request with email as parameter.
* email: email to receiver
* messageBoard: message board to be refreshed
 */
function refreshMessages(email, messageBoard) {
    var messageBoard = document.getElementById(messageBoard)
    var callback = function (response) {

        if (response.success == true) {
            while (messageBoard.firstChild) {
                messageBoard.removeChild(messageBoard.firstChild);
            }

            for (var i = 0; i < response.data.length; i++) {

                var message = response.data[i].message
                var sender = response.data[i].sender
                loadMessage(message, email, messageBoard, sender)

            }
        }

    }
    var emailString = email
    var params = "email="+emailString
    xmlHttpRequest("GET", "get_user_messages_by_email", null, params,callback)
}

/*
* Function to load a message and add it to the layout.
* Message is contained in draggable div.
 */
function loadMessage(message, email, messageBoard, sender){
    var textArea = document.createElement("textarea")
    textArea.setAttribute("class", "messageBox")
    textArea.setAttribute("readonly","readonly")
    var senderNode = document.createTextNode(sender + ": \n")
    var textNode = document.createTextNode(message)
    textArea.appendChild(senderNode)
    textArea.appendChild(textNode)
    var messageDiv = document.createElement("div")
    messageDiv.setAttribute("draggable", true)
    messageDiv.setAttribute("ondragstart", "drag(event)")
    messageDiv.setAttribute("class", "messageBox")
    messageDiv.appendChild(textArea)
    messageDiv.setAttribute("id", message)
    messageBoard.insertBefore(messageDiv, messageBoard.firstChild)
}

/*
* Function for allow drop on message board
* preventing default action.
 */
function allowDrop(ev) {
    ev.preventDefault();
}

/*
* Drag event stored target.id in data transferred in event, get text
 */
function drag(ev) {
    var stringList = ev.target.textContent.split('\n')
    var sender = stringList[0].slice(0,-2)
    stringList.splice(0,1)
    ev.dataTransfer.setData("element", stringList.join('\n'));
    ev.dataTransfer.setData("sender", sender)

}

/*
* sets target of drop event's text to drag event stored data
 */
function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("element")
    document.getElementById(ev.target.id).value = '"' + data + '"\nRepost from ' + ev.dataTransfer.getData("sender")

}

/*
* Function that searches for user
* Callback function defined to display all user data if response is successful.
* Sends http GET request with data in form an callback function
 */
function searchForUser() {

    var error = document.getElementById("error")
    var searchEmail = document.getElementById("searchEmail").value
    var callback = function (response) {
        if (response.success == true) {

        document.getElementById("searchResults").style.visibility="visible"
        document.getElementById("searchfirstname").innerHTML = response.data.firstName
        document.getElementById("searchfamilyname").innerHTML = response.data.familyName
        document.getElementById("displaySearchEmail").innerHTML = response.data.email
        document.getElementById("searchgender").innerHTML = response.data.gender
        document.getElementById("searchcountry").innerHTML = response.data.country
        document.getElementById("searchcity").innerHTML = response.data.city
        refreshMessages(searchEmail,"searchmessageBoard")

        } else {
            document.getElementById("searchResults").style.visibility="hidden"
      //  alert(serverMessage.message)
         }
    }

    var params = "email="+searchEmail
    xmlHttpRequest("GET", "get_user_data_by_email", null, params, callback)
}

/*
* Function called to create http request and send to server.
* method:  Kind of request, GET, POST etc.
* url: url corresponding on server side
* data: data to be sent in form(null if no data needed)
* params: params to be included, for example email.
* callback: function to be executed upon response.
 */
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

    xhttp.open(method, "http://localhost:7000/" + url+"?"+params, true);
    xhttp.setRequestHeader("token",sessionStorage.token)
    if (data==null){
        xhttp.send();
    }
    else
        xhttp.send(data);
}

/*
* Function to initiate websocket connection.
* Sends token to server when user logs in.
* Reads data sent from server when mesage is sent about chart update.
 */
function webSocket() {
    var connection = new WebSocket('ws://localhost:7000/echo');

    connection.onopen = function(){
        console.log('websocket open')
        connection.send(sessionStorage.token);
    }

    connection.onerror = function (error) {
        console.log('WebSocketError ' + error);
    }

    connection.onmessage = function (message) {
        var jsonMessage = JSON.parse(message.data)
        if (jsonMessage.message == 'logout'){
            sessionStorage.removeItem("token")
            sessionStorage.removeItem("email")
            displayView()
        }
        if (jsonMessage.message == 'updateChart'){
           console.log("JSON: " + jsonMessage.message)
                updateChart(jsonMessage.data)
        }
        console.log('WebSocketMessage ' + jsonMessage.message);
    }
}