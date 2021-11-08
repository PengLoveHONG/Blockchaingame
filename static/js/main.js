

// ================================================================ //
function createButton() {
    // remove the input id="newGameName" and id="joinGameName" if either exists
    if (document.getElementById("GameName")) {
        document.getElementById("GameName").remove();
    };
    if (document.getElementById("GameName")) {
        document.getElementById("GameName").remove();
    };

    

    // calling createButton adds a input text field to the id="buttonbox"
    input = document.createElement("input");
    input.setAttribute("type", "text");
    input.setAttribute("id", "GameName");
    input.name = "GameNameCreate";
    input.setAttribute("required", "");
    input.setAttribute("placeholder", "Create a Game ID");
    input.setAttribute("size", "20");
    document.getElementById("user-box").appendChild(input);

}
// ================================================================ //

function joinButton() {
    // remove the input id="newGameName" if it exists
    if (document.getElementById("GameName")) {
        document.getElementById("GameName").remove();
    };
    if (document.getElementById("GameName")) {
        document.getElementById("GameName").remove();
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

}
// ================================================================ //