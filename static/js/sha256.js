
// create a function where you grab id="noncevalue" and append a p tag with the random value from 0 to 1000000
//might have to put all the data into the form to be sent into flask

//flip card
$(document).ready(function() {

	var s_round = '.s_round';
  
	$(s_round).hover(function() {
	  $('.b_round').toggleClass('b_round_hover');
	  return false;
	});
  
	$(s_round).click(function() {
	  $('.flip_box').toggleClass('flipped');
	  $(this).addClass('s_round_click');
	  $('.s_arrow').toggleClass('s_arrow_rotate');
	  $('.b_round').toggleClass('b_round_back_hover');
	  return false;
	});
  
	$(s_round).on('transitionend', function() {
	  $(this).removeClass('s_round_click');
	  $(this).addClass('s_round_back');
	  return false;
	});
  });
  
"=================================================="

function randomNonce(gamename, username, difficulty, blockhash) {
    //check if the nonce is already in the page
	if (document.getElementById("nonce")) {
        //if it is, remove it
        document.getElementById("nonce").remove();
		document.getElementById("hash").remove();
    }

    var nonce = document.getElementById("noncevalue");
    var noncevalue = String(Math.floor(Math.random()*1000000));

    nonce_tag = document.createElement("output");
    nonce_tag.id = "nonce";
	nonce_tag.name = "nonce"

    nonce_tag.innerHTML = blockhash + "<br>" + noncevalue;
    nonce.appendChild(nonce_tag);

	console.log(blockhash + "\n" + noncevalue);
    hash_value = sha256((blockhash + "\n" + noncevalue));
	hash = document.getElementById("hashvalue");
	hash_tag = document.createElement("output");
	hash_tag.id = "hash";
	hash_tag.name = "hash"
	hash_tag.innerHTML = hash_value;
	hash.appendChild(hash_tag);


	if (hash_value.slice(0, difficulty.length) === String(difficulty)) {
		alert("You found a block!");
		updateBalance(gamename, username);
	}

};

"=================================================="
// On finding the correct nonce, function to ajax to alter bitcoing balance
function updateBalance(game_name, username) {
	$.ajax({
		url: `/api_updatebalance/${game_name}/${username}`,
		type: "POST",
		datatype: "json",
		success: function(data) {
			$(buyingpowerbox).replaceWith(data);
		}
	});

}


"=================================================="
function sendToNet(gamename, username){ //fix
	//timestamp, block_height, previous hash, transactions, last_nonce, block_hash, ledger
	
	prev_hash = String(document.getElementById("blockhash").innerHTML.replace(/\s/g, ''));
	hash = String(document.getElementById("hash").innerHTML.replace(/\s/g, ''));
	nonce = String(document.getElementById("nonce").innerHTML.replace(/\s/g, ''));
	//remove the prev_hash string value within nonce
	nonce = nonce.replace(prev_hash, "");
	nonce = nonce.replace(/<br>/g, '');

	
	//console.log(hash);
	//console.log(nonce);

	$.ajax({
		url: `/api_addblockchain/${gamename}/${username}/${hash}/${nonce}`,
		type: "POST",
		datatype: "json",
		success: function(data) {
			$(flip_box).replaceWith(data);
		}
	});

	//make an ajax call to update the nonce hash value so it 
	// is dynamic with the new hashes
	



}

"=================================================="
function queryForIncoming(game_name, username) {
	window.setInterval(function(){
		recieveBlockchain(game_name, username);
	}, 1000)

	function recieveBlockchain(game_name, username) { //make this more efficient later by just using {{username in inline html call}}
		//console.log(gamename);
		//console.log(username);
		$.ajax({
			url: `/api_recieveBlockchain/${game_name}/${username}`,
			type: "GET",
			datatype: "json",
			success: function(data) {
				$(requests).replaceWith(data);
			}
		});
	}
}



"=================================================="

