

// ================================================================ //
function createButton() {
    // remove the input id="newGameName" and id="joinGameName" if either exists
    if (document.getElementById("GameName")) {
        document.getElementById("GameName").remove();
    };
    if (document.getElementById("difficulty")) {
        document.getElementById("difficulty").remove();
    };
    if (document.getElementById("connection")) {
        document.getElementById("connection").remove();
    };
    

    // select drowndown creation
    input = document.createElement("input");
    input.setAttribute("type", "text");
    input.setAttribute("id", "GameName");
    input.name = "GameNameCreate";
    input.setAttribute("required", "");
    input.setAttribute("placeholder", "Create a Game ID");
    input.setAttribute("size", "20");
    document.getElementById("user-box").appendChild(input);

    select = document.createElement("select");
    select.setAttribute("id", "difficulty");
    select.name = "difficulty";
    select.value = "Select a level of difficulty"
    select.setAttribute("required", "");
    select.setAttribute("placeholder", "Select a Difficulty");
    select.setAttribute("size", "1");
    document.getElementById("user-box").appendChild(select);

    option = document.createElement("option");
    option.setAttribute("value", "default_difficulty");
    option.innerHTML = "Select a level of difficulty hashing";
    select.appendChild(option);

    option1 = document.createElement("option");
    option1.setAttribute("value", "one");
    option1.innerHTML = "0";
    select.appendChild(option1);

    option2 = document.createElement("option");
    option2.setAttribute("value", "two");
    option2.innerHTML = "00";
    select.appendChild(option2);

    option3 = document.createElement("option");
    option3.setAttribute("value", "three");
    option3.innerHTML = "000";
    select.appendChild(option3);

    option4 = document.createElement("option");
    option4.setAttribute("value", "four");
    option4.innerHTML = "0000";
    select.appendChild(option4);

    // select drop down for number of connections
    select_conn = document.createElement("select");
    select_conn.setAttribute("id", "connection");
    select_conn.name = "connection";
    select_conn.value = "Number of connections per miner"
    select_conn.setAttribute("required", "");
    select_conn.setAttribute("placeholder", "Select a Difficulty");
    select_conn.setAttribute("size", "1");
    document.getElementById("user-box").appendChild(select_conn);

    option_conn = document.createElement("option");
    option_conn.setAttribute("value", "default_connection");
    option_conn.innerHTML = "Select network connection level";
    select_conn.appendChild(option_conn);

    option1_conn = document.createElement("option");
    option1_conn.setAttribute("value", "all");
    option1_conn.innerHTML = "Instant connection to everyone";
    select_conn.appendChild(option1_conn);

    option2_conn = document.createElement("option");
    option2_conn.setAttribute("value", "ten");
    option2_conn.innerHTML = "10 connections";
    select_conn.appendChild(option2_conn);

    option3_conn = document.createElement("option");
    option3_conn.setAttribute("value", "five");
    option3_conn.innerHTML = "5 connections";
    select_conn.appendChild(option3_conn);

    option4_conn = document.createElement("option");
    option4_conn.setAttribute("value", "two");
    option4_conn.innerHTML = "2 connections";
    select_conn.appendChild(option4_conn);

    
    //add a h2 
    h2 = document.createElement("h2");
    h2.setAttribute("class", "h2_connection");
    h2.innerHTML = "Select the connection quality";
    document.getElementById("user-box").appendChild(h2);

    select_slider = document.createElement("input");
    select_slider.setAttribute("id", "slider");
    select_slider.name = "slider";
    select_slider.type = "range";
    select_slider.value = "1.0";
    select_slider.min = "0";
    select_slider.max = "1.0";
    select_slider.step = "0.01";
    select_slider.setAttribute("required", "");
    select_slider.setAttribute("size", "2");
    // add oninput="this.nextElementSibling.value = this.value" to select_slider
    // to update the value of the next element
    select_slider.oninput = function() {
        this.nextElementSibling.value = this.value;
        console.log(this.value);
    };
    
    document.getElementById("user-box").appendChild(select_slider);
    
    //add an output box for the slider value
    output = document.createElement("output");
    output.setAttribute("id", "slider_output");
    output.name = "slider_output";
    output.value = "1";
    document.getElementById("user-box").appendChild(output);





}
// ================================================================ //

function joinButton() {
    // remove the input id="newGameName" if it exists
    if (document.getElementById("GameName")) {
        document.getElementById("GameName").remove();
    };
    if (document.getElementById("difficulty")) {
        document.getElementById("difficulty").remove();
    };
    if (document.getElementById("connection")) {
        document.getElementById("connection").remove();
    };
    


    // calling createButton adds a input text field to the id="buttonbox"
    input = document.createElement("input");
    input.setAttribute("required", "");
    input.setAttribute("type", "text");
    input.setAttribute("id", "GameName");
    input.name = "GameNameJoin";
    input.setAttribute("placeholder", "Join a Game ID");
    input.setAttribute("size", "20");
    document.getElementById("user-box").appendChild(input);

};
// ================================================================ //



// ================================================================ //

//ajax request call to database bringing the data in somesort of interval, asynchronous calls
//xml https requests = fetch api, promises, 

//build an api endpoint, so the js can make an api endpoint to the flask api endpoint
//application.route("/<name to query>")
// ajax is asynchronous js