function sha256(ascii) {
	function rightRotate(value, amount) {
		return (value>>>amount) | (value<<(32 - amount));
	};
	
	var mathPow = Math.pow;
	var maxWord = mathPow(2, 32);
	var lengthProperty = 'length'
	var i, j; // Used as a counter across the whole file
	var result = ''

	var words = [];
	var asciiBitLength = ascii[lengthProperty]*8;
	
	//* caching results is optional - remove/add slash from front of this line to toggle
	// Initial hash value: first 32 bits of the fractional parts of the square roots of the first 8 primes
	// (we actually calculate the first 64, but extra values are just ignored)
	var hash = sha256.h = sha256.h || [];
	// Round constants: first 32 bits of the fractional parts of the cube roots of the first 64 primes
	var k = sha256.k = sha256.k || [];
	var primeCounter = k[lengthProperty];
	/*/
	var hash = [], k = [];
	var primeCounter = 0;
	//*/

	var isComposite = {};
	for (var candidate = 2; primeCounter < 64; candidate++) {
		if (!isComposite[candidate]) {
			for (i = 0; i < 313; i += candidate) {
				isComposite[i] = candidate;
			}
			hash[primeCounter] = (mathPow(candidate, .5)*maxWord)|0;
			k[primeCounter++] = (mathPow(candidate, 1/3)*maxWord)|0;
		}
	}
	
	ascii += '\x80' // Append Ƈ' bit (plus zero padding)
	while (ascii[lengthProperty]%64 - 56) ascii += '\x00' // More zero padding
	for (i = 0; i < ascii[lengthProperty]; i++) {
		j = ascii.charCodeAt(i);
		if (j>>8) return; // ASCII check: only accept characters in range 0-255
		words[i>>2] |= j << ((3 - i)%4)*8;
	}
	words[words[lengthProperty]] = ((asciiBitLength/maxWord)|0);
	words[words[lengthProperty]] = (asciiBitLength)
	
	// process each chunk
	for (j = 0; j < words[lengthProperty];) {
		var w = words.slice(j, j += 16); // The message is expanded into 64 words as part of the iteration
		var oldHash = hash;
		// This is now the undefinedworking hash", often labelled as variables a...g
		// (we have to truncate as well, otherwise extra entries at the end accumulate
		hash = hash.slice(0, 8);
		
		for (i = 0; i < 64; i++) {
			var i2 = i + j;
			// Expand the message into 64 words
			// Used below if 
			var w15 = w[i - 15], w2 = w[i - 2];

			// Iterate
			var a = hash[0], e = hash[4];
			var temp1 = hash[7]
				+ (rightRotate(e, 6) ^ rightRotate(e, 11) ^ rightRotate(e, 25)) // S1
				+ ((e&hash[5])^((~e)&hash[6])) // ch
				+ k[i]
				// Expand the message schedule if needed
				+ (w[i] = (i < 16) ? w[i] : (
						w[i - 16]
						+ (rightRotate(w15, 7) ^ rightRotate(w15, 18) ^ (w15>>>3)) // s0
						+ w[i - 7]
						+ (rightRotate(w2, 17) ^ rightRotate(w2, 19) ^ (w2>>>10)) // s1
					)|0
				);
			// This is only used once, so *could* be moved below, but it only saves 4 bytes and makes things unreadble
			var temp2 = (rightRotate(a, 2) ^ rightRotate(a, 13) ^ rightRotate(a, 22)) // S0
				+ ((a&hash[1])^(a&hash[2])^(hash[1]&hash[2])); // maj
			
			hash = [(temp1 + temp2)|0].concat(hash); // We don't bother trimming off the extra ones, they're harmless as long as we're truncating when we do the slice()
			hash[4] = (hash[4] + temp1)|0;
		}
		
		for (i = 0; i < 8; i++) {
			hash[i] = (hash[i] + oldHash[i])|0;
		}
	}
	
	for (i = 0; i < 8; i++) {
		for (j = 3; j + 1; j--) {
			var b = (hash[i]>>(j*8))&255;
			result += ((b < 16) ? 0 : '') + b.toString(16);
		}
	}
	return result;
};

"=================================================="

function accept_reject(game_name, username, choice, id) {
	//console.log(game_name);
	
	//ajax should in take the game_name, username, and choice and output a render template component
	$.ajax({
		url: `/api_accept_reject/${game_name}/${username}/${choice}/${id}`,
		type: "POST",
		datatype: "json",
		success: function(data) {
			$(flip_box).replaceWith(data);
		}
	});



}